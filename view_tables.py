"""
Script to view all database tables in RentEase project
Run: python view_tables.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def show_all_tables():
    """Display all tables in the database"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("\n" + "="*60)
        print("DATABASE TABLES IN RENTEASE PROJECT")
        print("="*60 + "\n")
        
        core_tables = []
        django_tables = []
        
        for table in tables:
            table_name = table[0]
            if table_name.startswith('core_'):
                core_tables.append(table_name)
            else:
                django_tables.append(table_name)
        
        print("CORE APPLICATION TABLES:")
        print("-" * 60)
        for i, table in enumerate(sorted(core_tables), 1):
            print(f"{i}. {table}")
        
        print(f"\nTotal Core Tables: {len(core_tables)}")
        
        print("\n" + "="*60)
        print("DJANGO SYSTEM TABLES:")
        print("-" * 60)
        for i, table in enumerate(sorted(django_tables), 1):
            print(f"{i}. {table}")
        
        print(f"\nTotal Django Tables: {len(django_tables)}")
        print(f"\nGRAND TOTAL: {len(tables)} tables")
        print("="*60 + "\n")

def show_table_structure(table_name):
    """Show structure of a specific table"""
    with connection.cursor() as cursor:
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        print(f"\n{'='*80}")
        print(f"TABLE: {table_name}")
        print('='*80)
        print(f"{'Column Name':<30} {'Type':<15} {'Null':<8} {'Key':<8}")
        print('-'*80)
        
        for col in columns:
            col_id, name, col_type, not_null, default, pk = col
            null_str = "NO" if not_null else "YES"
            key_str = "PK" if pk else ""
            print(f"{name:<30} {col_type:<15} {null_str:<8} {key_str:<8}")
        
        print('='*80 + "\n")

def count_records():
    """Count records in each core table"""
    from core.models import (
        User, Property, PropertyImage, Payment, 
        Conversation, Message, Wishlist, WebsiteFeedback
    )
    
    print("\n" + "="*60)
    print("RECORD COUNTS")
    print("="*60 + "\n")
    
    counts = {
        'Users': User.objects.count(),
        'Properties': Property.objects.count(),
        'Property Images': PropertyImage.objects.count(),
        'Payments': Payment.objects.count(),
        'Conversations': Conversation.objects.count(),
        'Messages': Message.objects.count(),
        'Wishlist Items': Wishlist.objects.count(),
        'Website Feedbacks': WebsiteFeedback.objects.count(),
    }
    
    for table, count in counts.items():
        print(f"{table:<25} : {count:>5} records")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    # Show all tables
    show_all_tables()
    
    # Show structure of core tables
    print("\nDETAILED TABLE STRUCTURES:")
    print("="*80)
    
    core_tables = [
        'core_user',
        'core_property',
        'core_propertyimage',
        'core_payment',
        'core_conversation',
        'core_message',
        'core_wishlist',
        'core_websitefeedback'
    ]
    
    for table in core_tables:
        show_table_structure(table)
    
    # Count records
    count_records()
