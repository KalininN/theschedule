# -*- coding: utf-8 -*-

import datetime

import unittest2
import webapp2
from google.appengine.ext import testbed

import main
from objects.pair import ScheduledPair


class PairsTest(unittest2.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()

    @staticmethod
    def make_request(url, method, body=''):
        request = webapp2.Request.blank(url)
        request.method = method
        request.body = body
        return request.get_response(main.application)

    @staticmethod
    def post_pair(pair, key=''):
        body = 'classname=' + pair.classname +\
            '&year=' + str(pair.date.year) +\
            '&month=' + str(pair.date.month) +\
            '&day=' + str(pair.date.day) +\
            '&hour=' + str(pair.start_time.hour) +\
            '&minute=' + str(pair.start_time.minute) + '&task=' + pair.task +\
            '&key=' + key
        return PairsTest.make_request('/pairs', 'POST', body)

    def check_pair_fields(self, pair1, pair2):
        self.assertEqual(pair1.classname,  pair2.classname)
        self.assertEqual(pair1.date,       pair2.date)
        self.assertEqual(pair1.start_time, pair2.start_time)
        self.assertEqual(pair1.task,       pair2.task)

    def test_create_pair(self):
        response = PairsTest.make_request('/new_pair', 'GET')
        self.assertEqual(response.status_int, 200)
        pair = ScheduledPair(classname='Math',
                             date=datetime.date(2015, 4, 14),
                             start_time=datetime.time(9, 40),
                             task='some_task')
        response = PairsTest.post_pair(pair)
        self.assertEqual(response.status_int, 302)
        pairs_list = ScheduledPair.query().fetch(2)
        self.assertEqual(len(pairs_list), 1)
        added_pair = pairs_list[0]
        self.check_pair_fields(added_pair, pair)
        response = PairsTest.make_request('/pairs', 'GET')
        self.assertEqual(response.status_int, 200)

    def test_edit_pair(self):
        pair = ScheduledPair(classname='Math',
                             date=datetime.date(2015, 4, 14),
                             start_time=datetime.time(9, 40),
                             task='some_task')
        response = PairsTest.post_pair(pair)
        added_pair = ScheduledPair.query().fetch(2)[0]
        response = PairsTest.make_request('/edit_pair?key=' +
                                          added_pair.key.urlsafe(), 'GET')
        self.assertEqual(response.status_int, 200)
        pair = ScheduledPair(classname='Math1',
                             date=datetime.date(2016, 5, 15),
                             start_time=datetime.time(10, 41),
                             task='some_task1')
        response = PairsTest.post_pair(pair, added_pair.key.urlsafe())
        self.assertEqual(response.status_int, 302)
        pairs_list = ScheduledPair.query().fetch(2)
        self.assertEqual(len(pairs_list), 1)
        added_pair = pairs_list[0]
        self.check_pair_fields(added_pair, pair)
        response = PairsTest.make_request('/pairs', 'GET')
        self.assertEqual(response.status_int, 200)

    def tearDown(self):
        self.testbed.deactivate()


if __name__ == '__main__':
    unittest2.main()