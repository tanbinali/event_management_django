import os
import django
import random
from faker import Faker
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_manager.settings')
django.setup()

from django.contrib.auth.models import User, Group
from events.models import Event, Category

fake = Faker()

def create_groups():
    for name in ['Admin', 'Organizer', 'Participant']:
        Group.objects.get_or_create(name=name)

def create_users():
    users = []
    for _ in range(10):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password="pass1234"
        )
        group_name = random.choices(
            ['Admin', 'Organizer', 'Participant'],
            weights=[1, 3, 6]
        )[0]
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        users.append((user, group_name))
        print(f"Created user: {user.username} in group: {group_name}")
    return users

def create_categories():
    category_names = ['Music', 'Tech', 'Art', 'Education']
    for name in category_names:
        Category.objects.get_or_create(name=name, defaults={'description': fake.text()})

def create_events(users):
    categories = list(Category.objects.all())
    organizers = [u for u, g in users if g == 'Organizer']
    participants = [u for u, g in users if g == 'Participant']

    for _ in range(5):
        if not organizers: continue
        org = random.choice(organizers)
        category = random.choice(categories)
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.text(),
            location=fake.city(),
            date=datetime.now().date() + timedelta(days=random.randint(1, 30)),
            time=datetime.now().time(),
            category=category
        )
        # Add random participants
        selected = random.sample(participants, k=random.randint(1, len(participants)))
        event.participants.set(selected)
        print(f"Created event: {event.name}, Organizer: {org.username}, Participants: {[u.username for u in selected]}")

if __name__ == '__main__':
    create_groups()
    users = create_users()
    create_categories()
    create_events(users)
    print("Database populated successfully!")