import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'emotional_checkin_screen.dart';

// --- Main App Entry Point ---
// The main function is the starting point for all Flutter apps.
void main() {
  // `runApp` takes the root widget of your app, which is `MyApp`.
  runApp(const MyApp());
}

// `MyApp` is the root widget of the entire application. It's stateless because
// it doesn't need to change over time. It defines the app's title, theme,
// and the initial screen, which is `HomeScreen`.
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Pathfinder MVP',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: const HomeScreen(),
    );
  }
}

// --- Home Screen ---
// This is the first screen the user sees. It provides navigation to the
// two main features of the app: the Socratic Tutor and the Emotional GPS.
class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Pathfinder MVP'),
        centerTitle: true,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                // Navigate to the ChatScreen when this button is pressed.
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const ChatScreen()),
                );
              },
              child: const Text('Launch Socratic Tutor'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Navigate to the EmotionalCheckinScreen when this button is pressed.
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => const EmotionalCheckinScreen()),
                );
              },
              child: const Text('Open Emotional GPS'),
            ),
          ],
        ),
      ),
    );
  }
}

// --- Chat Screen ---
// This screen handles the user's interaction with the Socratic Tutor.
// It is a stateful widget because the list of messages changes over time.
class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

// The State class for the ChatScreen. It holds the logic and data that can change.
class _ChatScreenState extends State<ChatScreen> {
  // A controller for the text input field.
  final TextEditingController _controller = TextEditingController();
  // A list to store the chat messages. Each message is a map with a 'role' (user/assistant) and 'text'.
  final List<Map<String, String>> _messages = [];

  // This asynchronous function sends the user's prompt to the backend.
  Future<void> _sendMessage() async {
    final prompt = _controller.text;
    if (prompt.isEmpty) return; // Don't send empty messages.

    // Immediately add the user's message to the list and clear the input field.
    setState(() {
      _messages.add({'role': 'user', 'text': prompt});
    });
    _controller.clear();

    // Make an HTTP POST request to the FastAPI backend.
    final response = await http.post(
      Uri.parse('http://localhost:8000/tutor/ask'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'prompt': prompt}),
    );

    // Check if the request was successful (status code 200).
    if (response.statusCode == 200) {
      // Decode the JSON response and add the assistant's reply to the message list.
      final data = jsonDecode(response.body);
      setState(() {
        _messages.add({'role': 'assistant', 'text': data['response']});
      });
    } else {
      // If the request fails, show an error message.
      setState(() {
        _messages.add({'role': 'assistant', 'text': 'Error: Could not get a response.'});
      });
    }
  }

  // The build method constructs the UI for the chat screen.
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Socratic Tutor'),
      ),
      body: Column(
        children: [
          // This `Expanded` widget makes the chat message list take up all
          // available space.
          Expanded(
            // `ListView.builder` efficiently builds a list of widgets.
            child: ListView.builder(
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];
                return ListTile(
                  title: Align(
                    // Align the message bubble to the right for the user and left for the assistant.
                    alignment: message['role'] == 'user'
                        ? Alignment.centerRight
                        : Alignment.centerLeft,
                    child: Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        // Use different colors for user and assistant messages.
                        color: message['role'] == 'user'
                            ? Colors.indigo[100]
                            : Colors.grey[200],
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(message['text']!),
                    ),
                  ),
                );
              },
            ),
          ),
          // This section contains the text input field and the send button.
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(
                      hintText: 'Ask an algebra question...',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send),
                  onPressed: _sendMessage,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
