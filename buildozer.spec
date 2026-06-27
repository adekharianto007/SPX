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
# Versi dikunci spesifik (bukan "kivy" tanpa versi) supaya python-for-android
# tidak mencoba mengambil rilis terbaru yang wheel-nya belum tersedia untuk
# versi Python target di Android (root cause error "Could not find a version
# that satisfies the requirement kivy==2.3.1" dkk saat versi tidak dikunci
# dengan benar / toolchain python-for-android terlalu baru).
requirements = python3,kivy==2.3.0,pyjnius==1.6.1,android

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
android.minapi = 24
android.api = 34
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a

android.allow_backup = True

# Diperlukan agar PermissionRequest.grant() & androidx tersedia.
android.gradle_dependencies = androidx.core:core:1.12.0

# Kunci python-for-android ke tag rilis stabil (BUKAN branch "master").
# "master" terus bergerak dan versi terbaru sempat memilih Python 3.14
# sebagai target build di dalam APK, padahal kivy/pyjnius/android belum
# punya wheel untuk versi itu -> error "Could not find a version that
# satisfies the requirement kivy==2.3.1" dkk. Tag di bawah ini sudah
# terbukti stabil dan menghasilkan target Python 3.11.
p4a.branch = v2024.01.21

p4a.bootstrap = sdl2
