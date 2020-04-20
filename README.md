# link-shortener

How to use:

- Configure settings.ini with your Client ID and Secret key
- Run 'docker-compose build', then 'docker-compose up'

**/**
Landing page - About

**/links/all**
Displays a list of all active links and their owners

**/links/me**
Authenticates the user, then displays a list of all the user's links
Based on the user's Google id

**/<link_endpoint>**
Redirects to a url corresponding to its respective endpoint

**/db_all** (development only)
Displays a JSON formatted data from the database - health check for development


To do eventually:

- Forbid using endpoints that already exist as part of the application
- Overview HTTP error codes and create templates to display them to users
- Write unit tests

To do before production:

- Hide environment variables
- Change DB configuration
- Change wait_for_db from sleep to pinging the db
- Change href links from localhost to fueled.by
