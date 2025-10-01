// lib/main.dart

import 'package:flutter/material.dart';
import 'scanner_screen.dart'; // <-- ADD THIS IMPORT

void main() {
  runApp(const MyApp());
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
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: const Text('QR Billing Scanner'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
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
              onPressed: () async {
                // <-- Make the function async
                // Navigate to the scanner screen and wait for a result
                final scannedData = await Navigator.of(context).push<String>(
                  MaterialPageRoute(
                    builder: (context) => const ScannerScreen(),
                  ),
                );

                if (scannedData != null) {
                  // For now, we'll just print the data to the console
                  print("--- SCANNED DATA ---");
                  print(scannedData);
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Successfully scanned session!')),
                  );
                }
              },
            ),
          ],
        ),
      ),
    );
  }
}
