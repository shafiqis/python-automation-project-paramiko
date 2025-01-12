import paramiko
import time

# Define router credentials
hostname = "192.168.96.11"  # IP of the router
username = "admin"
password = "admin"

def execute_command_on_router(hostname, username, password, command):
    try:
        # Initialize SSH client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the router
        print(f"Connecting to {hostname}...")
        ssh_client.connect(
            hostname=hostname,
            port=22,
            username=username,
            password=password,
            look_for_keys=False,
            allow_agent=False
        )
        print("Connected successfully!")

        # Open an interactive shell session
        device_access = ssh_client.invoke_shell()

        # Disable paging to get full output
        device_access.send("terminal length 0\n")
        time.sleep(1)

        # Execute the command
        device_access.send(f"{command}\n")
        time.sleep(2)  # Wait for the command to execute

        # Receive the output
        output = device_access.recv(65535).decode('utf-8')
        print("Command executed successfully!")
        return output

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        ssh_client.close()
        print("Connection closed.")

# Define the command to execute
command = "show config"

# Execute the command and print the output
output = execute_command_on_router(hostname, username, password, command)
if output:
    print("\n--- Command Output ---")
    print(output)