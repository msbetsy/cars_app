## General info
This project provides a simple REST API for car rating, db interacting with an external API.
It was created using Django, REST API. App tests were written using APITestCase and TestCase.

## Setup
To run this project, install it locally:

```
$ git clone https://github.com/msbetsy/car_app
```

## Usage
After you clone this repo to your desktop, create and activate virtual environment, install requirements, go to its cars/ directory, create .env file,  run migrations, and run application.

```
$ python -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
$ cd cars
$ echo SECRET_KEY="YOUR SECRET KEY" > .env
$ python manage.py migrate
$ python manage.py runserver
```
