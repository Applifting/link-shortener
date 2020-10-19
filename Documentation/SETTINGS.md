Create a settings.ini file, paste this inside:

[settings]
PRODUCTION=True/False

WTF_CSRF_SECRET_KEY=<your_key>
ACCESS_TOKEN=<your_api_token>

OAUTH_PROVIDER=sanic_oauth.providers.GoogleClient
OAUTH_REDIRECT_ENDPOINT=/oauth
OAUTH_REDIRECT_URI=http://localhost:8000/oauth
OAUTH_SCOPE=email
OAUTH_CLIENT_ID=<your_client_id>
OAUTH_CLIENT_SECRET=<your_client_secret>

SENTRY_DSN=<sentry_dsn>
ANALYTICS_DSN=<google_analytics_dsn>
ANALYTICS_ID=<google_analytics_id>

DOMAIN_NAME=<your_production_domain>
LOCAL_HOST=http://localhost:8000
DEFAULT_PASSWORD=<random_string>

WHITELISTED_EMAIL_1=<email_domain_1>
WHITELISTED_EMAIL_2=<email_domain_2>
...
WHITELISTED_EMAIL_N=<email_domain_n>

POSTGRES_HOST=<postgresql_host_name>
POSTGRES_DB=<postgresql_db_name>
POSTGRES_USER=<postgresql_user_name>
POSTGRES_PASSWORD=<postgresql_password>
POSTGRES_PORT=<postgresql_db_port> (Most likely 5432)
SSL_MODE=<prefer/require/other>

Notes:

- Your OAUTH_REDIRECT_URI has to match the Redirect URI set in your Google
developer console.
- List whitelisted domains without the @ symbol ('gmail.com' for example)
