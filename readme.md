# Goal of the project

This project aims to:
1. Receive a Windows image as input, mount it, and perform basic static analysis.
2. The static analysis should include:
   - Extracting data about the Windows machine using the Windows Registry.
   - Parsing all files from the image and calculating hashes for each file.
   - Checking each hash value using the VirusTotal API.
   - Investigating persistence if a hash is found to be malicious.
   - Storing all information in a relational database.

# Installation and Setup

1. **Install Dependencies**
   - Run `pip install -r requirements.txt` to install the necessary dependencies.

2. **FTK Imager**
   - Ensure that FTK Imager is installed on your system. The project was tested with version 4.7.1.2.
   - Edit the `FTImager_script.py` file to update the path to your local FTK Imager installation.

3. **Configuration**
   - Create a `.env` file in the root directory of the project.
   - Add your VirusTotal API key to the `.env` file using the following format:
     ```
     API_KEY=your_virustotal_api_key_here
     ```

4. **Running the Application**
   - To mount the image automatically, you need to run the application as an administrator.
   - Upon execution, the application will prompt you to choose whether to mount the image automatically. If you select 'y', you will need to provide the path to the image (e.g., `D:\Forensics\Image test\Windows 10 x64.vmdk`).
   - Note that automatic mounting may fail due to FTK Imager's behavior. If this occurs, you will need to manually mount the image using FTK Imager.

5. **Manual Mounting in FTK Imager**
   - Open FTK Imager.
   - Navigate to `File` -> `Image Mounting`.
   - Select the image file.
   - Set the `Mount Method` to `File System/Read Only`.
   - Click `Mount`.

6. **Post-Mounting Actions**
   - Once FTK Imager has mounted the image, start the application.
   - Enter 'n' when prompted.
   - After the application finishes running, unmount the images from FTK Imager.


# FTK Imager

FTK Imager is a forensics tool which we will use to extract data from Windows images. The benefit of using FTK Imager is that with its
help we can mount the image and if there is a need further manual investigation can be done by the user.

To use FTK Imager, I created a script that automatically mounts the Windows image, allowing the application to run. 

# Windows Registry

Windows Registry is a database collection of system configurations (profiles for each user, what aplications are installed, what hardware there is, what ports are being used etc.) which we will use to detect if there was any suspicious activity on the image.

