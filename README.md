# ASUS-TP3607-Linux
Tweaks for getting the ASUS TP306SA (Vivobook 16 flip) working on Linux.

## ISH Firmware
Provided in this repo. Obtained by downloading the "Intel Integrated Sensor Solution Driver" from ASUS at https://www.asus.com/us/supportonly/tp3607sa/helpdesk_download/
then running it in Windows, choosing the "Extract" option and grabbing the .bin file from Drivers/IshHeciExtensionTemplate/x64/FwImage/0003/

Place it in /usr/lib/firmware/intel/ish/ish_lnlm.bin and update your intitramfs (I did in Fedora by running `sudo dracut --force`).

You should then see it successful load in dmesg upon boot. e.g.
```sh
$ sudo dmesg | grep ish_ipc
[    2.329128] intel_ish_ipc 0000:00:12.0: ISH loader: load firmware: intel/ish/ish_lnlm.bin
[    2.355941] intel_ish_ipc 0000:00:12.0: ISH loader: firmware loaded. size:535040
[    2.355949] intel_ish_ipc 0000:00:12.0: ISH loader: FW base version: 5.8.0.7724
[    2.355951] intel_ish_ipc 0000:00:12.0: ISH loader: FW project version: 1.0.0.12631

```

This should allow some extra sensors to work, like the accelerometers for the tablet mode and autorotation section below.

## Audio
No audio output through speakers or 3.5mm jack out of the box currently.
Reported https://github.com/thesofproject/linux/issues/5504
and https://github.com/thesofproject/linux/issues/5473


I was able to get the internal speakers working by following:

https://gist.github.com/rraks/4edddb99b50b94fe6298adbf3c9f43eb

e.g i2c bus id is '0' from:
```
$ sudo modprobe i2c-dev
$ ls -alh /sys/bus/i2c/devices/
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-0 -> ../../../devices/pci0000:00/0000:00:15.0/i2c_designware.0/i2c-0
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-1 -> ../../../devices/pci0000:00/0000:00:19.0/i2c_designware.1/i2c-1
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-10 -> ../../../devices/pci0000:00/0000:00:02.0/i2c-10
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-11 -> ../../../devices/pci0000:00/0000:00:02.0/i2c-11
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-12 -> ../../../devices/pci0000:00/0000:00:02.0/drm/card1/card1-eDP-1/i2c-12
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-13 -> ../../../devices/pci0000:00/0000:00:02.0/drm/card1/card1-DP-1/i2c-13
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-14 -> ../../../devices/pci0000:00/0000:00:02.0/drm/card1/card1-DP-2/i2c-14
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-2 -> ../../../devices/pci0000:00/0000:00:19.1/i2c_designware.2/i2c-2
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-3 -> ../../../devices/pci0000:00/0000:00:02.0/i2c-3
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-4 -> ../../../devices/pci0000:00/0000:00:02.0/i2c-4
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-5 -> ../../../devices/pci0000:00/0000:00:02.0/i2c-5
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-6 -> ../../../devices/pci0000:00/0000:00:02.0/i2c-6
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-7 -> ../../../devices/pci0000:00/0000:00:02.0/i2c-7
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-8 -> ../../../devices/pci0000:00/0000:00:02.0/i2c-8
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-9 -> ../../../devices/pci0000:00/0000:00:02.0/i2c-9
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-ASCF1201:00 -> ../../../devices/pci0000:00/0000:00:19.1/i2c_designware.2/i2c-2/i2c-ASCF1201:00
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-TIAS2781:00 -> ../../../devices/pci0000:00/0000:00:15.0/i2c_designware.0/i2c-0/i2c-TIAS2781:00
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-TXNW3643:01 -> ../../../devices/pci0000:00/0000:00:15.0/i2c_designware.0/i2c-0/i2c-TXNW3643:01
lrwxrwxrwx. 1 root root 0 Oct 25 15:58 i2c-WDHT1F01:00 -> ../../../devices/pci0000:00/0000:00:19.0/i2c_designware.1/i2c-1/i2c-WDHT1F01:00

```
My resulting script from following that guide is in internal_speakers_i2c.sh

I currently don't get output from the headphone jack, although it seems like version sof-firmware is available, but likely just not available in Fedora (42) yet to enable this.

## Tablet mode and auto rotate
Make sure you have installed iio-sensor-proxy (e.g. `sudo dnf install iio-sensor-proxy`) and the ISH firmware is being loaded properly. Accelerometer orientation should now change when you tilt the laptop in different directions (https://gitlab.freedesktop.org/hadess/iio-sensor-proxy/ for more information).

I am using KDE6 on Wayland and so auto rotations works right awayw

https://github.com/asus-linux-drivers/asus-fliplock-driver works to run commands on KEY_PROG2 events that indicate flip transitions.

To get auto touch mode working in KDE6, I added commented out all the other commands in `conf/default.py` and added `su [username] bash -c '/opt/tp3607-linux/toggle_touch_mode.py on/off'`.


## Other useful software
https://github.com/intel/intel-lpmd

Disabled tuned or others before enabling tlp