# Android Build Notes

This project is based on `supertuxkart/stk-code`. The upstream Android scripts
are shell scripts and the upstream `android/README.ANDROID` states that the
Android build is designed for Linux; Windows/Cygwin may need tweaks.

## Prepared Locally

The following pieces were prepared on the Windows machine:

- `stk-assets` was checked out next to this repository with SVN.
- Assets checkout completed at SVN revision `18626`.
- GitHub CLI was installed and the project was pushed to `owagnerjrr/supertuxkart-br`.
- CMake was installed at `C:\Program Files\CMake\bin\cmake.exe`.
- Slik SVN was installed at `C:\Program Files\SlikSVN\bin\svn.exe`.
- Android SDK exists at `%LOCALAPPDATA%\Android\Sdk`.
- JDK 21 exists at `C:\Program Files\Eclipse Adoptium\jdk-21.0.11.10-hotspot`.
- `dependencies-android-src.tar.xz` was downloaded from the official
  `supertuxkart/dependencies` preview release.

## Current Windows Blockers

- WSL is not installed.
- The Android SDK does not currently include NDK r23.
- The Android SDK does not currently include `cmdline-tools/latest/bin/sdkmanager.bat`.
- Extracting `dependencies-android-src.tar.xz` with Windows `tar.exe` failed on
  Unix-style paths/symlinks.
- Extracting Android command-line tools with PowerShell `Expand-Archive` failed
  on long nested paths.
- Git Bash is installed, but this Windows install does not include GNU `make`
  or `xz`.

## Recommended Next Step

Use WSL/Ubuntu for the actual Android build. This matches upstream's supported
build environment and avoids Windows path/symlink problems.

After WSL is installed:

```bash
sudo apt update
sudo apt install -y build-essential autoconf automake cmake git subversion \
  python3 unzip zip imagemagick vorbis-tools pngquant advancecomp optipng \
  libjpeg-turbo-progs xz-utils
```

Then prepare Android SDK command-line tools and NDK r23 inside WSL, or mount the
Windows SDK and install `ndk;23.1.7779620` with `sdkmanager`.

Expected STK Android flow:

```bash
cd /mnt/c/Users/pvg12207/Documents/Codex/2026-05-20/chat-gostaria-de-criar-um-jogo/supertuxkart-br/android

export SDK_PATH=/mnt/c/Users/pvg12207/AppData/Local/Android/Sdk
export NDK_PATH="$SDK_PATH/ndk"
export STK_NDK_VERSION=23.1.7779620
export STK_TARGET_ANDROID_SDK=35
export STK_MIN_ANDROID_SDK=16
export COMPILE_ARCH=aarch64
export BUILD_TYPE=debug

./generate_assets.sh
./make_deps.sh
./make.sh -j4
```

The debug APK should appear under:

```text
android/build/outputs/apk/debug/
```

## iOS Note

iOS cannot use an APK. It must be built as an iOS app/IPA with Xcode on macOS
and signed with an Apple Developer profile.

