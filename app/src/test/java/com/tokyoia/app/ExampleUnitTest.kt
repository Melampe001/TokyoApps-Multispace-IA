package com.tokyoia.app

import org.junit.Test
import org.junit.Assert.*

/**
 * Example local unit test, which will execute on the development machine (host).
 *
 * See [testing documentation](http://d.android.com/tools/testing).
 */
class ExampleUnitTest {
    @Test
    fun addition_isCorrect() {
        assertEquals(4, 2 + 2)
    }
    
    @Test
    fun app_version_isValid() {
        val version = "1.0.0"
        assertTrue(version.matches(Regex("\\d+\\.\\d+\\.\\d+")))
    }
}
