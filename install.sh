#!/bin/bash
set -eu

sudo mkdir -p /opt/tp3607-linux
sudo cp internal_speakers_i2c.sh /opt/tp3607-linux/internal_speakers_i2c.sh
sudo chmod +x /opt/tp3607-linux/internal_speakers_i2c.sh

sudo cp asus-tp3607-speaker-i2c-setup.service /etc/systemd/system/asus-tp3607-speaker-i2c-setup.service
sudo systemctl daemon-reload
sudo systemctl enable --now asus-tp3607-speaker-i2c-setup.service

sudo cp ish/ish_lnlm.bin /usr/lib/firmware/intel/ish/ish_lnlm.bin
