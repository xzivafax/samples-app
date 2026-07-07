[app]

# (str) Title of your application
title = Мои образцы

# (str) Package name
package.name = samplesapp

# (str) Package domain
package.domain = org.mycompany

# (str) Source code location
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,ttf

# (str) Application version
version = 0.1

# (list) Requirements (без указания версии python, чтобы p4a сам подобрал совместимую)
requirements = python3,kivy==2.2.1,requests

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 31

# (int) Minimum API
android.minapi = 21

# (str) NDK version (используем рекомендованную 28c)
android.ndk = 28c

# (str) SDK version
android.sdk = 31

# (str) Build tools version (фиксируем)
android.build_tools = 31.0.0

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

# (str) Python version for host (совместимая с целевой)
android.python_version = 3.10.14

# (str) Gradle dependencies
android.gradle_dependencies = 'com.android.support:multidex:1.0.3'

# (bool) Use AndroidX
android.use_androidx = True

[buildozer]

# (int) Log level
log_level = 2

# (bool) Warn if run as root
warn_on_root = 1

# (str) Build directory
build_dir = ./buildozer

# (str) Binary directory
bin_dir = ./bin
