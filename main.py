# -*- coding: utf-8 -*-

import os


import jinja2
import webapp2

import environment
from handlers import pairs
from handlers import schedule
from handlers import crons


application = webapp2.WSGIApplication([
    webapp2.Route(r'/<group_id:[-\w]+>/pairs',
                  handler=pairs.ShowPairs,
                  name='pairs list'),
    webapp2.Route(r'/<group_id:[-\w]+>/new_pair',
                  handler=pairs.NewPair,
                  name='create pair'),
    webapp2.Route(r'/<group_id:[-\w]+>/edit_pair',
                  handler=pairs.EditPair,
                  name='edit pair'),
    webapp2.Route(r'/<group_id:[-\w]+>/',
                  handler=pairs.ShowSchedule,
                  name='schedule'),
    webapp2.Route(r'/<group_id:[-\w]+>/schedule',
                  handler=schedule.ShowDefaultSchedule,
                  name='show default schedule'),
    webapp2.Route(r'/<group_id:[-\w]+>/default_pairs',
                  handler=schedule.ShowDefaultPairs,
                  name='show default pairs'),
    webapp2.Route(r'/<group_id:[-\w]+>/edit_default_pair',
                  handler=schedule.EditDefaultPair,
                  name='edit default pair'),
    webapp2.Route(r'/<group_id:[-\w]+>/new_default_pair',
                  handler=schedule.NewDefaultPair,
                  name='create default pair'),
    webapp2.Route(r'/<group_id:[-\w]+>/delete_pair',
                  handler=pairs.DeletePair,
                  name='delete pair'),
    webapp2.Route(r'/<group_id:[-\w]+>/copy_from_default',
                  handler=schedule.CopyFromDefault,
                  name='copy from default'),
    webapp2.Route(r'/<group_id:[-\w]+>/schedule_settings',
                  handler=schedule.EditSettings,
                  name='schedule settings'),
    ('/cron/delete_old', crons.DeleteOld)
], debug=True)
