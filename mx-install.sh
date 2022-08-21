#!/bin/bash
#
# Simple install script for prettyasm
# for use under MX Linux
#
sudo rm -rf /usr/local/bin/prettyasm || true
sudo ln -s $HOME/Software/PrettyASM/prettyasm /usr/local/bin/prettyasm
chmod +x prettyasm
