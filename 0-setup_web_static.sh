#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static

if ! command -y -v nginx &> /dev/null; then
	sudo apt-get update
	sudo apt-get install nginx -y
fi

sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

echo "<html><head><title>Test Page</title></head><body>This is a test page</body></html>" | sudo tee /data/web_static/releases/test/index.html >/dev/null

sudo rm -rf /data/web_static/current
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

config_block="
server {
    listen 80;
    listen [::]:80;
    server_name naimah.tech;

    location /hbnb_static/ {
        alias /data/web_static/current/;
    }
}
"
echo "$config_block" | sudo tee /etc/nginx/sites-available/mydomainname.tech >/dev/null
sudo ln -sf /etc/nginx/sites-available/mydomainname.tech /etc/nginx/sites-enabled/mydomainname.tech

sudo service nginx restart

exit 0
