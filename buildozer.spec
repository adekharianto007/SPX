[app]

title = ADEK HARIANTO
package.name = adekharianto
package.domain = org.adekharianto

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,html,js,css,json
source.include_patterns = assets/*,assets/**/*

version = 1.0

# Kivy hanya dipakai sebagai shell minimal; kamera & rendering
# sesungguhnya ditangani Android WebView native.
#
# CATATAN: Downgrade Kivy ke 2.1.0 yang stable dan support Python 3.10+
# tanpa issue Cython dengan Python 3.14. Versi 2.3.0 belum fully support
# Python 3.14 API changes dalam compiled C extensions.
#
# pyjnius WAJIB ada untuk komunikasi Python → Java (WebView setup & bridge).
requirements = python3,kivy==2.1.0,pyjnius,android

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
# Source Java tambahan (WebViewHelper.java) ikut dikompilasi bersama APK.
add_src = src

android.permissions = CAMERA,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# WebView modern (getUserMedia, dsb) butuh minimal API yang cukup baru.
android.minapi = 21
android.api = 34
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a

android.allow_backup = True

# Diperlukan agar PermissionRequest.grant() & androidx tersedia.
android.gradle_dependencies = androidx.core:core:1.12.0

# Declare camera hardware features
android.features = android.hardware.camera,android.hardware.camera.autofocus

p4a.bootstrap = sdl2
