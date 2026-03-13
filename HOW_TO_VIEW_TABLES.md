# How to View Database Tables in RentEase

## Quick Methods to View Tables

### Method 1: Using Python Script (Easiest)
```bash
python view_tables.py
```
This will show:
- All table names
- Table structures
- Record counts

---

### Method 2: Django Shell
```bash
python manage.py shell
```

Then run:
```python
from django.db import connection

# Show all tables
with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        print(table[0])
```

---

### Method 3: Django dbshell (SQLite Command Line)
```bash
python manage.py dbshell
```

Then run these SQLite commands:
```sql
-- List all tables
.tables

-- Show table structure
.schema core_user
.schema core_property

-- Count records
SELECT COUNT(*) FROM core_user;
SELECT COUNT(*) FROM core_property;

-- View data
SELECT * FROM core_user LIMIT 5;

-- Exit
.quit
```

---

### Method 4: Using Django Admin
1. Start server: `python manage.py runserver`
2. Go to: `http://127.0.0.1:8000/admin/`
3. Login with superuser credentials
4. You'll see all models/tables listed

---

### Method 5: Django Models Inspection
```bash
python manage.py shell
```

```python
from django.apps import apps

# Get all models
for model in apps.get_app_config('core').get_models():
    print(f"{model.__name__}: {model._meta.db_table}")
    print(f"  Fields: {[f.name for f in model._meta.fields]}")
    print()
```

---

### Method 6: View Migrations
```bash
# See all migrations
python manage.py showmigrations

# See SQL for a specific migration
python manage.py sqlmigrate core 0001
```

---

## Common SQLite Commands

### In dbshell:
```sql
-- List all tables
.tables

-- Show table structure with details
PRAGMA table_info(core_user);

-- Show all columns
.schema core_property

-- Count records in each table
SELECT 
    'core_user' as table_name, 
    COUNT(*) as count 
FROM core_user
UNION ALL
SELECT 'core_property', COUNT(*) FROM core_property
UNION ALL
SELECT 'core_message', COUNT(*) FROM core_message;

-- Show recent messages
SELECT * FROM core_message ORDER BY created_at DESC LIMIT 10;

-- Show properties with owner names
SELECT 
    p.title, 
    p.price, 
    u.username as owner 
FROM core_property p 
JOIN core_user u ON p.owner_id = u.id 
LIMIT 10;
```

---

## Using DB Browser for SQLite (GUI Tool)

### Download:
https://sqlitebrowser.org/

### Steps:
1. Download and install DB Browser for SQLite
2. Open the tool
3. Click "Open Database"
4. Navigate to your project folder
5. Select `db.sqlite3`
6. You'll see all tables in a visual interface

**Features:**
- Browse data in tables
- Execute SQL queries
- View table structures
- Export data
- Modify records

---

## Python Script to Export Table Info

Create `export_tables.py`:
```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.apps import apps

print("# RentEase Database Tables\n")

for model in apps.get_app_config('core').get_models():
    print(f"## {model.__name__}")
    print(f"Table: {model._meta.db_table}\n")
    print("| Field | Type | Description |")
    print("|-------|------|-------------|")
    
    for field in model._meta.fields:
        field_type = field.get_internal_type()
        print(f"| {field.name} | {field_type} | {field.help_text or '-'} |")
    
    print("\n")
```

Run: `python export_tables.py > tables_export.md`

---

## Quick Commands Summary

```bash
# View all tables (Python script)
python view_tables.py

# Django shell
python manage.py shell

# SQLite shell
python manage.py dbshell

# Show migrations
python manage.py showmigrations

# Create superuser (to access admin)
python manage.py createsuperuser

# Run server and view in admin
python manage.py runserver
# Then go to: http://127.0.0.1:8000/admin/
```

---

## Troubleshooting

### Can't find db.sqlite3?
```bash
# Check if database exists
dir db.sqlite3  # Windows
ls -la db.sqlite3  # Linux/Mac

# If not exists, run migrations
python manage.py migrate
```

### Permission denied?
```bash
# Check file permissions
icacls db.sqlite3  # Windows
ls -l db.sqlite3  # Linux/Mac
```

### Database locked?
- Close any open connections
- Stop the Django server
- Close DB Browser if open
- Try again

---

## Expected Core Tables

You should see these 9 core tables:
1. ✅ core_user
2. ✅ core_property
3. ✅ core_propertyimage
4. ✅ core_payment
5. ✅ core_conversation
6. ✅ core_message
7. ✅ core_review
8. ✅ core_wishlist
9. ✅ core_websitefeedback

Plus Django system tables:
- django_migrations
- django_session
- django_admin_log
- django_content_type
- auth_permission
- auth_group
- etc.

---

**Recommended**: Use `python view_tables.py` for the quickest overview!
