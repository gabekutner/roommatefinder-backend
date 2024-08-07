#!/usr/bin/env bash

echo "Starting ${GITHUB_WORKFLOW}:${GITHUB_ACTION}"

# source project config
source project.config

coverage erase
# updated 07/30 : ignore the routing.py file - no executable code
coverage run --omit="*/routing.py" --source=roommatefinder.apps.api src/roommatefinder/manage.py test roommatefinder.apps.api --settings=roommatefinder.settings.test

# get coverage report
COVERAGE_RESULT=`coverage report | grep TOTAL | awk 'N=1 {print $NF}' | sed 's/%//g'`
if [[ $COVERAGE_RESULT -gt $MIN_COVERAGE ]]; then
  # echo ""{coverage_result}={$COVERAGE_RESULT}" >> $GITHUB_OUTPUT"
  echo "Coverage result: {$COVERAGE_RESULT}"
else
  echo "Code coverage below allowed threshold ($COVERAGE_RESULT<$MIN_COVERAGE)"
  exit 1
fi 

echo "Completed ${GITHUB_WORKFLOW}:${GITHUB_ACTION}"