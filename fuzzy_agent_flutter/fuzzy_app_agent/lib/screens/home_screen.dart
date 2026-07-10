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

class _HomeScreenState extends State<HomeScreen> {
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

  static const _langLabels = {
    "en": "English",
    "hi": "हिंदी",
    "mr": "मराठी",
  };

  @override
  void initState() {
    super.initState();
    _setup();
  }

  @override
  void dispose() {
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
      await _speakReply(res["reply"] as String? ?? "");
    } catch (e) {
      setState(() {
        _messages.add(ChatMessage(
          text: "Could not reach the backend at ${ApiService.baseUrl}.\n"
              "Make sure the Flask server is running and the URL in "
              "api_service.dart is correct.\nError: $e",
          isUser: false,
        ));
        _loading = false;
      });
    }
  }

  Future<void> _applyLanguage(String? code) async {
    if (code == null || code == _language) return;
    _language = code;
    await _speech.setLanguage(code);
    await _tts.setLanguage(code);
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

  Future<void> _speakReply(String text) async {
    if (text.isEmpty) return;
    setState(() => _speaking = true);
    await _tts.speakAndWait(text);
    if (!mounted) return;
    setState(() => _speaking = false);
    if (_autoListen && _sessionId != null) {
      _startListening();
    }
  }

  Future<void> _send(String text) async {
    if (text.trim().isEmpty || _sessionId == null) return;
    _textController.clear();
    if (_listening) {
      _speech.stop();
      setState(() => _listening = false);
    }
    try {
      final res = await _api.sendMessage(_sessionId!, text.trim());
      await _applyResponse(res, isUser: true, userText: text.trim());
      await _speakReply(res["reply"] as String? ?? "");
    } catch (e) {
      setState(() {
        _messages.add(ChatMessage(text: "Connection error: $e", isUser: false));
      });
    }
  }

  void _startListening() {
    if (_listening || _speaking || _sessionId == null) return;
    setState(() => _listening = true);
    _speech.listen(
      (result) {
        if (!mounted) return;
        setState(() => _listening = false);
        if (result.trim().isNotEmpty) _send(result);
      },
      onListening: () {},
    );
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
    Future.delayed(const Duration(milliseconds: 100), () {
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
      backgroundColor: const Color(0xFFF7F7F5),
      appBar: AppBar(
        title: const Text("Fuzzy Logic Voice Tutor"),
        backgroundColor: Colors.white,
        foregroundColor: Colors.black87,
        elevation: 0.5,
        actions: [
          if (_language.isNotEmpty)
            Chip(
              label: Text(_langLabels[_language] ?? _language,
                  style: const TextStyle(fontSize: 12)),
              backgroundColor: const Color(0xFFE8F5EE),
            ),
          IconButton(
            icon: Icon(_autoListen ? Icons.hearing : Icons.hearing_disabled),
            tooltip: _autoListen ? "Auto-listen ON" : "Auto-listen OFF",
            onPressed: () => setState(() => _autoListen = !_autoListen),
          ),
        ],
      ),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : Column(
              children: [
                if (_speaking || _listening)
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.symmetric(vertical: 6),
                    color: _listening
                        ? const Color(0xFFFFECEC)
                        : const Color(0xFFE8F5EE),
                    child: Text(
                      _listening ? "🎤 Listening..." : "🔊 Speaking...",
                      textAlign: TextAlign.center,
                      style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w500),
                    ),
                  ),
                Expanded(
                  child: ListView.builder(
                    controller: _scrollController,
                    padding: const EdgeInsets.all(12),
                    itemCount: _messages.length,
                    itemBuilder: (ctx, i) => _MessageBubble(message: _messages[i]),
                  ),
                ),
                _InputBar(
                  controller: _textController,
                  listening: _listening,
                  onSend: _send,
                  onMic: _toggleListen,
                ),
              ],
            ),
    );
  }
}

class _MessageBubble extends StatelessWidget {
  final ChatMessage message;
  const _MessageBubble({required this.message});

  @override
  Widget build(BuildContext context) {
    final align = message.isUser ? Alignment.centerRight : Alignment.centerLeft;
    final bubbleColor = message.isUser ? const Color(0xFF2F6F4F) : Colors.white;
    final textColor = message.isUser ? Colors.white : Colors.black87;
    final data = message.data;

    return Align(
      alignment: align,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 6),
        padding: const EdgeInsets.all(12),
        constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.88),
        decoration: BoxDecoration(
          color: bubbleColor,
          borderRadius: BorderRadius.circular(14),
          boxShadow: const [BoxShadow(color: Colors.black12, blurRadius: 3)],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(message.text, style: TextStyle(color: textColor, fontSize: 15)),
            if (data != null && data["diagram"] != null) ...[
              const SizedBox(height: 10),
              _DiagramCard(
                title: data["diagram_title"] as String? ?? "Architecture",
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
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: const Color(0xFF1E2A38),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title,
              style: const TextStyle(
                  color: Color(0xFF7EC8A8), fontWeight: FontWeight.bold, fontSize: 13)),
          const SizedBox(height: 8),
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Text(
              diagram,
              style: const TextStyle(
                fontFamily: "monospace",
                fontSize: 9.5,
                color: Color(0xFFE8EEF2),
                height: 1.35,
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
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: const Color(0xFFF0F4F1),
        borderRadius: BorderRadius.circular(10),
        border: Border.all(color: const Color(0xFFDDE5E0)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(data["operation"] ?? "",
              style: const TextStyle(fontWeight: FontWeight.bold)),
          const SizedBox(height: 4),
          Text(data["formula"] ?? "",
              style: const TextStyle(fontFamily: "monospace", fontSize: 12)),
          const SizedBox(height: 6),
          ...steps.map((s) => Text("• $s", style: const TextStyle(fontSize: 13))),
          if (data["result_set"] != null) ...[
            const SizedBox(height: 6),
            Text("Result: ${data["result_set"]}",
                style: const TextStyle(fontWeight: FontWeight.w600)),
          ],
        ],
      ),
    );
  }
}

class _InputBar extends StatelessWidget {
  final TextEditingController controller;
  final bool listening;
  final void Function(String) onSend;
  final VoidCallback onMic;

  const _InputBar({
    required this.controller,
    required this.listening,
    required this.onSend,
    required this.onMic,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(8),
      color: Colors.white,
      child: SafeArea(
        child: Row(
          children: [
            IconButton(
              icon: Icon(
                listening ? Icons.mic : Icons.mic_none,
                color: listening ? Colors.red : const Color(0xFF2F6F4F),
                size: 28,
              ),
              onPressed: onMic,
            ),
            Expanded(
              child: TextField(
                controller: controller,
                decoration: const InputDecoration(
                  hintText: "Speak or type... (e.g. Hindi, fuzzy logic kya hai)",
                  border: InputBorder.none,
                ),
                onSubmitted: onSend,
              ),
            ),
            IconButton(
              icon: const Icon(Icons.send, color: Color(0xFF2F6F4F)),
              onPressed: () => onSend(controller.text),
            ),
          ],
        ),
      ),
    );
  }
}
