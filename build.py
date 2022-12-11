import os

# PyInstaller.__main__.run([
#     'main.py',
#     '--windowed',
#     '-n Natural Grapher',
#     '-iassets/logo.ico',
#     '-F',
#     '--add-data assets;assets',
# ])

os.system('cmd.exe /k "python -m PyInstaller main.py --windowed -n "Natural Grapher" -i assets/logo.ico -F --add-data assets;assets"')