import subprocess
import getpass

def list_users():
    try:
        # List all users (excluding system users)
        users = subprocess.check_output(['cut', '-d:', '-f1', '/etc/passwd']).decode().split('\n')
        # Filter out system users and print normal users
        normal_users = [user for user in users if not user.startswith('_') and user not in ('root', 'nobody', 'daemon')]
        print("Existing users:")
        for user in normal_users:
            print(user)
        return normal_users
    except subprocess.CalledProcessError as e:
        print(f"Error listing users: {e}")
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
    # List existing users
    existing_users = list_users()
    
    if existing_users:
        # Get usernames to delete from user input
        delete_usernames = input("Enter usernames (comma separated) to delete: ").split(',')
        delete_usernames = [username.strip() for username in delete_usernames]
        
        for username in delete_usernames:
            if username in existing_users:
                delete_user(username)
            else:
                print(f"User {username} does not exist.")
    else:
        print("No users available for deletion.")

if __name__ == "__main__":
    if getpass.getuser() != 'root':
        print("This script must be run as root.")
    else:
        main()
