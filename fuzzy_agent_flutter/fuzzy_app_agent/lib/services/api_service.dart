import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = "http://35.234.218.138:5000";
  static const _timeout = Duration(seconds: 15);

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
    final res = await http
        .post(
          Uri.parse("$baseUrl/api/message"),
          headers: {"Content-Type": "application/json"},
          body: jsonEncode({
            "session_id": sessionId,
            "text": text,
            if (language != null) "language": language,
          }),
        )
        .timeout(_timeout);

    if (res.statusCode == 404) {
      // Session lost — auto recover and retry once
      final fresh = await startSession();
      final retry = await http
          .post(
            Uri.parse("$baseUrl/api/message"),
            headers: {"Content-Type": "application/json"},
            body: jsonEncode({
              "session_id": fresh["session_id"],
              "text": text,
              if (language != null) "language": language,
            }),
          )
          .timeout(_timeout);
      if (retry.statusCode != 200) {
        throw Exception("Server error ${retry.statusCode}");
      }
      final data = jsonDecode(retry.body) as Map<String, dynamic>;
      data["recovered"] = true;
      return data;
    }

    if (res.statusCode != 200) {
      throw Exception("Server error ${res.statusCode}");
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
