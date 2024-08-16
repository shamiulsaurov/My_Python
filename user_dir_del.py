import os
import subprocess
import getpass

def list_home_users():
    try:
        # List all users with home directories under /home
        home_users = []
        for user_dir in os.listdir('/home'):
            user_path = os.path.join('/home', user_dir)
            if os.path.isdir(user_path):
                # Check if the directory is owned by a user
                user_info = subprocess.check_output(['ls', '-ld', user_path]).decode().split()
                owner = user_info[2]
                if owner not in home_users:
                    home_users.append(owner)
        
        print("Existing users with home directories:")
        for user in home_users:
            print(user)
        return home_users
    except Exception as e:
        print(f"Error listing home users: {e}")
        return []

def delete_user(username):
    try:
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete user {username} and their home directory? (yes/no): ")
        if confirm.lower() == 'yes':
            # Delete the user and their home directory
            subprocess.run(['sudo', 'deluser', '--remove-home', username], check=True)
            print(f"User {username} and their home directory have been deleted.")
        else:
            print(f"Deletion of user {username} was cancelled.")
    except subprocess.CalledProcessError as e:
        print(f"Error deleting user {username}: {e}")

def main():
    # List existing home users
    existing_users = list_home_users()
    
    if existing_users:
        # Get usernames to delete from user input
        delete_usernames = input("Enter usernames (comma separated) to delete: ").split(',')
        delete_usernames = [username.strip() for username in delete_usernames]
        
        for username in delete_usernames:
            if username in existing_users:
                delete_user(username)
            else:
                print(f"User {username} does not exist or does not have a home directory.")
    else:
        print("No users with home directories available for deletion.")

if __name__ == "__main__":
    if getpass.getuser() != 'root':
        print("This script must be run as root.")
    else:
        main()
