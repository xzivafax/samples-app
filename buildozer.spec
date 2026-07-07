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

# (list) Requirements (do not specify python version here, use android.python_version)
requirements = python3,kivy==2.2.1,requests

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
# icon.filename = %(source.dir)s/data/icon.png

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE

# (int) Target Android API level
android.api = 31

# (int) Minimum API level
android.minapi = 21

# (str) Android NDK version (use recommended version 28c)
android.ndk = 28c

# (str) Android SDK version
android.sdk = 31

# (str) Build tools version (optional)
android.build_tools = 31.0.0

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

# (str) Python version for host and target (must match)
android.python_version = 3.10.14

# (str) Android Gradle plugin version
android.gradle_dependencies = 'com.android.support:multidex:1.0.3'

# (bool) Enable or disable the use of the AndroidX libraries
android.use_androidx = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (bool) Wether to warn if the buildozer is run as root
warn_on_root = 1

# (str) Path to build artifact storage
build_dir = ./buildozer

# (str) Path to the bin directory where the APK will be placed
bin_dir = ./bin
