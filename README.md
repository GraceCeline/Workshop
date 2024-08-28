Workshop

Workshop is a website created to show all workshops from SimpleVM Team. It is developed with django.

Installation

Clone this repository. Open the terminal in the directory in which you cloned the repo and run in the local server with the command:
python manage.py runserver

Usage

Once the program is ran in the local server you'll be redirected to a login page. Only public workshops are viewable without logging in, and without a user account it is impossible to register for a workshop. There's a link redirecting to Register page for opening an account. 

After logging in/ registering you'll see the homepage which contains all the workshop. If the user is a workshop administrator they will be able to create, edit, and delete their own workshop. Platform administrator (superuser) has the permission to every workshop. User logged in as participant can see all the workshops and register for them.
