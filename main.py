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

# Assume Chrome is not installed
chrome_exists = False

# Chrome executable name
chrome_exec_name = "chrome.exe"

# Empty list to store website details
websites = []

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

# Chrome executable path
chrome_fullpath = path.join(getenv("PROGRAMFILES"), "Google\Chrome\Application", chrome_exec_name)

# Name of the directory that will be placed on user desktop and will contain Seedify links
directory_name = "Seedify"

# Desktop path for shortcuts
target_full_path = path.join(desktop, directory_name)

##############################################
## Other Variables
##############################################

# Registry keys
HKEY_LOCAL_MACHINE = 0x80000002
HKEY_CURRENT_USER = 0x80000001

# Commands to fix network issues
fix_network_issues_1 = 'netsh winsock reset >nul'
fix_network_issues_2 = 'netsh int ip reset >nul'

# Command to clear DNS cache
flush_dns = 'ipconfig /flushdns'

# Windows Time Service commands
enable_timesync_service = 'w32tm /register'
disable_timesync_service = 'w32tm /unregister'
stop_timesync_service = 'net stop W32Time'
start_timesync_service = 'net start W32Time'
sync_time = 'w32tm /resync /rediscover'

# Function to check operating system
def check_os():
    global lang
    global win_version

    # Check if operating system is Windows, exit if it is not
    if psys() == "Windows":
        win_version = prls()
        windll = ctypes.windll.kernel32
        lang = locale.windows_locale[ windll.GetUserDefaultUILanguage() ]

        if lang != "tr_TR":
            lang = "en_EN"
    else:
        lang = "en_EN"
        print("This script is suitable for Windows operating system only.")
        terminate_script()

# Function to run the script as administrator
def run_as_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        # Terminate non-admin instance of script
        quit()

# Function to clear console and show script name
def show_header():
    call("cls", shell=True)

    print("{}###############################################".format(newline))

    if lang == "tr_TR":
        print("##    Easify - Seedify Fund Yardım Betiği    ##")
    else:
        print("##    Easify - Seedify Fund Helper Script    ##")

    print("###############################################{}{}".format(newline, newline))

    sleep(2)

# Function to check Chrome installation
def check_chrome():
    global chrome_exists

    if path.exists(chrome_fullpath):
        chrome_exists = True
    else:
        chrome_exists = False

        if lang == "tr_TR":
            print("{}Chrome kurulumu tespit edilemedi.{}Diğer işlemler uygulanacak.".format(newline))
        else:
            print("{}Couldn't detect a Chrome installation.{}Other steps will be applied.".format(newline))

        sleep(1)

# Function to show warning message
def show_warning():
    global chrome_exists

    if chrome_exists:
        # Show warning messages according to system language (for English and Turkish only)
        if lang == "tr_TR":
            print("Tüm Chrome pencereleri kapatılacak!{}Yarım kalan işlerinizi tamamlamadan devam etmeyin!".format(newline, newline))
            print("İşlem yapmadan çıkmak için pencerenin sağ üst köşesindeki X tuşu ile{}veya CTRL + C tuş kombinasyonu ile programı kapatın.".format(newline, newline))

            input_message = "Devam etmek için ENTER tuşuna basın..."
        else:
            print("All Chrome instances will be terminated!{}Please do not continue until you complete your work.{}".format(newline, newline))
            print("Click the X button on the top right corner of this window{}or press CTRL + C key combination to quit without making any changes.{}".format(newline, newline))

            input_message = "Press ENTER key to continue..."
    else:
        if lang == "tr_TR":
            input_message = "Devam etmek için ENTER tuşuna basın..."
        else:
            input_message = "Press ENTER key to continue..."

    input_message = "{}{}{}".format(newline, input_message, newline)

    print(input_message)

    # Wait for user to press ENTER key
    keyboard.wait('ENTER', suppress=True)

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
    kill_args = " /F /IM {} /T >nul".format(chrome_exec_name)

    # Combine path and arguments
    kill_with_args = kill_path + kill_args

    # Check if kill command exists
    if path.exists(kill_path):
        # Show warning message
        if lang == "tr_TR":
            print("{}* Tüm Chrome pencereleri kapatılıyor...".format(newline))
        else:
            print("{}* Terminating all Chrome instances...".format(newline))

        # Wait 1 second
        sleep(0.5)

        # Run kill command with previously set arguments
        call(kill_with_args, shell=True, stdout=DEVNULL, stderr=STDOUT)

