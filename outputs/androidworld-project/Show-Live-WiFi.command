#!/bin/bash
# Presentation launcher: shows the emulator while GELab-Zero really turns Wi-Fi on.
set -e
cd "$(dirname "$0")"
exec ./Run-WiFi-and-Record.command
