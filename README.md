<h1 align="center">MCPIL</h1>

<p align="center">
  Simple GUI launcher for Minecraft: Pi Edition and <a href="https://gitea.thebrokenrail.com/TheBrokenRail/minecraft-pi-reborn/">MCPI-Reborn</a>.
</p>

<p align="center">
	<a href="https://github.com/MCPI-Revival/MCPIL/blob/master/LICENSE">
		<img src="https://img.shields.io/github/license/MCPI-Revival/MCPIL?label=License" alt="GPL-2.0"></img>
	</a>																						   
	<a href="https://python.org">
		<img src="https://img.shields.io/badge/Python-%E2%89%A53.7.x-blue" alt="Required Python version"></img>
	</a>
	<a href="https://github.com/MCPI-Revival/MCPIL/actions?query=workflow%3ACodeQL">
		<img src="https://github.com/MCPI-Revival/MCPIL/workflows/CodeQL/badge.svg" alt="CodeQL results"></img>
	</a>
</p>

<p align="center">
	<img src="https://i.imgur.com/H9LLI0h.png" alt="screenshot"></img>
</p>

> This is a rewrite of the original [MCPIL](https://github.com/MCPI-Devs/MCPIL-Old) project meant to be less fragile and more compatible.

## Getting started

### Prerequisites
- Python >= 3.7.x
- [MCPI-Reborn](https://gitea.thebrokenrail.com/TheBrokenRail/minecraft-pi-reborn)

### System Requirements
Raspbian Buster/Ubuntu 18.04 Or Higher

### Installation
[![badge](https://github.com/Botspot/pi-apps/blob/master/icons/badge.png?raw=true)](https://github.com/Botspot/pi-apps)

## Features
 + Switch between Minecraft Pi and MCPE GUI/Touch GUI
 + Multiplayer and multiplayer username changing
 + Render distance toggle
 + Coming soon: More stuff 

## Changelog
[View Changelog](CHANGELOG.md)

## Debian Packages
[GitHub Releases](https://github.com/MCPI-Devs/MCPIL/releases/latest)

## Compiling/Packaging
```sh
git clone --recurse-submodules https://github.com/MCPI-Devs/MCPIL.git
cd MCPIL
./scripts/package.sh
```
