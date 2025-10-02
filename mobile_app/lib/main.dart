// lib/main.dart

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'scanner_screen.dart';
import 'connection_provider.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => ConnectionProvider(),
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'QR Billing Mobile',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final connectionProvider = Provider.of<ConnectionProvider>(context);

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('QR Billing Scanner'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            // Show a status indicator based on the connection status
            _buildStatusIndicator(connectionProvider.status),
            const SizedBox(height: 30),

            // If not connected, show the Session Scan button
            if (connectionProvider.status != ConnectionStatus.connected)
              ElevatedButton.icon(
                icon: const Icon(Icons.qr_code_scanner),
                label: const Text('Scan Session QR Code'),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 30,
                    vertical: 15,
                  ),
                  textStyle: const TextStyle(fontSize: 18),
                ),
                onPressed: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => const ScannerScreen(),
                    ),
                  );
                },
              )
            // If connected, show the Item Scan and Disconnect buttons
            else
              Column(
                children: [
                  ElevatedButton.icon(
                    icon: const Icon(Icons.qr_code),
                    label: const Text('Scan Item QR Code'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.blueAccent,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(
                        horizontal: 30,
                        vertical: 15,
                      ),
                      textStyle: const TextStyle(fontSize: 18),
                    ),
                    onPressed: () async {
                      final scannedItemCode = await Navigator.of(context)
                          .push<String>(
                            MaterialPageRoute(
                              builder: (context) => const ScannerScreen(),
                            ),
                          );
                      if (scannedItemCode != null && context.mounted) {
                        // Extract the actual code from the item's JSON
                        try {
                          final itemJson = jsonDecode(scannedItemCode);
                          final String? qrCode = itemJson['qr_code'];
                          if (qrCode != null) {
                            connectionProvider.sendItemScan(qrCode);
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(content: Text('Sent item: $qrCode')),
                            );
                          }
                        } catch (e) {
                          print("Scanned data was not a valid item JSON: $e");
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                              content: Text(
                                'Scanned code is not a valid item QR.',
                              ),
                            ),
                          );
                        }
                      }
                    },
                  ),
                  const SizedBox(height: 20),
                  ElevatedButton.icon(
                    icon: const Icon(Icons.cancel),
                    label: const Text('Disconnect'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.red,
                      foregroundColor: Colors.white,
                    ),
                    onPressed: () {
                      connectionProvider.disconnect();
                    },
                  ),
                ],
              ),
          ],
        ),
      ),
    );
  }

  // Helper widget to show the correct status message and icon
  Widget _buildStatusIndicator(ConnectionStatus status) {
    IconData icon;
    String text;
    Color color;

    switch (status) {
      case ConnectionStatus.connected:
        icon = Icons.check_circle;
        text = 'Connected';
        color = Colors.green;
        break;
      case ConnectionStatus.connecting:
        icon = Icons.sync;
        text = 'Connecting...';
        color = Colors.orange;
        break;
      case ConnectionStatus.error:
        icon = Icons.error;
        text = 'Connection Error';
        color = Colors.red;
        break;
      default:
        icon = Icons.cancel;
        text = 'Disconnected';
        color = Colors.grey;
    }
    return Column(
      children: [
        Icon(icon, color: color, size: 80),
        const SizedBox(height: 10),
        Text(text, style: TextStyle(fontSize: 24, color: color)),
      ],
    );
  }
}
