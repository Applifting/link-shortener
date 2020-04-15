# link-shortener

How to use:

- Configure settings.ini with your Client ID and Secret key
- Run 'docker-compose build', then 'docker-compose up'

**GET /api/links**
Responds with a JSON formatted list of all links in the database

**/<link_endpoint>**
Redirects to a url corresponding to its respective endpoint

To do for current pull request:

-

To do before production:

- Hide environment variables
- Change wait_for_db from sleep to pinging the db
