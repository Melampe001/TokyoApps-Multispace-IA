/// API Service for external API calls
library;

import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../utils/logger.dart';
import '../utils/constants.dart';

/// Service for making external API calls with retry logic
class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();
  
  final http.Client _client = http.Client();
  
  /// Make a GET request with retry logic
  Future<Map<String, dynamic>> get(
    String url, {
    Map<String, String>? headers,
    int maxRetries = AppConstants.maxRetries,
  }) async {
    return _executeWithRetry(
      () => _client.get(Uri.parse(url), headers: headers),
      maxRetries: maxRetries,
    );
  }
  
  /// Make a POST request with retry logic
  Future<Map<String, dynamic>> post(
    String url, {
    Map<String, String>? headers,
    dynamic body,
    int maxRetries = AppConstants.maxRetries,
  }) async {
    return _executeWithRetry(
      () => _client.post(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
          ...?headers,
        },
        body: body is String ? body : jsonEncode(body),
      ),
      maxRetries: maxRetries,
    );
  }
  
  /// Make a PUT request with retry logic
  Future<Map<String, dynamic>> put(
    String url, {
    Map<String, String>? headers,
    dynamic body,
    int maxRetries = AppConstants.maxRetries,
  }) async {
    return _executeWithRetry(
      () => _client.put(
        Uri.parse(url),
        headers: {
          'Content-Type': 'application/json',
          ...?headers,
        },
        body: body is String ? body : jsonEncode(body),
      ),
      maxRetries: maxRetries,
    );
  }
  
  /// Make a DELETE request with retry logic
  Future<Map<String, dynamic>> delete(
    String url, {
    Map<String, String>? headers,
    int maxRetries = AppConstants.maxRetries,
  }) async {
    return _executeWithRetry(
      () => _client.delete(Uri.parse(url), headers: headers),
      maxRetries: maxRetries,
    );
  }
  
  /// Execute HTTP request with retry logic and exponential backoff
  Future<Map<String, dynamic>> _executeWithRetry(
    Future<http.Response> Function() request, {
    required int maxRetries,
  }) async {
    int attempt = 0;
    
    while (attempt < maxRetries) {
      try {
        final response = await request();
        
        if (response.statusCode >= 200 && response.statusCode < 300) {
          return _parseResponse(response);
        } else if (response.statusCode >= 500 || response.statusCode == 429) {
          // Retry on server errors or rate limiting
          attempt++;
          if (attempt >= maxRetries) {
            throw ApiException(
              'Request failed after $maxRetries attempts',
              statusCode: response.statusCode,
              body: response.body,
            );
          }
          
          final delay = Duration(
            milliseconds: _calculateBackoffDelay(attempt),
          );
          AppLogger.warning('Request failed (${response.statusCode}), retrying in ${delay.inMilliseconds}ms');
          await Future.delayed(delay);
        } else {
          // Don't retry on client errors
          throw ApiException(
            'Request failed with status ${response.statusCode}',
            statusCode: response.statusCode,
            body: response.body,
          );
        }
      } catch (e) {
        if (e is ApiException) {
          rethrow;
        }
        
        attempt++;
        if (attempt >= maxRetries) {
          AppLogger.error('Request failed after $maxRetries attempts', e);
          rethrow;
        }
        
        final delay = Duration(
          milliseconds: _calculateBackoffDelay(attempt),
        );
        AppLogger.warning('Request error, retrying in ${delay.inMilliseconds}ms: $e');
        await Future.delayed(delay);
      }
    }
    
    throw Exception('Request failed after $maxRetries attempts');
  }
  
  /// Parse HTTP response
  Map<String, dynamic> _parseResponse(http.Response response) {
    try {
      if (response.body.isEmpty) {
        return {'status': 'success', 'statusCode': response.statusCode};
      }
      
      final decoded = jsonDecode(response.body);
      if (decoded is Map<String, dynamic>) {
        return decoded;
      } else {
        return {'data': decoded, 'statusCode': response.statusCode};
      }
    } catch (e) {
      AppLogger.error('Failed to parse response', e);
      return {
        'error': 'Failed to parse response',
        'body': response.body,
        'statusCode': response.statusCode,
      };
    }
  }
  
  /// Calculate exponential backoff delay
  int _calculateBackoffDelay(int attempt) {
    return (AppConstants.initialRetryDelayMs *
            AppConstants.retryBackoffMultiplier.pow(attempt - 1))
        .toInt();
  }
  
  /// Close the HTTP client
  void close() {
    _client.close();
  }
}

/// Custom API exception
class ApiException implements Exception {
  final String message;
  final int? statusCode;
  final String? body;
  
  ApiException(this.message, {this.statusCode, this.body});
  
  @override
  String toString() {
    return 'ApiException: $message (status: $statusCode)';
  }
}

extension on num {
  double pow(num exponent) {
    double result = 1;
    for (int i = 0; i < exponent; i++) {
      result *= this;
    }
    return result;
  }
}
