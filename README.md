# link-shortener

How to use:

- Configure settings.ini with your Client ID and Secret key
- Run 'docker-compose build', then 'docker-compose up'

How to test:

- Run 'docker-compose run web sh -c "pytest --disable-pytest-warnings"'
- All or most of the warnings should be about async syntax deprecation,
as sanic_oauth has old/deprecated versions of dependencies (httpx et al.)

**/**
Landing page - Redirects to About

**/links/about**
Displays information about the page

**/<link_endpoint>**
Redirects to a url corresponding to its respective endpoint

**/links/all**
Displays a list of all active links and their owners

**/links/me**
Authenticates the user, then displays a list of all the user's links
Based on the user's Google id

**/create**
A form for creating a new link. If an active link with the same endpoint
already exists, the new link will be created as inactive

**/edit/active/<link_id>**
A form for updating the URL of an active link pointed to via the id
specified within of the endpoint

**/edit/inactive/<link_id>**
A form for updating the URL of an inactive link pointed to via the id
specified within of the endpoint

**/deactivate/<link_id>**
Deactivates an active link pointed to via the id specified
within of the endpoint

**/activate/<link_id>**
Activates an inactive link pointed to via the id specified
within of the endpoint

**/delete/<status>/<link_id>** Status = {'active', 'inactive'}
Deletes a link with a status and id specified by the respective parameters
within the endpoint

**/get_links** (API)
Displays a JSON formatted data from the database - health check for development


To do eventually:

- Overview HTTP error codes and create templates to display them to users
- Write unit tests

To do before production:

- Hide environment variables
- Change DB configuration
- Change wait_for_db from sleep to pinging the db
