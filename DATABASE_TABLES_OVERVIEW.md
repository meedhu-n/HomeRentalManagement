# Database Tables Overview - RentEase Project

## Complete Database Schema

This document provides a comprehensive overview of all database tables (Django models) used in the RentEase Home Rental Management System.

---

## 1. User Table (Custom User Model)
**Model Name:** `User`  
**Extends:** Django's AbstractUser  
**Purpose:** Manages all users in the system (Admins, Owners, Tenants)

### Fields:
| Field Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| id | AutoField | Primary Key | Auto-generated |
| username | CharField | Username for login | Unique, Required |
| email | EmailField | User's email address | Unique, Required |
| password | CharField | Hashed password | Required |
| first_name | CharField | First name | Optional |
| last_name | CharField | Last name | Optional |
| role | CharField | User role (ADMIN/OWNER/TENANT) | Default: TENANT |
| profile_image | ImageField | Profile picture | Optional, Upload to 'profiles/' |
| phone_number | CharField | Contact number | Optional, Max 15 chars |
| is_active | BooleanField | Account active status | Default: True |
| is_staff | BooleanField | Staff status | Default: False |
| is_superuser | BooleanField | Superuser status | Default: False |
| date_joined | DateTimeField | Registration date | Auto-generated |
| last_login | DateTimeField | Last login timestamp | Auto-updated |

### Relationships:
- One-to-Many with Property (as owner)
- One-to-Many with Payment
- One-to-Many with RentalApplication
- One-to-Many with Lease
- One-to-Many with MaintenanceRequest
- One-to-Many with Inquiry
- One-to-Many with Conversation (as tenant/owner)
- One-to-Many with Message
- One-to-Many with Review
- One-to-Many with Wishlist

---

## 2. Property Table
**Model Name:** `Property`  
**Purpose:** Stores all property listings

### Fields:
| Field Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| id | AutoField | Primary Key | Auto-generated |
| owner | ForeignKey | Property owner | Links to User |
| title | CharField | Property title | Max 255 chars |
| ad_title | CharField | Short ad title | Optional, Max 255 chars |
| description | TextField | Detailed description | Required |
| price | DecimalField | Monthly rent | Max 10 digits, 2 decimals |
| location | CharField | Property location | Max 255 chars |
| property_type | CharField | Type (Apartment/Villa/etc) | Max 100 chars |
| bhk | IntegerField | Number of bedrooms | Default: 1 |
| bathrooms | IntegerField | Number of bathrooms | Default: 1 |
| furnishing | CharField | Furnishing status | Choices: UNFURNISHED/SEMI/FULLY |
| super_built_area | DecimalField | Area in sqft | Max 10 digits, 2 decimals |
| bachelors_allowed | BooleanField | Bachelor-friendly | Default: True |
| total_floors | IntegerField | Total floors in building | Default: 1 |
| facing | CharField | Property facing direction | 8 choices (N/S/E/W/NE/NW/SE/SW) |
| built_year | IntegerField | Year of construction | Optional |
| amenities | TextField | Comma-separated amenities | Optional |
| status | CharField | Property status | PENDING/AVAILABLE/RENTED/MAINTENANCE |
| is_paid | BooleanField | Payment completed | Default: False |
| plan_type | CharField | Subscription plan | basic/standard/premium |
| plan_expiry_date | DateTimeField | Plan expiration date | Optional |
| created_at | DateTimeField | Creation timestamp | Auto-generated |
| updated_at | DateTimeField | Last update timestamp | Auto-updated |

### Methods:
- `is_plan_active()` - Check if plan is still valid
- `days_remaining()` - Get remaining days in plan

### Relationships:
- Many-to-One with User (owner)
- One-to-Many with PropertyImage
- One-to-Many with RentalApplication
- One-to-Many with Lease
- One-to-Many with MaintenanceRequest
- One-to-Many with Inquiry
- One-to-One with Payment
- One-to-Many with Conversation
- One-to-Many with Review
- One-to-Many with Wishlist

---

## 3. PropertyImage Table
**Model Name:** `PropertyImage`  
**Purpose:** Stores multiple images for each property

### Fields:
| Field Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| id | AutoField | Primary Key | Auto-generated |
| property | ForeignKey | Associated property | Links to Property |
| image | ImageField | Property image | Upload to 'property_images/' |

### Relationships:
- Many-to-One with Property

---

## 4. Payment Table
**Model Name:** `Payment`  
**Purpose:** Tracks payment transactions for property listings

