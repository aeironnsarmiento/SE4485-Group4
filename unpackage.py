import os
import shutil
import zipfile
import sys

def merge_dirs(src, dst, progress_callback, total_files, processed_files):
    """Merge contents of src into dst, overwriting or adding files as necessary."""
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            processed_files = merge_dirs(s, d, progress_callback, total_files, processed_files)
        else:
            shutil.move(s, d)
            processed_files += 1
            progress = int((processed_files / total_files) * 100)
            progress_callback(progress)
    return processed_files

def unpackage_vscode(zipname, progress_callback):
    appdata_path = os.getenv("APPDATA")
    userprofile_path = os.getenv("USERPROFILE")

    with zipfile.ZipFile(zipname, 'r') as zip_ref:
        zip_ref.extractall("vscode_temp")

    total_files = sum([len(files) for _, _, files in os.walk("vscode_temp")])
    processed_files = 0

    code_path = os.path.join("vscode_temp", "Code")
    vscode_path = os.path.join("vscode_temp", ".vscode")

    if os.path.exists(code_path):
        processed_files = merge_dirs(code_path, os.path.join(appdata_path, "Code"), progress_callback, total_files, processed_files)
    if os.path.exists(vscode_path):
        processed_files = merge_dirs(vscode_path, os.path.join(userprofile_path, ".vscode"), progress_callback, total_files, processed_files)

    shutil.rmtree("vscode_temp")
    progress_callback(100)  # Ensure completion is reported

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python unpackage.py <zipname>")
        sys.exit(1)
    
    zipname = sys.argv[1]
    unpackage_vscode(zipname, print)
