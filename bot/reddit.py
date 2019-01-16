import discord, asyncio, praw, random, re

async def animemes(client, message):
    subreddit = client.reddit_app.subreddit("Animemes")
    
    submission = None
    hot_submissions = list(subreddit.hot(limit = 75))
    
    while True:
        random.seed()
        submission = random.choice(hot_submissions)

        if re.match(".*\.(jpg|png)", submission.url):
            break

    embed = discord.Embed(title="Animemes", description=submission.title, color=discord.Colour.dark_red())
    embed.set_footer(text="Created by {}".format(submission.author.name), icon_url=submission.author.icon_img)
    embed.set_image(url=submission.url)

    await message.channel.send(submission.permalink, embed=embed) 