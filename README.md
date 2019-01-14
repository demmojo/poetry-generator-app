# poetry-generator-app

poetry-generator-app generates poetry using pre-trained deep learning models. Shakespeare and Nazim Hikmet's works have both been modelled. This guide will show you how to run the app locally as well as deploy it to your own website. This can be a useful guide on how to deploy a python application using flask, uWSGI application server and Nginx as the front-end reverse proxy on a server. Also, you may use it as a template to serve your own web app with custom pre-trained models for prediction.

For a live demonstration head on to: https://shakespeare.mohamedabdulaziz.com/

Linux users: Before starting this guide, you should have a non-root user configured on your server. This user needs to have sudo privileges so that it can perform administrative functions.

## Part 1: Deploying a python flask application using Nginx and uWSGI

### Install Components from the Ubuntu Repositories
For Python 2, type in the terminal:
```
sudo apt-get update
```
```
sudo apt-get install python-pip python-dev nginx
```

For Python 3, type:
```
sudo apt-get update
```
```
sudo apt-get install python3-pip python3-dev nginx
```

### Create a Python Virtual Environment
Next, we'll set up a virtual environment for isolating our Flask application from the other Python files on the system.

Install virtualenv package using pip (if not installed):
For Python 2:
```
sudo pip install virtualenv
```
For Python 3:
```
sudo pip3 install virtualenv
```

Clone the project using git. 
```
git clone https://github.com/demmojo/poetry-generator-app/
```
Move into the directory after you create it:
```
cd ~/poetry-generator-app
```

Create a virtual environment to store our Flask project's Python requirements by typing:
```
virtualenv textgenenv
```

This will install Python and pip into a directory called textgenenv. 

Then we will activate the virtual environment so as to install necessary packages.
```
source textgenenv/bin/activate
```

### Install Packages
Use the local instance of pip to install uWSGI, Flask, Tensorflow and Keras (make sure you are in the virtual environment set above:
```
pip install flask uwsgi tensorflow keras
```

### Set up Flask application
First test the Flask app while in the virtual environment by going to the app directory and running wsgi.py:
```
python wsgi.py
```

To visit the poetry generator page locally, go to the below link in your web browser:
```
shakespeare.localhost:5000
```

You should be able to see the html file given in the templates folder. You can now deactivate the virtual environment:
```
deactivate
```

## Continue if you want to deploy to your own website!
This guide is mainly for Linux based systems such as Ubuntu. However, you will be able to run the python script and host it using the Flask in-build development server simply by running 'main.py'.

### Edit main.py

Change the server name (for this project it is mohamedabdulaziz.com):

```
app.config["SERVER_NAME"] = "mohamedabdulaziz.com"
```

Note: The app will read the subdomain and then route it to the text generator of that subdomain. For example: shakespeare.mohamedabdulaziz.com or nazim.mohamedabdulaziz.com. See the code in main.py for 

### Edit uWSGI configuration file (app.ini)

This will enable us to serve our application using uWSGI. You might need to change these values for your own project. It can be found in the 'app' directory. It's content is given below:

```
[uwsgi]
module = wsgi:app

master = true
processes = 5

socket = app.sock
chmod-socket = 660
vacuum = true

die-on-term = true
```

### Create systemd service unit file 
This will allow Ubuntu to automatically start uWSGI and serve our Flask application whenever the server boots. 

First, create the service file:

```
sudo nano /etc/systemd/system/poetry-generator.service
```
Copy the below text and paste it. Make sure to change any values specific to your own project and server/PC directory paths.
```
[Unit]
Description=uWSGI instance to serve myproject
After=network.target

[Service]
User=demmojo
Group=www-data
WorkingDirectory=/home/demmojo/Projects/poetry-generator-app/app
Environment="PATH=/home/demmojo/Projects/poetry-generator-app/textgenenv/bin"
ExecStart=/home/demmojo/Projects/poetry-generator-app/textgenenv/bin/uwsgi --ini app.ini

[Install]
WantedBy=multi-user.target
```
Make sure to start the service you have just created and allow it to run at startup:
```
sudo systemctl start poetry-generator.service
sudo systemctl enable poetry-generator.service
```

### Configure Nginx and place in the following directory: /etc/nginx/sites-available

We will configure Nginx so that it will pass web requests to the socket file in the project directory.

First we will create a server block configuration file:
```
sudo nano /etc/nginx/sites-available/shakespeare
```

Copy the below text and paste it. Make sure to change any values specific to your own project, server IP and server/PC directory paths.
```
server {
    listen 80;
    server_name shakespeare.mohamedabdulaziz.com;
    
    location / {
        include uwsgi_params;
        uwsgi_pass unix:///home/demmojo/Projects/poetry-generator-app/app/app.sock;
    }
}
```

To enable the Nginx server block configuration we've just created, link the file to the sites-enabled directory:
```
sudo ln -s /etc/nginx/sites-available/shakespeare /etc/nginx/sites-enabled
```

Test for syntax errors:
```
sudo nginx -t
```

If it returns a successful response then restart the Nginx process as well as the uWSGI service you made earlier:
```
sudo systemctl restart nginx
```

Allow access to the Nginx server through the firewall:
```
sudo ufw allow 'Nginx Full'
```

You can see a demo of the project here:
```
https://shakespeare.mohamedabdulaziz.com
```

### Common Issues

1. If you get a 502 bad gateway error. Check the nginx log files using:

```
sudo tail -30 /var/log/nginx/error.log
```

If the app.sock connection failed due to a permission denied error this could be due to Nginx needing to have +x access on all directories leading to the site's root directory.

Ensure you have +x on all of the directories in the path leading to the site's root. For example, if the site root is /home/username/project:
```
chmod +x /home/
chmod +x /home/username
chmod +x /home/username/project
```
