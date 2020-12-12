#!/bin/sh

set -e

# Prepare
rm -rf debian/tmp
mkdir debian/tmp
rm -rf out
mkdir -p out

# Add PIP To PATH
export PATH="${HOME}/.local/bin:${PATH}"

# Copy
mkdir -p debian/tmp/opt/mcpil-r
rsync -r debian/common/ debian/tmp
rsync -r src/ debian/tmp/opt/mcpil-r
minify() {
    # $1 = Input
    find "$1" -name '*.py' -exec sh -c 'OUT="$(pyminify --rename-globals --remove-literal-statements "$1")"; echo "${OUT}" > "$1"' -- {} \;
}
minify debian/tmp/opt/mcpil-r

# Substitute
sed -i 's/${VERSION}/'"$(cat src/VERSION)"'/g' debian/tmp/DEBIAN/control

# Build DEB
mkdir out/deb
dpkg -b debian/tmp out/deb

# Clean Up
#rm -rf debian/tmp