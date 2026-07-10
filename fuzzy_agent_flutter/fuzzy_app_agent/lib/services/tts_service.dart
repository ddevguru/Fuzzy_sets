import 'dart:async';
import 'package:flutter_tts/flutter_tts.dart';

class TtsService {
  final FlutterTts _tts = FlutterTts();
  String _lang = "en-US";

  Future<void> init() async {
    await _tts.setSpeechRate(0.48);
    await _tts.setPitch(1.0);
    await setLanguage("en");
  }

  Future<void> setLanguage(String code) async {
    final locale = switch (code) {
      "hi" => "hi-IN",
      "mr" => "mr-IN",
      _ => "en-US",
    };
    _lang = locale;
    await _tts.setLanguage(locale);
  }

  String get currentLocale => _lang;

  Future<void> speak(String text) async {
    await _tts.stop();
    await _tts.speak(text);
  }

  Future<void> stop() => _tts.stop();

  Future<void> speakAndWait(String text) async {
    await _tts.stop();
    final completer = Completer<void>();
    void handler() {
      if (!completer.isCompleted) completer.complete();
    }
    _tts.setCompletionHandler(handler);
    _tts.setErrorHandler((_) => handler());
    await _tts.speak(text);
    await completer.future.timeout(
      Duration(seconds: (text.length / 12).ceil().clamp(5, 120)),
      onTimeout: () {},
    );
  }
}
