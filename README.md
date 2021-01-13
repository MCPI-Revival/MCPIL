# MCPIL-R
This is a rewrite of th original [MCPIL](https://github.com/MCPI-Devs/MCPIL) project meant to be less fragile and more compatible.

## Getting started

### Prerequisites
- Python >= 3.7.x
- [MCPI-Docker](https://gitea.thebrokenrail.com/TheBrokenRail/minecraft-pi-docker)

### System Requirements
Raspbian Buster/Ubuntu 18.04 Or Higher

### Installation
Download and install MCPIL from the Packagecloud Debian repository:

```
# If you didn't add the repository yet
curl -s https://packagecloud.io/install/repositories/Alvarito050506/mcpi-devs/script.deb.sh | sudo bash

# Now the actual installation
sudo apt-get install mcpil-r
```

## Changelog
[View Changelog](CHANGELOG.md)

## Debian Packages
[GitHub Releases](https://github.com/MCPI-Devs/MCPIL-R/releases/latest)

## Packaging
```sh
git clone --recurse-submodules https://github.com/MCPI-Devs/MCPIL-R.git
cd MCPIL-R
./scripts/package.sh
```
