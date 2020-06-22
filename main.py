import time
import paramiko
import datetime
import encryption
import socket
import netcompare
import re
from os import listdir
from os.path import isfile, join
import os
import tkinter as tk
import getpass

class Application(tk.Frame):
    def __init__(self, text, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.text = text
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Text(self)
        self.label.insert(tk.END, self.text)
        self.label.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")


def showWindow(text):
    root = tk.Tk()
    app = Application(text, master=root)
    app.mainloop()

currentDevice = ""
exitTag = "X"
devicesFile = "devices.txt"
devices = []

user =""
password = ""
enable_password = ""

def GetPassword():
    global user
    global password
    global enable_password

    if user == "":
        user = input("Enter SSH username:")
        password = getpass.getpass("Enter SSH Password:")
        enable_password = getpass.getpass("Enter device enable password:")
    else:
        choice = input("Would you like to use the previously saved password? [Y/N]")
        if choice.upper() != "Y":
            user = input("Enter username:")
            password = getpass.getpass("Enter password:")
            enable_password = getpass.getpass("Enter device enable password for " + currentDevice + ":")

    return user, password, enable_password

def validateIP(Ip):
    try:
        nums = Ip.split(".")
        if len(nums) != 4:
            return False

        for num in nums:
            num = int(num)
            if num < 0 or num > 255:
                return False
    except:
        return False

    return True

def help():
    global exitTag
    global currentDevice

    print("0. Back-up all online devices.")
    print("1. Select a device.")
    print("2. Add a new device.")
    print("3. Remove a device.")
    if currentDevice != "":
        print("4. Back-up the configuration.")
        print("5. Display backed-up configuration.")
        print("6. Send configuration.")
        print("7. Troubleshooting commands.")
        print("8. Download IOS.")
        print("9. Configuration file comparison.")
    print(exitTag + ". Exit.")

def readAnswer():
    global currentDevice
    result = input("[" + currentDevice + "]: ")
    return result
def isNumber(a):
    try:
        a = int(a)
        return True
    except:
        return False

def process(answer):
    global devices
    global currentDevice
    global exitTag
    if answer == "0":
        backupAll()
    elif answer == "1":
        openDevicesFile()
        if len(devices) > 0:
            showDevices(ping = True)
            result = input("Type number of device or X to return to the main menu: ")
            if result.upper() != exitTag:
                selectDevice(result)
        else:
            printMessage("Device list is empty.")
    elif answer == "2":
        openDevicesFile()
        showDevices()
        result = input("Type the IP address of the new device or X to return to the main menu: ")
        if result.upper() != exitTag:
            if not validateIP(result):
                printMessage("Invalid IP format")
            else:
                if result in devices:
                    printMessage("Device is already on the list.")
                else:
                    addDevice(result)
                    printMessage("Device added: " + result)
    elif answer == "3":
        openDevicesFile()
        showDevices()
        result = input("Type number of device or X to return to the main menu: ")
        if result.upper() != exitTag:
            choice = input("Are you sure?[Y/N]")
            if choice.upper() == "Y":
                removeDevice(result)
    elif currentDevice != "":
        if answer == "4":
            downloadConfig(currentDevice)
        elif answer == "5":
            config = getConfigFromList(currentDevice)
            if config is not None:
                showWindow(config)

                os.system("cls")
        elif answer == "6":
            config = getConfigFromList(currentDevice)
            if config is not None:
                uploadConfig(config, currentDevice)
        elif answer == "7":
            commands = showCommands()
            choice = input("Select command or X to return to the main menu: ")
            if choice.upper() != exitTag:
                if isNumber(choice):
                    choice = int(choice)
                    if 0 <= choice < len(commands):
                        print("Sending " + commands[choice][0])
                        sendCommand(commands[choice][0], currentDevice)
                    else:
                        printMessage("Index out of range.")
                else:
                    printMessage("Incorrect value.")
        elif answer == "8":
            downloadImage(currentDevice)
        elif answer == "9":
            conf = getConfigFromList(currentDevice)
            if conf is not None:
                newConf = downloadConfig(currentDevice, saveFile=False)
                print("The following configuration lines are new:")
                result = netcompare.compareConfigs(newConf, conf)
                print(result)
                showWindow(result)
                printMessage("Comparison finished.")
        else:
            printMessage("Input error.")
    else:
        printMessage("Incorrect input. Try again.")

def backupAll():
    openDevicesFile()

    global devices
    devDone = []
    for ip in devices:
        if isOpen(ip):
            print("Creating back-up for: " + ip)
            downloadConfig(ip)
            devDone.append(ip)
    if len(devDone) > 0:
        print("Back-up successfull for: ")
        for ip in devDone:
            print(ip)
    printMessage("")

def connectSSH(ip):
    user, password, enable_password = GetPassword()
    print("Connecting using SSH to: " + ip)
    port = 22
    ip = ip.strip()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, user, password, look_for_keys=False)
    chan = ssh.invoke_shell()
    #time.sleep(2)
    return chan, ssh

