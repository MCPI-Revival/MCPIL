# MCPIL
This is a rewrite of the original [MCPIL](https://github.com/MCPI-Devs/MCPIL-Old) project meant to be less fragile and more compatible.

## Getting started

### Prerequisites
- Python >= 3.7.x
- [MCPI-Reborn](https://gitea.thebrokenrail.com/TheBrokenRail/minecraft-pi-reborn)

### System Requirements
Raspbian Buster/Ubuntu 18.04 Or Higher

### Installation
Download and install MCPIL from the Packagecloud Debian repository:

```
# If you didn't add the repository yet
curl -s https://packagecloud.io/install/repositories/Alvarito050506/mcpi-devs/script.deb.sh | sudo bash

# Now the actual installation
sudo apt-get install mcpil
```

## Changelog
[View Changelog](CHANGELOG.md)

## Debian Packages
[GitHub Releases](https://github.com/MCPI-Devs/MCPIL/releases/latest)

## Packaging
```sh
git clone --recurse-submodules https://github.com/MCPI-Devs/MCPIL.git
cd MCPIL
./scripts/package.sh
```
