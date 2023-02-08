import subprocess

from main import VERSION

subprocess.call(f"pyinstaller --onefile main.py --name room-runers-v{VERSION}")
