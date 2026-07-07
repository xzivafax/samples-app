[app]

# (str) Title of your application
title = Мои образцы

# (str) Package name
package.name = samplesapp

# (str) Package domain (reverse domain, e.g. org.mycompany)
package.domain = org.mycompany

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (do not include buildozer.spec)
source.include_exts = py,png,jpg,kv,atlas,ttf

# (str) Application versioning
version = 0.1

# (list) Requirements
requirements = python3==3.10.14,kivy==2.2.1,requests

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE

# (int) Target Android API level (e.g. 31 for Android 12)
android.api = 31

# (int) Minimum API level
android.minapi = 21

# (str) Android NDK version
android.ndk = 23b

# (str) Android SDK version
android.sdk = 31

# --- ДОБАВЛЕНЫ ДВЕ ВАЖНЫЕ СТРОКИ ДЛЯ АВТОМАТИЧЕСКОГО ПРИНЯТИЯ ЛИЦЕНЗИИ ---
android.build_tools = 31.0.0
android.accept_sdk_license = True

# (str) Android Gradle plugin version
android.gradle_dependencies = 'com.android.support:multidex:1.0.3'

# (bool) Enable or disable the use of the AndroidX libraries
android.use_androidx = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (bool) Wether to warn if the buildozer is run as root (dangerous)
warn_on_root = 1

# (str) Path to build artifact storage
build_dir = ./buildozer

# (str) Path to the bin directory where the APK will be placed
bin_dir = ./bin
