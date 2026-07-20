#!/usr/bin/env bash
# MediBridge — one-shot local setup (Phase 6: Deployment - Local)
set -e
cd "$(dirname "$0")"

echo "== 1/6 Creating virtual environment =="
python3 -m venv venv
source venv/bin/activate

echo "== 2/6 Installing dependencies =="
pip install --upgrade pip
pip install -r requirements.txt

echo "== 3/6 Setting up .env =="
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from .env.example — edit it if needed."
fi

echo "== 4/6 Running migrations =="
python manage.py makemigrations
python manage.py migrate

echo "== 5/6 Seeding demo data =="
python manage.py seed_demo_data

echo "== 6/6 Ready =="
echo "Create an admin superuser with: python manage.py createsuperuser"
echo "Then start the server with:      python manage.py runserver"
echo "Visit http://127.0.0.1:8000/"