### Fields:
| Field Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| id | AutoField | Primary Key | Auto-generated |
| property | OneToOneField | Associated property | Links to Property, Unique |
| owner | ForeignKey | Property owner | Links to User |
| razorpay_order_id | CharField | Razorpay order ID | Unique, Max 255 chars |
| razorpay_payment_id | CharField | Razorpay payment ID | Optional, Max 255 chars |
| razorpay_signature | CharField | Payment signature | Optional, Max 255 chars |
| amount | DecimalField | Payment amount (INR) | Max 10 digits, 2 decimals |
| status | CharField | Payment status | PENDING/SUCCESS/FAILED |
| created_at | DateTimeField | Creation timestamp | Auto-generated |
| updated_at | DateTimeField | Last update timestamp | Auto-updated |

### Relationships:
- One-to-One with Property
- Many-to-One with User (owner)

---

## 5. RentalApplication Table
**Model Name:** `RentalApplication`  
**Purpose:** Manages tenant applications for properties

### Fields:
| Field Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| id | AutoField | Primary Key | Auto-generated |
| tenant | ForeignKey | Applicant tenant | Links to User |
| property | ForeignKey | Applied property | Links to Property |
| application_date | DateTimeField | Application timestamp | Auto-generated |
| status | CharField | Application status | PENDING/APPROVED/REJECTED |
| message | TextField | Application message | Optional |

### Relationships:
- Many-to-One with User (tenant)
- Many-to-One with Property

---

## 6. Lease Table
**Model Name:** `Lease`  
**Purpose:** Manages lease agreements between owners and tenants

### Fields:
| Field Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| id | AutoField | Primary Key | Auto-generated |
| tenant | ForeignKey | Tenant in lease | Links to User |
| property | ForeignKey | Leased property | Links to Property |
| start_date | DateField | Lease start date | Required |
| end_date | DateField | Lease end date | Required |
| monthly_rent | DecimalField | Monthly rent amount | Max 10 digits, 2 decimals |
| document | FileField | Lease document | Optional, Upload to 'leases/' |
| is_active | BooleanField | Lease active status | Default: True |
| created_at | DateTimeField | Creation timestamp | Auto-generated |

### Relationships:
- Many-to-One with User (tenant)
- Many-to-One with Property

---

## 7. MaintenanceRequest Table
**Model Name:** `MaintenanceRequest`  
**Purpose:** Tracks maintenance requests from tenants

### Fields:
| Field Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| id | AutoField | Primary Key | Auto-generated |
| tenant | ForeignKey | Requesting tenant | Links to User |
| property | ForeignKey | Property needing maintenance | Links to Property |
| title | CharField | Request title | Max 255 chars |
| description | TextField | Detailed description | Required |
| priority | CharField | Request priority | LOW/MEDIUM/HIGH/EMERGENCY |
| status | CharField | Request status | OPEN/IN_PROGRESS/RESOLVED |
| image | ImageField | Supporting image | Optional, Upload to 'maintenance/' |
| created_at | DateTimeField | Creation timestamp | Auto-generated |
| updated_at | DateTimeField | Last update timestamp | Auto-updated |

### Relationships:
- Many-to-One with User (tenant)
- Many-to-One with Property

---

## 8. Inquiry Table
**Model Name:** `Inquiry`  
**Purpose:** Stores property inquiries from tenants

### Fields:
| Field Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| id | AutoField | Primary Key | Auto-generated |
| property | ForeignKey | Inquired property | Links to Property |
| tenant | ForeignKey | Inquiring tenant | Links to User |
| message | TextField | Inquiry message | Required |
| created_at | DateTimeField | Creation timestamp | Auto-generated |

### Relationships:
- Many-to-One with Property
- Many-to-One with User (tenant)

---

## 9. Conversation Table
**Model Name:** `Conversation`  
**Purpose:** Manages conversations between tenants and owners

### Fields:
| Field Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| id | AutoField | Primary Key | Auto-generated |
| property | ForeignKey | Property being discussed | Links to Property |
| tenant | ForeignKey | Tenant in conversation | Links to User |
| owner | ForeignKey | Owner in conversation | Links to User |
| created_at | DateTimeField | Creation timestamp | Auto-generated |
| updated_at | DateTimeField | Last update timestamp | Auto-updated |

### Constraints:
- Unique together: (property, tenant, owner)
- Ordering: -updated_at (newest first)

