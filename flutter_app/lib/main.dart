/// Tokyo-IA Flutter App - Main Entry Point
library;

import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'services/agent_orchestrator.dart';
import 'services/firebase_service.dart';
import 'utils/logger.dart';
import 'screens/home_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  try {
    // Load environment variables
    await dotenv.load(fileName: '.env');
    AppLogger.info('Environment variables loaded');
  } catch (e) {
    AppLogger.warning('Failed to load .env file: $e');
  }
  
  runApp(const TokyoIAApp());
}

class TokyoIAApp extends StatefulWidget {
  const TokyoIAApp({super.key});
  
  @override
  State<TokyoIAApp> createState() => _TokyoIAAppState();
}

class _TokyoIAAppState extends State<TokyoIAApp> {
  bool _initialized = false;
  String? _initError;
  
  @override
  void initState() {
    super.initState();
    _initializeApp();
  }
  
  Future<void> _initializeApp() async {
    try {
      AppLogger.info('🚀 Starting Tokyo-IA initialization...');
      
      // Initialize Firebase
      final firebaseService = FirebaseService();
      await firebaseService.initialize();
      AppLogger.info('✅ Firebase initialized');
      
      // Initialize Agent Orchestrator and all agents
      final orchestrator = AgentOrchestrator();
      await orchestrator.initializeAllAgents();
      AppLogger.info('✅ Agent Orchestrator initialized');
      
      setState(() {
        _initialized = true;
      });
      
      AppLogger.info('🎉 Tokyo-IA initialization complete!');
    } catch (e, stackTrace) {
      AppLogger.error('Failed to initialize Tokyo-IA', e, stackTrace);
      setState(() {
        _initError = e.toString();
      });
    }
  }
  
  @override
  void dispose() {
    // Shutdown agents when app is disposed
    AgentOrchestrator().shutdownAllAgents();
    super.dispose();
  }
  
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Tokyo-IA',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: _initialized
          ? const HomeScreen()
          : _initError != null
              ? ErrorScreen(error: _initError!)
              : const LoadingScreen(),
    );
  }
}

/// Loading screen shown during initialization
class LoadingScreen extends StatelessWidget {
  const LoadingScreen({super.key});
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const CircularProgressIndicator(),
            const SizedBox(height: 24),
            Text(
              '🤖 Initializing Tokyo-IA Agents...',
              style: Theme.of(context).textTheme.titleLarge,
            ),
            const SizedBox(height: 16),
            const Text(
              'Starting 7 autonomous agents',
              style: TextStyle(color: Colors.grey),
            ),
          ],
        ),
      ),
    );
  }
}

/// Error screen shown if initialization fails
class ErrorScreen extends StatelessWidget {
  final String error;
  
  const ErrorScreen({super.key, required this.error});
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(
                Icons.error_outline,
                size: 64,
                color: Colors.red,
              ),
              const SizedBox(height: 24),
              Text(
                'Initialization Failed',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const SizedBox(height: 16),
              Text(
                error,
                textAlign: TextAlign.center,
                style: const TextStyle(color: Colors.grey),
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () {
                  // Restart app
                },
                child: const Text('Retry'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
