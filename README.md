# WhatsApp Messaging Application

This is a Django-based web application that allows users to send and receive WhatsApp messages via Twilio's API. It includes user authentication, message management, and webhook integration for receiving messages.

---

## Features
- **User Authentication**: Login and logout functionality.
- **Send Messages**: Send WhatsApp messages via Twilio.
- **Receive Messages**: Process incoming messages via Twilio webhook.
- **Message Management**: View sent and received messages with statuses.

---

## Prerequisites
Before you begin, ensure you have the following installed on your computer:
- Python (>= 3.8)
- Docker and Docker Compose (if using Docker)
- A Twilio account with a WhatsApp-enabled number
- Ngrok account along with Installed and auth token added Ngrok (for exposing the webhook)

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository_url>
cd <repository_name>
```
### 2. Configure Environment variables
- Rename .env.sample file and add required credentials

### 3. Docker build
```bash
docker-compose up --build
```

### 4. Open another terminal and run below commands
```bash
docker-compose run app python manage.py makemigrations
docker-compose run app python manage.py migrate
docker-compose run app python manage.py createsuperuser
(give the username, password and email when prompted)
```

## Setting up Twilio Webhook

### 5. Start Ngrok
- Go to the relevant folder where ngrok.exe located, double click to start
- Copy the HTTPS URL provided by Ngrok (e.g., https://<your_ngrok_url>.ngrok-free.app).

### 6. Configure Twilio Webhook
- Navigate to **Messaging > WhatsApp Sandbox Settings**.
- Set the Incoming Messages Webhook URL to: ```https://<your_ngrok_url>.ngrok-free.app/webhook/``` and save changes

### 7. Visit the application at ```http://127.0.0.1:8000/login/``` and login

## Troubleshooting
- Webhook Not Working:
  - Ensure Ngrok is running and the correct URL is set in Twilio.
  Check for errors in the webhook log (ngrok dashboard or logs/debug.log if logging is enabled).
- Twilio Credentials:
  - Double-check your Twilio SandboxID and Auth Token in the .env file.
- Database Errors:
  - Ensure migrations have been applied (python manage.py migrate).

### View the API Documentation at ```http://127.0.0.1:8000/swagger/``` or ```http://127.0.0.1:8000/redoc/```

## Project Structure
```bash
support_whatsapp/
├── messaging/
│   ├── migrations/
│   ├── static/         # Static files (CSS, JS)
│   ├── templates/      # HTML templates
│   ├── admin.py        # Admin code
│   ├── apps.py         # 
│   ├── models.py       # Database models
│   ├── tests.py        # Tests
│   ├── views.py        # Application views
├── notifications/
│   ├── asgi.py
│   ├── settings.py     # Settings
│   ├── urls.py
│   ├── wsgi.py
├── env.sample          # rename this file as .env  
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker image configuration
├── docker-compose.yml  # Docker Compose configuration
├── requirements.txt    # Dependencies
```

