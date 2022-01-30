# Easify - Seedify Fund Helper Script

This is a Python script which tries to fix some issues that Windows users are experiencing while using **Seedify Fund** website (IGO participation, claiming, staking/farming).

Created by **@ZangetsuSF**

Telegram admin at **Seedify Fund Turkish Group** - https://t.me/sfundturkey

Special thanks to **Seedify HODLers** (https://t.me/SeedifyHODLers) for their awesome tools and feedbacks about this script.

**NOTE:** This is not an official Seedify tool/script. Please read LICENSE before using it.

Seedify Fund official website: https://launchpad.seedify.fund/

------

**Usage**

**For basic users**

Just download and run the standalone executable file (Easify.exe) via link below or from **Windows** folder.

https://github.com/ZangetsuSF/easify/raw/main/Windows/Easify.exe

**For advanced users**

Clone the repo with and install required modules via following commands.

* git clone https://github.com/ZangetsuSF/easify.git
* pip install --upgrade keyboard admin pywin32

Dependencies to create your own executables:
* pip install --upgrade pyinstaller pywin32 pefile

Executable creation command (run inside easify directory):
* pyinstaller --clean --distpath Windows --name Easify --onefile main.py

------

**Problems**
* Chrome shows an old version of web page from its cache (causing users to not be able to claim/approve etc)
* Chrome Translate (if user enables it) changes numbers and some details on page, making it unusable (shows wrong info and sometimes buttons don't work)
* User's PC time is not in sync (causing them to not be able to join IGO pools in time)
* Users forget or don't know which projects are claimed from **Seedify Fund** website and which are claimed from their own websites.
* Users don't always use official links, sometimes they use scam links when they see on scam Telegram channels or when a scammer messages them
* Users always ask for links of "Vesting Table", "Combotools", and related trusted tools/websites.

To avoid these problems, as **Seedify admins**, we are constantly telling our users to "clear browser cache/cookies", "sync PC time", "only use official links" etc.
But current situation is not effective/optimal so I have decided to create a script to help **Seedify Fund** users.

------

**What does this script do to fix those problems?**
* Terminates all Chrome instances
* Creates a directory on desktop called "Seedify"
* Creates website (check below for a list) shortcuts inside Seedify directory
* Runs a few commands to fix network issues (check below for a list)
* Resets Windows Time service, sets its skew tolerance to maximum, syncs local time to internet time

------

**What do these shortcuts have in common? (via runtime parameters)**
* Chrome Incognito mode is on (no browser history/cookie used/created)
* Chrome auto-translate feature is disabled
* Chrome DNS-Prefetch feature is disabled
* Chrome background tasks are disabled

------

**List of websites**
* Buy SFUND (KuCoin, Gate.io and Pancakeswap links):

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

**List of network fix commands**
* netsh winsock reset >nul
* netsh int ip reset >nul
* ipconfig /flushdns
