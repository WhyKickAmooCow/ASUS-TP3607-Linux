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

This should allow some extra sensors to work, like tablet mode detection.
