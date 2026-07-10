import 'dart:async';
import 'package:flutter_tts/flutter_tts.dart';

class TtsService {
  final FlutterTts _tts = FlutterTts();
  String _lang = "en-US";

  Future<void> init() async {
    await _tts.setSpeechRate(0.62);
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

  /// Speak [text] without blocking the UI thread for the full duration.
  Future<void> speakAsync(String text) async {
    if (text.isEmpty) return;
    await _tts.stop();
    await _tts.speak(text);
  }

  Future<void> speakAndWait(String text) async {
    if (text.isEmpty) return;
    await _tts.stop();
    final completer = Completer<void>();
    void handler() {
      if (!completer.isCompleted) completer.complete();
    }
    _tts.setCompletionHandler(handler);
    _tts.setErrorHandler((_) => handler());
    await _tts.speak(text);
    final maxSec = (text.length / 18).ceil().clamp(3, 45);
    await completer.future.timeout(
      Duration(seconds: maxSec),
      onTimeout: () {},
    );
  }
}
