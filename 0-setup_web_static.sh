#!/usr/bin/env bash
# Script that sets up your web servers for the deployment of web_static

sudo apt-get update
sudo apt-get -y install nginx

#Create the folder /data/ if it doesn’t already exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

#Create a fake HTML file /data/web_static/releases/test/index.html

sudo touch /data/web_static/releases/test/index.html

#Write a fake HTML content

echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body> " > /data/web_static/releases/test/index.html

#Create a symbolic link /data/web_static/current linked to the /data/web_static/releases/test/ folder

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

#Give ownership of the /data/ folder to the ubuntu user AND group (you can assume this user and group exist). This should be recursive; everything inside should be created/owned by this user/group.

sudo chown -R ubuntu:ubuntu /data/
sudo chown -R ubuntu:ubuntu /etc/nginx/sites-available/default

#Write the Nginx configuration to file

echo "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html index.htm;
    }
    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }
    error_page 404 /404.html;
    location = /404.html {
        root /var/www/html;
        internal;
    }
}" > /etc/nginx/sites-enabled/default

#Restart nginx
sudo service nginx restart
