#!/bin/sh

set -e

# Set Version
echo "$(git describe --tags --dirty)" > src/VERSION

# Prepare
rm -rf debian/tmp
mkdir debian/tmp
rm -rf out
mkdir -p out

# Copy
mkdir -p debian/tmp/opt/mcpil
rsync -r debian/common/ debian/tmp
rsync -r src/ debian/tmp/opt/mcpil

# Substitute
sed -i 's/${VERSION}/'"$(cat src/VERSION)"'/g' debian/tmp/DEBIAN/control

# Build DEB
dpkg-deb -b --root-owner-group debian/tmp out

# Clean Up
rm -rf debian/tmp
