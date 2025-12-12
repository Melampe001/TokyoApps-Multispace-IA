package com.tokyoia.app

import android.app.Application
import android.util.Log

/**
 * Tokyo-IA Application class
 * Main entry point for the Android application
 */
class TokyoApp : Application() {
    
    companion object {
        private const val TAG = "TokyoApp"
    }

    override fun onCreate() {
        super.onCreate()
        Log.d(TAG, "Tokyo-IA Application started")
        
        // Initialize application-wide services here
        initializeServices()
    }

    private fun initializeServices() {
        // TODO: Initialize Firebase, AI services, etc.
        Log.d(TAG, "Services initialized")
    }
}
