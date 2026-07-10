import 'package:flutter/material.dart';
import 'package:permission_handler/permission_handler.dart';
import '../models/chat_message.dart';
import '../services/api_service.dart';
import '../services/speech_service.dart';
import '../services/tts_service.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> with SingleTickerProviderStateMixin {
  final ApiService _api = ApiService();
  final SpeechService _speech = SpeechService();
  final TtsService _tts = TtsService();
  final TextEditingController _textController = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  String? _sessionId;
  String _language = "en";
  final List<ChatMessage> _messages = [];
  bool _listening = false;
  bool _loading = true;
  bool _autoListen = true;
  bool _speaking = false;
  bool _sending = false;
  late AnimationController _pulseCtrl;

  static const _langLabels = {"en": "English", "hi": "हिंदी", "mr": "मराठी"};
  static const _primary = Color(0xFF1B5E4B);
  static const _accent = Color(0xFF2F8F6B);
  static const _bg = Color(0xFFF0F4F2);

  static const _quickCommands = [
    ("Fuzzy logic?", "what is fuzzy logic"),
    ("Architecture", "fuzzy logic architecture diagram"),
    ("Use cases", "use cases"),
    ("Calculate", "start calculation"),
    ("Stop", "stop"),
    ("Change lang", "change language"),
  ];

  @override
  void initState() {
    super.initState();
    _pulseCtrl = AnimationController(vsync: this, duration: const Duration(milliseconds: 600))
      ..repeat(reverse: true);
    _setup();
  }

  @override
  void dispose() {
    _pulseCtrl.dispose();
    _textController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  Future<void> _setup() async {
    await Permission.microphone.request();
    await _speech.init();
    await _tts.init();
    try {
      final res = await _api.startSession();
      await _applyResponse(res, isUser: false);
      setState(() => _loading = false);
      await _speakReply(res["voice_reply"] as String? ?? res["reply"] as String? ?? "");
    } catch (e) {
      setState(() {
        _messages.add(ChatMessage(text: _connError(e.toString()), isUser: false, isError: true));
        _loading = false;
      });
    }
  }

  String _connError(String e) =>
      "Could not reach backend.\n${ApiService.baseUrl}\n\n$e\n\nTap retry below.";

  Future<void> _applyLanguage(String? code) async {
    if (code == null) return;
    if (code != _language) {
      _language = code;
      await _speech.setLanguage(code);
      await _tts.setLanguage(code);
    }
  }

  Future<void> _applyResponse(Map<String, dynamic> res, {required bool isUser, String? userText}) async {
    if (userText != null) {
      setState(() => _messages.add(ChatMessage(text: userText, isUser: true)));
    }
    await _applyLanguage(res["language"] as String?);
    setState(() {
      _sessionId = res["session_id"] as String? ?? _sessionId;
      _messages.add(ChatMessage(
        text: res["reply"] as String? ?? "",
        isUser: false,
        data: res["data"] as Map<String, dynamic>?,
      ));
    });
    _scrollToBottom();
  }

  Future<void> _handleAction(String? action, Map<String, dynamic> res) async {
    final voice = res["voice_reply"] as String? ?? res["reply"] as String? ?? "";
    if (action == "stop") {
      await _stopAll();
      return;
    }
    if (action == "change_language") {
      setState(() => _language = "en");
      await _speakReply(voice);
      return;
    }
    await _speakReply(voice);
  }

  Future<void> _stopAll() async {
    _speech.stop();
    await _tts.stop();
    if (mounted) setState(() {
      _listening = false;
      _speaking = false;
    });
  }

  Future<void> _speakReply(String text) async {
    if (text.isEmpty) return;
    setState(() => _speaking = true);
    await _tts.speakAndWait(text);
    if (!mounted) return;
    setState(() => _speaking = false);
    if (_autoListen && _sessionId != null) _startListening();
  }

  Future<void> _send(String text) async {
    final trimmed = text.trim();
    if (trimmed.isEmpty || _sessionId == null || _sending) return;

    if (trimmed.toLowerCase() == "stop" || trimmed == "रुको" || trimmed == "थांब") {
      await _stopAll();
      setState(() => _messages.add(ChatMessage(text: trimmed, isUser: true)));
      if (_sessionId != null) {
        try {
          final res = await _api.sendMessage(_sessionId!, trimmed, language: _language);
          await _applyResponse(res, isUser: false);
        } catch (_) {}
      }
      return;
    }

    _textController.clear();
    if (_listening) {
      _speech.stop();
      setState(() => _listening = false);
    }

    setState(() => _sending = true);
    try {
      final res = await _api.sendMessage(_sessionId!, trimmed, language: _language);
      await _applyResponse(res, isUser: true, userText: trimmed);
      await _handleAction(res["action"] as String?, res);
    } catch (e) {
      setState(() {
        _messages.add(ChatMessage(text: "Connection error: $e", isUser: false, isError: true));
      });
    } finally {
      if (mounted) setState(() => _sending = false);
    }
  }

  Future<void> _reconnect() async {
    setState(() => _loading = true);
    try {
      final res = await _api.startSession();
      await _applyResponse(res, isUser: false);
      await _speakReply(res["voice_reply"] as String? ?? res["reply"] as String? ?? "");
    } catch (e) {
      setState(() {
        _messages.add(ChatMessage(text: _connError(e.toString()), isUser: false, isError: true));
      });
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  void _startListening() {
    if (_listening || _speaking || _sessionId == null || _sending) return;
    setState(() => _listening = true);
    _speech.listen((result) {
      if (!mounted) return;
      setState(() => _listening = false);
      if (result.trim().isNotEmpty) _send(result);
    });
  }

  void _toggleListen() {
    if (_listening) {
      _speech.stop();
      setState(() => _listening = false);
      return;
    }
    _startListening();
  }

  void _scrollToBottom() {
    Future.delayed(const Duration(milliseconds: 120), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: _bg,
      appBar: AppBar(
        flexibleSpace: Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              colors: [_primary, _accent],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
          ),
        ),
        title: const Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("Fuzzy Logic Tutor", style: TextStyle(fontSize: 17, fontWeight: FontWeight.w600)),
            Text("Voice AI Agent", style: TextStyle(fontSize: 11, fontWeight: FontWeight.w400)),
          ],
        ),
        foregroundColor: Colors.white,
        elevation: 0,
        actions: [
          Container(
            margin: const EdgeInsets.only(right: 4),
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
            decoration: BoxDecoration(
              color: Colors.white24,
              borderRadius: BorderRadius.circular(20),
            ),
            child: Text(_langLabels[_language] ?? _language, style: const TextStyle(fontSize: 12)),
          ),
          IconButton(
            icon: Icon(_autoListen ? Icons.hearing : Icons.hearing_disabled, color: Colors.white),
            tooltip: _autoListen ? "Auto-listen ON" : "Auto-listen OFF",
            onPressed: () => setState(() => _autoListen = !_autoListen),
          ),
        ],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator(color: _primary))
          : Column(
              children: [
                _StatusBar(listening: _listening, speaking: _speaking, sending: _sending),
                SizedBox(
                  height: 42,
                  child: ListView.separated(
                    scrollDirection: Axis.horizontal,
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                    itemCount: _quickCommands.length,
                    separatorBuilder: (_, __) => const SizedBox(width: 6),
                    itemBuilder: (_, i) {
                      final (label, cmd) = _quickCommands[i];
                      return ActionChip(
                        label: Text(label, style: const TextStyle(fontSize: 12)),
                        backgroundColor: Colors.white,
                        side: const BorderSide(color: Color(0xFFD0DDD6)),
                        onPressed: () => _send(cmd),
                      );
                    },
                  ),
                ),
                Expanded(
                  child: ListView.builder(
                    controller: _scrollController,
                    padding: const EdgeInsets.fromLTRB(12, 4, 12, 12),
                    itemCount: _messages.length,
                    itemBuilder: (_, i) => _MessageBubble(
                      message: _messages[i],
                      onRetry: _messages[i].isError ? _reconnect : null,
                    ),
                  ),
                ),
                _InputBar(
                  controller: _textController,
                  listening: _listening,
                  speaking: _speaking,
                  pulse: _pulseCtrl,
                  onSend: _send,
                  onMic: _toggleListen,
                  onStop: _stopAll,
                ),
              ],
            ),
    );
  }
}

