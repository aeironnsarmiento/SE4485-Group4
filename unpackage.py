import zipfile
import os
import shutil
import sys

def extract_zip(zipname, extract_to_directory):
    """Extract a zip file to the specified directory."""
    try:
        with zipfile.ZipFile(zipname, 'r') as zip_ref:
            zip_ref.extractall(extract_to_directory)
        print(f"Successfully extracted '{zipname}' to '{extract_to_directory}'.")
    except Exception as e:
        print(f"Error unpacking: {e}. Please check the zip file and try again.")

def unpackage_vscode_environment(zipname):
    appdata_path = os.getenv("APPDATA")
    userprofile_path = os.getenv("USERPROFILE")

    if not appdata_path or not userprofile_path:
        print("Error: Environment variables APPDATA or USERPROFILE not found.")
        sys.exit(1)
    
    # Directories where VS Code settings and extensions will be restored
    code_dir = os.path.join(appdata_path, "Code")
    vscode_dir = os.path.join(userprofile_path, ".vscode")

    # Extract the zip to a temporary directory
    temp_dir = "vscode_temp"
    extract_zip(zipname, temp_dir)

    # Move the directories to their correct locations
    shutil.move(os.path.join(temp_dir, "vscode", "Code"), code_dir)
    shutil.move(os.path.join(temp_dir, "vscode", ".vscode"), vscode_dir)

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)

    print("VS Code environment has been successfully restored.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python unpackage.py <zipname>")
        sys.exit(1)
    
    zipname = sys.argv[1]
    unpackage_vscode_environment(zipname)
