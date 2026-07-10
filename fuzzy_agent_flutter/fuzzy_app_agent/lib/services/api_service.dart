import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // Google Cloud VM (production)
  static const String baseUrl = "http://35.234.218.138:5000";

  Future<Map<String, dynamic>> startSession() async {
    final res = await http.post(Uri.parse("$baseUrl/api/session"));
    if (res.statusCode != 200) {
      throw Exception("Server error ${res.statusCode}");
    }
    return jsonDecode(res.body) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> sendMessage(String sessionId, String text) async {
    final res = await http.post(
      Uri.parse("$baseUrl/api/message"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"session_id": sessionId, "text": text}),
    );
    if (res.statusCode != 200) {
      throw Exception("Server error ${res.statusCode}");
    }
    return jsonDecode(res.body) as Map<String, dynamic>;
  }

  Future<bool> healthCheck() async {
    try {
      final res = await http.get(Uri.parse("$baseUrl/api/health"));
      return res.statusCode == 200;
    } catch (_) {
      return false;
    }
  }
}
