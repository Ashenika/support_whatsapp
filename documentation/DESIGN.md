# Design Decisions and Assumptions

This document outlines the key design decisions made during the development of the WhatsApp Messaging Application, as well as the assumptions that influenced these decisions.

---

## **Design Decisions**

### 1. **Technology Stack**
- **Framework**: Django
- **Database**: SQLite
  - Selected for simplicity in development and testing; can be replaced with a production-ready database like PostgreSQL if needed.
- **Third-Party Service**: Twilio
  - Used for WhatsApp messaging due to its comprehensive API and reliable integration with Django.
- **Third-Party Service**: Ngrok
  - Used to expose local development environment to get the twilio received messages.


---

### 2. **Architecture**
- **Separation of Concerns**:
  - The application follows the MVC (Model-View-Controller) pattern, ensuring a clear separation of data, business logic, and user interface.
- **Reusable Components**:
  - Views, templates, and models were designed to be reusable and extensible for future feature additions.

---

### 3. **Features**
- **Login and Logout**:
  - Used Django's built-in `User` model and authentication system to simplify user management and security.
- **Send Message**:
  - Integrated Twilio's WhatsApp API for sending messages.
  - Added server-side validation for user input to ensure data integrity.
- **List Messages**:
  - Designed to display a paginated and sorted list of messages using the Django ORM.
- **View Single Message**:
  - Enabled retrieval and display of message details by ID.
- **Webhook for Incoming Messages**:
  - Implemented a webhook endpoint to process incoming messages from Twilio and save them to the database.
  - Simple JavaScript code to refresh the list messages page in order to view new messages.
---

### 4. **API Design**
- Used `@api_view` decorators to make views compatible with DRF-style API documentation (Swagger and Redoc).
- Followed REST principles for clarity and simplicity of the API endpoints:
  - `/webhook/`: Handles incoming WhatsApp messages.
  - `/send-message/`: Sends WhatsApp messages.
  - `/messages/`: Lists all messages.
  - `/messages/{message_id}/`: View single message.

---

### 5. **Error Handling**
- Used descriptive error messages to improve user experience (e.g., "All fields are required" for missing input).
- Added logging to capture key events and errors for debugging and monitoring:

---

### 6. **Testing**
- Implemented unit tests for all critical views and edge cases. (9 of 9 Tests Passed)
- Used mocking to simulate Twilio API calls and ensure reliable test results.

---

## **Assumptions**

1. **User Authentication**:
   - Assumes a single admin user for managing messages and testing the application.

3. **Data Volume**:
   - Assumes low-to-moderate traffic (development/testing use case).
   - SQLite is used for simplicity, assuming no need for high scalability at this stage.

4. **Message Storage**:
   - Assumes storing both incoming and outgoing messages in the database is sufficient for the use case.
   - No need for external storage or archiving at this stage.

7. **Frontend Design**:
   - Assumes minimal UI/UX design is acceptable for this phase (focused on basic functionality with practises).

---

## **Future Considerations**
- **Scalability**:
  - Replace SQLite with PostgreSQL for production use to handle higher traffic and concurrent requests.
- **Enhanced Features**:
  - Add support for media messages (images, videos) in WhatsApp.
  - Implement role-based access control for multi-user environments.
- **Monitoring and Alerts**:
  - Add monitoring tools to track message delivery, webhook events, and system health.
- **Deployment**:
  - Use Docker and CI/CD pipelines for easier deployment and maintenance in production.

---

## **Conclusion**
This document summarizes the design decisions and assumptions made during the development of the WhatsApp Messaging Application. The decisions prioritize simplicity, reusability, and extensibility, while the assumptions reflect the development and testing phase requirements. Future enhancements can build upon this foundation.

---
