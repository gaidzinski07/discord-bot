import discord, asyncio, praw, random, re

async def animemes(marshall, message):
    subreddit = marshall.reddit_app.subreddit("Animemes")
    urls_with_img = list()
    for submission in subreddit.hot(limit = 25):
        if re.match(".*\.(jpg|png)", submission.url):
            urls_with_img.append(submission.url)

    random.seed()
    image = random.choice(urls_with_img)
    await message.channel.send(image)