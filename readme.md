## Goals of project

1. Analyze virtual Windows images in FTK
    - I want to read about methods to infect Windows machines

# FTK Imager

FTK Imager is a forensics tool which we will use to extract data from Windows images, to do this I first infected a Windows machine with malware (downloaded from [vx-undergound](https://vx-underground.org/)) and then I added the machine in FTK Imager through the vmdks. ( which we will convert to an E01 (Expert Witness disk image or Encase image file) are used to store digital evidence like disk images.   WORKS OK WITHOUT THIS)

### To use this mount the vmdk

To mount the image I used FTK and made a python script that automates this (this has a lot to improve). 

# Windows Registry

Windows Registry is a database collection of system configurations (profiles for each user, what aplications are installed, what hardware there is, what ports are being used etc.) which we will use to detect if there was any suspicious activity on the image.

There are five root keys in the Registry:
1. HKEY_CLASSES_ROOT : handles how a file is opened by Windows Explorer, is abbreviated as HKCR.
2. HKEY_CURRENT_USER : root configuration of the logged in user (ex: users folders), is abbreviated as HKCU.
3. HKEY_LOCAL_MACHINE : information about the pc, is abbreviated as HKLM.
4. HKEY_HKEY_USERS : has all user profiles, is abbreviated as HKU.
5. HKEY_CURRENT_CONFIG : has the hardware configuration.

For all the registries except the HKEY_CURRENT_USER one the supporting files can be found in %SystemRoot%\System32\Config and for the HKEY_CURRENT_USER the support files can be found in %SystemRoot%\Profiles\Username.
Because we will analyze disk images, we don't have direct access to the registries through regedit.exe, that's why we need to access them on the disk, the majority of the hives are located in C:\Windows\System32\Config more specifically
1. DEFAULT (HKEY_USERS\DEFAULT)
2. SAM (HKEY_LOCAL_MACHINE\SAM)
3. SECURITY (HKEY_LOCAL_MACHINE\Security)
4. SOFTWARE (HKEY_LOCAL_MACHINE\Software)
5. SYSTEM (HKEY_LOCAL_MACHINE\System)

Other important locations include, the C:\Users\<username>\ with the hive: NTUSER.DAT (HKEY_CURRENT_USER) which is a hidden file. Another hive is the AmCache hive which keeps track of recently run aplications and is located in: C:\Windows\AppCompat\Programs\Amcache.hve.

These are important locations that we'll need to extract from FTK imager.

To access the Windows Registry keys we will be using the winreg library.

# Database

Since this was a small project which didn't need a complet database, I decided to use a relational database more exactly with SQLite. A couple of reasons why I chose SQLite:
- Simplicty 
- ACID (Atomicity, Consistency, Isolation, Durability) 
- Efficient with simple queries

# Future ideas

This project could be extended with the following features:
    - Find a way to read the filesystem easier (mayber dockerize FTKImager)
    - Make an interface which will allow future implementations for opening other types of images!
    