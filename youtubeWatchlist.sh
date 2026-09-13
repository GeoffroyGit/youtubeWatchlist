#!/bin/bash         

source .venv/bin/activate

if [ $# -eq 1 ]; then
    python3 youtubeWatchlist.py -n $1
else
    python3 youtubeWatchlist.py
fi

deactivate

