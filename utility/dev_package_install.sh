#! /usr/bin/env bash

if [ "${DJANGO_DEBUG}" == "True" ]; then
	echo "Dev environment, installing dev libraries"
	pip install -r test_requirements.txt
else
	echo "Not a dev environment. Skipping dev library installation."
fi
