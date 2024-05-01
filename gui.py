import PySimpleGUI as sg
import threading
from package import package_vscode
from unpackage import unpackage_vscode

def threaded_function(func, arg, window, progress_key, message):
    def progress_callback(progress):
        window.write_event_value('-UPDATE PROGRESS-', (progress_key, progress))

    try:
        func(arg, progress_callback)
        window.write_event_value('-SUCCESS-', f'{message} completed successfully.')
    except Exception as e:
        window.write_event_value('-ERROR-', str(e))
    finally:
        window[progress_key].update(visible=False)

layout = [
    [sg.Text('VSCode Environment Transfer Tool', size=(30, 1), justification='center', font=("Helvetica", 25))],
    [sg.Text('Destination Directory for ZIP:'), sg.InputText('', key='DESTINATION'), sg.FolderBrowse()],
    [sg.Button('Package VSCode Env')],
    [sg.Text('Select ZIP File for Setup:'), sg.InputText('', key='ZIP_FILE'), sg.FileBrowse(file_types=(("Zip Files", "*.zip"),))],
    [sg.Button('Setup VSCode Env')],
    [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS-', visible=False)]  # Progress bar at the bottom
]

window = sg.Window('VSCode Env Tool', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Package VSCode Env':
        if values['DESTINATION']:
            window['-PROGRESS-'].update(current_count=0, visible=True)
            threading.Thread(target=threaded_function, args=(package_vscode, values['DESTINATION'], window, '-PROGRESS-', 'Packaging'), daemon=True).start()
        else:
            sg.popup('Please select a destination for the ZIP file.', title='Error')
    elif event == 'Setup VSCode Env':
        if values['ZIP_FILE']:
            window['-PROGRESS-'].update(current_count=0, visible=True)
            threading.Thread(target=threaded_function, args=(unpackage_vscode, values['ZIP_FILE'], window, '-PROGRESS-', 'Unpackaging'), daemon=True).start()
        else:
            sg.popup('Please select a ZIP file to unpackage.', title='Error')
    elif event == '-UPDATE PROGRESS-':
        key, progress = values[event]
        window[key].update(progress)
    elif event == '-SUCCESS-':
        sg.popup(values[event])
        window['-PROGRESS-'].update(visible=False)
    elif event == '-ERROR-':
        sg.popup(values[event], title='Error')
        window['-PROGRESS-'].update(visible=False)

window.close()
