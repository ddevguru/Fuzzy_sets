import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "http://35.234.218.138:5000";
  static const _timeout = Duration(seconds: 20);

  Future<Map<String, dynamic>> startSession() async {
    final res = await http
        .post(Uri.parse("$baseUrl/api/session"))
        .timeout(_timeout);
    if (res.statusCode != 200) {
      throw Exception("Server error ${res.statusCode}");
    }
    return jsonDecode(res.body) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> sendMessage(
    String sessionId,
    String text, {
    String? language,
  }) async {
    final body = jsonEncode({
      "session_id": sessionId,
      "text": text,
      if (language != null && language.isNotEmpty) "language": language,
    });

    final res = await http
        .post(
          Uri.parse("$baseUrl/api/message"),
          headers: {"Content-Type": "application/json"},
          body: body,
        )
        .timeout(_timeout);

    if (res.statusCode != 200) {
      throw Exception("Server error ${res.statusCode}: ${res.body}");
    }

    return jsonDecode(res.body) as Map<String, dynamic>;
  }

  Future<bool> healthCheck() async {
    try {
      final res = await http
          .get(Uri.parse("$baseUrl/api/health"))
          .timeout(const Duration(seconds: 8));
      return res.statusCode == 200;
    } catch (_) {
      return false;
    }
  }
}
