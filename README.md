# link-shortener

How to use:

- Run 'docker-compose build', then 'docker-compose up'

GET /api/links
Responds with a JSON formatted list of all links in the database

/<link_endpoint>
Redirects to a url corresponding to its respective endpoint

To do:

- Create engine within the before-server-start listener
- Hide environment variables (before production)
