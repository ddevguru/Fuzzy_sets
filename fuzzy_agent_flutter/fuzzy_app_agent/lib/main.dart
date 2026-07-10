import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() => runApp(const FuzzyAgentApp());

class FuzzyAgentApp extends StatelessWidget {
  const FuzzyAgentApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Fuzzy Sets Tutor',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.teal,
        fontFamily: 'Roboto',
      ),
      home: const HomeScreen(),
    );
  }
}
