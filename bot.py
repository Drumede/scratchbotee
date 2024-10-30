# bot.py
import os
import random
import main
import scratchattach
import re
from datetime import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv
import html

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

    def project(id):
        project = scratchattach.get_project(id[1])
        user = project.author()
        title = project.title
        icon = user.icon_url
        ins = html.unescape(project.instructions)
        ins = ins.split("\n\n")
        ins = '\n\n'.join([i for i in ins if i != ""])
        note = html.unescape(project.notes)
        note = note.split("\n\n")
        note = '\n\n'.join([i for i in note if i != ""])
        thumb = project.thumbnail_url
        surl = project.url
        lov = project.loves
        fav = project.favorites
        rem = project.remix_count
        vie = project.views
        uurl = "https://scratch.mit.edu/users/" + user.name
        date = project.share_date
        date = date.replace("T", " ")
        date = project.share_date.replace("Z", "+00:00")
        date = datetime.fromisoformat(date)
        date = date.strftime("%b %d, %Y")
        #        response = title + "/n" + author + "/n" + ins + "/n" + note + "/n" + thumb
        #        await message.channel.send(response)
        if len(ins) > 200:
            ins = ins[0:200] + "..."
        if len(note) > 200:
            note = note[0:200] + "..."

        embed = discord.Embed(title=title, url=surl,
                              #                              description=ins + "/n" + note,
                              color=0x885CD4)
        embed.set_author(name=user.name, url=uurl,
                         icon_url=icon)
        embed.set_thumbnail(url=thumb)
        if ins != "":
            embed.add_field(name="Instructions", value=ins,
                            inline=False)
        if note != "":
            embed.add_field(name="Notes and Credits", value=note,
                            inline=False)
        embed.set_footer(text=f"👁️ {vie} ❤️ {lov} ⭐ {fav} 🍥 {rem} 📅 {date}")
        return embed

    def user(id):
        user = scratchattach.get_user(id[1])
        icon = user.icon_url
        abm = html.unescape(user.about_me)
        abm = abm.split("\n\n")
        abm = '\n\n'.join([i for i in abm if i != ""])
        wiw = html.unescape(user.wiwo)
        wiw = wiw.split("\n\n")
        wiw = '\n\n'.join([i for i in wiw if i != ""])
        con = user.country
        fol1 = user.follower_count()
        fol2 = user.following_count()
        pro = user.project_count()
        uurl = "https://scratch.mit.edu/users/" + id[1]
        if len(abm) > 100:
            abm = abm[0:100] + "..."
        if len(wiw) > 100:
            wiw = wiw[0:100] + "..."
        embed = discord.Embed(title=id[1], url=uurl,
                              #                              description=ins + "/n" + note,
                              color=0x885CD4)
        embed.set_thumbnail(url=icon)
        if abm != "":
            embed.add_field(name="About me", value=abm,
                            inline=False)
        if wiw != "":
            embed.add_field(name="What I'm working on", value=wiw,
                            inline=False)
        embed.set_footer(text=f"👤️ {fol1} 🫂️ {fol2} 🗳️️ {pro} 🏳️️️ {con}")
        return embed

    def studio(id):
        studio = scratchattach.get_studio(id[1])
        user = studio.host
        icon = user.icon_url
        title = html.unescape(studio.title)
        desc = html.unescape(studio.description)
        desc = desc.split("\n\n")
        desc = '\n\n'.join([i for i in desc if i != ""])
        thumb = studio.image_url
        fol = studio.follower_count
        proj = studio.project_count
        surl = "https://scratch.mit.edu/studios/" + str(id[1])
        uurl = "https://scratch.mit.edu/users/" + user.name
        if len(desc) > 300:
            desc = desc[0:300] + "..."
        embed = discord.Embed(title=title, url=surl,
                              #                              description=ins + "/n" + note,
                              color=0x885CD4)
        embed.set_thumbnail(url=thumb)
        embed.set_author(name="Host: "+user.name, url=uurl,
                         icon_url=icon)
        if desc != "":
            embed.add_field(name="Description", value=desc,
                            inline=False)
        embed.set_footer(text="👤️ " + str(fol) + " 🗳️️ " + str(proj))
        return embed

    def topic(id):
        top = scratchattach.get_topic(id[1])
        title = top.title
        cat = top.category
        post = top.first_post()
        user = post.get_author()
        auth = post.author
        icon = user.icon_url
        date = post.posted
        edit = post.edited
        date = date.replace("T", " ")
        edit = edit.replace("T", " ")
        date = post.posted.replace("Z", "+00:00")
        edit = post.edited.replace("Z", "+00:00")
        date, edit = datetime.fromisoformat(date), datetime.fromisoformat(edit)
        date, edit = date.strftime("%b %d, %Y"), edit.strftime("%b %d, %Y")
        print(str(date)+ "\n" + str(edit))
        cont = post.html_content
        pattern = re.compile('<.*?>')
        surl = "https://scratch.mit.edu/discuss/topic/" + id[1]
        uurl = "https://scratch.mit.edu/users/" + auth
        if len(cont) > 200:
            cont = cont[0:300] + "..."
        embed = discord.Embed(title=title, url=surl,
                              #                              description=ins + "/n" + note,
                              color=0x885CD4)