def printMessage(message):
    input(message + " " + "Press enter to continue")
    os.system("cls")

def sendCommand(command, ip):
    try:
        chan, ssh = connectSSH(ip)
    except:
        printMessage("SSH connection error")
        return

    chan.send('enable\n')
    chan.send(enable_password + '\n')
    time.sleep(1)
    chan.send(command + '\n')
    time.sleep(1)
    chan.send(' ')
    time.sleep(1)
    chan.send(' ')
    time.sleep(5)
    output = chan.recv(999999)
    output = output.decode().split("\r\n")
    for line in output:
        print(line)
    printMessage("Done")
    ssh.close()

def showCommands():
    with open("commands.txt", 'r') as content_file:
        content = content_file.read()
        content = content.split("\n")
        commands = []
        for line in content:
            items = line.split("(")
            items[1] = "(" + items[1]
            commands.append([items[0], items[1]])

        for i in range(0, len(commands)):
            print(str(i) + ". " + commands[i][0] + " " + commands[i][1])

        return commands

def getConfigFromList(deviceId):
    path = os.path.abspath(__file__)
    path = path.replace("main.py", "")
    files = [f for f in listdir(path) if isfile(join(path, f))]
    configs = []
    os.system("cls")
    for file in files:
        if deviceId in file:
            configs.append(file)

    if len(configs) == 0:
        printMessage("File not found.")
        return;

    for i in range(0, len(configs)):
        print(str(i) + ". " + configs[i])

    choice = input("Select configuration: ")

    try:
        filename = configs[int(choice)]
    except:
        printMessage("Index out of range.")
        return None

    with open(filename, 'r') as content_file:
        content = content_file.read()
        password = getpass.getpass("Type password for the encrypted file: ")
        try:
            content = encryption.AESCipher(password).decrypt(content)
        except:
            printMessage("Incorrect encryption password.")
            return None

        return content

    return None

def removeDevice(deviceId):
    global devices
    try:
        dev = devices[int(deviceId)]
        devices.remove(dev)
        saveDevicesFile()
        printMessage(dev + " removed")
    except:
        printMessage("Invalid number of device.")


def addDevice(device):
    global devices
    if device not in devices:
        devices.append(device)
        saveDevicesFile()

def saveDevicesFile():
    global devices
    global devicesFile
    f = open(devicesFile, "w")
    for device in devices:
        f.write(device + "\n")
    f.close()

def selectDevice(deviceId):
    global currentDevice
    global devices
    try:
        deviceId = int(deviceId)
        currentDevice = devices[deviceId]
        printMessage(currentDevice +" selected.")
    except:
        printMessage("Incorrect number of device.")

def showDevices(ping = False):
    ENDC = '\033[0m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    global devices
    for i in range(0, len(devices)):
        status = ""
        if ping:
            if isOpen(devices[i]):
                status = OKGREEN + "Online" + ENDC
            else:
                status = FAIL + "Offline" + ENDC

        print(str(i) + ". " + devices[i] + " " + status)

