# link-shortener

How to use:

- Configure settings.ini with your Client ID and Secret key
- Run 'docker-compose build', then 'docker-compose up'

**GET /**
Displays a list of all active links and their owners

**GET /my_links**
Authenticates the user, then displays a list of all the user's links
Based on the user's Google id

**/<link_endpoint>**
Redirects to a url corresponding to its respective endpoint


To do before production:

- Hide environment variables
- Change wait_for_db from sleep to pinging the db
- Change href links from localhost to fueled.by
