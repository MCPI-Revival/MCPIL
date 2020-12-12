### :warning: WARNING
The MCPIL rewrite is under active development and is very unstable. Anything can change at any time.

# MCPIL-R
This is a rewrite of th original MCPIL project meant to be less fragile and more compatible.

## System Requirements
Raspbian Buster/Ubuntu 18.04 Or Higher

## Dependencies
- Python 3
- [MCPI-Docker](https://gitea.thebrokenrail.com/TheBrokenRail/minecraft-pi-docker)

## Packaging
```sh
git clone --recurse-submodules https://github.com/MCPI-Devs/MCPIL-R.git
cd MCPIL-R
pip3 install python-minifier
./scripts/package.sh
```