
## New Update - 20/10/2023

### Custom Pagination and Error Renders

In this update, I've introduced custom pagination and error rendering for an enhanced user experience.

#### Custom Pagination

I've implemented a custom pagination solution to make navigation through large datasets more user-friendly. The custom pagination component can be found in `client.paginator.CustomPagination`.

#### Error Renders

I've improved error rendering to provide clear and informative error messages to users. I've enhanced error handling for a smoother user experience. The custom error rendering can be found in `client.renders.CustomRenderer`.

### Auth API's for Login

I've added new authentication APIs to support user login. These APIs enable users to securely log in to the application and access their accounts.

### Email OTP Verification

I've introduced email OTP (One-Time Password) verification to enhance account security and ensure that users have a seamless sign-up process. (10 minutes expiry)



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

## Contributing

I welcome contributions to this project! If you'd like to contribute, please follow these guidelines:
### Code Contributions

If you want to contribute code, feel free to [fork this repository](https://github.com/B-SAHIL/django-login-jwt.git) and submit a pull request. Please follow these guidelines when submitting your contributions:

- Follow the coding standards and conventions used in this project.
- Write clear and concise commit messages.
- Provide thorough documentation for new code.

### Contact
If you prefer to contact me directly, you can email me at `sahilbacked@gmail.com`.
For questions or discussions, you can reach out to me ,  you can telegram me at `@bunny_02824`. I welcome your feedback and questions.

