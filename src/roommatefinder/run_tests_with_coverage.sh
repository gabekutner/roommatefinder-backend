#!/usr/bin/env bash
coverage erase
coverage run --source=roommatefinder.apps.api manage.py test roommatefinder.apps.api --settings=roommatefinder.settings.test
coverage report