"""
This file packages a VSCode environment from the user's machine into the current directory.
This will keep the user's extensions, settings, keybindings, and snippets and put them into a single zip file
This will be executed only on windows machines
"""
print("Packaging VSCode environment...")
import os
import shutil

# Copy the user's VSCode settings and extensions to the current directory
shutil.copytree(os.path.join(os.getenv("APPDATA"), "Code"), "vscode/Code")

# copy the user's .vscode directory to the current directory
shutil.copytree(os.path.join(os.getenv("USERPROFILE"), ".vscode"), "vscode/.vscode")

# Zip the copied directory
shutil.make_archive("vscode", "zip", "vscode")

# Remove the copied directory
shutil.rmtree("vscode")

print("Packaging complete.")

