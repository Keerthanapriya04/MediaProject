# Distributed Media Processing Web Application

An event-driven backend application designed to handle heavy asynchronous media workloads using Django, Celery, Redis, and PostgreSQL, fully containerized with Docker.

## Project Overview
When the main web application receives user media uploads (images and videos), it offloads the heavy processing tasks (resizing, compressing, and transcoding) to asynchronous background workers. This architecture ensures high performance, responsiveness, and scalability.

## Tech Stack
* **Language:** Python 3.11+
* **Web Framework:** Django
* **Asynchronous Task Queue:** Celery
* **Message Broker & Cache:** Redis
* **Database:** PostgreSQL
* **Media Processing:** Pillow (Images), FFmpeg (Video)
* **Containerization:** Docker & Docker Compose

Mediaproject/
│
├── app/                  # Core application logic & Celery tasks
│   ├── celery_app.py     # Celery configuration
│   ├── tasks.py          # Background processing tasks
│   └── storage.py        # File storage handlers
│
├── mediaapp/             # Django views, models, forms, and templates
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   └── views.py
│
├── Mediaproject/         # Project settings and URL routing
│   ├── settings.py
│   └── urls.py
│
├── Dockerfile            # Container configuration for the web app
├── docker-compose.yml    # Multi-container orchestration (Web, DB, Redis, Celery)
├── requirements.txt      # Python dependencies
└── manage.py
