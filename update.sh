env="python3"
pip="$env -m pip"

$pip install -U praw --user
$pip install -U "https://github.com/Rapptz/discord.py/archive/rewrite.zip#egg=discord.py[voice]" --user
