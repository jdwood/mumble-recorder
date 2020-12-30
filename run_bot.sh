#/bin/sh

eval $(cat .env)

python -m stenographer.bot.bot.py
