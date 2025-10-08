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
    connect();
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
      _status = ConnectionStatus.error;
      notifyListeners();
    }
  }

  void createNewBill() {
    // Correctly check the status enum, not a non-existent property
    if (_status == ConnectionStatus.connected) {
      final message = {
        "type": "create_new_bill",
      };
      _webSocketService.sendMessage(jsonEncode(message));
    }
  }

  void sendItemScan(String scannedItemQrCode) {
    if (_status == ConnectionStatus.connected) {
        final message = {
          "type": "item_scanned",
          "data": {
            "qr_code": scannedItemQrCode,
          }
        };
        _webSocketService.sendMessage(jsonEncode(message));
    }
  }

  void disconnect() {
    _webSocketService.disconnect();
    _status = ConnectionStatus.disconnected;
    _scannedData = null;
    notifyListeners();
  }
}