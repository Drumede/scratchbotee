# bot.py
import os
import random
import main
import scratchattach
from datetime import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
import html
import embeds

load_dotenv()
TOKEN = os.environ.get("TOKEN")
GUILD = "just bonus emojis for nitro people (2/2)"
#intents = discord.Intents.default()
#intents.message_content = True

activity = discord.Activity(type=discord.ActivityType.watching, name="for >help")
bot = commands.Bot(command_prefix=">", intents=discord.Intents.all(),activity=activity)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to the following guilds:')
    for x in bot.guilds:
        print(
            f'{x.name}(id: {x.id})'
        )

#@bot.command(name='search')
#async def search(ctx):


@bot.event
async def on_message(message):
    if message.author == bot.user or message.webhook_id:
        return

    if "https://scratch.mit.edu" in message.content:
#        print("yes")
        links = message.content.split("https://")
        templinks = []
        for x in range(len(links)):
            templinks = templinks + links[x].split(" ")
        links = templinks
#        print(links)
        links = list(filter(lambda x: "scratch.mit.edu" in x, links))
#        print(links)
#        print(len(links))
        embedlist = []
        if len(links) == 1:
            id = main.parse("https://"+links[0]+"/")
            if " " in str(id[1]):
                filtid = list(filter(lambda x: x != " ", list(str(id[1]))))
                id[1] = "".join(map(str,filtid))
            print(id)
            if type(id) is list:
                embed = None
                if id[0] == "pro":
                    embed = embeds.project(id)
                elif id[0] == "use":
                    embed = embeds.user(id)
                elif id[0] == "stu":
                    embed = embeds.studio(id)
                elif id[0] == "for":
                    embed = embeds.topic(id)
                elif id[0] == "prof":
                    embed = embeds.fproject(id)
                elif id[0] == "pcom" or id[0] == "scom" or id[0] == "ppcom":
                    embed = embeds.comment(id)
                await message.channel.send(embed=embed)
        else:
            for i in range(len(links)):
                id = main.parse("https://"+links[i]+"/")
                filtid = list(filter(lambda x: x != " ", list(str(id[1]))))
                id[1] = "".join(map(str,filtid))
#                print(id)
                if type(id) is list:
                    embed = None
                    if id[0] == "pro":
                        embed = embeds.project(id)
                    elif id[0] == "use":
                        embed = embeds.user(id)
                    elif id[0] == "stu":
                        embed = embeds.studio(id)
                    elif id[0] == "for":
                        embed = embeds.topic(id)
                    elif id[0] == "prof":
                        embed = embeds.fproject(id)
                    elif id[0] == "pcom" or id[0] == "scom":
                        embed = embeds.comment(id)
                    embedlist.append(embed)
            await message.channel.send(embeds=embedlist)
    await bot.process_commands(message)

@bot.command()
async def search(ctx,*args):
    defaultval = [5, "popular", "en"]
    try:
        q = args[0]
        m = args[2]
        l = args[3]
        ll = int(args[1])
    except:
        await ctx.send("you have to fill in the parameters!")
        return
    search = scratchattach.search_projects(query=q, mode=m, language=l, limit=ll, offset=0)
    await ctx.message.add_reaction("<a:searching:1204038774066257950>")
    if len(search) != 0:
        embedlist = []
        for i in range(ll):
            project = search[i]
            user = project.author()
            title = project.title
            author = user.name
            icon = user.icon_url
            ins = project.instructions
            note = project.notes
            thumb = project.thumbnail_url
            surl = project.url
            lov = project.loves
            fav = project.favorites
            rem = project.remix_count
            vie = project.views
            uurl = "https://scratch.mit.edu/users/" + author
            #        response = title + "/n" + author + "/n" + ins + "/n" + note + "/n" + thumb
            #        await message.channel.send(response)
            if len(ins) > 50:
                ins = ins[0:50] + "..."
            if len(note) > 25:
                note = note[0:25] + "..."

            embed = discord.Embed(title=title, url=surl,
                                  color=0x885CD4)
            embed.set_author(name=author, url=uurl,
                             icon_url=icon)
            embed.set_thumbnail(url=thumb)
            embed.add_field(name="Instructions", value=ins,
                            inline=False)
            embed.add_field(name="Notes and Credits", value=note,
                            inline=False)
            embedlist.append(embed)
        await ctx.send(embeds=embedlist)
        await ctx.message.remove_reaction("<a:searching:1204038774066257950>", bot.user)
    else:
        await ctx.message.send("no search results returned")

@bot.command()
async def invite(ctx):
    await ctx.send("[invite link](https://discord.com/oauth2/authorize?client_id=1203706530818564196)")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help",
                          color=0x885CD4)
    embed.set_thumbnail(url="https://file.garden/YA1t3RgapBy70QKm/innocent")
    embed.set_author(name=ctx.author.display_name + " Asked for help:",
                     icon_url=ctx.author.avatar)
    embed.add_field(name=">help", value="The command you are using right now.",
                    inline=False)
    embed.add_field(name=">search [q] [ll] [m] [l]", value="Takes 4 parameters:\n[q] Query: The search query, has to be in quotes."
                                                           "\n[ll] Amount to display: The amount of projects to "
                                                           "display.\n[m] Type: Can be either \"trending\" or \"popular\"\n[l] Language: idk what languages you can use for this except \"en\" sorry",
                    inline=False)
    embed.add_field(name=">invite", value="The invite link.",
                    inline=False)
    embed.add_field(name=">randomq [q]", value="Random project based on query.\n"
                                               "[q] Query: Query to search projects under.",
                    inline=False)
    embed.add_field(name=">randome [m]", value="Random project based on the explore page.\n"
                                               "[m] Explore page to use, can only be \"trending\" or \"popular\".",
                    inline=False)
    embed.add_field(name="**LINK UTILITIES**", value="**Projects:**\n"
                                                     "Big thumbnail: Add \"fullscreen\" to the end of a project URL.",
                    inline=False)
    embed.set_footer(text="BOT VERSION 6.8")
    await ctx.send(embed=embed)

@bot.command()
async def randomq(ctx,*,arg):
    await ctx.message.add_reaction("<a:searching:1204038774066257950>")
    q = arg
    a = 3
    pt = ["popular", "trending"]
    search = []
    for i in range(a):
        search += scratchattach.search_projects(query=q, mode=random.choice(pt), language="en", limit=40, offset=i)

    proj = search[random.randint(0, len(search))]
    pid = proj.id
    embed = embeds.project([None,pid])
    await ctx.send(embed=embed)
    await ctx.message.remove_reaction("<a:searching:1204038774066257950>", bot.user)


@bot.command()
async def randome(ctx, *, arg):
    await ctx.message.add_reaction("<a:searching:1204038774066257950>")
    q = arg
    a = 3
    pt = ["popular", "trending"]
    search = []
    for i in range(a):
        search += scratchattach.explore_projects(query="*", mode=q, language="en", limit=40, offset=i)

    proj = search[random.randint(0, len(search))]
    pid = proj.id
    embed = embeds.project([None,pid])
    await ctx.send(embed=embed)
    await ctx.message.remove_reaction("<a:searching:1204038774066257950>", bot.user)

bot.run(TOKEN)