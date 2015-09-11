from google.appengine.ext import ndb
import logging, datetime, urllib

class JsonConvertableDateTimeProperty(ndb.DateTimeProperty):
    def  _get_for_dict(self, entity):
        value = self._get_value(entity) 
        return value.strftime('%Y-%m-%dT%H:%M:%S') if value is not None else None

class Sign(ndb.Model):
    sign_id = ndb.StringProperty(required=True)
    org = ndb.StringProperty(required=True)
    days = ndb.ComputedProperty(lambda self: self.name.lower())
    trouble = ndb.StringProperty(required=True)
    reseted = JsonConvertableDateTimeProperty(auto_now_add=True)
    created = JsonConvertableDateTimeProperty(auto_now_add=True)

    @classmethod
    def create(cls, org, trouble):
        sign = cls.get(urllib.quote(org + trouble))
        if sign:
            return sign

        record = cls()
        record.sign_id = urllib.quote(org + trouble)
        record.org = org
        record.trouble = trouble
        record.put()

        return record

    @classmethod
    def getAll(cls):
        return cls.query().fetch(1000)

    @classmethod
    def get(cls, id):
        return cls.query(cls.sign_id == id).get()

    @property
    def days(self):
        return (datetime.datetime.now() - self.reseted).days

    def reset(self):
        self.reseted = datetime.datetime.now()
        self.put()

        return self

