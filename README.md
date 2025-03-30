# Workshop

Workshop is a website created to show all workshops from SimpleVM Team. It is developed with django.

## Installation

Clone the repository using 
~~~BASH
git clone -b https://github.com/GraceCeline/Workshop.git
~~~
then go to terminal and go to the directory where the repository is cloned. Run the application using
~~~BASH
make dev
~~~
This will launch the application locally in localhost:8000. By running make dev, it will run the application in a tox environment, so make sure tox is installed. 
Command to install tox in Unix:
~~~BASH
pip install tox
~~~
### Makefile
There are several make commands available, including:
~~~BASH
make help
~~~
~~~BASH
make makemigrations
~~~
to make migrations to the database
~~~BASH
make migrate
~~~
to migrate the database