# Function to create Seedify directory on desktop
def create_directory():
    # Show directory creation message
    if lang == "tr_TR":
        print("{}* Masaüstünde Seedify klasörü oluşturuluyor...".format(newline))
    else:
        print("{}* Creating Seedify folder on desktop...".format(newline))

    sleep(0.5)

    # Check if the target directory for shortcuts exists
    if path.exists(target_full_path):
        # Delete target directory and everything in it
        rmtree(target_full_path)

    # Create target directory
    mkdir(target_full_path)

# Function to create a list of Seedify Fund related websites
def create_website_list():
    # CEX/DEX URLs to buy SFUND
    add_to_list(
        "https://pancakeswap.finance/swap?inputCurrency=0x477bc8d23c634c154061869478bce96be6045d12 \
            https://trade.kucoin.com/trade/SFUND-USDT \
            https://www.gate.io/trade/sfund_usdt",
        "1- Buy SFUND (Incognito)",
        "Chrome link to open SFUND trade pages in incognito mode."
    )

    # Seedify Fund official website
    add_to_list(
        "https://identity.blockpass.org/frontend/#/register/input",
        "2- KYC Check - Blockpass Login (Incognito)",
        "Chrome link to open Blockpass Login page in incognito mode."
    )

    # Seedify Fund official website
    add_to_list(
        "https://launchpad.seedify.fund",
        "3- Seedify - Launchpad (Incognito)",
        "Chrome link to open Seedify website in incognito mode."
    )

    # Seedify Fund staking page
    add_to_list(
        "https://staking.seedify.fund/",
        "4- Seedify - Staking-Farming (Incognito)",
        "Chrome link to open Seedify staking/farming page in incognito mode."
    )

    # Seedify Fund claim page
    add_to_list(
        "https://claim.seedify.fund/",
        "5- Seedify - Claim (Incognito)",
        "Chrome link to open Seedify claim page in incognito mode."
    )

    # Seedify Fund claim page
    add_to_list(
        "https://tinyurl.com/Seedify-IGO-Vesting",
        "6- Seedify - Vesting Table (Incognito)",
        "Chrome link to open Seedify Fund Vesting Table in incognito mode."
    )

    # Claim URL for Scotty Beam project
    add_to_list(
        "https://claim.scottybeam.io",
        "7- Claim - ScottyBeam (Incognito)",
        "Chrome link to open ScottyBeam Claim page in incognito mode."
    )

    # Claim URL for Hololoot project
    add_to_list(
        "https://claiming.hololoot.io",
        "8- Claim - Hololoot (Incognito)",
        "Chrome link to open Hololoot Claim page in incognito mode."
    )

    # Claim URL for Bit Hotel project
    add_to_list(
        "https://investors.bithotel.io",
        "9- Claim - BitHotel (Incognito)",
        "Chrome link to open BitHotel Claim page in incognito mode."
    )

    # Combotools URL - Seedify HODLers
    add_to_list(
        "https://combotools.online/",
        "10- Tools - Combotools - Investment Tracker (Incognito)",
        "Chrome link to open Combotools page in incognito mode."
    )

    # Calculator URL - Seedify HODLers
    add_to_list(
        "https://seedifyhodlers.com/tools/calculator",
        "11- Tools - SFUND Calculator (Incognito)",
        "Chrome link to open SFUND Calculator page in incognito mode."
    )

    # ROI Tracker URL - Seedify HODLers
    add_to_list(
        "https://seedifyhodlers.com/tools/roi/",
        "12- Tools - ROI Tracker (Incognito)",
        "Chrome link to open ROI Tracker page in incognito mode."
    )

# Function to create website list
def add_to_list(shortcut_url, shortcut_filename, shortcut_desc):
    websites.append([shortcut_url, shortcut_filename, shortcut_desc])

