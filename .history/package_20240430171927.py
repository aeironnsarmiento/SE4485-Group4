"""
This file packages a VSCode environment from the user's machine into the current directory.
This will keep the user's extensions, settings, keybindings, and snippets and put them into a single zip file
This will be executed only on windows machines
"""
import os
import shutil
import sys

def main():

    print("Packaging VSCode environment...")

    # Copy the user's VSCode settings and extensions to the current directory
    shutil.copytree(os.path.join(os.getenv("APPDATA"), "Code"), "vscode/Code")

    # copy the user's .vscode directory to the current directory
    shutil.copytree(os.path.join(os.getenv("USERPROFILE"), ".vscode"), "vscode/.vscode")

    # Zip the copied directory
    if len(sys.argv) == 1:
        shutil.make_archive("vscode", "zip", "vscode")
    elif len(sys.argv) == 2:
        destination_path = sys.argv[1]
        shutil.make_archive(destination_path + "vscode", "zip", "vscode")
    else:
        print("Usage: python package.py [optional: destination_path]")
        sys.exit(1)

    # Remove the copied directory
    shutil.rmtree("vscode")

    print("Packaging complete.")


if __name__ == "__main__":
    main()
