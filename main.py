#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################
## External modules
##############################################

# module install command: pip install keyboard
import keyboard
# module install command: pip install admin
import admin
# module install command: pip install pywin32
from win32com.client import Dispatch

##############################################
## Built-in modules
##############################################

from time import sleep
from shutil import rmtree
from platform import system as psys, release as prls
from subprocess import call, DEVNULL, STDOUT
from os import getenv, mkdir, path, linesep as newline

import sys
import locale
import ctypes
import winreg as registry

##############################################
## Variables
##############################################

easify_version = float(0.3)

# Default language
lang = "en_EN"

# Assume Chrome is not installed
chrome_exists = False

# Chrome executable name
chrome_exec_name = "chrome.exe"

# Chrome path
chrome_path = "Google\Chrome\Application"

# Empty website list for later use
websites = []

# File containing website details for shortcut creation
website_list = "websites.txt"

# Chrome arguments for shortcuts
args = "--start-maximized \
--incognito \
--disable-translate \
--dns-prefetch-disable \
--disable-background-mode \
--disable-session-crashed-bubble \
--new-window"

##############################################
## Paths
##############################################

# Desktop path of current user
desktop = path.join(getenv("UserProfile"), "Desktop")

# System32 path
system32 = path.join(getenv("WinDir"), "System32")

# Name of the directory that will be placed on user desktop and will contain Seedify links
directory_name = "Seedify"

# Desktop path for shortcuts
target_full_path = path.join(desktop, directory_name)

##############################################
## Network Fix Commands
##############################################

# Resets Winsock settings
reset_winsock = 'netsh winsock reset'

# Resets TCP/IP settings
reset_tcpip = 'netsh int ip reset'

# Renews DHCP leases
renew_dhcp = 'ipconfig /renew'

# Flushes the Address Resolution Protocol (ARP) cache
flush_arp = 'arp -d *'

# Reloads the NetBIOS cache
reload_netbios_cache = 'nbtstat -R'

# Updates the NetBIOS name
update_netbios_name = 'nbtstat -RR'

# Flushes/Clears DNS cache
flush_dns_cache = 'ipconfig /flushdns'

# Re-registers with DNS
register_with_DNS = 'ipconfig /registerdns'

##############################################
## Other Variables
##############################################

# Registry keys
HKEY_LOCAL_MACHINE = 0x80000002
HKEY_CURRENT_USER = 0x80000001

# Windows Time Service commands
enable_timesync_service = 'w32tm /register'
disable_timesync_service = 'w32tm /unregister'
stop_timesync_service = 'net stop W32Time'
start_timesync_service = 'net start W32Time'
sync_time = 'w32tm /resync /rediscover'

# Function to terminate the script itself
def terminate_script(exit_message):
    if (exit_message != ""):
        print(exit_message + newline)

    if lang == "tr_TR":
        print("* Betik sonlandırılıyor...")
    else:
        print("* Terminating script in...")

    [{print(x), sleep(1)} for x in range(3,0,-1)]
    sys.exit()

# Function to check operating system
def check_os():
    global lang
    global win_version

    # Check if operating system is Windows, exit if it is not
    if psys() == "Windows":
        win_version = float(prls())

        if (win_version >= float(7)):
            windll = ctypes.windll.kernel32
            lang = locale.windows_locale[ windll.GetUserDefaultUILanguage() ]

            if lang != "tr_TR":
                lang = "en_EN"
        else:
            terminate_script("This script is suitable for Windows 7 or above only.")
    else:
        terminate_script("This script is suitable for Windows operating system only.")

# Function to run the script as administrator
def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
            # Re-run the program with admin rights
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            # Terminate non-admin instance of script
            sys.exit()

# Function to clear console and show script name
def show_header():
    execute_command("cls")

    print("{}##################################################".format(newline))

    if (lang == "tr_TR"):
        print("##   Easify v{} - Seedify Fund Yardım Betiği   ##".format(easify_version))
    else:
        print("##   Easify v{} - Seedify Fund Helper Script   ##".format(easify_version))

    print("##################################################{}{}".format(newline, newline))

    sleep(1)

# Function to check Chrome installation
def check_chrome():
    global chrome_exists
    global chrome_fullpath

    prgfiles_temp = getenv("PROGRAMFILES")

    # Check prgfiles_temp and set variables for Program Files directories
    if (prgfiles_temp[-5:] == "(x86)"):
        prgFilesX86 = prgfiles_temp
        # Crop (x86) part from directory
        prgFilesDefault = prgfiles_temp[:len(prgfiles_temp)-6]
    else:
        prgFilesDefault = prgfiles_temp
        # Add (x86) part to directory
        prgFilesX86 = path.join(prgfiles_temp, " (x86)")

    # Try to locate Chrome using both prgFilesDefault and prgFilesX86
    chrome_fullpath = path.join(prgFilesDefault, chrome_path, chrome_exec_name)

    if path.exists(chrome_fullpath):
        chrome_exists = True
    else:
        chrome_fullpath = path.join(prgFilesX86, chrome_path, chrome_exec_name)

        if path.exists(chrome_fullpath):
            chrome_exists = True

