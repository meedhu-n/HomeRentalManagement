# RentEase Database Tables

This document lists all the database tables used in the RentEase project.

## Core Application Tables (8 tables)

### 1. core_user
- **Purpose**: Stores user accounts (Owners, Tenants, Admins)
- **Key Fields**: username, email, role, phone_number, profile_image
- **Relationships**: One-to-Many with Properties, Conversations, Messages, Wishlist, WebsiteFeedback

### 2. core_property
- **Purpose**: Stores property listings
- **Key Fields**: title, description, location, price, property_type, bhk, status, owner_id, plan_type, plan_expiry_date, views_count
- **Relationships**: 
  - Foreign Key to User (owner)
  - One-to-Many with PropertyImage, Conversation
- **Status Options**: PENDING_APPROVAL, AVAILABLE, RENTED, MAINTENANCE

### 3. core_propertyimage
- **Purpose**: Stores multiple images for each property
- **Key Fields**: property_id, image
- **Relationships**: Foreign Key to Property

### 4. core_payment
- **Purpose**: Tracks Razorpay payments for property listing plans
- **Key Fields**: property_id, owner_id, amount, razorpay_order_id, razorpay_payment_id, status
- **Relationships**: Foreign Keys to Property and User
- **Status Options**: PENDING, SUCCESS, FAILED

### 5. core_conversation
- **Purpose**: Manages messaging threads between tenants and property owners
- **Key Fields**: property_id, tenant_id, owner_id, created_at, updated_at
- **Relationships**: 
  - Foreign Keys to Property, User (tenant), User (owner)
  - One-to-Many with Message

### 6. core_message
- **Purpose**: Stores individual messages within conversations
- **Key Fields**: conversation_id, sender_id, content, is_read, created_at
- **Relationships**: Foreign Keys to Conversation and User (sender)

### 7. core_wishlist
- **Purpose**: Stores tenant's saved/favorite properties
- **Key Fields**: tenant_id, property_id, created_at
- **Relationships**: Foreign Keys to User (tenant) and Property

### 8. core_websitefeedback
- **Purpose**: Stores user feedback about the RentEase platform
- **Key Fields**: user_id, rating, title, comment, is_featured, is_approved, created_at
- **Relationships**: Foreign Key to User

## Removed Models (Successfully Deleted)

The following models have been removed from the database:

- **RentalApplication** ✅ Removed (no formal application system)
- **Inquiry** ✅ Removed (replaced by Conversation/Message system)
- **Review** ✅ Removed (property reviews not needed)

## Database Schema Summary

```
Total Core Tables: 8
Total Relationships: 15+ foreign key relationships
Primary Features:
  - User Management (Owners, Tenants, Admins)
  - Property Listings with Images
  - Payment Processing (Razorpay)
  - Messaging System (Conversations & Messages)
  - Wishlist Feature
  - Website Feedback System
  - Property View Tracking
```

## Current Database Status

```
Users                     :     3 records
Properties                :     2 records
Property Images           :     5 records
Payments                  :     2 records
Conversations             :     2 records
Messages                  :     1 records
Wishlist Items            :     0 records
Website Feedbacks         :     1 records
```

## How to View Tables

Run the following command to see all tables and their structures:

```bash
python view_tables.py
```

Or use Django shell:

```bash
python manage.py dbshell
.tables
.schema core_user
```

## Migration History

Latest migration: `0014_remove_rentalapplication_property_and_more.py`
- Removed RentalApplication model
- Removed Inquiry model
- Removed Review model

To view migration status:
```bash
python manage.py showmigrations
```

---

**Last Updated**: March 13, 2026
**Database**: SQLite3 (Development)
**ORM**: Django 5.2.10
**Focus**: Simple property listing and messaging platform
