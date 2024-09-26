#!/usr/bin/env python
import binascii
import yaml
import os

nginx_template = """
server {
    # Redirect HTTP to www
    listen 80;
    server_name fakedomain.com;
    location / {
        rewrite ^/(.*)$ https://www.fakedomain.com/$1 permanent;
    }
}

server {
    # Redirect payloads to HTTPS
    listen 80;
    server_name *.fakedomain.com;
    proxy_set_header X-Forwarded-For $remote_addr;

    return 307 https://$host$request_uri;
    client_max_body_size 500M; # In case we have an extra large payload capture 
}

server {
    # Redirect HTTPS to www
    listen 443 ssl;
    ssl_certificate /etc/nginx/ssl/fakedomain.com.crt; # Wildcard SSL certificate
    ssl_certificate_key /etc/nginx/ssl/fakedomain.com.key; # Wildcard SSL certificate key

    server_name fakedomain.com;
    location / {
        rewrite ^/(.*)$ https://www.fakedomain.com/$1 permanent;
    }
}

server {
    # API proxy
    listen 443 ssl;
    ssl_certificate /etc/nginx/ssl/fakedomain.com.crt; # Wildcard SSL certificate
    ssl_certificate_key /etc/nginx/ssl/fakedomain.com.key; # Wildcard SSL certificate key

    server_name *.fakedomain.com;
    access_log /var/log/nginx/fakedomain.com.vhost.access.log;
    error_log /var/log/nginx/fakedomain.com.vhost.error.log;

    client_max_body_size 500M;

    location / {
        proxy_pass  http://localhost:8888;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
}

server {
    # Redirect api to HTTPS
    listen 80;
    server_name api.fakedomain.com; # Subdomain for API server
    proxy_set_header X-Forwarded-For $remote_addr;

    return 307 https://api.fakedomain.com$request_uri;
    client_max_body_size 500M; # In case we have an extra large payload capture 
}

server {
   # Redirect www to HTTPS
   listen 80;
   server_name www.fakedomain.com;
   location / {
       rewrite ^/(.*)$ https://www.fakedomain.com/$1 permanent;
   }
}

server {
   # GUI proxy
   listen 443 ssl;
   server_name www.fakedomain.com;
   client_max_body_size 500M;
   ssl_certificate /etc/nginx/ssl/fakedomain.com.crt; # Wildcard SSL certificate
   ssl_certificate_key /etc/nginx/ssl/fakedomain.com.key; # Wildcard SSL certificate key

   location / {
       proxy_pass  http://localhost:1234;
       proxy_set_header Host $host;
   }
}
"""

settings = {
    "email_from": "whatismyname836@gmail.com",
    "mailgun_api_key": "",
    "mailgun_sending_domain": "",
    "domain": "",
    "abuse_email": "whatismyname836@gmail.com",
    "cookie_secret": "",
    "postgres_user": "",
    "postgres_password": "",
    "postgres_db": ""
}

print(""" 

██   ██ ███████ ███████ ██     ██  █████  ████████  ██████ ██   ██ ██████   ██████   ██████  
 ██ ██  ██      ██      ██     ██ ██   ██    ██    ██      ██   ██ ██   ██ ██    ██ ██       
  ███   ███████ ███████ ██  █  ██ ███████    ██    ██      ███████ ██   ██ ██    ██ ██   ███ 
 ██ ██       ██      ██ ██ ███ ██ ██   ██    ██    ██      ██   ██ ██   ██ ██    ██ ██    ██ 
██   ██ ███████ ███████  ███ ███  ██   ██    ██     ██████ ██   ██ ██████   ██████   ██████  
                                                                                             
                                                                                             

                                                                                    
                                           XSSWatchdog Setup Utility
""")

hostname = input("Domain (ex. www.example.com): ").strip()
if hostname:
    settings["domain"] = hostname
    nginx_template = nginx_template.replace("fakedomain.com", settings["domain"])
else:
    print("Error: Domain name cannot be empty!")
    exit(1)

settings["mailgun_api_key"] = input("Mailgun API key (ex. key-123abc): ").strip()
settings["mailgun_sending_domain"] = input("Mailgun domain (ex. example.com): ").strip()

settings["postgres_user"] = input("Postgres username (ex. xsshunter): ").strip()
settings["postgres_password"] = input("Postgres password: ").strip()
settings["postgres_db"] = input("Postgres DB (ex. xsshunter): ").strip()

settings["cookie_secret"] = binascii.hexlify(os.urandom(50)).decode('utf-8')

# Save config to YAML
try:
    yaml_config = yaml.dump(settings, default_flow_style=False)
    with open("config.yaml", "w") as config_file:
        config_file.write(yaml_config)
    print("YAML config saved successfully.")
except Exception as e:
    print(f"Error saving YAML config: {e}")
    exit(1)

# Save nginx config
try:
    with open("default", "w") as nginx_file:
        nginx_file.write(nginx_template)
    print("Nginx config saved successfully.")
except Exception as e:
    print(f"Error saving Nginx config: {e}")
    exit(1)

print(f"""
Setup complete! Please now copy the 'default' file to /etc/nginx/sites-enabled/default
sudo cp default /etc/nginx/sites-enabled/default

Ensure your wildcard SSL certificate and key are available at:
    /etc/nginx/ssl/{hostname}.crt
    /etc/nginx/ssl/{hostname}.key

Good luck hunting for XSS!
""")
