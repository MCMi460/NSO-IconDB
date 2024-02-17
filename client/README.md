# User Icons Grabber
This tutorial works for both Windows and MacOS.

*Table of Contents:*  
1. [Downloading Python](#downloading-python)
2. [Installing Python](#installing-python)
3. [Downloading the program](#downloading-the-program)
4. [Running the program](#running-the-program)
    - [Running on Windows](#running-on-windows)
    - [Running on MacOS](#running-on-macos)
5. 

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
