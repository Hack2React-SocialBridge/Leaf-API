#!/bin/bash

set -o errexit
set -o nounset

exec celery -A leaf.config.celery.celery worker --loglevel=info
