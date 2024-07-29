#!/usr/bin/env bash

echo "Starting ${GITHUB_WORKFLOW}:${GITHUB_ACTION}"

MIN_COVERAGE=85

coverage erase
coverage run --source=roommatefinder.apps.api src/roommatefinder/manage.py test roommatefinder.apps.api --settings=roommatefinder.settings.test

# get coverage report
COVERAGE_RESULT=`coverage report | grep TOTAL | awk 'N=1 {print $NF}' | sed 's/%//g'`
if [[ $COVERAGE_RESULT -gt $MIN_COVERAGE ]]; then
  echo "{coverage_result}={$COVERAGE_RESULT}" >> $GITHUB_OUTPUT
else
  echo "Code coverage below allowed threshold ($COVERAGE_RESULT<$MIN_COVERAGE)"
  exit 1
fi 

echo "Completed ${GITHUB_WORKFLOW}:${GITHUB_ACTION}"