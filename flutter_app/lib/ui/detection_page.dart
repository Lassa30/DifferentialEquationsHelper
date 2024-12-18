import 'package:camera/camera.dart';
import 'package:flutter/material.dart';

late List<CameraDescription> cameras_;

class DetectionPage extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return _DetectionPageState();
  }
}

class _DetectionPageState extends State<DetectionPage> {
  late CameraController controller;

  @override
  void initState() {
    super.initState();
    controller = CameraController(
      cameras_[0],
      ResolutionPreset.high,
      enableAudio: false,
    );

    controller.initialize().then((_) {
      if (!mounted) {
        return;
      }
      setState(() {});
    });
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (!controller.value.isInitialized) {
      return CircularProgressIndicator();
    } else {
      return CameraPreview(controller);
    }
  }
}
