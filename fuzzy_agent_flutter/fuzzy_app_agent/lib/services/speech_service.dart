import 'package:speech_to_text/speech_to_text.dart' as stt;

class SpeechService {
  final stt.SpeechToText _speech = stt.SpeechToText();
  bool isAvailable = false;
  String _locale = "en_US";
  String? _lastError;

  static const localeMap = {
    "en": "en_US",
    "hi": "hi_IN",
    "mr": "mr_IN",
  };

  Future<bool> init() async {
    isAvailable = await _speech.initialize(
      onError: (e) => _lastError = e.errorMsg,
      debugLogging: false,
    );
    return isAvailable;
  }

  String? get lastError => _lastError;

  Future<void> setLanguage(String code) async {
    final preferred = localeMap[code] ?? "en_US";
    try {
      final locales = await _speech.locales();
      if (locales.any((l) => l.localeId == preferred)) {
        _locale = preferred;
        return;
      }
      // Fallback: same language prefix e.g. hi_XX
      final prefix = preferred.split('_').first;
      final match = locales.where((l) => l.localeId.startsWith(prefix)).toList();
      if (match.isNotEmpty) {
        _locale = match.first.localeId;
        return;
      }
    } catch (_) {}
    _locale = "en_US";
  }

  String get currentLocale => _locale;

  /// Returns true if listening started successfully.
  Future<bool> listen(
    void Function(String) onResult, {
    void Function(String)? onPartial,
  }) async {
    _lastError = null;
    if (!isAvailable) return false;

    if (_speech.isListening) {
      await _speech.stop();
      await Future.delayed(const Duration(milliseconds: 200));
    }

    final started = await _speech.listen(
      onResult: (result) {
        final words = result.recognizedWords.trim();
        if (words.isEmpty) return;
        onPartial?.call(words);
        if (result.finalResult) {
          onResult(words);
        }
      },
      localeId: _locale,
      listenFor: const Duration(seconds: 30),
      pauseFor: const Duration(milliseconds: 2800),
      partialResults: true,
      cancelOnError: false,
      listenMode: stt.ListenMode.dictation,
    );
    return started;
  }

  Future<void> stop() async {
    if (_speech.isListening) {
      await _speech.stop();
    }
  }

  bool get isListening => _speech.isListening;
}