# Function to show warning message
def show_warning():
    # Show warning messages according to system language (for English and Turkish only)
    if lang == "tr_TR":
        if chrome_exists:
            print("Tüm Chrome pencereleri kapatılacak!{}Yarım kalan işlerinizi tamamlamadan devam etmeyin!{}".format(newline, newline))
            print("İşlem yapmadan çıkmak için{}pencerenin sağ üst köşesindeki X tuşu ile veya{}CTRL + C tuş kombinasyonu ile programı kapatın.{}".format(newline, newline, newline))
        else:
            print("Chrome kurulumu tespit edilemedi.{}Diğer işlemler uygulanacak.".format(newline))

        input_message = "Devam etmek için ENTER tuşuna basın..."
    else:
        if chrome_exists:
            print("All Chrome instances will be terminated!{}Please do not continue until you save your work.{}".format(newline, newline))
            print("Click the X button on the top right corner of{}this window or press CTRL + C key combination{}to quit without making any changes.{}".format(newline, newline, newline))
        else:
            print("Couldn't detect a Chrome installation.{}Other steps will be applied.".format(newline))

        input_message = "Press ENTER key to continue..."

    input_message = "{}{}{}{}".format(newline, input_message, newline, newline)

    print(input_message)

    # Wait for user to press ENTER key
    keyboard.wait('ENTER')

# Function to terminate all Chrome instances
def terminate_chrome():
    # Kill command to use
    kill_exec = "taskkill.exe"
    # Full path of kill command
    kill_path = path.join(system32, kill_exec)
    # /F - force
    # /IM - image name (window name of the target process)
    # /T - kill process and any child processes (terminate all windows)
    # leading space is necessary, not a typo
    kill_args = " /F /IM {} /T".format(chrome_exec_name)

    # Combine path and arguments
    kill_with_args = kill_path + kill_args

    # Check if kill command exists
    if path.exists(kill_path):
        # Show warning message
        if lang == "tr_TR":
            print("* Tüm Chrome pencereleri kapatılıyor...")
        else:
            print("* Terminating all Chrome instances...")

        # Wait 1 second
        sleep(1)

        try:
            # Run kill command with previously set arguments
            execute_command(kill_with_args)
        except:
            sleep(1)
            execute_command(kill_with_args)

# Function to create Seedify directory on desktop
def create_directory():
    # Show directory creation message
    if lang == "tr_TR":
        print("* Masaüstünde Seedify klasörü oluşturuluyor...")
    else:
        print("* Creating Seedify folder on desktop...")

    sleep(1)

    # Check if the target directory for shortcuts exists
    if path.exists(target_full_path):
        # Delete target directory and everything in it
        try:
            rmtree(target_full_path)
        except:
            sleep(1)
            rmtree(target_full_path)

    # Create target directory
    try:
        mkdir(target_full_path)
    except:
        try:
            sleep(1)
            mkdir(target_full_path)
        except:
            terminate_script("Seedify directory creation has failed.")

# Function to get website details from website_list file
def create_website_list():
    global websites

    count = 0

    with open(website_list, 'r') as details:
        lines = filter(None, (temp_line.strip() for temp_line in details))

        for line in lines:
            # avoid comment lines
            if (not line.startswith("#")):
                line_parts = line.split(",")

                count+=1
                line_parts[0] = str(count) + "- " + line_parts[0]

                websites.append([line_parts[0].strip(), line_parts[1].strip(), line_parts[2].strip()])

        # [print(w) for w in websites]
        # sys.exit()

    return websites

# Function to create website shortcuts inside Seedify directory
def create_shortcuts():
    # Show shortcut creation message
    if lang == "tr_TR":
        print("* Kısayollar oluşturuluyor...")
    else:
        print("* Creating shortcuts...")

    sleep(1)

    # Create shortcuts of websites inside target directory
    # usage: create_chrome_shortcut( URL, shortcut file name, description, shortcut directory path, working directory path, command to execute, command arguments)
    try:
        [create_chrome_shortcut(w[0], w[1], w[2], target_full_path, desktop, chrome_fullpath, args) for w in websites]
    except:
        sleep(1)
        [create_chrome_shortcut(w[0], w[1], w[2], target_full_path, desktop, chrome_fullpath, args) for w in websites]

# Function to create shortcut files
def create_chrome_shortcut(file_name, target_url, desc, target_dir, work_dir, chrome_exec, args):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path.join(target_dir, file_name) + ".lnk")

    shortcut.Targetpath = chrome_exec
    shortcut.WorkingDirectory = work_dir
    shortcut.Description = desc
    # Window styles: 1 - Normal, 3 - Maximized, 7 - Minimized
    shortcut.WindowStyle = "3"
    shortcut.Arguments = args + " " + target_url

    shortcut.save()

