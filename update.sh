#!/bin/sh

env = "python3 -m pip"
$env install --upgrade aiohttp --user
$env install --upgrade websockets --user
$env install --upgrade PyNaCl --user
$env install --upgrade "https://github.com/Rapptz/discord.py/archive/rewrite.zip#egg=discord.py[voice]" --user --no-dependencies
$env install --upgrade praw --user