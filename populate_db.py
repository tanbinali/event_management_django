from events.models import Category, Event, Participant
from faker import Faker
import random
from datetime import time

fake = Faker()

# Create 5 categories
categories = []
for _ in range(5):
    cat = Category.objects.create(
        name=fake.word().capitalize(),
        description=fake.sentence(nb_words=10)
    )
    categories.append(cat)

# Create 20 events
events = []
for _ in range(20):
    event_date = fake.date_between(start_date='-30d', end_date='+60d')
    event_time = time(
        hour=random.randint(8, 20),
        minute=random.choice([0, 15, 30, 45])
    )
    event = Event.objects.create(
        name=fake.catch_phrase(),
        description=fake.paragraph(nb_sentences=3),
        date=event_date,
        time=event_time,
        location=fake.city(),
        category=random.choice(categories)
    )
    events.append(event)

# Create 10 participants and assign random events
for _ in range(10):
    participant = Participant.objects.create(
        name=fake.name(),
        email=fake.email()
    )
    # Assign 1 to 5 random events to participant
    participant.events.set(random.sample(events, random.randint(1, 5)))
    participant.save()

print("Fake data created successfully!")
