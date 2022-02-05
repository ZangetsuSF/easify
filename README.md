# Easify - Seedify Fund Helper Script

This is a Python script which tries to fix some issues that Windows users are experiencing while using **Seedify Fund** website (IGO participation, claiming, staking/farming).

**NOTE:** This is **NOT** an **OFFICIAL Seedify Fund** tool/script. Please read LICENSE before using it.

------

[**Seedify Fund Official Website**](https://launchpad.seedify.fund/)

[**Seedify Fund Official Telegram Channel**](https://t.me/seedifyfundofficial)

Special thanks to [**Seedify HODLers**](https://t.me/SeedifyHODLers) for their awesome tools and their constructive feedback about this script.

------
## Index

* [Requirements](#requirements)
* [Usage](#usage)
* [Reasons Behind](#which-problems-are-users-facing-right-now)
* [What script does](#what-does-this-script-do-to-fix-those-problems)
* [Additional Info](#additional-info)
* [Troubleshooting](#troubleshooting)

------
## Requirements

* Script needs Windows 7/8/10 to operate.
* Chrome is needed to create shortcuts. If Chrome doesn't exist, script will apply other steps/fixes.
* Allowing Chrome Metamask extension to run on incognito mode is necessary. `Extensions -> Metamask -> Details -> Allow in Incognito`

------
## Usage

### For basic users

* Download the standalone executable by [**clicking here**](https://github.com/ZangetsuSF/easify/raw/main/Windows/Easify.exe) or manually from [**Windows**](https://github.com/ZangetsuSF/easify/tree/main/Windows) folder
* Run the executable (it is a self-extracting 7-zip archive, will create a folder named **Easify**)
* Open **Easify** folder and run **Easify.exe**

### For advanced users

Using Python 3.8 is suggested.

Clone the repo with and install required modules via following commands.

```
git clone https://github.com/ZangetsuSF/easify.git
cd easify
pip install --upgrade -r requirements.txt
python main.py
```

To create your own executable version via **PyInstaller**:
```
pip install --upgrade pyinstaller pywin32 pefile
```

Executable creation command (run inside **easify** directory):
```
pyinstaller --clean --distpath Windows --name Easify main.py
```

------
## Which problems are users facing right now?
* Chrome shows an old version of web page from its cache _(causing users to not be able to claim/approve etc)_
* Chrome Translate _(if user enables it)_ changes numbers and some details on web page, making it unusable _(shows wrong info and sometimes buttons don't work)_
* Users' PC time is not always in sync _(causing them to not be able to join IGO pools in time)_
* Users forget or don't know which projects are claimed from **Seedify Fund** website and which are claimed from their own websites
* Users don't always use official links, sometimes they use links from scam Telegram channels or scammer messages
* Users always ask for links of **Vesting Table**, **Combotools** and related trusted tools/websites

To avoid these problems, as **Seedify Fund admins**, we always remind our users to ***clear browser cache/cookies***, ***sync PC time***, ***only use official links*** etc.
But current situation is not effective/optimal so I have decided to create a script to help **Seedify Fund** users.

------
## What does this script do to fix those problems?
* Terminates all Chrome instances
* Creates a directory on desktop called **Seedify**
* Creates [website shortcuts](#list-of-websites-shortcuts-created-by-script) inside **Seedify** directory
* Runs [a few commands](#list-of-network-fix-commands) to fix network issues
* Resets **Windows Time** service, sets its skew tolerance to maximum, syncs local time to internet time

------
## Additional Info

### What do these shortcuts have in common? (via runtime parameters)
* Chrome Incognito mode is on _(no browser history/cookie used/created)_
* Chrome auto-translate feature is disabled
* Chrome DNS-Prefetch feature is disabled
* Chrome background tasks are disabled

------
### List of websites (shortcuts created by script)
* Buy SFUND _(KuCoin, Gate.io and Pancakeswap links)_:

https://pancakeswap.finance/swap?inputCurrency=0x477bc8d23c634c154061869478bce96be6045d12

https://trade.kucoin.com/trade/SFUND-USDT

https://www.gate.io/trade/sfund_usdt

* KYC Check - Blockpass Login:
https://identity.blockpass.org/frontend/#/register/input
* Seedify - Launchpad:
https://launchpad.seedify.fund
* Seedify - Staking-Farming:
https://staking.seedify.fund/
* Seedify - Claim:
https://claim.seedify.fund/
* Seedify - Vesting Table:
http://tinyurl.com/Seedify-IGO-Vesting
* Claim - ScottyBeam:
https://claim.scottybeam.io
* Claim - Hololoot:
https://claiming.hololoot.io
* Claim - BitHotel:
https://investors.bithotel.io
* Tools - Combotools - Investment Tracker:
https://combotools.online/
* Tools - SFUND Calculator:
https://seedifyhodlers.com/tools/calculator
* Tools - ROI Tracker:
https://seedifyhodlers.com/tools/roi/

------
### List of network fix commands
```
netsh winsock reset
netsh int ip reset
ipconfig /flushdns
```

------
### Tested On

Virtualbox VMs: Windows 7 (32/64 bit), Windows 8.1 (64 bit), Windows 10 (64 bit)

------
## Troubleshooting

If you are getting error messages about missing dll files on Windows 7/8 (Windows 10 includes all dlls), try installing **Microsoft Visual C++ Redistributable** packages below (both are official Microsoft download links):

[For Windows 7/8 32 bit](https://aka.ms/vs/17/release/vc_redist.x86.exe)

[For Windows 7/8 64 bit](https://aka.ms/vs/17/release/vc_redist.x64.exe)
