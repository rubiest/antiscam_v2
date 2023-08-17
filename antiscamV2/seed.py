import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'antiscamV2.settings')
django.setup()

from antiscam.models import Location, Category

location_names = [
    "Johor",
    "Kedah",
    "Kelantan",
    "Melaka",
    "Negeri Sembilan",
    "Pahang",
    "Perak",
    "Perlis",
    "Pulau Pinang",
    "Sabah",
    "Sarawak",
    "Selangor",
    "Terengganu",
    "WP Kuala Lumpur",
    "WP Labuan",
    "WP Putrajaya",
]

category_names = [
    "Investment Scams",
    "Romance Scams",
    "Lottery or Prize Scams",
    "Job Scams",
    "Charity Scams",
    "Impersonation Scams",
    "Vishing (Voice Phishing)",
    "Smishing (SMS Phishing)",
]

for location_name in location_names:
    Location.objects.get_or_create(name=location_name)

for category_name in category_names:
    Category.objects.get_or_create(name=category_name)

print("Seeding completed.")
