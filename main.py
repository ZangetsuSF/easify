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

from os import getenv, system, rmdir, mkdir, path
from time import sleep
from subprocess import call, DEVNULL, STDOUT
from shutil import rmtree

import sys
import platform
import locale
import ctypes
import winreg as registry

# Detect system language  
if platform.system() == "Windows":
    windll = ctypes.windll.kernel32
    lang = locale.windows_locale[ windll.GetUserDefaultUILanguage() ]
else:
    lang = "en_EN"
        
##############################################
## Variables
##############################################

# Assume Chrome is not installed
chrome_exists = False

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
desktop = getenv("UserProfile") + "\Desktop"

# System32 path
system32 = getenv("WinDir") + "\System32"

# Chrome executable path
chrome_fullpath = getenv("PROGRAMFILES") + "\Google\Chrome\Application\chrome.exe"

# name of the directory that will be placed on user desktop and will contain Seedify links
directory_name = "Seedify"

# Desktop path for shortcuts
target_full_path = desktop + "\\" + directory_name

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
    
    print("\n" + "###############################################")
    
    if lang == "tr_TR":
        print("##    Easify - Seedify Fund Yardım Betiği    ##")
    else:
        print("##    Easify - Seedify Fund Helper Script    ##")
    
    print("###############################################" + "\n" + "\n")
    
    sleep(2)

# Function to check operating system
def windows_only():
    # Check if operating system is Windows, exit if it is not
    if platform.system() != "Windows":
        if lang == "tr_TR":
            print("Bu betik yalnızca Windows işletim sistemi ile uyumludur.")
        else:
            print("This script is suitable for Windows operating system only.")
        terminate_script()

# Function to check Chrome installation
def check_chrome():
    global chrome_exists
    
    if path.exists(chrome_fullpath):
        chrome_exists = True
    else:
        chrome_exists = False
        
        if lang == "tr_TR":
            print("\n" + "Chrome kurulumu tespit edilemedi." + "\n" + "Diğer işlemler uygulanacak.")
        else:
            print("\n" + "Couldn't detect a Chrome installation." + "\n" + "Other steps will be applied.")
        
        sleep(1)

# Function to show warning message
def show_warning():
    global chrome_exists
    
    if chrome_exists:
        # Show warning messages according to system language (for English and Turkish only)
        if lang == "tr_TR":
            print("Tüm Chrome pencereleri kapatılacak!" + "\n" + "Yarım kalan işlerinizi tamamlamadan devam etmeyin!" + "\n")
            print("İşlem yapmadan çıkmak için pencerenin sağ üst köşesindeki X tuşu ile" + "\n" + "veya CTRL + C tuş kombinasyonu ile programı kapatın." + "\n")
            
            input_message = "Devam etmek için ENTER tuşuna basın..."
        else:
            print("All Chrome instances will be terminated!" + "\n" + "Please do not continue until you complete your work." + "\n")
            print("Click the X button on the top right corner of this window" + "\n" + "or press CTRL + C key combination to quit without making any changes." + "\n")
            
            input_message = "Press ENTER key to continue..."
    else:
        if lang == "tr_TR":
            input_message = "Devam etmek için ENTER tuşuna basın..."
        else:
            input_message = "Press ENTER key to continue..."
    
    print("\n" + input_message + "\n")
    
    # Wait for user to press ENTER key
    keyboard.wait('ENTER', suppress=True)

# Function to terminate all Chrome instances
def terminate_chrome():
    # Kill command to use
    kill_exec = "taskkill.exe"
    # Full path of kill command
    kill_path = system32 + "\\" + kill_exec
    # /F - force
    # /IM - image name (window name of the target process)
    # /T - kill process and any child processes (terminate all windows)
    kill_args = "/F /IM chrome.exe /T >nul"
    # Combine path and arguments
    kill_with_args = kill_path + " " + kill_args
    
    # Check if kill command exists
    if path.exists(kill_path):
        # Show warning message
        if lang == "tr_TR":            
            print("\n" + "* Tüm Chrome pencereleri kapatılıyor...")
        else:
            print("\n" + "* Terminating all Chrome instances...")
        
        # Wait 1 second
        sleep(0.5)
        
        # Run kill command with previously set arguments
        call(kill_with_args, shell=True, stdout=DEVNULL, stderr=STDOUT)

