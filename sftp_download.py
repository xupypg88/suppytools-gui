#!/usr/bin/python3

#
# Author: Mikhail Topskiy
#
#

# todo put all into a class and restructure
# todo check for file tree presentation in GUI
# todo check for exception when access to the SFTP is denied
# todo check if the url is correct
# todo add logging module for API executed and errors

import pysftp
import PySimpleGUI as sg
import clipboard
import os

url = clipboard.paste()

# username and pass

myHostname = url.split('@')[1].split('/')[0]
myUsername = url.split('@')[0].split('/')[2].split(':')[0]
myPassword = url.split('@')[0].split(':')[2]
caseNumber = myUsername[3:]
pathCases = '/home/grizzly/Cases/' + caseNumber + '/'

if os.path.isfile(pathCases):
    os.mkdir(pathCases)

print(myHostname)
print((myUsername, myPassword))


def openfiletree(filelist):

    sg.theme('DarkAmber')

    layout = [[sg.Text('Select a file')]]
    for f in filelist:
        layout.append([sg.Checkbox(f, default=False)])
    layout.append([sg.Button('Ok'), sg.Button('Close')])

    print(layout)

    # Create the Window
    window = sg.Window('Download', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    result = []
    while True:
        event, values = window.read()
        if event in (None, 'Close'):
            return
        if event in 'Ok':
            return values
        print('You entered ', event)

    window.close()
# connection closed automatically at the end of the with-block


cnopts = pysftp.CnOpts()
cnopts.hostkeys = None


with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
    print("Connection successfully established ... ")

    # Switch to a remote directory
    sftp.cwd('upload')

    # Obtain structure of the remote directory
    directory_structure = sftp.listdir_attr()

    # Print data
    filenames = []
    for file in directory_structure:
        filenames.append(file.filename)

    options = openfiletree(filenames)
    print(options)
    for key, value in options.items():
        if value:
            print('downloading ', filenames[key], ' ...')
            # todo checking for directory before download
            sftp.get(filenames[key], pathCases + filenames[key])



