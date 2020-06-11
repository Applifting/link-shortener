# link-shortener

How to use:

- Configure settings.ini with your Client ID and Secret key
- Run 'docker-compose build', then 'docker-compose up'

How to test:

- Run 'docker-compose down' and 'docker-compose up', the DB has to be fresh
for the tests to work
- Run 'docker-compose run web sh -c "pytest --disable-pytest-warnings"'
- All or most of the warnings should be about async syntax deprecation,
as sanic_oauth has old/deprecated versions of dependencies (httpx et al.)

**/**
Landing page - Redirects to /links/about.

**/links/about**
Displays information about the application.

**/<link_endpoint>**
Redirects to the URL corresponding to its respective endpoint.

**/links/all**
Displays a list of all active links and their owners.

**/links/me**
Displays a list of all links created by the authenticated user.

**/create**
A form for creating new links. Creating a link with identical endpoint to an already
existing active link is not allowed.

**/edit/<link_id>**
A form for updating attributes of a link identified by the endpoint's
link_id parameter.

**/deactivate/<link_id>**
Deactivates an active link identified by the endpoint's link_id parameter.
If a deactivation date had been set, it will not be carried over.

**/activate/<link_id>**
Activates an inactive link identified by the endpoint's link_id parameter.
If an activation date had been set, it will not be carried over.

**/delete/<link_id>**
Deletes a link identified by the endpoint's link_id parameter.

**/reset/<link_id>**
Resets password of a link identified by the endpoint's link_id parameter.

**/authorize/<link_id>**
A form for submitting a password of a link identified by the endpoint's
link_id parameter.
Attempts at accessing password secured links will be automatically redirected
to this endpoint.
Submitting the correct password results in redirection to the link's
specific URL.


To do before production:

- Change wait_for_db from sleep to pinging the db
