# Tokyo-IA
genera ramas ordenadas y flujos optimizados. crea archivos giphu
app/src/main/AndroidManifest.xml<application
    android:name=".TokyoApp"
    android:label="TokyoIA"
    android:icon="@mipmap/ic_launcher">scripts/bump-version.sh#!/bin/bash
VERSION=$(grep versionName app/build.gradle | awk '{print $2}' | tr -d '"')
IFS='.' read -r major minor patch <<< "$VERSION"
patch=$((patch + 1))
NEW_VERSION="$major.$minor.$patch"

sed -i "s/versionName \".*\"/versionName \"$NEW_VERSION\"/" app/build.gradle

echo "🚀 Nueva versión: $NEW_VERSION"🔥 
Notas de TokyoIA
• Motor MCP mejorado
• IA más rápida
• Mejoras visuales
• Correccioneswhatsnew/en-US/whatsnew.txt
whatsnew/es-MX/whatsnew.txt
app/build.gradle
android {
    compileSdk 34

    defaultConfig {
        applicationId "com.tokyoia.app"
        minSdk 24
        targetSdk 34
        versionCode 1
        versionName "1.0.0"
    }

    signingConfigs {
        release {
            storeFile file("tokyoia-keystore.jks")
            storePassword System.getenv("ANDROID_KEYSTORE_PASSWORD")
            keyAlias System.getenv("ANDROID_KEY_ALIAS")
            keyPassword System.getenv("ANDROID_KEY_PASSWORD")
        }
    }

    buildTypes {
        release {
            minifyEnabled true
            shrinkResources true
            signingConfig signingConfigs.release
            proguardFiles getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro"
        }

        debug {
            minifyEnabled false
        }
    }

    bundle {
        storeArchive {
            enable = true
        }
    }
}

dependencies {
    implementation 'androidx.core:core-ktx:1.13.0'
    implementation 'androidx.appcompat:appcompat:1.7.0'
    implementation 'com.google.android.material:material:1.12.0'
} 
android.enableJetifier=true
android.useAndroidX=true
org.gradle.jvmargs=-Xmx4G -Dfile.encoding=UTF-8tokyoia-release-to-play.yml (Workflow PRO – Opción B)

Guárdalo en:

.github/workflows/tokyoia-release-to-play.yml

Aquí va completo:

name: 🚀 TokyoIA – Publish to Google Play

on:
  workflow_dispatch:
  push:
    tags:
      - "v*.*.*"

jobs:
  deploy:
    name: Upload AAB to Google Play
    runs-on: ubuntu-latest

    steps:
      # 1. Checkout
      - name: 🧩 Checkout code
        uses: actions/checkout@v4

      # 2. Install JDK
      - name: ☕ Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      # 3. Decode Keystore
      - name: 🔐 Decode Keystore
        run: |
          echo "$ANDROID_KEYSTORE_BASE64" | base64 -d > tokyoia-keystore.jks

      # 4. Create Google Play Service Account JSON
      - name: 🧾 Create Google Play JSON key
        run: |
          echo "$GOOGLE_PLAY_JSON" > google-play-key.json
{
  "type": "service_account",
  "project_id": "tu-proyecto-google",
  "private_key_id": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIBV...TU CLAVE COMPLETA ...\n-----END PRIVATE KEY-----\n",
  "client_email": "google-play@tu-proyecto-google.iam.gserviceaccount.com",
  "client_id": "123456789012345678901",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/google-play%40tu-proyecto-google.iam.gserviceaccount.com"
}GOOGLE_PLAY_JSON
GOOGLE_PLAY_JSON
