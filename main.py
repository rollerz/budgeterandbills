#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import urllib
import os
import time
import datetime
import models
from google.appengine.ext import ndb

Bill = models.Bill
Account = models.Account

# IDEA: Use a json file to have a precreated set of bills and load them in a class

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#  End of imports
# IDEA: The jinja2 temp is always index.html? Because Angular?
# IDEA: write class that is run maybe always that checks bill dates and increments


class NewBill(webapp2.RequestHandler):
    def post(self):
        name = self.request.get("bName")
        date = str(self.request.get("bDate"))
        repeat = self.request.get("bRep")  # IDEA: If curdate is after the bDate, incr by repeat
        amount = float(self.request.get("bAmt"))

        date = time.strptime(date, "%Y-%m-%d")

        finDate = datetime.date(year=date.tm_year, month=date.tm_mon, day=date.tm_mday)
        newBill = Bill(bName=name, bDate=finDate, bRepeat=repeat, bAmount=amount)
        newBill.put()
        # TODO: Maybe check to see if bill name is taken, tho not indexed

        template_values = {
            'bill': newBill
        }

        template = JINJA_ENVIRONMENT.get_template('success-temp.html')
        self.response.write(template.render(template_values))


class Update(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('update.html')
        self.response.write(template.render())


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())
# IDEA: Use webapp2 to load jinja2 templates from routeparams? ('#/bills', ListBills)?
app = webapp2.WSGIApplication([
    ('/newBill', NewBill),
    ('/update', Update),
    ('/', MainHandler)
], debug=True)
