#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3.11+ is required." >&2
  exit 1
fi

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if [ ! -f .env ]; then
  SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"
  cat > .env <<ENV
SECRET_KEY=$SECRET_KEY
DATABASE_URL=sqlite:///acc_portal.db
SESSION_COOKIE_SECURE=0
ENV
fi

python -m flask --app run.py init-db
python seed_scholarships.py

echo
echo "Setup complete."
echo "Create an admin: .venv/bin/python -m flask --app run.py create-admin"
echo "Start the app:    .venv/bin/python run.py"
echo "Open:             http://127.0.0.1:5000"
