#!/usr/bin/env python3

# Adapted from: https://discuss.kde.org/t/a-script-to-toggle-tablet-mode-or-touch-mode-on-plasma/19224

import sys
import subprocess
import gi

gi.require_version('Gio', '2.0')
from gi.repository import Gio, GLib

KDE_VERSION = 6
OBJECT_PATH = '/kwinrc'
INTERFACE_NAME = 'org.kde.kconfig.notify'
SIGNAL_NAME = 'ConfigChanged'


def usage_and_exit():
    print("Usage: toggle_touch_mode.py [on|off|toggle]")
    print("If no argument is given the script will toggle the current state (previous behaviour).")
    sys.exit(2)

# Behaviour:
# - no args: toggle (preserve previous behaviour)
# - 'toggle': explicit toggle
# - 'on' / 'off': set explicitly
requested = None
mode = None
if len(sys.argv) == 1:
    mode = 'toggle'
elif len(sys.argv) == 2:
    mode = sys.argv[1].lower()
    if mode in ('-h', '--help'):
        usage_and_exit()
else:
    usage_and_exit()

current_mode: str = subprocess.check_output([f"kreadconfig{KDE_VERSION}", "--file", "kwinrc", "--group", "Input", "--key", "TabletMode", "--default", "auto"]).decode(encoding='utf-8').strip()

if mode in ('toggle', 't'):
    # invert the current mode; if current is 'auto' or unknown, default to 'on'
    if current_mode == 'on':
        requested = 'off'
    else:
        requested = 'on'
elif mode in ('on', 'off'):
    requested = mode
else:
    usage_and_exit()

# Only write if the requested state differs from the current one.
if requested is not None and current_mode != requested:
    subprocess.check_call([f"kwriteconfig{KDE_VERSION}", "--file", "kwinrc", "--group", "Input", "--key", "TabletMode", requested])

# Notify KWin of the config change so the mode takes effect immediately.
connection = Gio.bus_get_sync(Gio.BusType.SESSION, None)
Gio.DBusConnection.emit_signal(connection, None, OBJECT_PATH, INTERFACE_NAME, SIGNAL_NAME, GLib.Variant.new_tuple(GLib.Variant('a{saay}', {'Input': [b'TabletMode']})))

print(f"TabletMode set to '{requested}' (was: '{current_mode}')")