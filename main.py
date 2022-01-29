from os import getenv, system, rmdir, mkdir, path
from time import sleep
from subprocess import call, DEVNULL, STDOUT
from shutil import rmtree

# from pynput.keyboard import Listener, Key
import keyboard

import sys
import platform
import locale
import ctypes

from win32com.client import Dispatch

##############################################
## Variables
##############################################

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

# Function to send website details to website list function
def create_website_list():
    # CEX/DEX URLs to buy SFUND
    add_to_list(
        "https://pancakeswap.finance/swap?inputCurrency=0x477bc8d23c634c154061869478bce96be6045d12 https://trade.kucoin.com/trade/SFUND-USDT https://www.gate.io/trade/sfund_usdt",
        "Buy SFUND (Incognito)",
        "Chrome link to open SFUND trade pages in incognito mode."
    )
    
    # Seedify Fund official website
    add_to_list(
        "https://launchpad.seedify.fund",
        "Seedify Launchpad (Incognito)",
        "Chrome link to open Seedify website in incognito mode."
    )
    
    # Claim URL for Scotty Beam project
    add_to_list(
        "https://claim.scottybeam.io",
        "Claim - ScottyBeam (Incognito)",
        "Chrome link to open ScottyBeam Claim page in incognito mode."
    )
    
    # Claim URL for Hololoot project
    add_to_list(
        "https://claiming.hololoot.io",
        "Claim - Hololoot (Incognito)",
        "Chrome link to open Hololoot Claim page in incognito mode."
    )
    
    # Claim URL for Bit Hotel project
    add_to_list(
        "https://investors.bithotel.io",
        "Claim - BitHotel (Incognito)",
        "Chrome link to open BitHotel Claim page in incognito mode."
    )
    
    # Combotools URL - Seedify HODLers
    add_to_list(
        "https://combotools.online/",
        "Tools - Combotools - Investment Tracker (Incognito)",
        "Chrome link to open Combotools page in incognito mode."
    )
    
    # Calculator URL - Seedify HODLers
    add_to_list(
        "https://seedifyhodlers.com/tools/calculator",
        "Tools - SFUND Calculator (Incognito)",
        "Chrome link to open SFUND Calculator page in incognito mode."
    )
    
    # ROI Tracker URL - Seedify HODLers
    add_to_list(
        "https://seedifyhodlers.com/tools/roi/",
        "Tools - ROI Tracker (Incognito)",
        "Chrome link to open ROI Tracker page in incognito mode."
    )

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

# Function to create website list
def add_to_list(shortcut_url, shortcut_filename, shortcut_desc):
    websites.append([shortcut_url, shortcut_filename, shortcut_desc])

# Function to terminate the script itself
def terminate_script():
    print("* Terminating in...")
    [{print(x), sleep(1)} for x in range(3,0,-1)]
    quit()

def main():
    call("cls", shell=True)
    
    print("")
    print("Easify - Seedify Fund Helper Script")
    print("")
    
    # Check if operating system is Windows, exit if it is not
    if platform.system() != "Windows":
        print("This script is for Windows only.")
        terminate_script()
    
    # Detect system language   
    windll = ctypes.windll.kernel32
    lang = locale.windows_locale[ windll.GetUserDefaultUILanguage() ]
    
    sleep(1)
    
    # Show warning messages according to system language (for English and Turkish only)
    if lang == "tr_TR":
        print("Tüm Chrome pencereleri kapatılacak! Yarım kalan işlerinizi tamamlamadan devam etmeyin!\n")
        print("İşlem yapmadan çıkmak için pencerenin sağ üst köşesindeki X tuşu ile \nveya CTRL + C tuş kombinasyonu ile programı kapatın.")
        
        input_message = "Devam etmek için ENTER tuşuna basın..."
    else:
        print("All Chrome instances will be terminated. Please do not continue until you complete your work.\n")
        print("Click the X button on the top right corner of this window \nor press CTRL + C key combination to quit without making any changes.")
        
        input_message = "Press ENTER key to continue..."
    
    print("\n" + input_message + "\n")
    
    # Wait for user to press ENTER key
    keyboard.wait('ENTER', suppress=True)
    
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
        sleep(1)
        
        # Run kill command with previously set arguments
        call(kill_with_args, shell=True, stdout=DEVNULL, stderr=STDOUT)
    
    # Create a list of Seedify Fund related websites
    create_website_list()
    
    # Show directory creation message
    if lang == "tr_TR":
        print("\n" + "* Masaüstünde Seedify klasörü oluşturuluyor...")
    else:
        print("\n" + "* Creating Seedify folder on desktop...")
        
    sleep(1)
        
    # Check if the target directory for shortcuts exists
    if path.exists(target_full_path):
        # Delete target directory and everything in it
        rmtree(target_full_path)
    
    # Create target directory
    mkdir(target_full_path)
    
    # Show shortcut creation message
    if lang == "tr_TR":
        print("\n" + "* Kısayollar oluşturuluyor...")
    else:
        print("\n" + "* Creating shortcuts...")
    
    sleep(1)
        
    # Create shortcuts of websites inside target directory
    # create_chrome_shortcut( URL, shortcut file name, description, shortcut directory path, working directory path, command to execute, command arguments)
    [create_chrome_shortcut(w[0], w[1], w[2], target_full_path, desktop, chrome_fullpath, args) for w in websites]
    
    # Show completion message
    if lang == "tr_TR":
        print("\n" + "* İşlem tamamlandı.")
        
        sleep(1)
        
        print("\n" + "\n" + "Kısayolların bulunduğu klasör:" + "\n" + target_full_path + "\n")
    else:
        print("\n" + "* Process is complete.")
        
        sleep(1)
        
        print("\n" + "\n" + "The directory where shortcuts are located:" + "\n" + target_full_path + "\n")
    
if __name__ == "__main__":
   main()