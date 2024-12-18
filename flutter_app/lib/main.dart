import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:diffur/ui/detection_page.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  bool exceptionOccured = false;

  try {
    cameras_ = await availableCameras();
  } on Exception catch (e) {
    print(e);
    exceptionOccured = true;
  }

  runApp(MaterialApp(
    home: Center(
      child: Container(
        child: (exceptionOccured)
            ? Text(
                "Something went wrong...\nProbably camera access is denied. Try to enable camera access.",
                textScaler: TextScaler.linear(0.5),
              )
            : DetectionPage(),
        height: 500,
        width: 500,
      ),
    ),
  ));
}
