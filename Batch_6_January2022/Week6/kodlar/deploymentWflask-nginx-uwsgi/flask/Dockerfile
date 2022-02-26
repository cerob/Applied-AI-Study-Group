# Use the Python3.7.8 image
FROM python:3.7.8

# Set the working directory to /myapp
WORKDIR /myapp

# Copy the current directory contents into the container at /myapp 
ADD . /myapp

# Install the dependencies
RUN pip install -r requirements.txt

#opencv dependencies
RUN apt-get update
RUN apt-get install 'libgl1-mesa-dev' -y

# run the command to start uWSGI
CMD ["uwsgi", "myapp.ini"]