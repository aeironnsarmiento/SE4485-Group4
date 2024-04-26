import PySimpleGUI as sg
import subprocess
import os

def call_package_script(destination):
    # Call the package.py script as a subprocess
    subprocess.run(['python', 'package.py', destination], check=True)

def call_unpackage_script(zip_file):
    # Call the unpackage.py script as a subprocess
    subprocess.run(['python', 'unpackage.py', zip_file], check=True)

layout = [
    [sg.Text('VSCode Environment Transfer Tool', size=(30, 1), justification='center', font=("Helvetica", 25))],
    [sg.Text('Destination Directory:'), sg.InputText('C:\\Users\\jg\\Desktop', key='DESTINATION'), sg.FolderBrowse()],
    [sg.Button('Package VSCode Env'), sg.Button('Setup VSCode Env'), sg.FileBrowse('Select Zip File', key='ZIP_FILE')]
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
        zip_file_path = values.get('ZIP_FILE')
        if zip_file_path and zip_file_path.endswith('.zip'):
            try:
                call_unpackage_script(zip_file_path)
                sg.popup('Unpackaging complete.')
            except subprocess.CalledProcessError as e:
                sg.popup(f'An error occurred: {e}', title='Error')
        else:
            sg.popup('Please select a valid VSCode environment zip file.', title='Error')

window.close()