# Function to create website shortcuts inside Seedify directory
def create_shortcuts():
    # Show shortcut creation message
    if lang == "tr_TR":
        print("{}* Kısayollar oluşturuluyor...".format(newline))
    else:
        print("{}* Creating shortcuts...".format(newline))

    sleep(0.5)

    # Create shortcuts of websites inside target directory
    # usage: create_chrome_shortcut( URL, shortcut file name, description, shortcut directory path, working directory path, command to execute, command arguments)
    [create_chrome_shortcut(w[0], w[1], w[2], target_full_path, desktop, chrome_fullpath, args) for w in websites]

# Function to create shortcut files
def create_chrome_shortcut( target_url, file_name, desc, target_dir, work_dir, chrome_exec, args):
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
        print("{}* Temel ağ problemleri çözülüyor...{}".format(newline, newline))
    else:
        print("{}* Fixing basic network issues...{}".format(newline, newline))

    for s in fix_network_issues_1, fix_network_issues_2, flush_dns:
        call(s, shell=True)
        sleep(2)

# Function to reset Windows Time service
def reset_time_service():
    if lang == "tr_TR":
        print("{}* Windows Time hizmeti ve ayarları sıfırlanıyor...{}".format(newline, newline))
    else:
        print("{}* Resetting Windows Time Service and its settings...{}".format(newline, newline))

    for s in stop_timesync_service, disable_timesync_service, enable_timesync_service:
        call(s, shell=True)
        sleep(2)

    set_registry_keys()

# Function to modify Windows Time service registry values
def set_registry_keys():
    # Set target registry folder to edit keys-values (Windows Time Service error ranges) in it
    key = registry.OpenKey(registry.HKEY_LOCAL_MACHINE,
                           r"SYSTEM\\CurrentControlSet\\Services\\w32time\\Config\\",
                           0,
                           registry.KEY_ALL_ACCESS)

    # Increase the error interval to enable wider range of skews to be fixed (these are the maximum values possible)
    registry.SetValueEx(key, "MaxNegPhaseCorrection", 0, registry.REG_DWORD, 4294967295)
    registry.SetValueEx(key, "MaxPosPhaseCorrection", 0, registry.REG_DWORD, 4294967295)

    # Run on Windows 10 only
    if win_version == 10:
        # Set target registry folder to edit keys-values (Windows Time Service auto-sync settings) in it
        key = registry.OpenKey(registry.HKEY_LOCAL_MACHINE,
                            r"SYSTEM\\CurrentControlSet\\Services\\tzautoupdate",
                            0,
                            registry.KEY_ALL_ACCESS)

        # Enable auto-sync via internet time
        registry.SetValueEx(key, "Start", 0, registry.REG_DWORD, 3)

# Function to sync local time to internet time
def sync_local_time():
    if lang == "tr_TR":
        print("{}* Bilgisayarın saati internet üzerinden senkronize ediliyor...{}".format(newline, newline))
    else:
        print("{}* Syncing pc time with internet time...{}".format(newline, newline))

    # double sync is not a typo, it is to make sure sync is successful
    for s in start_timesync_service, sync_time, sync_time:
        call(s, shell=True)
        sleep(2)

# Function to show completion message
def the_end():
    if lang == "tr_TR":
        print("{}* Tebrikler! İşlem tamamlandı.".format(newline))

        sleep(1)

        print("{}{}Kısayolların bulunduğu klasör:{}{}{}".format(newline, newline, newline, target_full_path, newline))
        print("{}Çıkmak için ENTER tuşuna basın...{}".format(newline, newline))
    else:
        print("{}* Congratulations! Process is complete.".format(newline))

        sleep(1)

        print("{}{}The directory where shortcuts are located:{}{}{}".format(newline, newline, newline, target_full_path, newline))
        print("{}Press ENTER to exit...{}".format(newline, newline))

    # Wait for user to press ENTER key
    keyboard.wait('ENTER', suppress=True)

# Function to terminate the script itself
def terminate_script():
    if lang == "tr_TR":
        print("* Betik sonlandırılıyor...")
    else:
        print("* Terminating script in...")

    [{print(x), sleep(1)} for x in range(3,0,-1)]
    quit()

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