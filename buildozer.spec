[app]

title = Academic Word Editor
package.name = academicword
package.domain = org.academic

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf,otf,txt,md
source.exclude_dirs = tests,bin,venv,.buildozer,.git,__pycache__

version = 5.0.0

icon.filename = %(source.dir)s/assets/icon.png

android.presplash_color = #37474F

requirements = python3,kivy==2.1.0,arabic-reshaper,pillow

p4a.branch = v2024.01.21
p4a.bootstrap = sdl2

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.allow_backup = True

[buildozer]

log_level = 2
warn_on_root = 0