def openDevicesFile():
    global devices
    global devicesFile
    try:
        f = open(devicesFile, "r")
        rawData = f.read()
        f.close()
        devices = rawData.split("\n")
        devices = [dev for dev in devices if dev != ""]
    except:
        printMessage(devicesFile + " is missing.")
        devices = []

def uploadConfig(configContent, ip):
    try:
        chan, ssh = connectSSH(ip)
    except:
        printMessage("SSH connection error")
        return

    chan.send('enable\n')
    chan.send(enable_password + '\n')
    time.sleep(1)
    chan.send('conf t\n')
    time.sleep(1)
    chan.send(configContent)
    time.sleep(5)
    output = chan.recv(999999)
    output = output.decode().split("\r\n")
    os.system("cls")
    for line in output:
        print(line)
    printMessage("File uploaded.")
    ssh.close()

def downloadConfig(ip, saveFile = True):
    now = datetime.datetime.now()

    try:
        chan, ssh = connectSSH(ip)
    except:
        printMessage("SSH connection error.")
        return

    print("Working..")

    chan.send('enable\n')
    chan.send(enable_password + '\n')
    time.sleep(1)
    chan.send('term len 0\n')
    time.sleep(1)
    chan.send('sh run\n')
    time.sleep(5)
    output = chan.recv(999999)

    if not saveFile:
        return output.decode("utf-8")

    print("Configuration captured.")
    filePassword = getpass.getpass("Type encryption password: ")
    filePasswordConfirm = getpass.getpass("Confirm encryption password: ")

    while filePassword != filePasswordConfirm:
        printMessage("Encryption passwords do not match. Try again.")
        filePassword = getpass.getpass("Type encryption password: ")
        filePasswordConfirm = getpass.getpass("Confirm encryption password: ")

    filename = "%s_%.2i%.2i%i_%.2i%.2i%.2i" % (ip, now.year, now.month, now.day, now.hour, now.minute, now.second)
    f1 = open(filename, 'w')
    data = output.decode("utf-8")
    data = encryption.AESCipher(filePassword).encrypt(data)
    f1.write(data.decode("utf-8"))
    f1.close()
    ssh.close()
    printMessage("Configuration saved for device " + ip + " under file name: " + filename)
    return filename

def downloadImage(ip):
    now = datetime.datetime.now()

    try:
        chan, ssh = connectSSH(ip)
    except:
        printMessage("SSH connection error")
        return

    chan.send('enable\n')
    chan.send(enable_password + '\n')
    time.sleep(1)
    chan.send('show ver\n  ')
    time.sleep(5)
    output = chan.recv(999999)
    output = output.decode().split("\r\n")

    file = None
    for line in output:
        #print(line)
        if "System image file is \"" in line:
            file = line.split("System image file is \"")
            file = file[1].replace("\"", "")
            print(file)

    if file is not None:
        toSend = "copy " + file + " ftp://admin:admin@192.168.1.2\n"
        #toSend = "copy flash:soft.bin ftp://admin:admin@192.168.1.2"
        chan.send(toSend)
        time.sleep(1)
        chan.send("\n")
        time.sleep(1)
        timestamp = "%s_%.2i%.2i%i_%.2i%.2i%.2i" % (ip, now.year, now.month, now.day, now.hour, now.minute, now.second)
        chan.send("IOS_" + timestamp + ".bin\n")
        time.sleep(5)
        output = chan.recv(999999)
        output = output.decode().split("\r\n")
        for line in output:
            print(line)

        time.sleep(1)
        while chan.recv(1).decode() == "!":
            print(".", end='')

        print("")
    ssh.close()
    printMessage("Done")

def isOpen(ip,port = 22):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(0.2)
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except Exception as e:
        pass
      #print(e)
    finally:
        s.close()

    return False

def main():
    answer = ""
    while answer.upper() != exitTag:
        help()
        answer = readAnswer()
        os.system("cls")
        if answer.upper() != exitTag:
            process(answer)

if __name__ == '__main__':
    main()