# Function to fix network issues
def fix_network():
    if lang == "tr_TR":
        print("* Temel ağ problemleri çözülüyor (bir dakika kadar sürebilir)...")
    else:
        print("* Fixing basic network issues (might take a minute)...")

    try:
        for s in reset_winsock, reset_tcpip, renew_dhcp, flush_arp, reload_netbios_cache, update_netbios_name, flush_dns_cache, register_with_DNS:
            execute_command(s)
            sleep(2)
    except:
        sleep(1)
        for s in reset_winsock, reset_tcpip, renew_dhcp, flush_arp, reload_netbios_cache, update_netbios_name, flush_dns_cache, register_with_DNS:
            execute_command(s)
            sleep(2)

# Function to reset Windows Time service
def reset_time_service():
    if lang == "tr_TR":
        print("* Windows Time hizmeti sıfırlanıyor...")
    else:
        print("* Resetting Windows Time service...")

    try:
        for s in stop_timesync_service, disable_timesync_service, enable_timesync_service:
            execute_command(s)
            sleep(2)
    except:
        sleep(1)
        for s in stop_timesync_service, disable_timesync_service, enable_timesync_service:
            execute_command(s)
            sleep(2)

    set_registry_keys()

# Function to modify Windows Time service registry values
def set_registry_keys():
    try:
        # Set target registry folder to edit keys-values (Windows Time Service error ranges) in it
        key = registry.OpenKey(registry.HKEY_LOCAL_MACHINE,
                            r"SYSTEM\\CurrentControlSet\\Services\\w32time\\Config\\",
                            0,
                            registry.KEY_ALL_ACCESS)

        # Increase the error interval to enable wider range of skews to be fixed (these are the maximum values possible)
        registry.SetValueEx(key, "MaxNegPhaseCorrection", 0, registry.REG_DWORD, 4294967295)
        registry.SetValueEx(key, "MaxPosPhaseCorrection", 0, registry.REG_DWORD, 4294967295)
    except:
        pass

    try:
        # Set target registry folder to edit keys-values (Windows Time Service auto-sync settings) in it
        key = registry.OpenKey(registry.HKEY_LOCAL_MACHINE,
                            r"SYSTEM\\CurrentControlSet\\Services\\tzautoupdate",
                            0,
                            registry.KEY_ALL_ACCESS)

        # Enable auto-sync via internet time
        registry.SetValueEx(key, "Start", 0, registry.REG_DWORD, 3)
    except:
        pass

# Function to sync local time to internet time
def sync_local_time():
    if lang == "tr_TR":
        print("* Saat internet üzerinden senkronize ediliyor...")
    else:
        print("* Syncing time over internet...")

    try:
        # double sync is not a typo, it is to make sure sync is successful
        for s in start_timesync_service, sync_time, sync_time:
            execute_command(s)
            sleep(2)
    except:
        sleep(1)
        for s in start_timesync_service, sync_time, sync_time:
            execute_command(s)
            sleep(2)

# Function to show completion message
def the_end():
    if lang == "tr_TR":
        print("* Tebrikler! İşlem tamamlandı.")
        sleep(1)

        if chrome_exists:
            print("{}{}Kısayolların bulunduğu klasör:{}{}{}".format(newline, newline, newline, target_full_path, newline))
            sleep(1)

        print("{}Değişikliklerin etkili olabilmesi için{}lütfen bilgisayarınızı yeniden başlatın.{}".format(newline, newline, newline))
        sleep(1)

        print("{}Çıkmak için ENTER tuşuna basın...{}".format(newline, newline))
    else:
        print("* Congratulations! Process is complete.")
        sleep(1)

        if chrome_exists:
            print("{}{}The directory where shortcuts are located:{}{}{}".format(newline, newline, newline, target_full_path, newline))
            sleep(1)

        print("{}Please restart your computer{}for changes to take effect.{}".format(newline, newline, newline))
        sleep(1)

        print("{}Press ENTER key to exit...{}".format(newline, newline))

    # Wait for user to press ENTER key
    keyboard.wait('ENTER')

    # Exit script
    sys.exit()

# Function to run console commands
def execute_command(command_to_run):
    call(command_to_run, shell=True, stdout=DEVNULL, stderr=DEVNULL)

def main():
    # Make sure we are on Windows
    check_os()

    # Run script with elevated rights
    run_as_admin()

    # Show script name
    show_header()

    # Check Chrome installation
    check_chrome()

    # Show warning message
    show_warning()

    if chrome_exists:
        # Terminate all Chrome instances
        terminate_chrome()

        # Create Seedify directory on desktop
        create_directory()

        # Create a list of Seedify Fund related websites
        create_website_list()

        # Create website shortcuts inside Seedify directory
        create_shortcuts()

    # Fix network issues, flush DNS cache
    fix_network()

    # Stop, disable and re-enable time synchronization service (to reset its settings)
    reset_time_service()

    # Start time synchronization service and sync time with ntp server
    sync_local_time()

    # Show completion message
    the_end()

if __name__ == "__main__":
    main()
