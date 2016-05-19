from google.appengine.ext import ndb


class Bill(ndb.Model):
    bName = ndb.StringProperty(indexed=False)
    bDate = ndb.DateProperty(indexed=False)
    bRepeat = ndb.StringProperty(indexed=False)
    bAmount = ndb.FloatProperty(indexed=False)
    bUser = ndb.StringProperty(indexed=True)
    bPaid = ndb.BooleanProperty(indexed=True)
    bPayDate = ndb.DateProperty(indexed=False)


class User(ndb.Model):
    uName = ndb.StringProperty(indexed=True)
    password = ndb.StringProperty(indexed=False)
    accAmount = ndb.FloatProperty(indexed=False)
