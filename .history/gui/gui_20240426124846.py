import PySimpleGUI as sg
import subprocess
import os

# Get the path to the current user's Downloads folder
default_download_path = os.path.expanduser('~/Downloads')

def call_package_script(destination):
    subprocess.run(['python', 'package.py', destination], check=True)

def call_unpackage_script(zip_file):
    subprocess.run(['python', 'unpackage.py', zip_file], check=True)

layout = [
    [sg.Text('VSCode Environment Transfer Tool', size=(30, 1), justification='center', font=("Helvetica", 25))],
    [sg.Text('Destination Directory:'), sg.InputText(default_download_path, key='DESTINATION'), sg.FolderBrowse()],
    [sg.InputText('', key='ZIP_FILE', enable_events=True, visible=False), sg.FileBrowse('Select Zip File', file_types=(("Zip Files", "*.zip"),), target='ZIP_FILE')],
    [sg.Button('Package VSCode Env'), sg.Button('Setup VSCode Env')]
]

window = sg.Window('VSCode Env Tool', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Package VSCode Env':
        try:
            call_package_script(values['DESTINATION'])
            sg.popup('Packaging complete.')
        except subprocess.CalledProcessError as e:
            sg.popup(f'An error occurred: {e}', title='Error')
    elif event == 'Setup VSCode Env':
        zip_file_path = values['ZIP_FILE']
        if zip_file_path and zip_file_path.endswith('.zip'):
            try:
                call_unpackage_script(zip_file_path)
                sg.popup('Unpackaging complete.')
            except subprocess.CalledProcessError as e:
                sg.popup(f'An error occurred: {e}', title='Error')
        else:
            sg.popup('Please select a valid VSCode environment zip file.', title='Error')

window.close()
