import os


os.system("git clone --recursive https://github.com/TurboWarp/desktop turbowarp-desktop")
os.system("cd turbowarp-desktop")
os.sytem("pacman -S nodejs npm")
os.system("npm ci")
os.system("npm run fetch")
os.system("npm run dist")
os.system("cd ..")
os.system("rm -r turbowarp-desktop")
os.system("pip install scratchattach")
os.system("npm install @errorgamer2000/scratch-cloud")
