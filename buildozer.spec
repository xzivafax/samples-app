[app]
title = Мои образцы
package.name = samplesapp
package.domain = org.mycompany

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 0.1

requirements = python3,kivy==2.2.1,requests

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE

android.api = 31
android.minapi = 21
android.ndk = 23b
android.sdk = 31
android.accept_sdk_license = True
android.use_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./buildozer
bin_dir = ./bin
