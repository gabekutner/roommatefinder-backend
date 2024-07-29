#!/usr/bin/env bash
coverage erase
coverage run --source=src.roommatefinder.roommatefinder.apps.api src/roommatefinder/manage.py test src.roommatefinder.roommatefinder.apps.api --settings=src.roommatefinder.roommatefinder.settings.test
coverage report