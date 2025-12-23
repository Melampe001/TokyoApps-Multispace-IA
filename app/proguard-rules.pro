# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.
#
# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

# Keep Tokyo-IA specific classes
-keep class com.tokyoia.app.** { *; }

# Keep Kotlin metadata
-keep class kotlin.Metadata { *; }

# General Android rules
-keepattributes *Annotation*
-keepattributes Signature
-keepattributes Exception

# If you keep the line number information, uncomment this to
# hide the original source file name.
#-renamesourcefileattribute SourceFile
