/// Normalizes speech-to-text output so numbers work for fuzzy set input.
class VoiceNormalize {
  static const _devanagari = "०१२३४५६७८९";

  static const _spoken = {
    "zero": "0",
    "oh": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
    "point": ".",
    "dot": ".",
    "decimal": ".",
    "शून्य": "0",
    "एक": "1",
    "दो": "2",
    "दोन": "2",
    "तीन": "3",
    "चार": "4",
    "पांच": "5",
    "पाच": "5",
    "छह": "6",
    "सात": "7",
    "आठ": "8",
    "नौ": "9",
    "दहा": "10",
    "बिंदु": ".",
    "दशांश": ".",
  };

  static String forBackend(String raw) {
    var t = raw.trim();
    if (t.isEmpty) return t;

    for (var i = 0; i < _devanagari.length; i++) {
      t = t.replaceAll(_devanagari[i], "$i");
    }

    var lower = t.toLowerCase();
    final sorted = _spoken.keys.toList()..sort((a, b) => b.length.compareTo(a.length));
    for (final word in sorted) {
      lower = lower.replaceAll(RegExp(r'\b' + RegExp.escape(word) + r'\b'), _spoken[word]!);
    }

    lower = lower.replaceAll(",", ".");
    lower = lower.replaceAll(RegExp(r'\s+'), "");

    // "x 1" / "ex one" → x1
    lower = lower.replaceAll(RegExp(r'^(ex|x)(\d+)$', caseSensitive: false), r'x$2');

    return lower.isNotEmpty ? lower : raw.trim();
  }

  static bool looksLikeCount(String normalized) => RegExp(r'^\d+$').hasMatch(normalized);

  static bool looksLikeMembership(String normalized) =>
      RegExp(r'^\d*\.?\d+$').hasMatch(normalized);

  static bool isArchitectureQuery(String text) {
    final t = text.toLowerCase();
    return t.contains("architecture") ||
        t.contains("diagram") ||
        t.contains("आर्किटेक्चर") ||
        t.contains("आकृति") ||
        t.contains("संरचना");
  }
}