# Function to create Seedify directory on desktop
def create_directory():
    # Show directory creation message
    if lang == "tr_TR":
        print("\n" + "* Masaüstünde Seedify klasörü oluşturuluyor...")
    else:
        print("\n" + "* Creating Seedify folder on desktop...")
        
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
        "https://pancakeswap.finance/swap?inputCurrency=0x477bc8d23c634c154061869478bce96be6045d12 https://trade.kucoin.com/trade/SFUND-USDT https://www.gate.io/trade/sfund_usdt",
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
        print("\n" + "* Kısayollar oluşturuluyor...")
    else:
        print("\n" + "* Creating shortcuts...")
    
    sleep(0.5)
        
    # Create shortcuts of websites inside target directory
    # create_chrome_shortcut( URL, shortcut file name, description, shortcut directory path, working directory path, command to execute, command arguments)
    [create_chrome_shortcut(w[0], w[1], w[2], target_full_path, desktop, chrome_fullpath, args) for w in websites]

# Function to create shortcut files
def create_chrome_shortcut( target_url, file_name, desc, target_dir, work_dir, chrome_exec, args):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(target_dir + "\\" + file_name + ".lnk")
    
    shortcut.Targetpath = chrome_exec
    shortcut.WorkingDirectory = work_dir
    shortcut.Description = desc
    # 1 - Normal, 3 - Maximized, 7 - Minimized
    shortcut.WindowStyle = "3"
    shortcut.Arguments = args + " " + target_url
    
    shortcut.save()

# Function to fix network issues
def fix_network():
    if lang == "tr_TR":
        print("\n" + "* Temel ağ problemleri çözülüyor..." + "\n")
    else:
        print("\n" + "* Fixing basic network issues..." + "\n")
    
    for s in fix_network_issues_1, fix_network_issues_2, flush_dns:
        call(s, shell=True)
        sleep(2)

# Function to reset Windows Time service
def reset_time_service():
    if lang == "tr_TR":
        print("\n" + "* Windows Time hizmeti ve ayarları sıfırlanıyor..." + "\n")
    else:
        print("\n" + "* Resetting Windows Time Service and its settings..." + "\n")
    
    for s in stop_timesync_service, disable_timesync_service, enable_timesync_service:
        call(s, shell=True)
        sleep(2)
    
    set_registry_keys()

# Function to modify Windows Time service registry values
def set_registry_keys():
    # Set target registry folder to edit keys-values in it (Windows Time Service error range)
    key = registry.OpenKey(registry.HKEY_LOCAL_MACHINE,
                           r"SYSTEM\\CurrentControlSet\\Services\\w32time\\Config\\",
                           0,
                           registry.KEY_ALL_ACCESS)

    # Increase the error interval to enable wider range of skews to be fixed (these are the maximum values possible)
    registry.SetValueEx(key, "MaxNegPhaseCorrection", 0, registry.REG_DWORD, 4294967295)
    registry.SetValueEx(key, "MaxPosPhaseCorrection", 0, registry.REG_DWORD, 4294967295)
    
    # Set target registry folder to edit keys-values in it (Windows Time Service auto-sync)
    key = registry.OpenKey(registry.HKEY_LOCAL_MACHINE,
                           r"SYSTEM\\CurrentControlSet\\Services\\tzautoupdate",
                           0,
                           registry.KEY_ALL_ACCESS)

    # Enable auto-sync via internet time
    registry.SetValueEx(key, "Start", 0, registry.REG_DWORD, 3)

# Function to sync local time to internet time
def sync_local_time():
    if lang == "tr_TR":
        print("\n" + "* Bilgisayarın saati internet üzerinden senkronize ediliyor..." + "\n")
    else:
        print("\n" + "* Syncing pc time with internet time..." + "\n")
    
    # double sync is not a typo, to make sure it worked
    for s in start_timesync_service, sync_time, sync_time:
        call(s, shell=True)
        sleep(2)

# Function to show completion message
def the_end():
    if lang == "tr_TR":
        print("\n" + "* Tebrikler! İşlem tamamlandı.")
        
        sleep(1)
        
        print("\n" + "\n" + "Kısayolların bulunduğu klasör:" + "\n" + target_full_path + "\n")
        print("\n" + "Çıkmak için ENTER tuşuna basın..." + "\n")
    else:
        print("\n" + "* Congratulations! Process is complete.")
        
        sleep(1)
        
        print("\n" + "\n" + "The directory where shortcuts are located:" + "\n" + target_full_path + "\n")
        print("\n" + "Press ENTER to exit..." + "\n")
    
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
    # Run script with elevated rights
    run_as_admin()
    
    # Show script name
    show_header()
        
    # Check OS
    windows_only()
    
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