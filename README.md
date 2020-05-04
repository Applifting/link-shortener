# link-shortener

How to use:

- Configure settings.ini with your Client ID and Secret key
- Run 'docker-compose build', then 'docker-compose up'

How to test:

- Run 'docker-compose run web sh -c "pytest --disable-pytest-warnings"'
- All or most of the warnings should be about async syntax deprecation,
as sanic_oauth has old/deprecated versions of dependencies (httpx et al.)

**/**
Landing page - Redirects to /links/about.

**/links/about**
Displays information about the page.

**/<link_endpoint>**
Redirects to the URL corresponding to its respective endpoint.

**/links/all**
Displays a list of all active links and their owners.

**/links/me**
Authenticates the user, then displays a list of all the user's links.
Based on the user's Google id.

**/create**
A form for creating new links. If an active link with the same endpoint
already exists, an error will be thrown.

**/edit/active/<link_id>**
A form for updating the URL of an active link pointed to via the id
specified within the endpoint's link_id parameter.

**/edit/inactive/<link_id>**
A form for updating the URL of an inactive link pointed to via the id
specified within the endpoint's link_id parameter.

**/deactivate/<link_id>**
Deactivates the active link pointed to via the id specified
within the endpoint's link_id parameter.

**/activate/<link_id>**
Activates the inactive link pointed to via the id specified
within the endpoint's link_id parameter.

**/delete/<status>/<link_id>**
Status = {'active', 'inactive'}.
Deletes the link with the status and the id specified by
the endpoint's respective parameters status and link_id.

**/reset/<status>/<link_id>**
Status = {'active', 'inactive'}.
Resets the password of the link with the status and the id specified by
the endpoint's respective parameters status and link_id.

**/get_links** (API)
Displays a JSON formatted data from the database - health check for development.

**/authorize/<link_id>**
A form for entering a password for an active link pointed to via the id
specified within the endpoint's link_id parameter.
An automatic redirection target for accessing any link secured by a password.
Submitting a correct password results in redirection to the link's
specific URL.


To do eventually:

- Overview HTTP error codes and create templates to display them to users
- Write unit tests

To do before production:

- Hide environment variables
- Change DB configuration
- Change wait_for_db from sleep to pinging the db
