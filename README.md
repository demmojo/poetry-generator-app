# text-gen-flask
This guide will be divided into two parts. First, how to deploy a python application using flask, using uWSGI application server and Nginx as the front-end reverse proxy on a server. And second, how to serve your own web app with custom pre-trained models for prediction.

You can use this guide as a way to serve web apps that generate predictions using pre-trained models on your server. The web app will be served using uWSGI application server and Nginx as the front-end reverse proxy.

For a live demonstration head on to: https://nazim.mohamedabdulaziz.com/

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

Make a parent directory for our Flask project. 
```mkdir ~/myproject```
Move into the directory after you create it:
```
cd ~/myproject
```

Create a virtual environment to store our Flask project's Python requirements by typing:
```
virtualenv myprojectenv
```

This will install Python and pip into a directory called myprojectenv. 

Then we will activate the virtual environment so as to install necessary packages.
```
source myprojectenv/bin/activate
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

Visit your server's domain name or IP address followed by :5000 in your web browser:
```
http://server_IP_or_domain:5000
```

You should be able to see the html file given in the templates folder. You can now deactivate the virtual environment:
```
deactivate
```
This guide is mainly for Linux based systems such as Ubuntu. However, you will be able to run the python script and host it using the Flask in-build development server simply by running 'main.py'.

### Edit uWSGI configuration file (app.ini)

This will enable us to serve our application using uWSGI. You might need to change these values for your own projects.

### Create systemd service unit file 
This will allow Ubuntu to automatically start uWSGI and serve our Flask application whenever the server boots. 

```
sudo nano /etc/systemd/system/text-gen.service
```

Copy the text in the text-gen.service file found in the directory 'files to be moved' and paste it. Make sure to change any values specific to your own project and server/PC directory paths.

### Configure Nginx and place in the following directory: /etc/nginx/sites-available

We will configure Nginx so that it will pass web requests to the socket file in the project directory.

First we will create a server block configuration file:
```
sudo nano /etc/nginx/sites-available/text-gen
```

Copy the text in the 'text-gen.txt' file found in the directory 'files to be moved' and paste it. Make sure to change any values specific to your own project, server IP and server/PC directory paths.

To enable the Nginx server block configuration we've just created, link the file to the sites-enabled directory:
```
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```

Test for syntax errors:
```
nginx -t
```

If it returns a successful response then restart the Nginx process:
```
sudo systemctl restart nginx
```

Allow access to the Nginx server through the firewall:
```
sudo ufw allow 'Nginx Full'
```

You can now go to your own server's IP or domain name in your web browser:
```
http://server_IP_or_domain:5000
```

Which should show your web app page.

## Part 2: Using your own custom pre-trained models (Under construction)
