Create a settings.ini file, paste this inside:

[settings]
OAUTH_PROVIDER=sanic_oauth.providers.GoogleClient
OAUTH_REDIRECT_URI=<your_domain_uri>/oauth
OAUTH_SCOPE=email
OAUTH_CLIENT_ID=<your_client_id>
OAUTH_CLIENT_SECRET=<your_client_secret>

WTF_CSRF_SECRET_KEY=<generated_key>

DOMAIN_NAME=<your_domain>

WHITELISTED_EMAIL_1=<email_domain_1>
WHITELISTED_EMAIL_2=<email_domain_2>
...
WHITELISTED_EMAIL_N=<email_domain_n>

Notes:

- Your OAUTH_REDIRECT_URI has to match the Redirect URI set in your Google
developer console.
- List whitelisted domains without the @ symbol ('gmail.com' for example)
