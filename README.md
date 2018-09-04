# NFC-Printing

## Purpose of the application
This application was developed during the internship in Innopolis University. The task was to implement a system that would help university employees to print documents more effectively using their NFC-cards. This implies that any printer that is existent in the database of the printers should have NFC-reader connected to it.

## Structure of the application
The application consists of three parts:
* Virtual IPP printer
* NFC-Reader
* Listener of NFC-Reader requests
### Virtual IPP printer
Is actually a server that behaves as a printer so that other devices could send files to print on it.
### NFC-Reader
Is the only piece of hardware we designed. It sends requests that contain reader id and card id to the server.
### Listener of NFC-Reader requests
Processes requests from NFC-Reader and sends the documents to printing module.

## Stack of technologies
* flask
* pyodbc

## Installation
### Requirements
* python3
* pip3
* nodejs ([quick installation and project usage guide](https://github.com/reconrus/NFC-Printing/tree/master/server/virtial-ipp-printer))
### The process
* Download the repository from GitHub (is made through Git Bash)
```sh
git clone https://github.com/reconrus/NFC-Printing
```
* Intall requirements
```sh
pip install -r requirements.txt
```
* Follow [the guide](https://github.com/reconrus/NFC-Printing/tree/master/server/virtial-ipp-printer) to install nodejs
* Launch the MS SQL Database if it is not already started
* Add printers to the server manually
* Add printers and NFC-Readers to the database
* Turn off Windows firewall for ports 3000 (Virtual IPP printer) and 5000 (Listener of NFC-Reader requests)
### Running
You have to start both Virtual IPP printer and Listener of NFC-Reader requests separately. 
* Instructions to launch Virtual IPP printer were described [here](https://github.com/reconrus/NFC-Printing/tree/master/server/virtial-ipp-printer).
* To start the listener you have to type the following in the administrator cmd from /server folder (the code is for windows)
```sh
python.exe main.py
```
