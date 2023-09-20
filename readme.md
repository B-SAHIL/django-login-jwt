# Django App Setup Guide

This guide will walk you through the process of setting up a Django web application and login process using JWT.

## Prerequisites

Before you begin, ensure that you have the following prerequisites installed on your system:

- Python (3.x recommended)
- pip (Python package manager)
- Git (optional but recommended for version control)

## Installation

1. **Clone the Repository**

   ```shell
   git clone https://github.com/B-SAHIL/django-login-jwt.git
   ```


2. **Start the Project**


```shell script
python -m venv venv
```

```shell script
venv\Scripts\activate 
```

<!-- on mac -->
```shell script
source venv/bin/activate
```

```shell script
pip install -r requirements.txt
```


```shell script
python manage.py migrate
```

<!-- Can create super user or use 'user/register' api -->

```shell script
python manage.py createsuperuser
```

```shell script
python manage.py runserver
```
