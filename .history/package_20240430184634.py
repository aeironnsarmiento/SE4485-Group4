import sys
import os
import shutil

def package_vscode(destination):
    # Assuming 'Code' and '.vscode' directories are in specific paths
    appdata_code_path = os.path.join(os.getenv('APPDATA'), 'Code')
    userprofile_vscode_path = os.path.join(os.getenv('USERPROFILE'), '.vscode')
    temp_dir = 'vscode_backup'

    os.makedirs(temp_dir, exist_ok=True)
    shutil.copytree(appdata_code_path, os.path.join(temp_dir, 'Code'), dirs_exist_ok=True)
    shutil.copytree(userprofile_vscode_path, os.path.join(temp_dir, '.vscode'), dirs_exist_ok=True)
    archive_path = shutil.make_archive(os.path.join(destination, 'vscode_backup'), 'zip', temp_dir)
    shutil.rmtree(temp_dir)
    print(f'Packaging complete. Archive created at: {archive_path}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python package.py <destination>")
        sys.exit(1)
    destination_path = sys.argv[1]
    package_vscode(destination_path)
