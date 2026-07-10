import 'package:flutter/material.dart';

/// Visual fallback when the PNG asset is missing from the APK.
class FuzzyArchitectureDiagram extends StatelessWidget {
  const FuzzyArchitectureDiagram({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFFF8FBF9),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: const Color(0xFF3D8B72)),
      ),
      child: Column(
        children: [
          _box("Crisp Input", const Color(0xFFE3F2FD)),
          const Icon(Icons.arrow_downward, color: Color(0xFF1B5E4B), size: 20),
          _box("Fuzzifier", const Color(0xFFFFF3E0)),
          const Icon(Icons.arrow_downward, color: Color(0xFF1B5E4B), size: 20),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              _box("Rules", const Color(0xFFF3E5F5), small: true),
              const SizedBox(width: 8),
              _box("Inference Engine", const Color(0xFFE8F5E9), small: true),
            ],
          ),
          const Icon(Icons.arrow_downward, color: Color(0xFF1B5E4B), size: 20),
          _box("Defuzzifier", const Color(0xFFFFF3E0)),
          const Icon(Icons.arrow_downward, color: Color(0xFF1B5E4B), size: 20),
          _box("Crisp Output", const Color(0xFFE3F2FD)),
        ],
      ),
    );
  }

  Widget _box(String label, Color color, {bool small = false}) {
    return Container(
      width: small ? 130 : double.infinity,
      padding: EdgeInsets.symmetric(vertical: small ? 8 : 12, horizontal: 10),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: const Color(0xFF1B5E4B), width: 1.2),
      ),
      child: Text(
        label,
        textAlign: TextAlign.center,
        style: TextStyle(
          fontWeight: FontWeight.w600,
          fontSize: small ? 11 : 13,
          color: const Color(0xFF1B5E4B),
        ),
      ),
    );
  }
}
