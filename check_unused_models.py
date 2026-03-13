"""
Check which models are actually being used in the project
"""
import os
import re

def search_in_files(pattern, directory, extensions):
    """Search for pattern in files"""
    matches = []
    for root, dirs, files in os.walk(directory):
        # Skip migrations and pycache
        if 'migrations' in root or '__pycache__' in root or 'venv' in root:
            continue
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if re.search(pattern, content):
                            matches.append(filepath)
                except:
                    pass
    return matches

print("="*70)
print("CHECKING MODEL USAGE IN RENTEASE PROJECT")
print("="*70)

models_to_check = {
    'RentalApplication': r'RentalApplication',
    'Inquiry': r'Inquiry',
    'Review': r'Review',
}

for model_name, pattern in models_to_check.items():
    print(f"\n{model_name}:")
    print("-" * 70)
    
    # Search in views.py
    views_matches = search_in_files(pattern, 'core', ['.py'])
    
    # Search in templates
    template_matches = search_in_files(pattern, 'core/templates', ['.html'])
    
    if views_matches or template_matches:
        print(f"  ✅ USED in:")
        for match in views_matches:
            if 'models.py' not in match:
                print(f"     - {match}")
        for match in template_matches:
            print(f"     - {match}")
    else:
        print(f"  ❌ NOT USED (only defined in models.py)")

print("\n" + "="*70)
print("RECOMMENDATION:")
print("="*70)
print("""
Based on your project description (simple messaging platform):

KEEP:
- User (authentication)
- Property (listings)
- PropertyImage (property photos)
- Payment (Razorpay integration)
- Conversation (messaging)
- Message (chat messages)
- Wishlist (favorites)
- WebsiteFeedback (platform reviews)

REMOVE (if not needed):
- RentalApplication (if you don't have application system)
- Inquiry (replaced by messaging system)
- Review (if you don't want property reviews)
""")
