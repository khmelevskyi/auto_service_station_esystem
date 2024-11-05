# auto_service_station_esystem

Курсова робота з Бази Даних з теми "Облік ремонтів на СТО"
(Також доповнення проєкту для предмету Основи Web-технологій 2024)

## Enviroment
> python --version >>> Python 3.8.5
>
> linux version >>> Ubuntu 18.04 or WSL

Django Framework: [django](https://docs.djangoproject.com/en/4.2/)

On a AWS Ubuntu 18.04 new machine, below installations are required:

* `sudo apt-get install gcc libpq-dev`
* `sudo apt-get install python3-dev python3-pip python3-venv python3-wheel`
* `sudo apt install git-all`
* `pip3 install wheel`


## Launch
* `git clone https://repo.url` - clone repo
* `cd repo` - move to project directory
---
* `source setup.sh` - create and activate virtual environment, install dependencies
* `cp .env.example .env` - create your .env file and insert your values

* `python3 manage.py runserver` - run the app via Django manage.py file

Go to http://127.0.0.1:8000/ to see the Web page
