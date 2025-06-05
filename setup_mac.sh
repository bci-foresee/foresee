#!/bin/bash

set -e  # Exit on error

# === CONFIG ===
TCL_VERSION="8.6.12"
TCL_DIR="/opt/tcl86"
FORESEE_DIR="$(pwd)"
OPENSTA_DIR="$FORESEE_DIR/backend/external/OpenSTA"
BUILD_DIR="$OPENSTA_DIR/build"

# === 1. Install system dependencies ===
echo "🔧 Installing required tools via Homebrew..."
brew install bison flex cmake swig eigen

# === 2. Download and build Tcl 8.6 ===
if [ ! -d "$TCL_DIR" ]; then
  echo "📦 Building Tcl $TCL_VERSION from source..."
  curl -L -O "https://downloads.sourceforge.net/project/tcl/Tcl/${TCL_VERSION}/tcl${TCL_VERSION}-src.tar.gz"
  tar -xzf "tcl${TCL_VERSION}-src.tar.gz"
  cd "tcl${TCL_VERSION}/unix"
  ./configure --prefix="$TCL_DIR"
  make -j8
  sudo make install
  cd "$FORESEE_DIR"
  rm -rf "tcl${TCL_VERSION}" "tcl${TCL_VERSION}-src.tar.gz"
else
  echo "✅ Tcl already installed at $TCL_DIR"
fi

# === 3. Set environment variables ===
echo "🌱 Setting build environment..."
export PATH="$(brew --prefix bison)/bin:$(brew --prefix flex)/bin:$PATH"
export CMAKE_INCLUDE_PATH="$(brew --prefix flex)/include"
export CMAKE_LIBRARY_PATH="$(brew --prefix flex)/lib:$(brew --prefix bison)/lib"
export CFLAGS="-I${TCL_DIR}/include"
export LDFLAGS="-L${TCL_DIR}/lib"

# === 4. Build OpenSTA ===
echo "🏗️  Building OpenSTA..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"
cd "$BUILD_DIR"

cmake .. \
  -DBISON_EXECUTABLE="$(brew --prefix bison)/bin/bison" \
  -DFLEX_EXECUTABLE="$(brew --prefix flex)/bin/flex" \
  -DTCL_LIBRARY="${TCL_DIR}/lib/libtcl8.6.dylib"

make -j8

# === 5. Verify output ===
if [ -f "$BUILD_DIR/sta" ]; then
  echo ""
  echo "✅ Build complete!"
  echo "   OpenSTA binary is located at:"
  echo "   $BUILD_DIR/sta"
  echo ""
  echo "To run:"
  echo "   $BUILD_DIR/sta --version"
else
  echo "❌ Build failed — 'sta' binary not found."
  exit 1
fi
