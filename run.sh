#!/usr/bin/env bash
source 'env/bin/activate'
pip install -r requirements.txt
python server.py collectstatic --noinput
python server.py migrate --noinput
