# User Icons Grabber
This tutorial works for both Windows and MacOS.

*Table of Contents:*  
1. [Downloading Python](#downloading-python)
2. [Installing Python](#installing-python)
3. [Downloading the program](#downloading-the-program)
4. [Running the program](#running-the-program)
    - [Running on Windows](#running-on-windows)
    - [Running on MacOS](#running-on-macos)
5. [Completing `private.py`](#completing-privatepy)
    - [Getting your cookies from Google Chrome](#getting-your-cookies-from-google-chrome)
    - [Entering cookie into `private.py`](#entering-cookie-into-privatepy)
6. [Getting your icons](#getting-your-icons)

## Downloading Python
Go to [python.org](https://www.python.org/downloads/), hover your mouse over the **Downloads** tab, select your operating system, and download the latest version of Python.

## Installing Python
Run the file you just downloaded. It is rather simple on both MacOS and Windows. If you'd like to avoid using Admin, uncheck the "Use admin privileges" option on Windows.

***Please check the "Add python.exe to PATH" option on Windows.***

## Downloading the program
[Click here](https://github.com/MCMi460/NSO-IconDB/archive/refs/heads/main.zip) to download the zip file of the current `main` branch version.  

Once done, enter your Downloads folder where the file has been downloaded and extract the file. This can be done by right-clicking and choosing "Extract All" on Windows and "Open" on MacOS.  
This will create a new directory in your Downloads folder. We are done downloading the program.

## Running the program
Running the program is something that you will likely need to do more than once as you set up the authorization requirements.  
This step can be repeated as many times as you wish.

### Running on Windows
Press Win+R and type in `powershell.exe`. Press enter.  
Enter the following (copy line-by-line):
```ps1
cd "$((New-Object -ComObject Shell.Application).NameSpace('shell:Downloads').Self.Path)\NSO-IconDB-main\NSO-IconDB-main\client\"
py client.py
```

### Running on MacOS
Press Cmd+Space and type in `Terminal.app`. Press enter.  
Enter the following (copy line-by-line):
```sh
cd ~/Downloads/NSO-IconDB-main/client/
python3 client.py
```

## Completing `private.py`
In order to login to your Nintendo Account and retrieve your owned icons, you will first need to get your login information from Nintendo's website.

Because of the differences between web browsers and operating systems, this tutorial will simplify it to one web browser for sanity's sake: Google Chrome.

### Getting your cookies from Google Chrome
If you haven't already, download [Google Chrome](https://www.google.com/chrome/) and log into [accounts.nintendo.com](https://accounts.nintendo.com/).

**Once you have logged in, right click and press "Inspect."**

![inspect](/resources/1.png)

Then, choose the ">>" and click on "Application."

![application](/resources/2.png)

Under Cookies, select "https://accounts.nintendo.com/".

![cookies](/resources/3.png)

Find your "NASID" cookie amongst them.

![NASID](/resources/4.png)

Then copy, the value from the cookie at the bottom.

![like so](/resources/5.png)

### Entering cookie into `private.py`
Once you have that cookie copied, *do not share it*. It is essentially a key into your Nintendo account. Keep it private.

Now, we will add the cookie into our `private.py` file. Be sure to have ran the program at least once by this point.

**On Windows:**
> Press Win+R and type in `powershell.exe`. Press enter.  
> Enter the following:
```ps1
start notepad "$((New-Object -ComObject Shell.Application).NameSpace('shell:Downloads').Self.Path)\NSO-IconDB-main\NSO-IconDB-main\client\private.py"
```
---
**On MacOS:**
> Press Cmd+Space and type in `Terminal.app`. Press enter.  
> Enter the following:
```sh
open -a TextEdit ~/Downloads/NSO-IconDB-main/client/private.py
```
---
Now, where it says `'Cookie': '[REDACTED]'`, replace `[REDACTED]` with `NASID=<enter your token here>`. Paste your token there as instructed.

The final product should look something like this:

```py
headers:dict = {
    # ...
    'Cookie': 'NASID=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJPZiBjb3Vyc2UgdGhpcyBpc24ndCByZWFsIiwibmFtZSI6IkxtYW8geW91IHRob3VnaHQiLCJpYXQiOi0xfQ.zujv5o01hh5Y0X6RmCYInBAi1CNR4jWWYDuBV1Go2Go',
    'Host': 'accounts.nintendo.com',
    # ...
}
```

## Getting your icons
Now, it should be as simple as [running the program](#running-the-program)!

Please [join my Discord server](https://discord.gg/pwFASr2NKx) if you need assistance.
