# FYPCiscoAutomation
A tool created to automate network administration as part of my final year project.

1.1	User manual

1.1.1	Introduction
This document covers The Net Helper usage and documentation

1.1.2	The user manual
1.1.3	The main menu (limited view)
 
After starting the software, the default view is the main menu. This view will change depending on if the current working device has been selected. In case the device was selected, the extended menu is displayed. To select a device to work with, use option “1” and confirm with enter.
 
Select the device from the list and confirm with the Enter key. The extended menu is displayed now.
 
1.1.4	The main menu (extended view)

Now that all options are available, there are many functionalities to select from.
1.1.5	Backup all online devices
To use this functionality, select 0 in the main menu. The Net Helper will try to download the content of the running configuration from every device from the list that is available. To check availability, the Net Helper uses ICMP protocol on port 22 (SSH). 
If it is the first time you are using the SSH connection since The Net Helper started, you will be asked to provide SSH credentials and the enable password for the device.
 
The credentials need to be relevant for the device with the IP address displayed in the top line. During password input, the content of the password is not displayed as a security measure.
 
When the Net Helper succeeds in downloading the running configuration for the device, enter the encryption password. The Net Helper users AES encryption for every read/write interaction with stored configuration files. This guarantees that files are stored securely.
 
The following message is generated when single back-up task is over. The files are saved in the software’s current working directory. When there is more than one online device, the process will continue for each of the devices. 
 
At the end of the process, a final confirmation message is generated. 

1.1.6	Device selection
Device selection functionality unlocks the extended menu view and allows you to select a single device that all the functionalities will then apply to. To use device selection, you need to choose option 1 -Select a device from the main menu. The following view is displayed.
 
The program stores saved devices in devices.txt file in the current working directory. Select device functionality displays which from the saved devices are available at the moment and allows you to choose from the list. To check availability, the Net Helper uses ICMP protocol on port 22 (SSH).
To select a device, input corresponding number from the list. The Net Helper will display a confirmation message and currently selected device will be now displayed in the bottom of the main menu.
 
To change the device, use Select a device option again.
1.1.7	Add a new device
Select option 2 – Add a new device to update the list of saved devices. The Net Helper will list stored devices.
 
Type the IP address of the new device. When successful, a confirmation message is displayed.
1.1.8	Remove a device
To remove a device from the list of saved devices select option 3 – Remove a device, from the main menu. 
The Net Helper will list stored devices.
 
Input the corresponding number of a device you wish to remove, then confirm with “Y”. A confirmation message is displayed.

1.1.9	Back-up the configuration

To use this functionality, select 4 from the main menu. The Net Helper will try to download the content of the running configuration from currently selected device. 
If it is the first time you are using the SSH connection since The Net Helper started, you will be asked to provide SSH credentials and the enable password for the device.
 
If you already used the SSH connection and provided credentials, you will be asked if you would like to re-use them.
 
During password input, the content of the password is not displayed as a security measure.
 
When the Net Helper succeeds in downloading the running configuration for the device, you will be asked to input the encryption password. The Net Helper users AES encryption for every read/write interaction with stored configuration files. This guarantees that files are stored securely.
 
The following message is generated when back-up task is over. The file is saved in the software’s current working directory.
1.1.10	Display backed-up configuration
To view saved configuration, select 5 – Display backed-up configuration from the main menu. The Net Helper will scan current working directory for all the previously saved configuration for the currently selected device. Configurations for other devices will not be displayed.
 
As the configurations are stored securely with use of AES encryption, the password needs to be provided. During password input, the content of the password is not displayed as a security measure.
 
A pop-up window will be opened showing the configuration from the file. You can copy it’s content. In order for the Net Helper to continue, please press QUIT.
 
1.1.11	Configuration deployment

To send saved configuration to the device, please select 6 – Send configuration from the main menu. The list of the available configuration is displayed. Note that only configuration for the currently selected device are displayed.
 
Select configuration from the list. If you already used the SSH connection and provided credentials, you will be asked if you would like to re-use them.
 
After providing the credentials, the Net Helper will show following message:
 
When the process is over, the result of the deployed configuration will be displayed, showing all successful and unsuccessful commands. Press enter to return to the main menu.
 
 
1.1.12	Troubleshooting commands
Troubleshooting commands allows you to send pre-configured troubleshooting commands and view the output. The commands are included in commands.txt file and can be edited using any text editor. When editing the commands, you must stick to the format of command (Description). Please see picture below for the list of pre-configured commands.
 
To use this functionality, select 7 – Troubleshooting commands from the main menu. The list of available commands will be displayed.
 
Select desired command and confirm with the Enter key, then provide password. 
 
The output will be displayed in the command line interface. Press Enter key to return to the main menu.
 

1.1.13	Download the IOS
The Download IOS features allow you to back-up current IOS image from the device. The Network Helper uses FTP to transfer the IOS. This requires the FTP server to be running on the host device. In the prototype version, the address for FTP server is set up as: 192.168.1.2. The default credentials are set up as admin:admin.
To use this feature, select 8. Download IOS from the main menu. The Net Helper will ask you for SSH credentials.
 
The download will start shortly. You will be updated on the progress of the download by “.” symbol. The file is saved into the default FTP directory on the remote host (default:192.168.1.2). The name of the file contains the date and hour of the functionality execution.
 

If the functionality fails, make sure the FTP protocol is allowed through the firewall and the FTP server is running on the remote host.

1.1.14	Configuration comparison
Configuration comparison features is based on netcompare library. The feature takes two inputs: stored configuration file and current configuration from the live device. The two files are compared against each other.
To use the Configuration comparison functionality, select option 9 – Configuration file comparison from the main menu. You will be presented with the list of available configurations for current device. Your selection will act as original configuration file.
 
The target configuration will be the configuration from the currently selected device. The difference will be shown in a pop-up window. 
1.	For every line of the original configuration file, check if the entry is present in the target file. If the entry is not detected, the script assumes that to bring the configuration file to the target file a “no” prefix is required for the missing lines.
2.	For each line of target configuration, check if the entry is present in the origin file. If the entry is not detected, the script assumes that to bring the configuration file to the target file a “no” prefix is required for the missing lines.
 
 
Press QUIT to continue to the main menu.