class _StatusBar extends StatelessWidget {
  final bool listening, speaking, sending;
  const _StatusBar({required this.listening, required this.speaking, required this.sending});

  @override
  Widget build(BuildContext context) {
    if (!listening && !speaking && !sending) return const SizedBox.shrink();
    final (icon, label, color) = listening
        ? ("🎤", "Listening…", const Color(0xFFFFE8E8))
        : speaking
            ? ("🔊", "Speaking…", const Color(0xFFE3F5EC))
            : ("⏳", "Thinking…", const Color(0xFFFFF8E1));
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(vertical: 7),
      color: color,
      child: Text("$icon  $label", textAlign: TextAlign.center,
          style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w600)),
    );
  }
}

class _MessageBubble extends StatelessWidget {
  final ChatMessage message;
  final VoidCallback? onRetry;
  const _MessageBubble({required this.message, this.onRetry});

  @override
  Widget build(BuildContext context) {
    final isUser = message.isUser;
    final isError = message.isError;
    final align = isUser ? Alignment.centerRight : Alignment.centerLeft;
    final bubbleColor = isError
        ? const Color(0xFFFFF0F0)
        : isUser
            ? const Color(0xFF1B5E4B)
            : Colors.white;
    final textColor = isUser ? Colors.white : const Color(0xFF1A2E28);
    final data = message.data;

    return Align(
      alignment: align,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 5),
        padding: const EdgeInsets.all(14),
        constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.9),
        decoration: BoxDecoration(
          color: bubbleColor,
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(16),
            topRight: const Radius.circular(16),
            bottomLeft: Radius.circular(isUser ? 16 : 4),
            bottomRight: Radius.circular(isUser ? 4 : 16),
          ),
          border: isError ? Border.all(color: const Color(0xFFE57373)) : null,
          boxShadow: const [BoxShadow(color: Color(0x12000000), blurRadius: 6, offset: Offset(0, 2))],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (!isUser && !isError)
              const Padding(
                padding: EdgeInsets.only(bottom: 4),
                child: Text("🤖 Tutor", style: TextStyle(fontSize: 11, color: Color(0xFF2F8F6B), fontWeight: FontWeight.w600)),
              ),
            Text(message.text, style: TextStyle(color: textColor, fontSize: 15, height: 1.4)),
            if (isError && onRetry != null) ...[
              const SizedBox(height: 8),
              TextButton.icon(
                onPressed: onRetry,
                icon: const Icon(Icons.refresh, size: 16),
                label: const Text("Retry connection"),
              ),
            ],
            if (data != null && data["diagram"] != null) ...[
              const SizedBox(height: 10),
              _DiagramCard(
                title: data["diagram_title"] as String? ?? "Fuzzy Logic Architecture",
                diagram: data["diagram"] as String,
              ),
            ],
            if (data != null && data["formula"] != null) ...[
              const SizedBox(height: 8),
              _FormulaCard(data: data),
            ],
          ],
        ),
      ),
    );
  }
}

