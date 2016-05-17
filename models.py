from google.appengine.ext import ndb

# IDEA: Add a user model for login and stuff


class Bill(ndb.Model):
    bName = ndb.StringProperty(indexed=False)
    bDate = ndb.DateProperty(indexed=False)
    bRepeat = ndb.StringProperty(indexed=False)
    bAmount = ndb.FloatProperty(indexed=False)


class Account(ndb.Model):
    accAmount = ndb.FloatProperty(indexed=False)
    accBills = ndb.StructuredProperty(Bill, repeated=True)
