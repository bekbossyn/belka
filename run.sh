#!/usr/bin/env bash
source '/root/dev/envs/belka_env/bin/activate'
pip install -r requirements.txt
python server.py collectstatic --noinput
python server.py migrate --noinput

