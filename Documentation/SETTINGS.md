Create a settings.ini file, paste this inside:

[settings]
OAUTH_PROVIDER=sanic_oauth.providers.GoogleClient
OAUTH_REDIRECT_URI=<your_domain_uri>/oauth
OAUTH_SCOPE=email
OAUTH_CLIENT_ID=<your_client_id>
OAUTH_CLIENT_SECRET=<your_client_secret>

Notes:

- Your OAUTH_REDIRECT_URI has to match the Redirect URI set in your Google
developer console.
