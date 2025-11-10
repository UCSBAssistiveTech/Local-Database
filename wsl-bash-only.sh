#!/bin/bash

# starts everything but it will only work on wsl
docker compose up -d
explorer.exe `wslpath -w "app/test/static/index.html"`
python3 app/main.py