class _DiagramCard extends StatelessWidget {
  final String title;
  final String diagram;
  const _DiagramCard({required this.title, required this.diagram});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFF0F1F2D), Color(0xFF1A3344)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFF3D8B72)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.account_tree, color: Color(0xFF6ECFAA), size: 16),
              const SizedBox(width: 6),
              Expanded(
                child: Text(title,
                    style: const TextStyle(
                        color: Color(0xFF6ECFAA), fontWeight: FontWeight.bold, fontSize: 13)),
              ),
            ],
          ),
          const SizedBox(height: 8),
          ConstrainedBox(
            constraints: const BoxConstraints(maxHeight: 280),
            child: SingleChildScrollView(
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Text(
                  diagram,
                  style: const TextStyle(
                    fontFamily: "monospace",
                    fontSize: 9,
                    color: Color(0xFFE0EBF0),
                    height: 1.4,
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _FormulaCard extends StatelessWidget {
  final Map<String, dynamic> data;
  const _FormulaCard({required this.data});

  @override
  Widget build(BuildContext context) {
    final steps = (data["steps"] as List?)?.cast<String>() ?? [];
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFFF4FAF7),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: const Color(0xFFB8D9C8)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(data["operation"] ?? "", style: const TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF1B5E4B))),
          const SizedBox(height: 4),
          Container(
            padding: const EdgeInsets.all(6),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(6),
            ),
            child: Text(data["formula"] ?? "",
                style: const TextStyle(fontFamily: "monospace", fontSize: 12, color: Color(0xFF2F4F45))),
          ),
          const SizedBox(height: 6),
          ...steps.map((s) => Padding(
                padding: const EdgeInsets.only(bottom: 2),
                child: Text("• $s", style: const TextStyle(fontSize: 12.5, color: Color(0xFF334840))),
              )),
          if (data["result_set"] != null) ...[
            const SizedBox(height: 6),
            Text("Result: ${data["result_set"]}",
                style: const TextStyle(fontWeight: FontWeight.w700, color: Color(0xFF1B5E4B))),
          ],
        ],
      ),
    );
  }
}

