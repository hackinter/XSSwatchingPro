```markdown
# XSSWatchdog Setup Utility

XSSWatchdog is a utility designed to help you set up Nginx configurations and manage settings for an XSS monitoring system. This utility simplifies the process of configuring your server to handle XSS payloads and ensures that all necessary components are in place.

## Features

- Generate Nginx configuration for handling HTTP to HTTPS redirection.
- Create a YAML configuration file for managing application settings.
- Automatically generate a secure cookie secret for your application.
- Set up logging for access and errors to help monitor XSS attempts.

## Requirements

- Python 2.7 or higher
- Nginx
- Postgres
- Mailgun account for email notifications

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/hackinter/XSSWatchdog.git
   cd XSSWatchdog
   ```

2. Install the required Python packages:

   ```bash
   pip install pyyaml
   ```

3. Make the setup script executable:

   ```bash
   chmod +x setup.py
   ```

## Usage

1. Run the setup script:

   ```bash
   ./setup.py
   ```

2. Follow the prompts to enter your domain, Mailgun API key, Postgres credentials, and other settings.

3. After completing the setup, copy the generated Nginx configuration file to the appropriate directory:

   ```bash
   sudo cp default /etc/nginx/sites-enabled/default
   ```

4. Ensure that your wildcard SSL certificate and key are placed in `/etc/nginx/ssl/`.

5. Restart Nginx:

   ```bash
   sudo systemctl restart nginx
   ```

## Configuration

The utility generates a `config.yaml` file containing the following settings:

```yaml
email_from: "whatismyname836@gmail.com"
mailgun_api_key: "YOUR_MAILGUN_API_KEY"
mailgun_sending_domain: "YOUR_MAILGUN_DOMAIN"
domain: "YOUR_DOMAIN"
abuse_email: "whatismyname836@gmail.com"
cookie_secret: "GENERATED_COOKIE_SECRET"
postgres_user: "YOUR_POSTGRES_USERNAME"
postgres_password: "YOUR_POSTGRES_PASSWORD"
postgres_db: "YOUR_POSTGRES_DB"
```

### Nginx Configuration

The generated Nginx configuration file (`default`) includes:

- Redirection from HTTP to HTTPS
- API proxy settings
- Logging for access and errors

## Troubleshooting

- Ensure Nginx is installed and running properly.
- Check that the SSL certificate and key are correctly placed in the specified directory.
- Review the logs for any errors or issues in the configuration.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- (HACKINTER)
```

### Customization
Feel free to update any sections, especially the installation instructions, usage, and troubleshooting parts, to fit the specific details and requirements of your project.
