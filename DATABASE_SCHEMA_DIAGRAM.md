# Database Schema Diagram - RentEase

## Visual Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              USER TABLE                                      │
│  (Custom User Model - Extends AbstractUser)                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  • id (PK)                    • is_active                                   │
│  • username (Unique)          • is_staff                                    │
│  • email (Unique)             • is_superuser                                │
│  • password                   • date_joined                                 │
│  • first_name                 • last_login                                  │
│  • last_name                  • groups (M2M)                                │
│  • role (ADMIN/OWNER/TENANT)  • user_permissions (M2M)                      │
│  • profile_image                                                            │
│  • phone_number                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
         │                    │                    │
         │ (owner)            │ (tenant)           │ (reviewer/sender)
         ▼                    ▼                    ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│    PROPERTY      │  │ RENTAL           │  │    REVIEW        │
│                  │  │ APPLICATION      │  │                  │
├──────────────────┤  ├──────────────────┤  ├──────────────────┤
│ • id (PK)        │  │ • id (PK)        │  │ • id (PK)        │
│ • owner (FK)     │  │ • tenant (FK)    │  │ • property (FK)  │
│ • title          │  │ • property (FK)  │  │ • reviewer (FK)  │
│ • ad_title       │  │ • status         │  │ • rating (1-5)   │
│ • description    │  │ • message        │  │ • comment        │
│ • price          │  │ • created_at     │  │ • created_at     │
│ • location       │  └──────────────────┘  │ • updated_at     │
│ • property_type  │                        └──────────────────┘
│ • bhk            │  ┌──────────────────┐
│ • bathrooms      │  │    WISHLIST      │
│ • furnishing     │  │                  │
│ • super_built_   │  ├──────────────────┤
│   area           │  │ • id (PK)        │
│ • bachelors_     │  │ • tenant (FK)    │
│   allowed        │  │ • property (FK)  │
│ • total_floors   │  │ • created_at     │
│ • facing         │  └──────────────────┘
│ • built_year     │
│ • amenities      │  ┌──────────────────┐
│ • status         │  │     LEASE        │
│ • is_paid        │  │                  │
│ • plan_type      │  ├──────────────────┤
│ • plan_expiry_   │  │ • id (PK)        │
│   date           │  │ • tenant (FK)    │
│ • created_at     │  │ • property (FK)  │
│ • updated_at     │  │ • start_date     │
└──────────────────┘  │ • end_date       │
         │             │ • monthly_rent   │
         │             │ • document       │
         ▼             │ • is_active      │
┌──────────────────┐  │ • created_at     │
│ PROPERTY IMAGE   │  └──────────────────┘
│                  │
├──────────────────┤  ┌──────────────────┐
│ • id (PK)        │  │  MAINTENANCE     │
│ • property (FK)  │  │    REQUEST       │
│ • image          │  │                  │
└──────────────────┘  ├──────────────────┤
         │             │ • id (PK)        │
         │             │ • tenant (FK)    │
         ▼             │ • property (FK)  │
┌──────────────────┐  │ • title          │
│    PAYMENT       │  │ • description    │
│  (One-to-One)    │  │ • priority       │
├──────────────────┤  │ • status         │
│ • id (PK)        │  │ • image          │
│ • property (FK)  │  │ • created_at     │
│ • owner (FK)     │  │ • updated_at     │
│ • razorpay_      │  └──────────────────┘
│   order_id       │
│ • razorpay_      │  ┌──────────────────┐
│   payment_id     │  │    INQUIRY       │
│ • razorpay_      │  │                  │
│   signature      │  ├──────────────────┤
│ • amount         │  │ • id (PK)        │
│ • status         │  │ • property (FK)  │
│ • created_at     │  │ • tenant (FK)    │
│ • updated_at     │  │ • message        │
└──────────────────┘  │ • created_at     │
         │             └──────────────────┘
         │
         ▼             ┌──────────────────┐
