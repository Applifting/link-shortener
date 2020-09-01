Create a settings.ini file, paste this inside:

[settings]
PRODUCTION=True/False

OAUTH_PROVIDER=sanic_oauth.providers.GoogleClient
OAUTH_REDIRECT_URI=/oauth
OAUTH_SCOPE=email
OAUTH_CLIENT_ID=<your_client_id>
OAUTH_CLIENT_SECRET=<your_client_secret>

SENTRY_DSN=<sentry_dsn>

DOMAIN_NAME=<your_production_domain>
LOCAL_HOST=http://localhost:8000

WHITELISTED_EMAIL_1=<email_domain_1>
WHITELISTED_EMAIL_2=<email_domain_2>
...
WHITELISTED_EMAIL_N=<email_domain_n>

MYSQL_HOST=<mysql_host_name>
MYSQL_DB=<mysql_db_name>
MYSQL_USER=<mysql_user_name>
MYSQL_PASSWORD=<mysql_password>
MYSQL_PORT=<mysql_db_port> (Most likely 3306)

Notes:

- Your OAUTH_REDIRECT_URI has to match the Redirect URI set in your Google
developer console.
- List whitelisted domains without the @ symbol ('gmail.com' for example)
