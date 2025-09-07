import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

// --- Emotional Check-in Screen ---
// This screen allows the user to write about their feelings. The text is sent
// to the backend for sentiment analysis.
class EmotionalCheckinScreen extends StatefulWidget {
  const EmotionalCheckinScreen({super.key});

  @override
  State<EmotionalCheckinScreen> createState() => _EmotionalCheckinScreenState();
}

// The State class for EmotionalCheckinScreen. It manages the text controller,
// the sentiment result, and the loading state.
class _EmotionalCheckinScreenState extends State<EmotionalCheckinScreen> {
  // A controller for the text input field.
  final TextEditingController _controller = TextEditingController();
  // Stores the sentiment result received from the backend.
  String _sentiment = '';
  // A boolean flag to show a loading indicator while waiting for the response.
  bool _isLoading = false;

  // This asynchronous function sends the user's text to the backend for analysis.
  Future<void> _submitCheckin() async {
    // Do not proceed if the text field is empty.
    if (_controller.text.isEmpty) return;

    // Update the UI to show a loading state.
    setState(() {
      _isLoading = true;
      _sentiment = ''; // Clear previous sentiment.
    });

    // Make an HTTP POST request to the FastAPI backend.
    final response = await http.post(
      Uri.parse('http://localhost:8000/checkin/emotional'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'text': _controller.text}),
    );

    // After the request is complete, stop the loading indicator.
    setState(() {
      _isLoading = false;
    });

    // Check if the request was successful (status code 200).
    if (response.statusCode == 200) {
      // Decode the JSON response and update the sentiment.
      final data = jsonDecode(response.body);
      setState(() {
        _sentiment = 'Sentiment recorded: ${data['sentiment']}';
      });
      // Display a snackbar with a confirmation message.
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Check-in submitted! Sentiment: ${data['sentiment']}')),
      );
    } else {
      // If the request fails, show an error message.
      setState(() {
        _sentiment = 'Error submitting check-in.';
      });
    }
  }

  // The build method constructs the UI for the emotional check-in screen.
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Emotional GPS'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'How are you feeling today?',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _controller,
              maxLines: 4,
              decoration: const InputDecoration(
                hintText: 'Write about your day...',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              // The button is disabled while the app is loading.
              onPressed: _isLoading ? null : _submitCheckin,
              child: _isLoading
                  ? const CircularProgressIndicator() // Show a spinning indicator while loading.
                  : const Text('Submit Check-in'), // Show the button text when not loading.
            ),
            // Conditionally display the sentiment result if it's not empty.
            if (_sentiment.isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 16),
                child: Text(_sentiment),
              ),
          ],
        ),
      ),
    );
  }
}
