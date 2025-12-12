package com.tokyoia.app

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.widget.TextView

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Create a simple TextView programmatically for testing
        val textView = TextView(this).apply {
            text = "Tokyo-IA App\nVersion 1.0.0\nReady for Testing"
            textSize = 24f
            setPadding(32, 32, 32, 32)
        }
        
        setContentView(textView)
    }
}
