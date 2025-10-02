// lib/websocket_service.dart

import 'package:web_socket_channel/web_socket_channel.dart';

class WebSocketService {
  WebSocketChannel? _channel;

  void connect(String url) {
    try {
      // Parse the URL and create a WebSocket channel
      _channel = WebSocketChannel.connect(Uri.parse(url));
      print('WebSocket connected to: $url');
    } catch (e) {
      print('Error connecting to WebSocket: $e');
    }
  }

  void sendMessage(String message) {
    if (_channel != null) {
      _channel!.sink.add(message);
      print('Sent WebSocket message: $message');
    }
  }

  void disconnect() {
    _channel?.sink.close();
    print('WebSocket disconnected.');
  }
}
