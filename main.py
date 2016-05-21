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
from dateutil import relativedelta
import datetime
import tzlocal
import models
from google.appengine.ext import ndb

Bill = models.Bill
User = models.User

# IDEA: Use a json file to have a precreated set of bills and load them in a class

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#  End of imports


class NewBill(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'curUser': self.request.cookies.get('uName')
        }
        template = JINJA_ENVIRONMENT.get_template('temp/newbill-temp.html')
        self.response.write(template.render(template_values))

    def post(self):
        name = self.request.get("bName")
        date = str(self.request.get("bDate"))
        repeat = self.request.get("bRep")  # IDEA: If curdate is after the bDate, incr by repeat
        amount = self.request.get("bAmt")
        stramount = str(amount)
        fltamount = float(stramount)
        # FIXME: when uploaded to appspot, throws error cannot convert string to float
        # FIXME: but saves to datastore anyway

        date = time.strptime(date, "%Y-%m-%d")

        finDate = datetime.date(year=date.tm_year, month=date.tm_mon, day=date.tm_mday)
        newBill = Bill(bName=name, bDate=finDate, bRepeat=repeat, bAmount=fltamount, bUser=self.request.cookies.get('uName'), bPaid=False)
        newBill.put()

        template_values = {
            'bill': newBill,
            'curUser': self.request.cookies.get('uName')
        }

        template = JINJA_ENVIRONMENT.get_template('temp/success-temp.html')
        self.response.write(template.render(template_values))


class Update(webapp2.RequestHandler):
    def get(self):
        user = User.query(User.uName == self.request.cookies.get('uName')).fetch()[0]
        template_values = {
            'curUser': self.request.cookies.get('uName'),
            'user': user
        }
        template = JINJA_ENVIRONMENT.get_template('temp/update-temp.html')
        self.response.write(template.render(template_values))

    def post(self):
        user = User.query(User.uName == self.request.cookies.get('uName')).fetch()[0]
        add = self.request.get("uAdd")
        rem = self.request.get("uRem")
        cha = self.request.get("uCha")
        init = self.request.get("uInit")
        template_values = {
            'user': user,
            'curUser': self.request.cookies.get('uName')
        }

        if add:
            user.accAmount = user.accAmount + float(add)
            user.put()
            template_values.update({'succ': 'add', 'num': float(add)})
        if rem:
            if user.accAmount > float(rem):
                user.accAmount = user.accAmount - float(rem)
                user.put()
                template_values.update({'succ': 'rem', 'num': float(rem)})
            else:
                template_values.update({'error': 'fundFail', 'num': float(rem)})
        if cha:
            user.accAmount = float(cha)
            user.put()
            template_values.update({'succ': 'cha', 'num': float(cha)})
        if init:
            user.accAmount = float(init)
            user.put()
            template_values.update({'succ': 'init', 'num': float(init)})

        # unpaid bill list
        bList = Bill.query(Bill.bUser == self.request.cookies.get('uName')).fetch()
        unpaid = []

        for b in bList:
            if b.bPaid is False:
                unpaid.append(b)
        template_values.update({'bList': unpaid})

        template = JINJA_ENVIRONMENT.get_template('temp/account-temp.html')
        self.response.write(template.render(template_values))


class Bills(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'bList': Bill.query(Bill.bUser == self.request.cookies.get('uName')).fetch(),
            'curUser': self.request.cookies.get('uName')
        }
        template = JINJA_ENVIRONMENT.get_template('temp/bills-temp.html')
        self.response.write(template.render(template_values))


class BillDetail(webapp2.RequestHandler):
    def get(self, para):
        curBill = Bill.get_by_id(int(para))
        template_values = {
            'curUser': self.request.cookies.get('uName'),
            'bill': curBill
        }
        template = JINJA_ENVIRONMENT.get_template('temp/bill-temp.html')
        self.response.write(template.render(template_values))


class PayBill(webapp2.RequestHandler):
    def post(self, para):
        curBill = Bill.get_by_id(int(para))
        user = User.query(User.uName == self.request.cookies.get('uName')).fetch()[0]

        if user.accAmount < curBill.bAmount:
            template_values = {
                'user': User.query(User.uName == self.request.cookies.get('uName')).fetch()[0],
                'curUser': self.request.cookies.get('uName'),
                'bill': curBill,
                'error': 'insFail'
            }

        else:
            user.accAmount = user.accAmount - curBill.bAmount
            curDate = datetime.datetime.today().date()
            curBill.bPayDate = curDate
            curBill.bPaid = True
            curBill.put()
            user.put()
            template_values = {
                'curUser': self.request.cookies.get('uName'),
                'user': user,
                'billPaid': curBill
            }
            if curBill.bRepeat is not 'never':
                if curBill.bRepeat == 'month':
                    nextDate = curBill.bDate + relativedelta.relativedelta(months=1)

                if curBill.bRepeat == 'week':
                    nextDate = curBill.bDate + relativedelta.relativedelta(weeks=1)

                if curBill.bRepeat == 'year':
                    nextDate = curBill.bDate + relativedelta.relativedelta(years=1)

                nextBill = Bill(bName=curBill.bName, bDate=nextDate, bRepeat=curBill.bRepeat, bAmount=curBill.bAmount, bUser=self.request.cookies.get('uName'), bPaid=False)
                nextBill.put()
                template_values.update({'next': nextBill})

        # updated bill list
        bList = Bill.query(Bill.bUser == self.request.cookies.get('uName')).fetch()
        unpaid = []

        for b in bList:
            if b.bPaid is False:
                unpaid.append(b)

        template_values.update({'bList': unpaid})
        template = JINJA_ENVIRONMENT.get_template('temp/account-temp.html')
        self.response.write(template.render(template_values))


