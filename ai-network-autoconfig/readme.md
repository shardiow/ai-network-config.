# AI Network Auto-Config Agent

This project automatically:
✔ Pulls desired configs from GitHub  
✔ Compares them to real network devices  
✔ Detects configuration drift  
✔ Pushes new configs automatically  

---

## How it Works

1. Edit or upload a config file in `desired-configs/`
2. Commit/push to GitHub
3. GitHub Actions triggers `ai_agent.py`
4. Agent connects to real network devices
5. Drift is corrected automatically

---

## Requirements

- Python 3.9+
- Network devices accessible via SSH
- Netmiko compatible devices
- OpenAI API key (if using AI generation)

---

## Commands

Run locally:
