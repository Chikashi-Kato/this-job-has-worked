import os, webapp2, model, logging, jinja2, urllib

TEMPLATE_PATH = os.path.dirname(__file__) + '/views'
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_PATH, encoding='utf8'),
    autoescape=True)

class SignListHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("signList.html")
        signs = model.Sign.getAll()

        data = {}
        data['signs'] = signs

        self.response.out.write(template.render(data))

    def post(self):
        org = self.request.get('org')
        trouble = self.request.get('trouble')
        sign = model.Sign.create(org, trouble)

        return webapp2.redirect(webapp2.uri_for('signList'))

class SignHandler(webapp2.RequestHandler):
    def get(self, id):
        sign = model.Sign.get(urllib.quote(id))
        data = {}
        data['sign'] = sign
        template = jinja_env.get_template("sign.html")

        self.response.out.write(template.render(data))

    def post(self, id):
        reset = self.request.get('reset')

        if not reset:
            self.response.out.write("")
            return
    
        sign = model.Sign.get(urllib.quote(id))
        sign.reset()

        return webapp2.redirect(webapp2.uri_for('sign', id=urllib.unquote(sign.sign_id)))

app = webapp2.WSGIApplication([
        webapp2.Route('/sign/<id>', handler=SignHandler, name='sign'),
        webapp2.Route('/sign/', handler=SignListHandler, name='signList')
], debug=True)
