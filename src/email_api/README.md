# email-api

## Overview
`email-api` provides a simple, provider-agnostic interface for working with email messages.  
It defines a lightweight `Email` data model and an in-memory `Client` for basic email operations.

This module is intentionally minimal and is designed to be easy to replace with a real email service implementation.

## Responsibilities
- Define a standard `Email` message representation
- Provide a simple email client API
- Support basic send, list, retrieve, and delete operations
- Remain independent of any external email provider

## Core Models

### Email
`Email` represents a single email message with common fields.

```python
from email_api import Email

email = Email(
    sender="alice@example.com",
    recipient="bob@example.com",
    subject="Hello",
    body="Hi Bob!"
)
```

## Client API
`Client` provides basic email operations using an in-memory store.

```python
from email_api import Client, Email

client = Client()
client.send_email(email)

emails = client.list_emails()
first = client.get_email(0)
client.delete_email(0)
```

## Behavior and Constraints
- `send_email` raises `ValueError` if sender or recipient is missing
- Emails are stored in memory only
- Index-based access is used for retrieval and deletion

## Testing and Usage
This module is suitable for:
- Local development
- Testing workflows that require email-like behavior
- Demonstrations without external dependencies

It is **not** intended for production email delivery.

## Non-Goals
This module does not:
- Send real emails
- Persist messages to disk or database
- Handle authentication, SMTP, or external APIs
- Guarantee delivery or reliability
