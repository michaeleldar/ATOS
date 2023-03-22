# Code taken from Orange OS LE (made by the same creator as this)


import sys, os

hard_drive = ""
host_name = ""
keyboard_layout = ""
language = ""
time_zone = ""
location = ""


def ui():
    global hard_drive, host_name, keyboard_layout, language, time_zone, location
    print("Welcome to the ATOS install script.")
    print("We will ask you a few questions to make sure you get a great configuration.")

    hard_drive = input("Please input your disk drive file, like /dev/sda: ")
    host_name = input(
    "Please enter the name you want to give your computer (a.k.a your hostname): "
    )
    keyboard_layout = input("Now enter your keyboard layout, like uk or us: ")

    language = input(
        'Now please enter your locale language. This should be something like "en_US": '
    )

    time_zone = input(
        "Now we need your timezone, this is usually in the format of <Continent>/<City>, e.g Europe/Paris: "
    )

    location = input(
        "Finally, we need to know what country you live in. If you don't want to answer this, enter worldwide."
    ).capitalize()

    print("Okay, now we are going to setup users for you.")
    user_creds = open("user_credentials.json", "w")
    user_creds.write(
        """{
        "!users": ["""
    )
    users_no = int(input("First, how many users do you want the system to hold: "))
    for x in range(0, users_no):
        user_creds.write("{\n")
        username = input(f"Ok what the you want the username of user {x + 1} to be: ")
        password = input(f"Now, what password do you want to give {username}: ")
        superuser = input(
            f"Lastly do you want {username} to be a superuser? Leave blank if you don't: "
        )
        user_creds.write(f'"!password": "{password}",\n')
        if superuser:
            user_creds.write('"sudo": true,\n')
        else:
            user_creds.write('"sudo": false,\n')

        user_creds.write(f'"username": "{username}"\n')
        user_creds.write("}")
        if x == users_no - 1:
            user_creds.write("\n")
        else:
            user_creds.write(",\n")
    user_creds.write("]\n}")
    user_creds.close()

def config_file():
    global hard_drive, host_name, keyboard_layout, language, time_zone, location
    config = open(sys.argv[1], 'r')
    hard_drive = config.readline().replace("\n", "")
    host_name = config.readline().replace("\n", "")
    keyboard_layout = config.readline().replace("\n", "")
    language = config.readline().replace("\n", "")
    time_zone = config.readline().replace("\n", "")
    location = config.readline().capitalize().replace("\n", "")

    user_creds = open("user_credentials.json", "w")
    user_creds.write(
        """{
        "!users": ["""
    )
    users_no = int(config.readline().replace("\n", ""))
    for x in range(0, users_no):
        user_creds.write("{\n")
        username = config.readline().replace("\n", "")
        password = config.readline().replace("\n", "")
        superuser = config.readline().replace("\n", "")
        user_creds.write(f'"!password": "{password}",\n')
        if superuser:
            user_creds.write('"sudo": true,\n')
        else:
            user_creds.write('"sudo": false,\n')

        user_creds.write(f'"username": "{username}"\n')
        user_creds.write("}")
        if x == users_no - 1:
            user_creds.write("\n")
        else:
            user_creds.write(",\n")
    user_creds.write("]\n}")
    user_creds.close()




if sys.argv.__len__() == 2:
    config_file()
else:
    ui()


user_config = open("user_configuration.json", "w")
user_config.write(
    f"""{'{'}
"additional-repositories": "",
"audio": "pipewire",
"bootloader": "grub-install",
"filesystem": "ext4",
"HSM": null,
"config_version": "2.5.0",
"debug": false,
"harddrives": [
    "{hard_drive}"
],
"kernels": [
    "linux"
],
"swap": true,
"keyboard-language": "{keyboard_layout}",
"mirror-region": "{location}",
"hostname": "{host_name}",
"keyboard-layout": "{keyboard_layout}",
"mount_point": null, 
"nic": {'{'}
    "dhcp": true,
    "dns": null,
    "gateway": null,
    "iface": null,
    "ip": null,
    "type": "iso"
{'}'},
"ntp": true,
"plugin": null,
"profile": {'{'}
    "path": "/usr/lib/python3.10/site-packages/archinstall/profiles/minimal.py"
{'}'},
"script": "guided",
"silent": false,
"sys-language": "{language}",
"sys-encoding": "utf-8",
"timezone": "{time_zone}",
"version": "2.5.0",
"packages": ["xorg", "xorg-server", "gnome"],
"custom-commands": [
        "pacman -Syu",
        "systemctl enable gdm.service",
        "pacman -S NetworkManager",
        "pacman -S git",
        "sysetmctl enable NetworkManager"
]
{'}'}"""
)
user_config.close()
# user creds
print("Now we will setup the disks for you. Unfourtuanatley, we can't offer to let you")
print("do the disk partioning, but we might offer this in future.")
confirm_installation = input(
    "This will delete all data on the disk you have chosen,\nIf you agree to the conditions, submit with a \"Y\". Otherwise, submit with any other letter."
)
if confirm_installation.lower() != "y":
    print("Quiting the script, but run the script again if you change your mind.")
    quit(0)
else:
    print("Here we go...")
user_disks = open("user_disk_layout.json", "w")
user_disks.write(
    f"""{'{'}
    "{hard_drive}": {'{'}
        "partitions": [
            {'{'}
                "boot": true,
                "encrypted": false,
                "filesystem": {'{'}
                    "format": "fat32"
                {'}'},
                "mountpoint": "/boot",
                "size": "{'203MiB' if not os.path.exists("/sys/firmware/efi") else '512MiB'}",
                "start": "{'3MiB' if not os.path.exists("/sys/firmware/efi") else '1MiB'}",
                "type": "primary",
                "wipe": true
            {'}'},
            {'{'}
                "encrypted": false,
                "filesystem": {'{'}
                    "format": "ext4",
                    "mount_options": []
                {'}'},
                "mountpoint": "/",
                "size": "100%",
                "start": "{'206MiB' if not os.path.exists("/sys/firmware/efi") else '513MiB'}",
                "type": "primary",
                "wipe": true
            {'}'}
        ],
        "wipe": true
    {'}'}
{'}'}"""
)
user_disks.close()
if sys.argv.__len__() == 2:
    os.system(
        "sudo archinstall --silent --config ./user_configuration.json --creds ./user_credentials.json --disk_layouts ./user_disk_layout.json"
    )
    os.system(
        "sudo archinstall --silent --config ./user_configuration.json --creds ./user_credentials.json --disk_layouts ./user_disk_layout.json"
    )
else:
    os.system(
        "sudo archinstall --silent --config ./user_configuration.json --creds ./user_credentials.json --disk_layouts ./user_disk_layout.json"
    )
    os.system(
        "sudo archinstall --silent --config ./user_configuration.json --creds ./user_credentials.json --disk_layouts ./user_disk_layout.json"
    )

os.system("reboot -h now")
