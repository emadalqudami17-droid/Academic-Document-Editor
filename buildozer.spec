[app]

title = Academic Word Editor
package.name = academicword
package.domain = org.academic

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf,otf,txt,md

source.include_patterns = assets/*,data/*,screens/*,widgets/*,document/*,utils/*

version = 0.1.0

requirements = python3,kivy==2.3.0,kivymd==1.1.1

icon.filename = %(source.dir)s/assets/icon.png

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.api = 33
android.minapi = 24

android.archs = arm64-v8a

android.ndk = 25b

android.allow_backup = True

android.presplash_color = #37474F


[buildozer]

log_level = 2
warn_on_root = 1
