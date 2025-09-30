# Event Manager

A modern platform to create, manage, and participate in events. Designed for administrators, organizers, and participants, providing intuitive dashboards and seamless workflows.

🔗 [Live Demo](https://event-management-django-neon.vercel.app/)

---

## 📌 Features

* **Role-Based Dashboards**: Tailored views for Admins, Organizers, and Participants.
* **Event Management**: Easy creation, updating, and categorization of events.
* **RSVP System**: Participants can explore and RSVP to events with a single click.
* **User Authentication**: Secure login and registration processes.

---

## ⚙️ Tech Stack

* **Backend**: Django (Python)
* **Frontend**: HTML, CSS, JavaScript
* **Database**: PostgreSQL
* **Deployment**: Vercel

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* PostgreSQL
* Vercel account

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/tanbinali/event_management_django.git
   cd event_management_django
   ```

2. Set up a virtual environment:

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database:

   * Set up a PostgreSQL database.

5. Apply migrations:

   ```bash
   python manage.py migrate
   ```

6. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

---

## 🧪 Testing

Run tests using Django's test framework:

```bash
python manage.py test
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
