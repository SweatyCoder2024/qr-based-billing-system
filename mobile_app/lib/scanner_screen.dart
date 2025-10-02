// lib/scanner_screen.dart

import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:provider/provider.dart';
import 'connection_provider.dart';

class ScannerScreen extends StatefulWidget {
  const ScannerScreen({super.key});

  @override
  State<ScannerScreen> createState() => _ScannerScreenState();
}

class _ScannerScreenState extends State<ScannerScreen> {
  final MobileScannerController controller = MobileScannerController();
  bool isProcessing = false;

  @override
  void dispose() {
    // Make sure to dispose of the controller when the screen is closed
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Scan QR Code')),
      body: MobileScanner(
        controller: controller, // Use the controller
        onDetect: (capture) {
          // Prevent multiple detections while processing
          if (isProcessing) return;
          setState(() {
            isProcessing = true;
          });

          final List<Barcode> barcodes = capture.barcodes;
          if (barcodes.isNotEmpty) {
            final String? scannedData = barcodes.first.rawValue;
            if (scannedData != null) {
              // Manually stop the camera BEFORE leaving the screen
              controller.stop();

              // Use a short delay to ensure the camera has stopped before popping
              Future.delayed(const Duration(milliseconds: 50), () {
                if (Navigator.canPop(context)) {
                  // Check if the app is connected to a session
                  final connectionProvider = Provider.of<ConnectionProvider>(
                    context,
                    listen: false,
                  );
                  if (connectionProvider.status == ConnectionStatus.connected) {
                    // If connected, we are scanning an item, so pop with the item data
                    Navigator.of(context).pop(scannedData);
                  } else {
                    // If not connected, we are scanning a session, so set the data
                    connectionProvider.setScannedData(scannedData);
                    Navigator.of(context).pop();
                  }
                }
              });
            }
          }
        },
      ),
    );
  }
}
