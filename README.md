# Chandauli Samachar

Hindi local-news website built with Django.

## Setup

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Create the MySQL database and user matching `.env` before migration. For a quick local SQLite run, set `DB_ENGINE=sqlite`.
