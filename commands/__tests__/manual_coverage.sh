#!/usr/bin/env bash
coverage erase
coverage run --omit="*/routing.py" --source=roommatefinder.apps.api src/roommatefinder/manage.py test roommatefinder.apps.api --settings=roommatefinder.settings.test
coverage report