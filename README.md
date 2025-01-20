# Python_Task

# URL Shortener with Flask

This is a simple URL shortener built using Python, Flask, and SQLite. The application allows users to shorten URLs, protect them with passwords, set expiration times, and view analytics for each shortened URL.

---

## Features

- **Shorten URLs**: Convert long URLs into concise and easy-to-share links.
- **Password Protection**: Optionally secure shortened URLs with a password.
- **Expiration**: Set expiration times for shortened URLs.
- **Analytics**: View access counts and logs for shortened URLs, including IP addresses and access times.
- **Error Handling**: Comprehensive error handling for invalid inputs, expired URLs, incorrect passwords, and more.

---

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Libraries Used**:
  - `Flask`: Web framework for building the API.
  - `sqlite3`: Python library for interacting with the SQLite database.
  - `hashlib`: Used for generating unique hashes for URLs.
  - `datetime`: For handling time-related operations like expiration.
  - `jsonify` and `request`: Flask utilities for handling requests and JSON responses.

---

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Madhavilatha-dev/Python_Task.git
   cd Python_Task
   ```
2. **Install Dependencies**
   ```bash
   pip install flask
   ```
3. **Initialize the Database**
   Run the application once to initialize the database:
   ```bash
   python flaskapp.py
   ```

---

## API Endpoints

### 1. **Shorten URL**
   - **Endpoint**: `/shorten`
   - **Method**: `POST`
   - **Description**: Shorten a URL with optional expiration and password.
   - **Request Body**:
     ```json
     {
       "original_url": "http://example.com",
       "expiration_hours": 24,  # Optional (default: 24 hours)
       "password": "mypassword"  # Optional
     }
     ```
   - **Response**:
     ```json
     {
       "shortened_url": "http://short.ly/abcd12"
     }
     ```

### 2. **Redirect to Original URL**
   - **Endpoint**: `/<short_url>`
   - **Method**: `GET`
   - **Description**: Redirect to the original URL using the shortened URL.
   - **Query Parameters**:
     - `password` (if the URL is password-protected)
   - **Errors**:
     - `404`: URL not found
     - `410`: URL expired
     - `403`: Incorrect or missing password

### 3. **View Analytics**
   - **Endpoint**: `/analytics/<short_url>`
   - **Method**: `GET`
   - **Description**: Retrieve analytics for a shortened URL.
   - **Response**:
     ```json
     {
       "original_url": "http://example.com",
       "creation_time": "2025-01-20T12:00:00",
       "expiration_time": "2025-01-21T12:00:00",
       "access_count": 10,
       "access_logs": [
         {
           "access_time": "2025-01-20T12:30:00",
           "ip_address": "192.168.1.1"
         }
       ]
     }
     ```

---

## Error Handling

- **404 Not Found**: If a shortened URL does not exist.
- **410 Gone**: If a shortened URL has expired.
- **403 Forbidden**: If a password is incorrect or missing.
- **400 Bad Request**: If required fields are missing during URL shortening.

---

## How to Test

### Using Curl
1.
curl --location 'http://127.0.0.1:5000/shorten' \
--header 'Content-Type: application/json' \
--data '{
"original_url" : "http://example.com",
"expiration_hours" : 24,
"password" : "pass123"
}
'

2. curl --location 'http://127.0.0.1:5000/a9b9f0?password=pass123'

3. curl --location 'http://127.0.0.1:5000/analytics/a9b9f0'

---

## Contributors

- Madhavilatha
