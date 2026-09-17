[app]

title = Academic Word Editor

package.name = academicword

package.domain = org.academic

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf,otf,txt,md

source.include_patterns = assets/*,data/*,screens/*,widgets/*,document/*,utils/*

version = 2.2.0

requirements = python3,kivy==2.3.0,kivymd==1.1.1,arabic-reshaper,python-bidi

icon.filename = %(source.dir)s/assets/icon.png

orientation = portrait

fullscreen = 0


# ============================================================
# Android
# ============================================================

android.api = 33

android.minapi = 24

android.ndk = 25b

android.archs = arm64-v8a

android.allow_backup = True

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.debug_artifact = apk


# ============================================================
# Python-for-Android
# ============================================================

p4a.url = https://github.com/kivy/python-for-android.git

p4a.fork = kivy

p4a.branch = master

p4a.commit = 957a3e5


# ============================================================
# Android Appearance
# ============================================================

android.presplash_color = #37474F


# ============================================================
# Buildozer
# ============================================================

[buildozer]

log_level = 2

warn_on_root = 1