class _InputBar extends StatelessWidget {
  final TextEditingController controller;
  final bool listening, speaking;
  final AnimationController pulse;
  final void Function(String) onSend;
  final VoidCallback onMic, onStop;

  const _InputBar({
    required this.controller,
    required this.listening,
    required this.speaking,
    required this.pulse,
    required this.onSend,
    required this.onMic,
    required this.onStop,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.fromLTRB(8, 8, 8, 4),
      decoration: const BoxDecoration(
        color: Colors.white,
        boxShadow: [BoxShadow(color: Color(0x15000000), blurRadius: 8, offset: Offset(0, -2))],
      ),
      child: SafeArea(
        child: Row(
          children: [
            ScaleTransition(
              scale: listening
                  ? Tween<double>(begin: 1.0, end: 1.15).animate(pulse)
                  : const AlwaysStoppedAnimation<double>(1.0),
              child: IconButton(
                icon: Icon(listening ? Icons.mic : Icons.mic_none,
                    color: listening ? Colors.red : const Color(0xFF1B5E4B), size: 28),
                onPressed: onMic,
              ),
            ),
            IconButton(
              icon: Icon(speaking ? Icons.stop_circle : Icons.stop_circle_outlined,
                  color: speaking ? Colors.red : Colors.grey, size: 26),
              tooltip: "Stop",
              onPressed: onStop,
            ),
            Expanded(
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 14),
                decoration: BoxDecoration(
                  color: const Color(0xFFF4F7F5),
                  borderRadius: BorderRadius.circular(24),
                  border: Border.all(color: const Color(0xFFD8E5DD)),
                ),
                child: TextField(
                  controller: controller,
                  decoration: const InputDecoration(
                    hintText: "Speak or type…",
                    hintStyle: TextStyle(fontSize: 14, color: Colors.grey),
                    border: InputBorder.none,
                  ),
                  onSubmitted: onSend,
                ),
              ),
            ),
            const SizedBox(width: 4),
            CircleAvatar(
              backgroundColor: const Color(0xFF1B5E4B),
              child: IconButton(
                icon: const Icon(Icons.send, color: Colors.white, size: 20),
                onPressed: () => onSend(controller.text),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
