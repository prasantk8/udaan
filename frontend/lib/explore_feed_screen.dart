import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:url_launcher/url_launcher.dart'; // Add this to your pubspec.yaml

class ExploreFeedScreen extends StatefulWidget {
  final List<String> tags;
  const ExploreFeedScreen({super.key, required this.tags});

  @override
  State<ExploreFeedScreen> createState() => _ExploreFeedScreenState();
}

class _ExploreFeedScreenState extends State<ExploreFeedScreen> {
  List _feedItems = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchFeed();
  }

  Future<void> _fetchFeed() async {
  setState(() {
    _isLoading = true;
  });

  // Convert the list of tags into query parameters for the GET request
  final queryString = widget.tags.map((t) => 'tags=$t').join('&');

  final response = await http.get(
    Uri.parse('http://localhost:8000/feed/explore?$queryString'),
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    setState(() {
      _feedItems = data['feed_items'];
    });
  } else {
    // Optionally handle errors
    print('Error fetching feed: ${response.statusCode}');
    setState(() {
      _feedItems = [];
    });
  }

  setState(() {
    _isLoading = false;
  });
}


  void _launchURL(String url) async {
    final uri = Uri.parse(url);
    if (await canLaunchUrl(uri)) {
      await launchUrl(uri);
    } else {
      throw 'Could not launch $url';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Explore Feed'),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _feedItems.isEmpty
              ? const Center(
                  child: Text('No relevant content found.', style: TextStyle(fontSize: 16)),
                )
              : ListView.builder(
                  itemCount: _feedItems.length,
                  itemBuilder: (context, index) {
                    final item = _feedItems[index];
                    return Card(
                      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                      child: ListTile(
                        title: Text(item['title']),
                        subtitle: Text('Tags: ${item['tags'].join(', ')}'),
                        onTap: () => _launchURL(item['url']),
                      ),
                    );
                  },
                ),
    );
  }
}