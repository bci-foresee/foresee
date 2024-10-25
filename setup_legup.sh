#!/bin/bash

# Install required packages for LegUp and general build tools
echo "Installing required packages..."
sudo apt-get update
sudo apt-get install -y llvm clang make cmake g++ build-essential git tcl-dev libgmp-dev libmpfr-dev

# Remove any existing cached LegUp submodule data
echo "Removing previous cached LegUp submodule (if exists)..."
if [ -d "external/legup" ]; then
  git rm --cached external/legup
  rm -rf external/legup
else
  echo "No previous submodule found for LegUp."
fi

# Correct LegUp repository URL (example URL, update with actual repository)
LEGUP_REPO_URL="https://github.com/legup-hls/legup-hls.git"  # Update with the actual repository URL

# Initialize the submodule for LegUp
echo "Adding LegUp as a submodule..."
git submodule add --force $LEGUP_REPO_URL external/legup
if [ $? -ne 0 ]; then
  echo "Failed to add LegUp submodule. Please check if the repository URL is correct."
  exit 1
fi

git submodule init
git submodule update

# Navigate into the LegUp directory and build it
echo "Building LegUp..."
if [ -d "external/legup" ]; then
  cd external/legup/
  mkdir build
  cd build
  cmake ..
  if [ $? -ne 0 ]; then
    echo "CMake configuration failed. Check for missing CMakeLists.txt or dependencies."
    exit 1
  fi
  make
else
  echo "LegUp submodule directory not found. Build process cannot proceed."
  exit 1
fi

# Add LegUp to the PATH by appending it to .bashrc
echo "Adding LegUp to PATH..."
echo "export PATH=\$PATH:$(pwd)/bin" >> ~/.bashrc
source ~/.bashrc

# Verify the installation
echo "Verifying LegUp installation..."
if command -v legup >/dev/null 2>&1; then
    echo "LegUp installed successfully and is ready to use!"
else
    echo "LegUp installation failed."
    exit 1
fi
