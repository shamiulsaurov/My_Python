import os
import subprocess
import getpass

def get_os_info():
    print("Select your OS:")
    print("1. Ubuntu")
    print("2. CentOS")
    print("3. Red Hat")
    os_choice = input("Enter the OS number: ")
    
    if os_choice == '1':
        os_name = 'Ubuntu'
    elif os_choice == '2':
        os_name = 'CentOS'
    elif os_choice == '3':
        os_name = 'Red Hat'
    else:
        print("Invalid option selected.")
        return None, None
    
    os_version = input(f"Enter the version of {os_name}: ")
    
    return os_name, os_version

def create_user(username):
    try:
        # Create the user
        subprocess.run(['sudo', 'useradd', '-m', '-s', '/bin/bash', username], check=True)
        print(f"User {username} created successfully.")
        
        # Set the default password to the same as the username
        password_cmd = f"echo '{username}:{username}' | sudo chpasswd"
        subprocess.run(password_cmd, shell=True, check=True)
        print(f"Password for {username} set to {username}.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating user {username}: {e}")

def create_directories_for_user(username, directories):
    home_directory = f"/home/{username}"

    for directory in directories:
        dir_path = os.path.join(home_directory, directory)
        try:
            # Create the directory
            os.makedirs(dir_path)
            print(f"Directory {dir_path} created successfully.")
            
            # Change ownership to the user
            subprocess.run(['sudo', 'chown', username + ':' + username, dir_path], check=True)
            print(f"Ownership of {dir_path} changed to {username}.")
            
            # Set specific permissions: 700 (rwx------) for the user
            os.chmod(dir_path, 0o700)
            print(f"Permissions set for {dir_path}.")
        except OSError as e:
            print(f"Error creating directory {dir_path}: {e}")

def execute_os_specific_commands(os_name, os_version):
    if os_name == 'Ubuntu':
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
    elif os_name == 'CentOS' or os_name == 'Red Hat':
        subprocess.run(['sudo', 'yum', 'update', '-y'], check=True)
    print(f"{os_name} {os_version} update command executed.")

def main():
    os_name, os_version = get_os_info()
    if not os_name or not os_version:
        return
    
    # Get usernames from the user as a comma-separated list
    usernames = input("Enter usernames (comma separated): ").split(',')
    
    # Trim any extra whitespace from the usernames
    usernames = [username.strip() for username in usernames]
    
    # Get directory names from user
    directories = input("Enter directory names (comma separated) to create in each user's home directory: ").split(',')
    
    # Trim any extra whitespace from directory names
    directories = [dir_name.strip() for dir_name in directories]
    
    for username in usernames:
        create_user(username)
        create_directories_for_user(username, directories)
    
    execute_os_specific_commands(os_name, os_version)

if __name__ == "__main__":
    if getpass.getuser() != 'root':
        print("This script must be run as root.")
    else:
        main()
