# bot.py
import os
import random
import main
import scratchattach
import discord
from discord.ext import commands
from dotenv import load_dotenv
import embeds
import fixvideo as fixvid
#import ai

load_dotenv()
TOKEN = os.environ.get("TOKEN")
GUILD = 1185563607736537098
maintenance = False
#intents = discord.Intents.default()
#intents.message_content = True

if maintenance:
    activity = discord.CustomActivity(name="🛠️ undergoing maintenance")
else:
    activity = discord.Activity(type=discord.ActivityType.watching, name="for >help")
bot = commands.Bot(command_prefix=">", intents=discord.Intents.all(),activity=activity)
bot.remove_command('help')

#@bot.event
#async def on_ready():
#    print(f'{bot.user} is connected to the following guilds:')
#    for x in bot.guilds:
#        print(
#            f'{x.name}(id: {x.id})'
#        )

#@bot.command(name='search')
#async def search(ctx):

@bot.event
async def on_message(message):
    if message.author == bot.user or message.webhook_id:
        return

    if maintenance and message.guild.id != 1185563607736537098:
        return

    if "https://scratch.mit.edu" in message.content:
#       print("yes")

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
                embed.set_footer(text=f"{embed.footer.text} , Requested by: @{message.author.name}" )
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
                    if i == 0:
                        embed.set_footer(text=f"{embed.footer.text} , Requested by: @{message.author.name}")
                    embedlist.append(embed)
            await message.channel.send(embeds=embedlist)
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(react,user):
        if react.emoji == "❌" and react.message.author.id == 1203706530818564196:
            if f"@{user.name}" in react.message.embeds[0].footer.text:
                await react.message.delete()


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
    embed.add_field(name=">download [id]", value="Downloads a project.\n"
                                               "[id] Id of project to download.",
                    inline=False)
    embed.add_field(name=">fixvideo", value="Reply to a message with a broken webm video, or attach one to fix it.",
                    inline=False)
    embed.add_field(name="**LINK UTILITIES**", value="**Projects:**\n"
                                                     "Big thumbnail: Add \"fullscreen\" to the end of a project URL.",
                    inline=False)
    embed.add_field(name="**OTHER UTILITIES**", value="React with an ❌ emoji to an embed you requested to delete it.",
                    inline=False)
    embed.set_footer(text="BOT VERSION 8.2")
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

@bot.command()
async def download(ctx, *, arg):
    pid = arg
    try:
        f = open("downloadedproj.sb3","w+")
        f.close()
        proj = scratchattach.get_project(pid)
        body = proj.body()
        body.save(filename="downloadedproj.sb3",dir="")
        file = discord.File(r"downloadedproj.sb3")
        file.filename = proj.title + ".sb3"
        await ctx.send(file=file)
        os.remove("downloadedproj.sb3")
    except:
        await ctx.send("invalid project id")

@bot.command()
async def fixvideo(ctx):
    if ctx.message.reference:
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    else:
        message = ctx.message
    if message.attachments:
        video = message.attachments[0]
    else:
        await ctx.send("Message has no video!")
        return
    try:
        await video.save(fp=video.filename)
        fixvid.fix(video.filename)
        file = discord.File(r"fixVideo.mp4")
        file.filename = "converted.mp4"
        await ctx.send(reference=ctx.message, file=file)
        os.remove(video.filename)
        os.remove("fixVideo.avi")
        os.remove("fixVideo.mp4")
    except:
        await ctx.send("Video is already fixed! / File isn't a video!")
        os.remove(video.filename)
        os.remove("converted.mp4")

bot.run(TOKEN)