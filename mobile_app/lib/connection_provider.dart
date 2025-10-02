// lib/connection_provider.dart

import 'package:flutter/foundation.dart';
import 'dart:convert';
import 'websocket_service.dart';

enum ConnectionStatus { disconnected, connecting, connected, error }

class ConnectionProvider with ChangeNotifier {
  final WebSocketService _webSocketService = WebSocketService();

  String? _scannedData;
  String? get scannedData => _scannedData;

  ConnectionStatus _status = ConnectionStatus.disconnected;
  ConnectionStatus get status => _status;

  void setScannedData(String data) {
    _scannedData = data;
    print('Data set in provider. Attempting to connect...');
    connect(); // Automatically try to connect when data is set
    notifyListeners();
  }

  void connect() {
    if (_scannedData == null) return;

    try {
      final data = jsonDecode(_scannedData!);
      final String? url = data['websocket_url'];

      if (url != null) {
        _status = ConnectionStatus.connecting;
        notifyListeners();
        _webSocketService.connect(url);
        _status = ConnectionStatus.connected;
        notifyListeners();
      } else {
        _status = ConnectionStatus.error;
        notifyListeners();
      }
    } catch (e) {
      print('Failed to parse scanned data or connect: $e');
      _status = ConnectionStatus.error;
      notifyListeners();
    }
  }

  void sendItemScan(String scannedItemQrCode) {
    // We create a JSON message to send to the backend
    final message = {
      "type": "item_scanned",
      "data": {"qr_code": scannedItemQrCode},
    };
    _webSocketService.sendMessage(jsonEncode(message));
  }

  void disconnect() {
    _webSocketService.disconnect();
    _status = ConnectionStatus.disconnected;
    _scannedData = null;
    notifyListeners();
  }
}
