# Mono build scripts for Godot
This repository contains scripts for building the Mono runtime to use with Godot Engine

## Command-line options

**Requires Python 3.7 or higher**

These scripts are based on the Mono [sdks](https://github.com/mono/mono/tree/master/sdks) makefiles, with some changes to work well with Godot. Some platforms or targets depend on files from the `sdks` directory in the Mono source repository. This directory may be missing from tarballs. If that's the case, cloning the git repository may be needed. [This table](https://www.mono-project.com/docs/about-mono/versioning/#mono-source-versioning) can be used to determine the branch for a specific version of Mono.

Run `python SCRIPT.py --help` for the full list of command line options.

By default, the scripts will install the resulting files to `$HOME/mono-installs`.
A custom output directory can be specified with the `--install-dir` option.

When cross-compiling to Windows, `--mxe-prefix` must be specified. For example, with the `mingw-w64` package installed on Ubuntu, one can pass `--mxe-prefix=/usr`.

A path to the Mono source tree must be provided with the `--mono-sources` option or with the `MONO_SOURCE_ROOT` environment variable:

```bash
export MONO_SOURCE_ROOT=$HOME/git/mono
```

### Notes
- Python 3.7 or higher is required.
- Cross-compiling for macOS via osxcross is not yet supported.
- Building on Windows is not supported. It's possible to use Cygwin or WSL (Windows Subsystem for Linux) but this hasn't been tested.

## Desktop

```bash
# Build the runtimes for 32-bit and 64-bit Linux.
./linux.py configure --target=i686 --target=x86_64
./linux.py make --target=i686 --target=x86_64

# Build the runtimes for 32-bit and 64-bit Windows.
./windows.py configure --target=i686 --target=x86_64 --mxe-prefix=/usr
./windows.py make --target=i686 --target=x86_64 --mxe-prefix=/usr

# Build the runtime for 64-bit macOS.
./osx.py configure --target=x86_64
./osx.py make --target=x86_64
```

_AOT cross-compilers for desktop platforms cannot be built with these scripts yet._

## Android

Some patches may need to be applied to the Mono sources before building for Android. This can be done by running `./patch_mono.py`.

```bash
# These are the default values. This step can be omitted if SDK and NDK root are in this location.
export ANDROID_SDK_ROOT=$HOME/Android/Sdk
export ANDROID_NDK_ROOT=$ANDROID_SDK_ROOT/ndk-bundle

# Build the runtime for all supported Android ABIs.
./android.py configure --target=all-runtime
./android.py make --target=all-runtime

# Build the AOT cross-compilers targeting all supported Android ABIs.
./android.py configure --target=all-cross
./android.py make --target=all-cross

# Build the AOT cross-compilers for Windows targeting all supported Android ABIs.
./android.py configure --target=all-cross-win --mxe-prefix=/usr
./android.py make --target=all-cross-win --mxe-prefix=/usr
```

The option `--target=all-runtime` is a shortcut for `--target=armeabi-v7a --target=x86 --target=arm64-v8a --target=x86_64`. The equivalent applies for `all-cross` and `all-cross-win`.

## WebAssembly

Just like with Godot, an active Emscripten SDK is needed for building the Mono WebAssembly runtime.

Some patches may need to be applied to the Emscripten SDK before building Mono. This can be done by running `./patch_emscripten.py`.

```bash
# Build the runtime for WebAssembly.
./wasm.py configure --target=runtime
./wasm.py make --target=runtime
```

_AOT cross-compilers for WebAssembly cannot be built with this script yet._

## Base Class library

```bash
# Build the Desktop BCL.
./bcl.py make --product=desktop

# Build the Desktop BCL for Windows.
./bcl.py make --product=desktop-win32

# Build the Android BCL.
./bcl.py make --product=android

# Build the WebAssembly BCL.
./bcl.py make --product=wasm
```

## Reference Assemblies

```bash
./reference_assemblies.py install
```
