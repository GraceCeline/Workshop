# Workshop

Workshop is a website created to show all workshops from SimpleVM Team. It is developed with django.

## Installation

Clone the repository using 
~~~BASH
git clone -b https://github.com/GraceCeline/Workshop.git
~~~
then go to terminal and go to the directory where the repository is cloned. Run the application using
~~~BASH
python manage.py runserver
~~~
### Makefile
There are several make commands available, including:
~~~BASH
make help
~~~
~~~BASH
make dev
~~~
to run the application in a virtual environment and launch it locally in localhost:8000
~~~BASH
make makemigrations
~~~
to make migrations to the database
~~~BASH
make migrate
~~~
to migrate the database
