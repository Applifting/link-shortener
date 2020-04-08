# link-shortener

How to use:

- Run 'docker-compose build', then 'docker-compose up'

GET /api/links
Responds with a JSON formatted list of all links in the database

/<link_endpoint>
Redirects to the url corresponding to the respective endpoint

To do:

- Use an SQL builder tool (pypika, SQLAlchemy Core)
- Hide environment variables
- Use Listeners to initialise a populate the database
- Use a connection pool instead of connection
