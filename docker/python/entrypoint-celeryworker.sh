#!/bin/bash

set -o errexit
set -o nounset

exec celery -A leaf.celery.celery worker --loglevel=info