[app]

# (str) Title of your application
title = GymTrack Pro

# (str) Package name
package.name = gymtrackpro

# (str) Package domain (needed for android/ios packaging)
package.domain = org.mau.gymtrack

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,jpeg,kv,atlas,wav,json

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
# fuente unica de verdad: deben coincidir con las versiones usadas al
# probar la app en escritorio (ver requirements.txt)
requirements = python3,kivy==2.3.0,kivymd==1.2.0,plyer,pillow,pyjnius==1.6.1

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/assets/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/assets/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
# VIBRATE: para el aviso al terminar el descanso.
# WAKE_LOCK: evita que la pantalla se apague mientras se usa el timer.
android.permissions = VIBRATE,WAKE_LOCK

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK / AAB will support.
android.minapi = 23

# (str) Android NDK version to use
android.ndk = 25b

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Accept the SDK license without a dialog during install
android.accept_sdk_license = True

# (str) The format used to package the app for release mode (aab or apk).
android.release_artifact = apk

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
