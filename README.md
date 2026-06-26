# YS - YourShell

[![Version](https://img.shields.io/github/v/release/ykazky-993/YS?color=blue&label=version)](https://github.com/ykazky-993/YS/releases)
[![Python](https://img.shields.io/badge/Python-3.6%2B-green?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/github/license/ykazky-993/YS?color=red)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/ykazky-993/YS)](https://github.com/ykazky-993/YS/issues)
[![GitHub stars](https://img.shields.io/github/stars/ykazky-993/YS?style=social)](https://github.com/ykazky-993/YS/stargazers)

A lightweight, custom shell built with Python using subprocess for enhanced system interaction and file management.

# 📋 Table of Contents
About

Features

Installation

Usage

Commands

Special Features

Configuration

Contributing

License

# 🚀 About
YS (YourShell) is a minimalist yet powerful custom shell implementation written in Python. It leverages the subprocess module to provide a seamless command-line experience while adding unique features for package management, file operations, and system ghosting capabilities.

# ✨ Features
🔧 Custom Package Management - Update and upgrade packages with simple commands

📁 Advanced File Management - Intuitive file operations with help system

👻 Ghost Features - Multiple ghosting modes for different environments

🖥️ Cross-Platform - Works on PC and Termux environments

🔄 Extensible - Easy to configure and extend

📦 Package Installation - Automated package installation scripts

📦 Installation
# Clone the repository
    git clone https://github.com/ykazky-993/YS.git

# Navigate to directory
    cd YS/yourshell

# Run YourShell
    python3 yourshell.py
# 🎯 Usage
Basic Commands
bash
# Update package lists
fdel pkg update

# Upgrade installed packages
fdel pkg upgrade

# File management help
fdel -h
Ghost Features
YS comes with powerful ghosting capabilities for various environments:

# Command	Description	Compatibility
ysGhost	Standard ghost mode	All platforms
ysGhost-x	Enhanced ghost mode	PC only
ysGhost-m	Mobile optimized	Termux & PC
ysGhost-v	Versatile mode	Termux & PC (some packages may not be found)
ysGhost-v-install	Install packages	Configure at lock/install_all.sh
# 📖 Commands Reference
Package Management
bash
fdel pkg update    # Update package lists
fdel pkg upgrade   # Upgrade all packages
File Management
bash
fdel -h            # Show file management help
Ghost Modes
bash
ysGhost            # Standard ghosting
ysGhost-x          # PC enhanced ghosting
ysGhost-m          # Mobile/Termux ghosting
ysGhost-v          # Versatile ghosting
ysGhost-v-install  # Install ghost packages
# ⚙️ Configuration
Package Configuration
You can customize package installations by editing:

lock/install_all.sh

YS automatically detects your environment (PC/Termux) and adjusts features accordingly.

# 🤝 Contributing
Contributions are welcome! If you encounter any issues or have suggestions:

Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

Reporting Issues
If you find any bugs or errors, please report them through the GitHub Issues page.

# 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

# 🙏 Acknowledgments
Built with Python's subprocess module

Inspired by the need for a lightweight, customizable shell

Special thanks to all contributors and users


