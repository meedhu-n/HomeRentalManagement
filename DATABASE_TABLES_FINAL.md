# Database Tables - RentEase Project (Final)

## Complete Database Schema

This document provides the final overview of all database tables used in the RentEase Home Rental Management System.

---

## Total Tables: 10

### Core Tables:
1. User
2. Property
3. PropertyImage
4. Payment

### Application & Communication:
5. RentalApplication
6. Inquiry
7. Conversation
8. Message

### Engagement:
9. Review
10. Wishlist

---

## 1. User Table (Custom User Model)
**Purpose:** Manages all users (Admins, Owners, Tenants)

### Fields:
- id (PK)
- username (Unique)
- email (Unique)
- password
- first_name, last_name
- role (ADMIN/OWNER/TENANT)
- profile_image
- phone_number
- is_active, is_staff, is_superuser
- date_joined, last_login

---

## 2. Property Table
**Purpose:** Stores property listings with plan system

### Fields:
- id (PK)
- owner (FK → User)
- title, ad_title, description
- price, location, property_type
- bhk, bathrooms
- furnishing (UNFURNISHED/SEMI/FULLY)
- super_built_area
- bachelors_allowed
- total_floors, facing
- built_year, amenities
- status (PENDING/AVAILABLE/RENTED/MAINTENANCE)
- is_paid
- plan_type (basic/standard/premium)
- plan_expiry_date
- created_at, updated_at

### Methods:
- is_plan_active()
- days_remaining()

---

## 3. PropertyImage Table
**Purpose:** Multiple images per property

### Fields:
- id (PK)
- property (FK → Property)
- image

---

## 4. Payment Table
**Purpose:** Razorpay payment tracking

### Fields:
- id (PK)
- property (OneToOne → Property)
- owner (FK → User)
- razorpay_order_id (Unique)
- razorpay_payment_id
- razorpay_signature
- amount
- status (PENDING/SUCCESS/FAILED)
- created_at, updated_at

---

## 5. RentalApplication Table
**Purpose:** Tenant applications for properties

### Fields:
- id (PK)
- tenant (FK → User)
- property (FK → Property)
- application_date
- status (PENDING/APPROVED/REJECTED)
- message

---

## 6. Inquiry Table
**Purpose:** Property inquiries from tenants

### Fields:
- id (PK)
- property (FK → Property)
- tenant (FK → User)
- message
- created_at

---

## 7. Conversation Table
**Purpose:** Messaging between tenants and owners

### Fields:
- id (PK)
- property (FK → Property)
- tenant (FK → User)
- owner (FK → User)
- created_at, updated_at

### Constraints:
- Unique: (property, tenant, owner)

---

## 8. Message Table
**Purpose:** Individual messages in conversations

### Fields:
- id (PK)
- conversation (FK → Conversation)
- sender (FK → User)
- content
- is_read
- created_at

---

## 9. Review Table
**Purpose:** Property ratings and reviews

### Fields:
- id (PK)
- property (FK → Property)
- reviewer (FK → User)
- rating (1-5)
- comment
- created_at, updated_at

### Constraints:
- Unique: (property, reviewer)

---

## 10. Wishlist Table
**Purpose:** Tenant's favorite properties

### Fields:
- id (PK)
- tenant (FK → User)
- property (FK → Property)
- created_at

### Constraints:
- Unique: (tenant, property)

---

## Removed Tables:
- ❌ Lease (Not needed)
- ❌ MaintenanceRequest (Not needed)

---

## Key Relationships:

### User (1:N):
- Properties (as owner)
- Payments
- RentalApplications (as tenant)
- Inquiries (as tenant)
- Conversations (as tenant/owner)
- Messages (as sender)
- Reviews (as reviewer)
- Wishlist items (as tenant)

### Property (1:N):
- PropertyImages
- RentalApplications
- Inquiries
- Conversations
- Reviews
- Wishlist entries

### Property (1:1):
- Payment

### Conversation (1:N):
- Messages

---

## Plan System:

### Basic Plan (₹99):
- 1 property
- 90 days visibility
- Standard priority

### Standard Plan (₹199):
- 3 properties
- 180 days visibility
- Priority badge

### Premium Plan (₹399):
- 10 properties
- 365 days visibility
- Featured badge
- Top priority
- Home page display

---

## Features Supported:

✅ User Management (3 roles)
✅ Property Listings with Images
✅ Payment Integration (Razorpay)
✅ Plan-based Subscriptions
✅ Tenant Applications
✅ Messaging System
✅ Reviews & Ratings
✅ Wishlist/Favorites
✅ Property Inquiries

❌ Lease Agreements (Removed)
❌ Maintenance Requests (Removed)

---

## Database Statistics:
- Total Tables: 10
- Total Relationships: 20+
- User Roles: 3
- Property Statuses: 4
- Payment Statuses: 3
- Plan Types: 3
- Rating Scale: 1-5 stars
