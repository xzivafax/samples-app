[app]

title = Samples App
package.name = samplesapp
package.domain = org.example

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,kv,atlas,ttf,json

version = 0.1

requirements = python3,kivy

orientation = portrait
fullscreen = 0

log_level = 2
warn_on_root = 1

android.api = 34
android.minapi = 23
android.ndk = 28b
android.accept_sdk_license = True

# РµСЃР»Рё РµСЃС‚СЊ main.py
source.exclude_dirs = venv,.venv,bin,.git,__pycache__
