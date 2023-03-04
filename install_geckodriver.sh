#!/bin/bash

# USAGE:
# Run script in <venv>/bin/

# Check on https://github.com/mozilla/geckodriver/releases for the latest release
wget https://github.com/mozilla/geckodriver/releases/download/v0.32.2/geckodriver-v0.32.2-linux32.tar.gz
tar -xvzf geckodriver-v0.32.2-linux32.tar.gz
rm geckodriver-v0.32.2-linux32.tar.gz
chmod +x geckodriver

PATH=$PATH:$(pwd)/geckodriver
export PATH

geckodriver --version