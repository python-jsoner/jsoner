#!/usr/bin/env bash

cleanup() {
    rv=$?
    # on exit code 1 this is normal (some tests failed), do not stop the build
    if [ "$rv" = "1" ]; then
        exit 0
    else
        exit $rv
    fi
}

trap "cleanup" INT TERM EXIT

# First the raw for coverage
echo -e "\n\n****** Running tests ******\n\n"
if [ "${TRAVIS_PYTHON_VERSION}" = "3.5" ]; then
   # full
   coverage run --source jsoner -m pytest --junitxml=reports/junit/junit.xml --html=reports/junit/report.html -v jsoner/tests/
   # buggy
   # python -m pytest --junitxml=reports/junit/junit.xml --html=reports/junit/report.html --cov-report term-missing --cov=./jsoner -v jsoner/tests/
else
   # faster - skip coverage and html report
   python -m pytest --junitxml=reports/junit/junit.xml -v jsoner/tests/
fi
