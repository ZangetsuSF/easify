# Easify - Seedify Fund Helper Script

A little tool to fix some basic issues Windows users are experiencing while using **Seedify Fund** website (participating in IGOs, claiming, staking/farming).

------

**Usage**

* For non-tech users
Just download the standalone executable file which is located in "dist" folder.

* Techy users
Clone the repo with and install required modules via following commands.
*git clone https://github.com/ZangetsuSF/easify.git
*pip install --upgrade keyboard admin pywin32

Dependencies to create your own executables:
*pip install --upgrade pyinstaller pywin32 pefile

------

**Problems:**
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
* Incognito mode is on (no browser history/cookie used/created)
* Auto-translate feature is disabled
* DNS-Prefetch feature of Chrome is disabled
* Background tasks of Chrome are disabled

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
