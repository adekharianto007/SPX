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
# CATATAN PENTING soal versi Python target di Android:
# python-for-android (p4a) menentukan sendiri versi Python yang dikompilasi
# ke dalam APK berdasarkan resep (recipe) python3 yang dipakai. Build
# sebelumnya gagal karena p4a memilih Python 3.14, sementara pyjnius
# (jembatan ke Java) memakai sintaks lama yang sudah dibuang Cython modern
# untuk target sebaru itu. "python3" di requirements TIDAK mengunci versi
# minor secara langsung lewat buildozer.spec biasa -- versi sesungguhnya
# ditentukan oleh resep python3 di dalam python-for-android itu sendiri.
# Karena itu, perbaikan utama untuk masalah ini ada di langkah CI
# (.github/workflows/build.yml), bukan di sini: di sana kita memaksa p4a
# yang dipakai berasal dari rilis PyPI yang sudah teruji (bukan clone
# langsung dari branch master GitHub yang versinya terus berubah).
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

p4a.bootstrap = sdl2
