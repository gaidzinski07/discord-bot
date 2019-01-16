import discord, asyncio, praw, random, re

async def animemes(marshall, message):
    subreddit = marshall.reddit_app.subreddit("Animemes")
    submissions_with_img = list()

    for submission in subreddit.hot(limit = 50):
        if re.match(".*\.(jpg|png)", submission.url):
            submissions_with_img.append(submission)

    random.seed()
    submission = random.choice(submissions_with_img)
    embed = discord.Embed(title="Animemes", description=submission.title, color=discord.Colour.dark_red())
    embed.set_footer(text="Created by {}".format(submission.author.name), icon_url=submission.author.icon_img)
    embed.set_image(url=submission.url)
    await message.channel.send(embed=embed) 