#        embed.set_thumbnail(url=thumb)
        embed.add_field(name="Category", value=cat,
                        inline=False)
        embed.add_field(name="Content", value=re.sub(pattern, " ", cont),
                        inline=False)
        embed.set_author(name=auth, url=uurl,
                         icon_url=icon)
        embed.set_footer(text=f"📥️ {date} 📝️️ {edit}")
        return embed

    def fproject(id):

        project = scratchattach.get_project(id[1])
        user = project.author()
        title = project.title
        icon = user.icon_url
        ins = html.unescape(project.instructions)
        ins = ins.split("\n\n")
        ins = '\n\n'.join([i for i in ins if i != ""])
        note = html.unescape(project.notes)
        note = note.split("\n\n")
        note = '\n\n'.join([i for i in note if i != ""])
        thumb = project.thumbnail_url
        surl = project.url
        lov = project.loves
        fav = project.favorites
        rem = project.remix_count
        vie = project.views
        uurl = "https://scratch.mit.edu/users/" + user.name
        date = project.share_date
        date = date.replace("T", " ")
        date = project.share_date.replace("Z", "+00:00")
        date = datetime.fromisoformat(date)
        date = date.strftime("%b %d, %Y")
        #        response = title + "/n" + author + "/n" + ins + "/n" + note + "/n" + thumb
        #        await message.channel.send(response)
        if len(ins) > 200:
            ins = ins[0:200] + "..."
        if len(note) > 200:
            note = note[0:200] + "..."

        embed = discord.Embed(title=title, url=surl,
                              #                              description=ins + "/n" + note,
                              color=0x885CD4)
        embed.set_author(name=user.name, url=uurl,
                         icon_url=icon)
        embed.set_image(url=thumb)
        if ins != "":
            embed.add_field(name="Instructions", value=ins,
                            inline=False)
        if note != "":
            embed.add_field(name="Notes and Credits", value=note,
                            inline=False)
        embed.set_footer(text=f"👁️ {vie} ❤️ {lov} ⭐ {fav} 🍥 {rem} 📅 {date}")
        return embed

    def comment(id):
        if id[0] == "pcom":
            project = scratchattach.get_project(id[1])
            comment = project.comment_by_id(comment_id=id[2])
            content = html.unescape(comment.content)
            surl = f"https://scratch.mit.edu/projects/{id[1]}/#comments-{id[2]}"
            auth = comment.author()
            username = auth.name
            uurl = f"https://scratch.mit.edu/users/{username}"
            icon = auth.icon_url
            date = comment.datetime_created.replace("Z", "+00:00")
            date = datetime.fromisoformat(date)
            date = date.strftime("%b %d, %Y")

            embed = discord.Embed(title=f"Comment left under project \"{project.title}\"",
                                  url=surl,
                                  description=f"*\' {content} \'*",
                                  color=0x885CD4)
            embed.set_author(name=username, url=uurl,
                             icon_url=icon)
            embed.set_footer(text=f"📅 {date}")
            embed.set_thumbnail(url=project.thumbnail_url)
            return embed
        elif id[0] == "pcom":
            studio = scratchattach.get_studio(id[1])
            comment = studio.comment_by_id(comment_id=id[2])
            content = html.unescape(comment.content)
            surl = f"https://scratch.mit.edu/projects/{id[1]}/#comments-{id[2]}"
            auth = comment.author()
            username = auth.name
            uurl = f"https://scratch.mit.edu/users/{username}"
            icon = auth.icon_url
            date = comment.datetime_created.replace("Z", "+00:00")
            date = datetime.fromisoformat(date)
            date = date.strftime("%b %d, %Y")

            embed = discord.Embed(title=f"Comment left under studio \"{studio.title}\"",
                                  url=surl,
                                  description=f"*\' {content} \'*",
                                  color=0x885CD4)
            embed.set_author(name=username, url=uurl,
                             icon_url=icon)
            embed.set_footer(text=f"📅 {date}")
            embed.set_thumbnail(url=studio.image_url)
            return embed
        elif id[0] == "ppcom":
            user = scratchattach.get_user(id[1])
            comment = user.comment_by_id(comment_id=id[2])
            content = html.unescape(comment.content)
            surl = f"https://scratch.mit.edu/projects/{id[1]}/#comments-{id[2]}"
            auth = comment.author()
            username = auth.name
            uurl = f"https://scratch.mit.edu/users/{username}"
            icon = auth.icon_url
            date = comment.datetime_created.replace("Z", "+00:00")
            date = datetime.fromisoformat(date)
            date = date.strftime("%b %d, %Y")

            embed = discord.Embed(title=f"Comment left under profile \"{user.name}\"",
                                  url=surl,
                                  description=f"*\' {content} \'*",
                                  color=0x885CD4)
            embed.set_author(name=username, url=uurl,
                             icon_url=icon)
            embed.set_footer(text=f"📅 {date}")
            embed.set_thumbnail(url=user.icon_url)
            return embed


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
                    embed = project(id)
                elif id[0] == "use":
                    embed = user(id)
                elif id[0] == "stu":
                    embed = studio(id)
                elif id[0] == "for":
                    embed = topic(id)
                elif id[0] == "prof":
                    embed = fproject(id)
                elif id[0] == "pcom" or id[0] == "scom" or id[0] == "ppcom":
                    embed = comment(id)
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
                        embed = project(id)
                    elif id[0] == "use":
                        embed = user(id)
                    elif id[0] == "stu":
                        embed = studio(id)
                    elif id[0] == "for":
                        embed = topic(id)
                    elif id[0] == "prof":
                        embed = fproject(id)
                    elif id[0] == "pcom" or id[0] == "scom":
                        embed = comment(id)
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
    embed.set_footer(text="BOT VERSION 6.1")
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
    project = scratchattach.get_project(pid)
    user = project.author()
    title = project.title
    icon = user.icon_url
    ins = html.unescape(project.instructions)
    ins = ins.split("\n\n")
    ins = '\n\n'.join([i for i in ins if i != ""])
    note = html.unescape(project.notes)
    note = note.split("\n\n")
    note = '\n\n'.join([i for i in note if i != ""])
    thumb = project.thumbnail_url
    surl = project.url
    lov = project.loves
    fav = project.favorites
    rem = project.remix_count
    vie = project.views
    uurl = "https://scratch.mit.edu/users/" + user.name
    date = project.share_date
    date = date.replace("T", " ")
    date = project.share_date.replace("Z", "+00:00")
    date = datetime.fromisoformat(date)
    date = date.strftime("%b %d, %Y")
    #        response = title + "/n" + author + "/n" + ins + "/n" + note + "/n" + thumb
    #        await message.channel.send(response)
    if len(ins) > 200:
        ins = ins[0:200] + "..."
    if len(note) > 200:
        note = note[0:200] + "..."

    embed = discord.Embed(title=title, url=surl,
                          #                              description=ins + "/n" + note,
                          color=0x885CD4)
    embed.set_author(name=user.name, url=uurl,
                     icon_url=icon)
    embed.set_thumbnail(url=thumb)
    if ins != "":
        embed.add_field(name="Instructions", value=ins,
                        inline=False)
    if note != "":
        embed.add_field(name="Notes and Credits", value=note,
                        inline=False)
    embed.set_footer(text=f"👁️ {vie} ❤️ {lov} ⭐ {fav} 🍥 {rem} 📅 {date}")

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
    project = scratchattach.get_project(pid)
    user = project.author()
    title = project.title
    icon = user.icon_url
    ins = html.unescape(project.instructions)
    ins = ins.split("\n\n")
    ins = '\n\n'.join([i for i in ins if i != ""])
    note = html.unescape(project.notes)
    note = note.split("\n\n")
    note = '\n\n'.join([i for i in note if i != ""])
    thumb = project.thumbnail_url
    surl = project.url
    lov = project.loves
    fav = project.favorites
    rem = project.remix_count
    vie = project.views
    uurl = "https://scratch.mit.edu/users/" + user.name
    date = project.share_date
    date = date.replace("T", " ")
    date = project.share_date.replace("Z", "+00:00")
    date = datetime.fromisoformat(date)
    date = date.strftime("%b %d, %Y")
    #        response = title + "/n" + author + "/n" + ins + "/n" + note + "/n" + thumb
    #        await message.channel.send(response)
    if len(ins) > 200:
        ins = ins[0:200] + "..."
    if len(note) > 200:
        note = note[0:200] + "..."

    embed = discord.Embed(title=title, url=surl,
                          #                              description=ins + "/n" + note,
                          color=0x885CD4)
    embed.set_author(name=user.name, url=uurl,
                     icon_url=icon)
    embed.set_thumbnail(url=thumb)
    if ins != "":
        embed.add_field(name="Instructions", value=ins,
                        inline=False)
    if note != "":
        embed.add_field(name="Notes and Credits", value=note,
                        inline=False)
    embed.set_footer(text=f"👁️ {vie} ❤️ {lov} ⭐ {fav} 🍥 {rem} 📅 {date}")

    await ctx.send(embed=embed)
    await ctx.message.remove_reaction("<a:searching:1204038774066257950>", bot.user)

bot.run(TOKEN)