### Methods:
- `get_last_message()` - Returns the last message in conversation

### Relationships:
- Many-to-One with Property
- Many-to-One with User (tenant)
- Many-to-One with User (owner)
- One-to-Many with Message

---

## 10. Message Table
**Model Name:** `Message`  
**Purpose:** Stores individual messages within conversations

### Fields:
| Field Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| id | AutoField | Primary Key | Auto-generated |
| conversation | ForeignKey | Parent conversation | Links to Conversation |
| sender | ForeignKey | Message sender | Links to User |
| content | TextField | Message content | Required |
| is_read | BooleanField | Read status | Default: False |
| created_at | DateTimeField | Creation timestamp | Auto-generated |

### Constraints:
- Ordering: created_at (oldest first)

### Relationships:
- Many-to-One with Conversation
- Many-to-One with User (sender)

---

## 11. Review Table
**Model Name:** `Review`  
**Purpose:** Manages property reviews and ratings

### Fields:
| Field Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| id | AutoField | Primary Key | Auto-generated |
| property | ForeignKey | Reviewed property | Links to Property |
| reviewer | ForeignKey | User giving review | Links to User |
| rating | IntegerField | Star rating (1-5) | Choices: 1/2/3/4/5 |
| comment | TextField | Review comment | Required |
| created_at | DateTimeField | Creation timestamp | Auto-generated |
| updated_at | DateTimeField | Last update timestamp | Auto-updated |

### Constraints:
- Unique together: (property, reviewer) - One review per user per property
- Ordering: -created_at (newest first)

### Relationships:
- Many-to-One with Property
- Many-to-One with User (reviewer)

---

## 12. Wishlist Table
**Model Name:** `Wishlist`  
**Purpose:** Stores tenant's favorite/saved properties

### Fields:
| Field Name | Type | Description | Constraints |
|------------|------|-------------|-------------|
| id | AutoField | Primary Key | Auto-generated |
| tenant | ForeignKey | Tenant who saved | Links to User |
| property | ForeignKey | Saved property | Links to Property |
| created_at | DateTimeField | Creation timestamp | Auto-generated |

### Constraints:
- Unique together: (tenant, property) - One entry per tenant per property
- Ordering: -created_at (newest first)

### Relationships:
- Many-to-One with User (tenant)
- Many-to-One with Property

---

## Database Relationships Summary

### User Relationships:
- **Owns** → Properties (as owner)
- **Makes** → Payments
- **Submits** → RentalApplications (as tenant)
- **Signs** → Leases (as tenant)
- **Creates** → MaintenanceRequests (as tenant)
- **Sends** → Inquiries (as tenant)
- **Participates in** → Conversations (as tenant/owner)
- **Sends** → Messages
- **Writes** → Reviews
- **Saves** → Wishlist items (as tenant)

### Property Relationships:
- **Belongs to** → User (owner)
- **Has** → PropertyImages
- **Receives** → RentalApplications
- **Has** → Leases
- **Receives** → MaintenanceRequests
- **Receives** → Inquiries
- **Has** → Payment (one-to-one)
- **Has** → Conversations
- **Has** → Reviews
- **Saved in** → Wishlists

---

## Total Tables: 12

1. User (Custom User Model)
2. Property
3. PropertyImage
4. Payment
5. RentalApplication
6. Lease
7. MaintenanceRequest
8. Inquiry
9. Conversation
10. Message
11. Review
12. Wishlist

---

## Key Features by Table:

### Authentication & Authorization:
- User (with role-based access: Admin/Owner/Tenant)

### Property Management:
- Property
- PropertyImage
- Payment (Razorpay integration)

### Tenant-Owner Interaction:
- RentalApplication
- Lease
- MaintenanceRequest
- Inquiry
- Conversation
- Message

### Engagement Features:
- Review (ratings & comments)
- Wishlist (favorites)

### Plan System:
- Basic Plan (₹99) - 1 property, 90 days
- Standard Plan (₹199) - 3 properties, 180 days
- Premium Plan (₹399) - 10 properties, 365 days

---

## Database Migrations:
All tables are managed through Django migrations located in `core/migrations/`:
- 0001_initial.py - Initial models
- 0002 through 0009 - Various updates
- 0010_wishlist.py - Latest (Wishlist feature)

---

## Admin Panel:
All models are registered in Django Admin for easy management:
- Located in `core/admin.py`
- Custom admin configurations for better UX
- Inline editing for PropertyImages
