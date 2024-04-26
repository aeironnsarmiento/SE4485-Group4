import os
import shutil
import sys

def merge_dirs(src, dst):
    """Merge two directories."""
    if not os.path.exists(dst):
        shutil.move(src, dst)
    else:
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                merge_dirs(s, d)
            else:
                shutil.move(s, d)

def unpackage_vscode_environment(zipname):
    appdata_path = os.getenv("APPDATA")
    userprofile_path = os.getenv("USERPROFILE")

    if not appdata_path or not userprofile_path:
        print("Error: Environment variables APPDATA or USERPROFILE not found.")
        return
    
    # Prepare target directories
    code_dir = os.path.join(appdata_path, "Code")
    vscode_dir = os.path.join(userprofile_path, ".vscode")

    # Extract zip to a temporary directory
    temp_dir = "vscode_temp"
    shutil.unpack_archive(zipname, temp_dir)

    # Merge directories
    merge_dirs(os.path.join(temp_dir, "vscode", "Code"), code_dir)
    merge_dirs(os.path.join(temp_dir, "vscode", ".vscode"), vscode_dir)

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)

    print("VS Code environment has been successfully restored.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python unpackage.py <zipname>")
        sys.exit(1)
    
    zipname = sys.argv[1]
    unpackage_vscode_environment(zipname)
