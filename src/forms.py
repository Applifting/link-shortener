'''
Copyright (C) 2020 Link Shortener Authors (see AUTHORS in Documentation).
Licensed under the MIT (Expat) License (see LICENSE in Documentation).
'''
from sanic import Blueprint
from sanic.response import redirect, html

from sanic_wtf import SanicForm

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


forms_blueprint = Blueprint('forms')


class CreateForm(SanicForm):
    endpoint = StringField('Endpoint', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired()])
    submit = SubmitField('Create')


@forms_blueprint.route('/create', methods=['GET', 'POST'])
async def create_link(request):
    form = CreateForm(request)
    if request.method == 'POST' and form.validate():
        endpoint = form.endpoint.data
        url = form.url.data
        print('New link: Endpoint = {}, URL = {}'.format(endpoint, url))
        return redirect('/')

    content = f"""
    <div class="container">
    <form action="" method="POST" width="50%">
      <h1>Create a new link</h1>
      {'<br>'.join(form.csrf_token.errors)}
      {form.csrf_token}
      {'<br>'.join(form.endpoint.errors)}
      <br>
      Endpoint: {form.endpoint(size=20, placeholder="")}
      <br>
      URL: {form.url(size=20, placeholder="")}
      <br>
      {form.submit}
    </form>
    """
    base = open('src/templates/base.html', 'r').read()
    appendix = open('src/templates/forms/create_form.html', 'r').read()

    return html(base + content + appendix)