Because the image is mounted on the host, we can't use the `winreg` library to read values from the registry. That's why this project
uses the [python-registry](https://github.com/williballenthin/python-registry) library to access the registry.

There are five root keys in the Registry:
1. **HKEY_CLASSES_ROOT (HKCR)**: Handles how files are opened by Windows Explorer.
2. **HKEY_CURRENT_USER (HKCU)**: Configuration of the logged-in user (e.g., user folders).
3. **HKEY_LOCAL_MACHINE (HKLM)**: Information about the PC.
4. **HKEY_USERS (HKU)**: Contains all user profiles.
5. **HKEY_CURRENT_CONFIG**: Contains hardware configuration.

For all the registries except the HKEY_CURRENT_USER one the supporting files can be found in %SystemRoot%\System32\Config and for the HKEY_CURRENT_USER the support files can be found in %SystemRoot%\Profiles\Username.
Because we will analyze disk images, we don't have direct access to the registries through regedit.exe, that's why we need to access them on the disk, the majority of the hives are located in C:\Windows\System32\Config more specifically
1. DEFAULT (HKEY_USERS\DEFAULT)
2. SAM (HKEY_LOCAL_MACHINE\SAM)
3. SECURITY (HKEY_LOCAL_MACHINE\Security)
4. SOFTWARE (HKEY_LOCAL_MACHINE\Software)
5. SYSTEM (HKEY_LOCAL_MACHINE\System)

Other important locations include, the C:\Users\<username>\ with the hive: NTUSER.DAT (HKEY_CURRENT_USER) which is a hidden file. Another hive is the AmCache hive which keeps track of recently run aplications and is located in: C:\Windows\AppCompat\Programs\Amcache.hve.

For this project we will need to extract the following information about the Windows image:
- ips
- hosts
- users
- guid

To extract the `ips` we will use the `SYSTEM` registry hive with the key: `Tcpip\\Parameters\\Interface`. This key contains information related to network interfaces. We only extract the information that is in one of the following fields:`DhcpIPAddress`, `DhcpServer`, `DhcpNameServer` and `IPAddress`.

For the hosts the `SYSTEM` hive is used with the key: `ComputerName`. 

For the GUID the `SOFTWARE` hive is used with the key: `MacchineGuid`.

For the users the `SOFTWARE` hive is used with the key:`ProfileList`.
More information about the registry values for the users can be found [here](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-identifiers). 


## Persistence checking

Persistence on a Windows system is commonly established using registry run keys and the startup folder.
Therefore, we will check the following:

- If the file path exists in the `Windows startup` folder. There are two locations to check:   
    1. C:\Users\USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup (user-specific) 
    2. C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp (system-wide)

-   The `registry Runs keys` which causes a command to run when a user logs on. There is also the RunOnce registry key that is used to clear the associated entry from the registry as soon as the command is run. To do this the following registries needs to be checked:
    1. HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
    2. HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
    3. HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce
    4. HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce

# Database

Since this was a small project which didn't need a complex database, I decided to use a relational database. To manage the database I used `SQLalchemy`.

### Tables

#### WindowsImage
Stores each Windows image file to be analyzed. The name of each file needs to be entered manually.
| Field        | Type         | Description                            |
|--------------|--------------|----------------------------------------|
| `image_id`   | Primary Key   | Unique identifier for each image.      |
| `image_name` | String       | Name of the Windows image.             |

#### ImageFile
Stores each file path from the analyzed Windows image and if the file is malicious.

| Field        | Type         | Description                            |
|--------------|--------------|----------------------------------------|
| `file_id`    | Primary Key   | Unique identifier for each file.       |
| `image_id`   | Foreign Key   | Reference to `WindowsImage`.           |
| `path`       | String       | File path.                             |
| `is_malicious` | Boolean     | Indicates if the file is malicious.    |

#### FileHash
Stores the hash for each analyzed file from the Windows image.

| Field        | Type         | Description                            |
|--------------|--------------|----------------------------------------|
| `file_id`    | Foreign Key   | Reference to `ImageFile`.              |
| `hash_type`  | String       | Type of hash (e.g., MD5, SHA1).        |
| `hash_value` | String       | Value of the hash.                     |

#### ImageGUID
Stores the GUID for each analyzed Windows image. 

| Field        | Type         | Description                            |
|--------------|--------------|----------------------------------------|
| `guid_id`    | Primary Key   | Unique identifier for the GUID entry.  |
| `image_id`   | Foreign Key   | Reference to `WindowsImage`.           |
| `guid_value` | String       | The GUID value.                        |

#### ImageHost
Stores the hosts for each analyzed Windows image.

| Field        | Type         | Description                            |
|--------------|--------------|----------------------------------------|
| `host_id`    | Primary Key   | Unique identifier for each host.       |
| `image_id`   | Foreign Key   | Reference to `WindowsImage`.           |
| `host_name`  | String       | Name of the host.                      |

#### ImageIP
Stores the ips for each analyzed Windows image.

| Field               | Type         | Description                            |
|---------------------|--------------|----------------------------------------|
| `ip_id`             | Primary Key   | Unique identifier for each IP entry.   |
| `image_id`          | Foreign Key   | Reference to `WindowsImage`.           |
| `interface`         | String       | Network interface.                     |
| `DhcpIPAddress`     | String       | DHCP IP address.                       |
| `DhcpServer`        | String       | DHCP server address.                  |
| `DhcpNameServer`    | String       | DHCP name server address.             |
| `IPAddress`         | String       | IP address.                            |

#### ImageUser
Stores all the users from a Windows image.

| Field        | Type         | Description                            |
|--------------|--------------|----------------------------------------|
| `user_id`    | Primary Key   | Unique identifier for each user.       |
| `image_id`   | Foreign Key   | Reference to `WindowsImage`.           |
| `user_value` | String       | User information.                      |

#### FilePersistence
Stores the files that have persistence on the Windows image.

| Field               | Type         | Description                            |
|---------------------|--------------|----------------------------------------|
| `persistence_id`    | Primary Key   | Unique identifier for each persistence entry. |
| `image_id`          | Foreign Key   | Reference to `WindowsImage`.           |
| `name`              | String       | Name of the file with persistence.     |
| `path`              | String       | Path related to the file with persistence. |
| `persistence_type`  | String       | Type of persistence (e.g., 'run', 'runOnce'). |

### Relationships

- **`WindowsImage`** is the central table, with foreign key references in:
  - **`ImageFile`**
  - **`ImageGUID`**
  - **`ImageHost`**
  - **`ImageIP`**
  - **`ImageUser`**
  - **`FilePersistence`**

- **`ImageFile`** is connected to **`FileHash`** through `file_id`.

- **`FilePersistence`** supports different persistence types, with `name` and `path` fields used accordingly.

     