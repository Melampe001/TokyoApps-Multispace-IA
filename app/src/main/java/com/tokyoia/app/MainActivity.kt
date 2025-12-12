package com.tokyoia.app

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

/**
 * Main Activity for Tokyo-IA
 * Entry point for the user interface
 */
class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        
        // Initialize UI components
        setupUI()
    }

    private fun setupUI() {
        // TODO: Setup chat interface, voice input, etc.
    }
}