┌──────────────────┐  │  CONVERSATION    │
│  CONVERSATION    │  │                  │
│                  │  ├──────────────────┤
├──────────────────┤  │ • id (PK)        │
│ • id (PK)        │  │ • property (FK)  │
│ • property (FK)  │  │ • tenant (FK)    │
│ • tenant (FK)    │  │ • owner (FK)     │
│ • owner (FK)     │  │ • created_at     │
│ • created_at     │  │ • updated_at     │
│ • updated_at     │  └──────────────────┘
└──────────────────┘           │
         │                     │
         ▼                     ▼
┌──────────────────┐  ┌──────────────────┐
│    MESSAGE       │  │    MESSAGE       │
│                  │  │                  │
├──────────────────┤  ├──────────────────┤
│ • id (PK)        │  │ • id (PK)        │
│ • conversation   │  │ • conversation   │
│   (FK)           │  │   (FK)           │
│ • sender (FK)    │  │ • sender (FK)    │
│ • content        │  │ • content        │
│ • is_read        │  │ • is_read        │
│ • created_at     │  │ • created_at     │
└──────────────────┘  └──────────────────┘
```

## Relationship Types Legend:

- **PK** = Primary Key
- **FK** = Foreign Key
- **M2M** = Many-to-Many
- **│** = One-to-Many relationship
- **▼** = Points to related table

## Cardinality:

### One-to-Many (1:N):
- User → Properties (One owner has many properties)
- User → Payments (One owner has many payments)
- User → RentalApplications (One tenant has many applications)
- User → Leases (One tenant has many leases)
- User → MaintenanceRequests (One tenant has many requests)
- User → Inquiries (One tenant has many inquiries)
- User → Reviews (One user has many reviews)
- User → Wishlist (One tenant has many wishlist items)
- User → Messages (One user sends many messages)
- Property → PropertyImages (One property has many images)
- Property → RentalApplications (One property has many applications)
- Property → Leases (One property has many leases)
- Property → MaintenanceRequests (One property has many requests)
- Property → Inquiries (One property has many inquiries)
- Property → Reviews (One property has many reviews)
- Property → Wishlist (One property in many wishlists)
- Property → Conversations (One property has many conversations)
- Conversation → Messages (One conversation has many messages)

### One-to-One (1:1):
- Property ↔ Payment (One property has one payment record)

### Many-to-Many (M:M):
- User ↔ Groups (Through Django's auth system)
- User ↔ Permissions (Through Django's auth system)

### Unique Together Constraints:
- Conversation: (property, tenant, owner) - Prevents duplicate conversations
- Review: (property, reviewer) - One review per user per property
- Wishlist: (tenant, property) - One wishlist entry per tenant per property

## Data Flow Examples:

### Property Listing Flow:
```
Owner (User) → Creates Property → Uploads PropertyImages → Makes Payment
→ Property Status: PENDING → Admin Approves → Status: AVAILABLE
```

### Tenant Application Flow:
```
Tenant (User) → Views Property → Submits RentalApplication
→ Owner Reviews → Approves → Creates Lease → Status: RENTED
```

### Messaging Flow:
```
Tenant → Sends Inquiry → Creates Conversation → Exchanges Messages with Owner
```

### Review Flow:
```
Tenant/Owner → Visits Property → Writes Review (rating + comment)
→ Stored in Review table
```

### Wishlist Flow:
```
Tenant → Browses Properties → Adds to Wishlist → Saved in Wishlist table
```

## Indexes & Performance:

### Indexed Fields (Automatic):
- All Primary Keys (id)
- All Foreign Keys
- Unique fields (username, email, razorpay_order_id)

### Recommended Additional Indexes:
- Property.status (for filtering)
- Property.plan_type (for filtering)
- Property.plan_expiry_date (for expiry checks)
- Message.is_read (for unread counts)
- Conversation.updated_at (for sorting)

## Database Statistics:

- **Total Tables:** 12
- **Total Relationships:** 25+
- **User Roles:** 3 (Admin, Owner, Tenant)
- **Property Statuses:** 4 (Pending, Available, Rented, Maintenance)
- **Payment Statuses:** 3 (Pending, Success, Failed)
- **Plan Types:** 3 (Basic, Standard, Premium)
