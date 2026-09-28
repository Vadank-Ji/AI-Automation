# AIIAU

Ansible project for deploying and checking an AI service configuration.

## Requirements

- Ansible
- Python 3
- Python packages: `PyYAML` and `requests`

For model discovery, set `OPENAI_API_KEY` in `scripts/.env` or in the shell environment. The local `.env` file is ignored by Git and must not be committed.

## Layout

- `config/` - service configuration and approved model backups
- `inventory/` - Ansible inventory
- `playbooks/` - deployment playbooks
- `scripts/` - health, model, and service checks

## Run

```bash
ansible-playbook -i inventory/hosts.ini playbooks/deploy.yml
python3 scripts/model_checker.py
python3 scripts/health_check.py
```