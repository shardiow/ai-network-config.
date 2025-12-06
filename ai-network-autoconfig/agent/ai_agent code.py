import yaml
import os
from git import Repo
from network_runner import get_running_config, apply_config
 
REPO_PATH = "."
 
def main():
    print("[AI AGENT] Starting network automation engine...")
 
    # Read network credentials from secure GitHub Secrets (environment variables)
    NET_USER = os.environ.get("NET_USER")
    NET_PASS = os.environ.get("NET_PASS")
 
    # 1. Pull the latest desired state from the repository
    repo = Repo(REPO_PATH)
    repo.remotes.origin.pull() 
 
    with open("inventory/devices.yml") as f:
        inventory = yaml.safe_load(f)
 
    for device_data in inventory["devices"]:
        device_name = device_data["name"]
        
        # Merge secure credentials into the device data dictionary
        device = {
            **device_data,
            "username": NET_USER,
            "password": NET_PASS,
        }
 
        desired_file = f"desired-configs/{device_name}.cfg"
        
        # ... (Config file check logic remains the same) ...
        try:
            with open(desired_file) as f:
                desired_config = f.read()
        except FileNotFoundError:
            print(f"[!] No desired config for {device_name}. Skipping.")
            continue
 
        print(f"\n[+] Checking device: {device_name}")
 
        # 2. Compare running config to desired config
        running_config = get_running_config(device)
 
        if running_config.strip() != desired_config.strip():
            print(f"[!] Config drift detected on {device_name}")
            print(f"[+] Applying new configuration...")
            apply_config(device, desired_config)
        else:
            print(f"[✓] {device_name} is up-to-date.")
 
    # 3. CRITICAL: Remove all repo.git.add, repo.index.commit, and repo.remotes.origin.push() lines!
    # The push trigger is handled by the human merging a PR into 'main'.
    
    print("\n[✓] Deployment complete.")
 
if __name__ == "__main__":
    main()