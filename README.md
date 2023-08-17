# Library Api Service

## Table of Contents
 1. [Introduction](#introduction)
 2. [Requirements](#requirements)
 3. [Installation](#installation)
 4. [Used technologies](#used-technologies)
 5. [Usage](#usage)
 6. [Endpoints](#endpoints) 
 7. [License](#license) 


## Introduction
Library Api Service is providing functionality for users of borrowing books
for some period. Users can borrow books, set a period of borrowing, 
process payment and return books. Users are receiving notifications in telegram
of creating new borrowing, returning a borrowing, reminding about expiring
borrowing time day before exact expiration, successful payment and list of 
books that user hasn't returned in time. Admin users can create new or modify
existing Books, spectate list of borrowing and payment of all users, filter it
by user id. Admin users are also receiving notifications about all users with 
borrowing debts and all notifications that users are receiving.  

## Requirements
### For local running
* python 3.8
* pip

### For Docker
* Docker

## Installation
1. Clone this repository:

    ```
    git clone https://github.com/Kirontiko/library-api.git
    ```
 2. Create .env file and define environmental variables following .env.example:
    ```
    DJANGO_SECRET_KEY=your django secret key
    STRIPE_API_KEY=your stripe api key
    TELEGRAM_TOKEN=token of your telegram bot
    BOT_NAME=name of your telegram bot
    POSTGRES_HOST=your db host
    POSTGRES_DB=name of your db
    POSTGRES_USER=username of your db user
    POSTGRES_PASSWORD=your db password
    PYTHONPATH={
    DOCKER: you have to pass here your workdir
    from Docker
    
    LOCAL RUNNING: you have to pass here your absolute path
    to project dir
    }
    ```
 ### 3. To run it locally
1. Create virtual environment and activate it:
   * Tooltip for windows:
     - ```python -m venv venv``` 
     - ```venv\Scripts\activate```
   * Tooltip for mac:
     - ```python -m venv venv```
     - ```source venv/bin/activate```

2. Install dependencies:
    - ```pip install -r requirements.txt```
3. Apply all migrations in database:
   - ```python manage.py migrate```
4. Run redis server
   - ```docker run --name my-redis-server -d -p 127.0.0.1:6379:6379 redis```
5. Run Qcluster
   - ```python manage.py qcluster```
6. Run server
   - ```python manage.py runserver```
7. Run telegram server
   - ```python notification/telegram_server.py```
### 3. To run it from docker
1. Run command:
      ```
      docker-compose up --build
      ```
### 4. App will be available at: ```127.0.0.1:8000```

## Used technologies
    - Django framework
    - Django Rest Framework
    - PostgreSQL
    - DjangoQ
    - Redis
    - Docker

## Usage
### For users
    1. Borrowing books and returning them
    2. Only reading all data from endpoints
### For admins
    1. Creating or modifying books
    2. Spectating at list of all payments and borrowings
    3. Filtering payments or borrowings by user id
    5. + all user allowances

## Endpoints
    "books": "http://127.0.0.1:8000/api/v1/books/",
    "borrowings": "http://127.0.0.1:8000/api/v1/borrowings/",
    "users": "http://127.0.0.1:8000/api/v1/users/",
    "payments": "http://127.0.0.1:8000/api/v1/payments/",
    "documentation": "http://127.0.0.1:8000/api/v1/doc/swagger/"

# License
This project is licensed under the MIT License.
Feel free to use and modify the codebase as needed.
