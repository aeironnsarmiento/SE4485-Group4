import PySimpleGUI as sg
import subprocess

def call_script(script, arguments):
    try:
        subprocess.run(['python', script] + arguments, check=True)
        sg.popup(f'{script} completed successfully.')
    except subprocess.CalledProcessError as e:
        sg.popup(f'An error occurred: {e}', title='Error')

layout = [
    [sg.Text('VSCode Environment Transfer Tool', size=(30, 1), justification='center', font=("Helvetica", 25))],
    [sg.Text('Destination Directory for ZIP:'), sg.InputText('', key='DESTINATION'), sg.FolderBrowse()],
    [sg.Button('Package VSCode Env')],
    [sg.Text('Select ZIP File for Setup:'), sg.InputText('', key='ZIP_FILE'), sg.FileBrowse(file_types=(("Zip Files", "*.zip"),))],
    [sg.Button('Setup VSCode Env')]
]

window = sg.Window('VSCode Env Tool', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Package VSCode Env':
        if values['DESTINATION']:
            call_script('package.py', [values['DESTINATION']])
        else:
            sg.popup('Please select a destination for the ZIP file.', title='Error')
    elif event == 'Setup VSCode Env':
        if values['ZIP_FILE']:
            call_script('unpackage.py', [values['ZIP_FILE']])
        else:
            sg.popup('Please select a ZIP file to unpackage.', title='Error')

window.close()
