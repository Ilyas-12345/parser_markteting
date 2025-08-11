#!/bin/bash

echo "Running migrations..."

cd /parser
alembic -c migration/alembic.ini upgrade head

echo "Migration up!"