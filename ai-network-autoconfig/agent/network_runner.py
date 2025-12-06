from netmiko import ConnectHandler
import os # <-- We need this to access environment variables

# --- Helper function to securely inject credentials ---
def _inject_credentials(device):
    """Pulls username/password from environment variables (GitHub Secrets)"""
    device['username'] = os.environ.get('NET_USERNAME')
    device['password'] = os.environ.get('NET_PASSWORD')
    # If using Netmiko's secret/enable password, you'd add:
    # device['secret'] = os.environ.get('NET_SECRET') 

def get_running_config(device):
    _inject_credentials(device) # Securely add credentials
    conn = ConnectHandler(**device)
    # The 'show run' command is common across Cisco and Juniper, but often specific.
    # We will use 'show running-config' as defined in your prompt.
    output = conn.send_command("show running-config")
    conn.disconnect()
    return output

def apply_config(device, config):
    _inject_credentials(device) # Securely add credentials
    conn = ConnectHandler(**device)
    print(f"[+] Sending config to {device['name']}...")
    
    # Netmiko expects a list of configuration commands
    conn.send_config_set(config.splitlines()) 
    conn.save_config()
    conn.disconnect()
    print(f"[✓] Configuration applied and saved on {device['name']}.")