class Register(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'curUser': self.request.cookies.get('uName')
        }
        template = JINJA_ENVIRONMENT.get_template('temp/register-temp.html')
        self.response.write(template.render(template_values))

    def post(self):
        # TODO: Add more try blocks around any data forms
        uName = self.request.get('user')
        raw_password = self.request.get('pass')
        confirm = self.request.get('conf')
        userList = User.query().fetch()
        userCheck = False
        template_values = {}

        if len(User.query(User.uName == uName).fetch(1)) == 0:  # if no user
            self.response.set_cookie('uName', uName, path="/")
            newUser = User(uName=uName, password=raw_password)
            newUser.put()
            template_values.update({'user': newUser, 'succ': 'uReg', 'curUser': self.request.cookies.get('uName')})
            userCheck = True
        else:
            template_values.update({'userFail': uName, 'error': 'uDup'})

        if userCheck:
            template = JINJA_ENVIRONMENT.get_template('temp/account-temp.html')
        else:
            template = JINJA_ENVIRONMENT.get_template('temp/register-temp.html')

        self.response.write(template.render(template_values))


class Login(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'curUser': self.request.cookies.get('uName')
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

    def post(self):
        uName = self.request.get('loginUser')
        password = self.request.get('loginPass')
        attUser = None
        template_values = {}
        login = False

        try:
            attUser = User.query(User.uName == uName).fetch()[0]

        except IndexError:
            if not User.query().fetch():
                template_values.update({'error': 'noUsers'})
                passFail = True
            else:
                template_values.update({'userFail': uName, 'error': 'uNotFound'})
                passFail = True

        else:
            if attUser and attUser.password == password:  # success
                self.response.set_cookie('uName', uName, path="/")
                template_values.update({'user': attUser, 'succ': 'login', 'curUser': attUser.uName})
                login = True

            else:  # fail
                template_values.update({'userFail': uName, 'error': 'passFail'})
                passFail = True

        if login:
            template = JINJA_ENVIRONMENT.get_template('temp/account-temp.html')
        elif passFail:
            template = JINJA_ENVIRONMENT.get_template('index.html')
        else:
            template = JINJA_ENVIRONMENT.get_template('temp/account-temp.html')
        self.response.write(template.render(template_values))


class LogOut(webapp2.RequestHandler):
    def get(self):
        curUser = self.request.cookies.get('uName')
        tempUser = curUser  # used to display user for user logout

        template_values = {
            'user': tempUser
        }
        self.response.delete_cookie('uName')
        template = JINJA_ENVIRONMENT.get_template('temp/logout-temp.html')
        self.response.write(template.render(template_values))


class Account(webapp2.RequestHandler):
    def get(self):
        user = User.query(User.uName == self.request.cookies.get('uName')).fetch()[0]
        bList = Bill.query(Bill.bUser == self.request.cookies.get('uName')).fetch()
        unpaid = []

        for b in bList:
            if b.bPaid is False:
                unpaid.append(b)

        template_values = {
            'user': user,
            'curUser': self.request.cookies.get('uName'),
            'bList': unpaid
        }
        template = JINJA_ENVIRONMENT.get_template('temp/account-temp.html')
        self.response.write(template.render(template_values))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        today = datetime.datetime.now()
        threeWks = today + datetime.timedelta(days=21)
        bList = Bill.query(Bill.bUser == self.request.cookies.get('uName')).fetch()
        upcBills = []
        upcTotal = 0
        print today.date()
        # FIXME: no matter what happens, I cannot get the actual local time. its totally borked
        # print "the tz is "
        # print timezone('US/Central')
        # print datetime.datetime.now(tz=get_localzone())

        # generate unpaid bills for next 3 weeks
        for b in bList:
            if b.bDate < threeWks.date() and b.bDate >= today.date() and not b.bPaid:
                upcTotal = b.bAmount + upcTotal
                upcBills.append(b)

        template_values = {
            'curUser': self.request.cookies.get('uName'),
            'upcoming': upcBills,
            'sum': upcTotal,
            'today': today.date(),
            'happy': datetime.datetime(2016, 5, 19, 0, 0, 0).date()
        }
        if self.request.cookies.get('uName'):
            template_values.update({'user': User.query(User.uName == self.request.cookies.get('uName')).fetch()[0]})
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/newbill', NewBill),
    ('/update', Update),
    ('/bills', Bills),
    (r'/bill/(\w+)', BillDetail),
    ('/reg', Register),
    ('/login', Login),
    ('/logout', LogOut),
    (r'/pay/(\w+)', PayBill),
    ('/account', Account),
    ('/', MainHandler)
], debug=True)
