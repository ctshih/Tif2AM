import subprocess
import os
import sys
import ast

def _run_tkinter_script(script):
    """
    Runs a small python script in a subprocess to execute Tkinter commands safely.
    """
    # Use config-friendly python command
    cmd = [sys.executable, "-c", script]
    try:
        # Run subprocess and capture stdout
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        # Parse output safely
        if output:
             return output
    except subprocess.CalledProcessError as e:
        print(f"Dialog Error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return None
    return None

def get_open_filenames(initial_dir="."):
    """
    Opens a file selection dialog for Tif files.
    Returns a list of selected file paths (strings).
    """
    # Python script to run in subprocess
    # We use 'root.attributes("-topmost", True)' to ensure it pops up over browser
    script = f"""
import tkinter as tk
from tkinter import filedialog
import os

root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)

# Force focus
root.lift()
root.focus_force()

file_paths = filedialog.askopenfilenames(
    title="Select 2D Tif files to stack",
    filetypes=[("TIFF Files", "*.tif *.tiff")],
    initialdir=r"{initial_dir}"
)

# Tkinter returns a tuple of strings. Print it as a list representation for easy parsing.
print(list(file_paths))

root.destroy()
"""
    output = _run_tkinter_script(script)
    if output:
        try:
            # Safely evaluate string representation of list -> list
            return ast.literal_eval(output)
        except:
            return []
    return []

def get_save_filename(initial_dir=".", default_name="output-3d-ascii.am"):
    """
    Opens a save file dialog.
    Returns the selected file path (string).
    """
    script = f"""
import tkinter as tk
from tkinter import filedialog
import os

root = tk.Tk()
root.withdraw()
root.attributes("-topmost", True)

root.lift()
root.focus_force()

save_path = filedialog.asksaveasfilename(
    title="Save AmiraMesh File",
    defaultextension=".am",
    filetypes=[("AmiraMesh Files", "*.am")],
    initialdir=r"{initial_dir}",
    initialfile=r"{default_name}"
)

print(save_path)

root.destroy()
"""
    output = _run_tkinter_script(script)
    return output if output and output != "''" and output != '""' else None
