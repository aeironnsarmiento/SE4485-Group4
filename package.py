import os
import zipfile
import sys

def zipdir(path, ziph, progress_callback):
    total_files = sum([len(files) for r, d, files in os.walk(path)])
    processed_files = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if 'cache' not in file.lower() and 'tmp' not in file.lower():
                ziph.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file),
                           os.path.join(path, '..')))
                processed_files += 1
                progress_callback(processed_files / total_files * 100)
    progress_callback(100)

def package_vscode(destination, progress_callback):
    appdata_code_path = os.path.join(os.getenv('APPDATA'), 'Code')
    userprofile_vscode_path = os.path.join(os.getenv('USERPROFILE'), '.vscode')
    zip_filename = os.path.join(destination, 'vscode_backup.zip')

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(appdata_code_path, zipf, progress_callback)
        zipdir(userprofile_vscode_path, zipf, progress_callback)

    print(f'Packaging complete. Archive created at: {zip_filename}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python package.py <destination>")
        sys.exit(1)
    destination_path = sys.argv[1]
    package_vscode(destination_path, print)
