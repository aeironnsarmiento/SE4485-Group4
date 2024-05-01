import PySimpleGUI as sg
import subprocess
import threading
import os

def call_script(script, arguments, window):
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script)
    try:
        process = subprocess.Popen(['python', script_path] + arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Dummy progress updates
        for i in range(100):
            sg.time.sleep(0.1)  # simulate some work being done
            window.write_event_value('-UPDATE PROGRESS-', i+1)
        if process.wait() == 0:
            window.write_event_value('-COMPLETE-', f'{script} completed successfully.')
        else:
            window.write_event_value('-ERROR-', f'An error occurred: {process.stderr.read()}')
    except Exception as e:
        window.write_event_value('-ERROR-', f'An error occurred: {str(e)}')

layout = [
    [sg.Text('VSCode Environment Transfer Tool', size=(30, 1), justification='center', font=("Helvetica", 25))],
    [sg.Text('Destination Directory for ZIP:'), sg.InputText('', key='DESTINATION'), sg.FolderBrowse()],
    [sg.Button('Package VSCode Env'), sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS-', visible=False)],
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
            window['-PROGRESS-'].update(current_count=0, visible=True)
            threading.Thread(target=call_script, args=('package.py', [values['DESTINATION']], window), daemon=True).start()
        else:
            sg.popup('Please select a destination for the ZIP file.', title='Error')
    elif event == 'Setup VSCode Env':
        if values['ZIP_FILE']:
            window['-PROGRESS-'].update(current_count=0, visible=True)
            threading.Thread(target=call_script, args=('unpackage.py', [values['ZIP_FILE']], window), daemon=True).start()
        else:
            sg.popup('Please select a ZIP file to unpackage.', title='Error')
    elif event == '-UPDATE PROGRESS-':
        window['-PROGRESS-'].update(values[event])  # Update progress bar based on the event value
    elif event == '-COMPLETE-':
        sg.popup(values[event])
        window['-PROGRESS-'].update(visible=False)
    elif event == '-ERROR-':
        sg.popup(values[event], title='Error')
        window['-PROGRESS-'].update(visible=False)

window.close()
