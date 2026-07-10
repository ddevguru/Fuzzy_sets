import 'package:speech_to_text/speech_to_text.dart' as stt;

class SpeechService {
  final stt.SpeechToText _speech = stt.SpeechToText();
  bool isAvailable = false;
  String _locale = "en_US";

  static const localeMap = {
    "en": "en_US",
    "hi": "hi_IN",
    "mr": "mr_IN",
  };

  Future<bool> init() async {
    isAvailable = await _speech.initialize();
    return isAvailable;
  }

  Future<void> setLanguage(String code) async {
    _locale = localeMap[code] ?? "en_US";
  }

  String get currentLocale => _locale;

  void listen(void Function(String) onResult, {void Function()? onListening}) {
    _speech.listen(
      localeId: _locale,
      listenFor: const Duration(seconds: 30),
      pauseFor: const Duration(seconds: 3),
      onResult: (result) {
        if (result.finalResult) {
          onResult(result.recognizedWords);
        }
      },
    );
    onListening?.call();
  }

  void stop() => _speech.stop();
  bool get isListening => _speech.isListening;
}
