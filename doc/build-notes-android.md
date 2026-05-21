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

## Earlier Windows Blockers

- WSL is not installed.
- The Android SDK does not currently include NDK r23.
- The Android SDK does not currently include `cmdline-tools/latest/bin/sdkmanager.bat`.
- Extracting `dependencies-android-src.tar.xz` with Windows `tar.exe` failed on
  Unix-style paths/symlinks.
- Extracting Android command-line tools with PowerShell `Expand-Archive` failed
  on long nested paths.
- Git Bash is installed, but this Windows install does not include GNU `make`
  or `xz`.

## Home PC Build Status, 2026-05-20

The repository has been cloned on the home PC at:

```text
C:\Users\owagn\Documents\Codex\2026-05-20\codex-estou-continuando-o-projeto-supertuxkart\supertuxkart-br
```

Initial checks on this machine:

- `wsl.exe` exists at `C:\WINDOWS\system32\wsl.exe`.
- WSL now reports default version 2.
- `wsl.exe --install --no-distribution` completed successfully to enable the
  WSL2 virtual machine platform component.
- Installing Ubuntu with WSL2 still fails with
  `HCS_E_HYPERV_NOT_INSTALLED`, which means Windows cannot start the WSL2 VM
  until the machine is restarted and/or firmware virtualization is enabled.
- `wsl.exe --install --enable-wsl1 --no-distribution` completed, but Windows
  reported that changes only take effect after a restart.
- No WSL distribution is currently registered.
- Android SDK is not present at `%LOCALAPPDATA%\Android\Sdk`.
- `svn` is not currently available in `PATH`.
- `java -version` reports Java 8 (`1.8.0_251`).

After restart, WSL2 was still blocked by `HCS_E_HYPERV_NOT_INSTALLED`, so the
Android build was completed with Ubuntu running as WSL1. The working distro is
`Ubuntu-STK`, visible from elevated PowerShell.

The Android SDK packages were installed outside the repository, next to it:

```text
C:\Users\owagn\Documents\Codex\2026-05-20\codex-estou-continuando-o-projeto-supertuxkart\android-sdk
```

Installed SDK/NDK pieces:

- `platform-tools`
- `platforms;android-35`
- `build-tools;35.0.0`
- `build-tools;34.0.0` (downloaded by Gradle during the first APK build)
- `ndk;28.1.13356709`
- `ndk;23.1.7779620`

NDK r28 failed under WSL1 with `clang: cannot execute binary file: Exec format
error`. NDK r23.1.7779620 worked and was used for the successful APK build.

Additional Ubuntu packages needed beyond the first dependency list:

```bash
apt-get install -y openjdk-21-jdk gradle dos2unix meson ninja-build ccache \
  glslang-tools python3-mako python3-ply python3-yaml pkg-config \
  bison byacc flex
```

The official `dependencies-android-src.tar.xz` extracted `libadrenotools` with
an empty `lib/linkernsbypass` directory. The missing subdependency was restored
locally with:

```powershell
git clone https://github.com/bylaws/liblinkernsbypass.git lib\libadrenotools\lib\linkernsbypass
```

`android/make_deps.sh` was adjusted so `libadrenotools` can be copied from the
extracted dependency package when it is not a local Git repository. This lets the
official dependency tarball build cleanly after `linkernsbypass` is present.

The successful smoke-test build used a minimal asset set:

For the Caramelo Dash character test roster, first create the placeholder karts
inside the sibling `stk-assets` checkout:

```powershell
.\tools\create_caramelo_placeholder_karts.ps1 -Force
```

```bash
cd /mnt/c/Users/owagn/Documents/Codex/2026-05-20/codex-estou-continuando-o-projeto-supertuxkart/supertuxkart-br/android

export KARTS='atho popo favela nina'
export TRACKS=abyss
export RUN_OPTIMIZE_SCRIPT=0
export DECREASE_QUALITY=1
export COMPILE_ARCH=aarch64
export BUILD_TYPE=debug

bash ./generate_assets.sh
```

Dependencies were built with:

```bash
export NDK_PATH=/mnt/c/Users/owagn/Documents/Codex/2026-05-20/codex-estou-continuando-o-projeto-supertuxkart/android-sdk/ndk
export STK_NDK_VERSION=23.1.7779620
export COMPILE_ARCH=aarch64
export BUILD_TYPE=debug

bash ./make_deps.sh
```

The debug APK was generated successfully with:

```bash
export SDK_PATH=/mnt/c/Users/owagn/Documents/Codex/2026-05-20/codex-estou-continuando-o-projeto-supertuxkart/android-sdk
export NDK_PATH=/mnt/c/Users/owagn/Documents/Codex/2026-05-20/codex-estou-continuando-o-projeto-supertuxkart/android-sdk/ndk
export STK_NDK_VERSION=23.1.7779620
export STK_TARGET_ANDROID_SDK=35
export STK_MIN_ANDROID_SDK=21
export COMPILE_ARCH=aarch64
export BUILD_TYPE=debug

bash ./make.sh
```

Generated APK:

```text
C:\Users\owagn\Documents\Codex\2026-05-20\codex-estou-continuando-o-projeto-supertuxkart\supertuxkart-br\android\build\outputs\apk\debug\android-debug.apk
```

APK size from the first successful build: `93,517,526` bytes.

## Recommended Next Step

Use WSL/Ubuntu for the actual Android build. This matches upstream's supported
build environment and avoids Windows path/symlink problems. Prefer WSL2 if CPU
virtualization is available; otherwise WSL1 can work with NDK r23.

From an elevated Windows PowerShell, enable/install WSL and Ubuntu:

```powershell
wsl --install -d Ubuntu
```

If WSL2 still fails with `HCS_E_HYPERV_NOT_INSTALLED`, either enable CPU
virtualization in BIOS/UEFI or install Ubuntu as WSL1:

```powershell
wsl --install -d Ubuntu --version 1
```

If Windows reports that optional features must be enabled manually, run this in
the elevated shell, restart Windows, and then run `wsl --install -d Ubuntu`
again:

```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux -All
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -All
```

After Ubuntu opens and the Linux user is created:

```bash
sudo apt update
sudo apt install -y build-essential autoconf automake cmake git subversion \
  python3 unzip zip imagemagick vorbis-tools pngquant advancecomp optipng \
  libjpeg-turbo-progs xz-utils openjdk-21-jdk gradle dos2unix meson \
  ninja-build ccache glslang-tools python3-mako python3-ply python3-yaml \
  pkg-config bison byacc flex
```

Then prepare Android SDK command-line tools and NDK r23 inside WSL, or mount the
Windows SDK and install `ndk;23.1.7779620` with `sdkmanager`.

Expected STK Android flow:

```bash
cd /mnt/c/Users/owagn/Documents/Codex/2026-05-20/codex-estou-continuando-o-projeto-supertuxkart/supertuxkart-br/android

export SDK_PATH=/mnt/c/Users/owagn/AppData/Local/Android/Sdk
export NDK_PATH="$SDK_PATH/ndk"
export STK_NDK_VERSION=23.1.7779620
export STK_TARGET_ANDROID_SDK=35
export STK_MIN_ANDROID_SDK=21
export COMPILE_ARCH=aarch64
export BUILD_TYPE=debug

bash ./generate_assets.sh
bash ./make_deps.sh
bash ./make.sh
```

The debug APK should appear under:

```text
android/build/outputs/apk/debug/
```

## iOS Note

iOS cannot use an APK. It must be built as an iOS app/IPA with Xcode on macOS
and signed with an Apple Developer profile.

