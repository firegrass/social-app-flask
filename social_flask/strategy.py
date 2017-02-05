from flask import current_app, request, redirect, make_response, session, \
                  render_template, render_template_string

from social_core.utils import build_absolute_uri
from social_core.strategy import BaseStrategy, BaseTemplateStrategy


class FlaskTemplateStrategy(BaseTemplateStrategy):
    def render_template(self, tpl, context):
        return render_template(tpl, **context)

    def render_string(self, html, context):
        return render_template_string(html, **context)


class FlaskStrategy(BaseStrategy):
    DEFAULT_TEMPLATE_STRATEGY = FlaskTemplateStrategy

    def get_setting(self, name):
        return current_app.config[name]

    def request_data(self, merge=True):
        if merge:
            data = request.form.copy()
            data.update(request.args)
        elif request.method == 'POST':
            data = request.form
        else:
            data = request.args
        return data

    def request_host(self):
        return request.host

    def request_is_secure(self):
        return request.is_secure

    def request_path(self):
        return request.path

    def request_get(self):
        return request.args.copy()

    def request_post(self):
        return request.form.copy()

    def request_port(self):
        return request.environ['SERVER_PORT']

    def redirect(self, url):
        return redirect(url)

    def html(self, content):
        response = make_response(content)
        response.headers['Content-Type'] = 'text/html;charset=UTF-8'
        return response

    def session_get(self, name, default=None):
        return session.get(name, default)

    def session_set(self, name, value):
        session[name] = value

    def session_pop(self, name):
        return session.pop(name, None)

    def session_setdefault(self, name, value):
        return session.setdefault(name, value)

    def build_absolute_uri(self, path=None):
        return build_absolute_uri(request.host_url, path)
