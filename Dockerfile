FROM python:3.10-slim

# Create the app directory
RUN mkdir /app
 
# Set the working directory inside the container
WORKDIR /app

RUN apt-get update

# Copy the Django project  and install dependencies
COPY requirements.txt  .
RUN pip install -r requirements.txt

# Copy the Django project to the container
COPY . .
 
# Expose the Django port
EXPOSE 8000
 
# Run Django’s development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
