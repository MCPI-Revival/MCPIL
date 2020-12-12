#!/bin/sh

set -e

# Prepare
rm -rf debian/tmp
mkdir debian/tmp
rm -rf out
mkdir -p out

# Copy
mkdir -p debian/tmp/opt/mcpil-r
rsync -r debian/common/ debian/tmp
rsync -r src/ debian/tmp/opt/mcpil-r

# Substitute
sed -i 's/${VERSION}/'"$(cat src/VERSION)"'/g' debian/tmp/DEBIAN/control

# Build DEB
mkdir out/deb
dpkg -b debian/tmp out/deb

# Clean Up
rm -rf debian/tmp