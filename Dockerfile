FROM python:3.10.16-slim

# Create the app directory
RUN mkdir /app
 
# Set the working directory inside the container
WORKDIR /app

RUN apt-get update 
RUN apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config -y

# Copy the Django project  and install dependencies
COPY requirements.txt  .
RUN pip install -r requirements.txt

# Copy the Django project to the container
COPY . .
 
# Expose the Django port
EXPOSE 8000
 
# Run Django’s development server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
