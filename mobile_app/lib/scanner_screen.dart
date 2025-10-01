// mobile_app/lib/scanner_screen.dart

import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';

class ScannerScreen extends StatelessWidget {
  const ScannerScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Scan QR Code')),
      body: MobileScanner(
        onDetect: (capture) {
          final List<Barcode> barcodes = capture.barcodes;
          if (barcodes.isNotEmpty) {
            final String? scannedData = barcodes.first.rawValue;
            if (scannedData != null) {
              // When a code is found, pop the screen and return the data
              Navigator.of(context).pop(scannedData);
            }
          }
        },
      ),
    );
  }
}
