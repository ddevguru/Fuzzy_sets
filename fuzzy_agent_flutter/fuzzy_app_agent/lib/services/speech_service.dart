import 'package:speech_to_text/speech_to_text.dart' as stt;

class SpeechService {
  final stt.SpeechToText _speech = stt.SpeechToText();
  bool isAvailable = false;
  String _locale = "en_US";
  bool _delivered = false;
  String _lastWords = "";

  static const localeMap = {
    "en": "en_US",
    "hi": "hi_IN",
    "mr": "mr_IN",
  };

  static const _quickWords = {
    "next", "stop", "help", "restart", "hindi", "english", "marathi",
    "calculate", "agla", "aage", "pudhe", "ruk", "ruko", "thamb", "thamba",
    "madad", "madat", "one", "two", "three", "four", "five",
    "अगला", "रुको", "पुढे", "थांब", "मदद", "हिंदी", "मराठी", "गणना",
  };

  Future<bool> init() async {
    isAvailable = await _speech.initialize(
      onError: (_) {},
      onStatus: (status) {
        // When mic stops, send whatever was heard (fixes missing finalResult)
        if ((status == 'done' || status == 'notListening') &&
            !_delivered &&
            _lastWords.trim().isNotEmpty) {
          _delivered = true;
          _onResultCallback?.call(_lastWords.trim());
        }
      },
    );
    return isAvailable;
  }

  void Function(String)? _onResultCallback;

  Future<void> setLanguage(String code) async {
    _locale = localeMap[code] ?? "en_US";
  }

  String get currentLocale => _locale;

  bool _isQuickCommand(String text) {
    final t = text.trim().toLowerCase();
    if (t.isEmpty || t.length > 40) return false;
    if (_quickWords.contains(t)) return true;
    for (final w in _quickWords) {
      if (t.startsWith("$w ")) return true;
    }
    return RegExp(r'^[\d\s.]+$').hasMatch(t);
  }

  void listen(void Function(String) onResult, {void Function()? onListening}) {
    _delivered = false;
    _lastWords = "";
    _onResultCallback = onResult;

    _speech.listen(
      localeId: _locale,
      listenFor: const Duration(seconds: 20),
      pauseFor: const Duration(milliseconds: 2200),
      partialResults: true,
      cancelOnError: false,
      onResult: (result) {
        final words = result.recognizedWords.trim();
        if (words.isEmpty || _delivered) return;
        _lastWords = words;

        if (result.finalResult) {
          _delivered = true;
          _speech.stop();
          onResult(words);
        } else if (_isQuickCommand(words)) {
          _delivered = true;
          _speech.stop();
          onResult(words);
        }
      },
    );
    onListening?.call();
  }

  void stop() {
    if (!_delivered && _lastWords.trim().isNotEmpty) {
      _delivered = true;
      _onResultCallback?.call(_lastWords.trim());
    } else {
      _delivered = true;
    }
    _speech.stop();
  }

  bool get isListening => _speech.isListening;
}
