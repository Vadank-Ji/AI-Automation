# AIIAU

Ansible project for deploying and checking an AI service configuration.

## Requirements

- Ansible
- Python 3
- Python packages: `groq`, `python-dotenv`, `PyYAML`, and `requests`

Install Python dependencies with:

```bash
python3 -m pip install -r requirements.txt
```

Set `GROQ_API_KEY` in `scripts/.env`. The local `.env` file is ignored by Git and must not be committed.

## Layout

- `config/` - service configuration and approved model backups
- `inventory/` - Ansible inventory
- `playbooks/` - deployment playbooks
- `scripts/` - health, model, and service checks

## Run

```bash
ansible-playbook -i inventory/hosts.ini playbooks/deploy.yml
python3 scripts/ai_service.py
python3 scripts/ai_service.py --health
scripts/restart_service.sh
```

`--health` sends a real request to the model in `config/app_config.yml` and
returns exit code `0` only when Groq responds successfully. The deployment
playbook uses that check after an applicable model update; on failure it
restores the backed-up configuration, restarts the service, and verifies the
previous model before failing the deployment. The restart helper runs the
service's periodic health monitor in the background and records output in
`logs/ai_service.log`.
