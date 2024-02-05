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
import math
load_dotenv()
TOKEN = os.environ.get("TOKEN")
GUILD = "just bonus emojis for nitro people (2/2)"
#intents = discord.Intents.default()
#intents.message_content = True

activity = discord.Activity(type=discord.ActivityType.watching, name="for >help")
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(),activity=activity)

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
    if message.author == bot.user:
        return

    def project(id):

        project = scratchattach.get_project(id[1])
        user = scratchattach.get_user(project.author)
        title = project.title
        author = project.author
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
        if len(ins) > 200:
            ins = ins[0:200] + "..."
        if len(note) > 200:
            note = note[0:200] + "..."

        embed = discord.Embed(title=title, url=surl,
                              #                              description=ins + "/n" + note,
                              color=0x885CD4)
        embed.set_author(name=author, url=uurl,
                         icon_url=icon)
        embed.set_thumbnail(url=thumb)
        embed.add_field(name="Instructions", value=ins,
                        inline=False)
        embed.add_field(name="Notes and Credits", value=note,
                        inline=False)
        embed.set_footer(text="👁️ " + str(vie) + " ❤️ " + str(lov) + " ⭐ " + str(fav) + " 🍥 " + str(rem))
        return embed

    def user(id):
        user = scratchattach.get_user(id[1])
        icon = user.icon_url
        abm = user.about_me
        wiw = user.wiwo
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
        embed.add_field(name="About me", value=abm,
                        inline=False)
        embed.add_field(name="What I'm working on", value=wiw,
                        inline=False)
        embed.set_footer(text="👤️ " + str(fol1) + " 🫂️ " + str(fol2) + " 🗳️️ " + str(pro) + " 🏳️️️ " + str(con))
        return embed

    def studio(id):
        studio = scratchattach.get_studio(id[1])
        user = studio.managers(limit=1, offset=0)[0]
        icon = user.icon_url
        title = studio.title
        desc = studio.description
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
        embed.set_footer(text="📥️ " + str(date.strftime("%b %d, %Y")) + " 📝️️ " + str(edit.strftime("%b %d, %Y")))
        return embed

    if "https://" in message.content:
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
                if id[0] == "pro":
                    embed = project(id)
                    await message.channel.send(embed=embed)
                elif id[0] == "use":
                    embed = user(id)
                    await message.channel.send(embed=embed)
                elif id[0] == "stu":
                    embed = studio(id)
                    await message.channel.send(embed=embed)
                elif id[0] == "for":
                    embed = topic(id)
                    await message.channel.send(embed=embed)
        else:
            for i in range(len(links)):
                id = main.parse("https://"+links[i]+"/")
                if str(id[1]) in id[1]:
                    filtid = list(filter(lambda x: x != " ", list(str(id[1]))))
                    id[1] = "".join(map(str,filtid))
#                print(id)
                if type(id) is list:
                    if id[0] == "pro":
                        embed = project(id)
                        embedlist.append(embed)
                    elif id[0] == "use":
                        embed = user(id)
                        embedlist.append(embed)
                    elif id[0] == "stu":
                        embed = studio(id)
                        embedlist.append(embed)
                    elif id[0] == "for":
                        embed = topic(id)
                        embedlist.append(embed)
            await message.channel.send(embeds=embedlist)
    elif str(message.content)[0:7] == ">search":
        defaultval = [5,"popular","en"]
        try :
            ctx = message.content[7:].split(",")
            q = ctx[0]
            m = ctx[2]
            l = ctx[3]
            ll = int(ctx[1])
        except:
            await message.channel.send("you have to fill in the parameters!")
        search = scratchattach.search_projects(query=q, mode=m, language=l, limit=ll, offset=0)
        await message.add_reaction("<a:searching:1204038774066257950>")
        if len(search) != 0:
            embedlist = []
            for i in range(int(ctx[1])):
                project = search[i]
                user = scratchattach.get_user(project.author)
                title = project.title
                author = project.author
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
            await message.channel.send(embeds=embedlist)
            await message.remove_reaction("<a:searching:1204038774066257950>",bot.user)
        else:
            await message.channel.send("no search results returned")
    if str(message.content)[0:7] == ">invite":
        await message.channel.send("[invite link](https://discord.com/api/oauth2/authorize?client_id=1203706530818564196&permissions=1067299752000&scope=bot)")
    if str(message.content)[0:5] == ">help":
        embed = discord.Embed(title="Help",
                              color=0x885CD4)
        embed.set_author(name=message.author.display_name+" Asked for help:",
                         icon_url=message.author.avatar)
        embed.add_field(name=">help", value="The command you are using right now.",
                        inline=False)
        embed.add_field(name=">search [q],[ll],[m],[l]", value="Takes 4 parameters:\n[q] Query: The search query."
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
        embed.set_footer(text="VERSION 3.11")
        await message.channel.send(embed=embed)
    if str(message.content)[0:8] == ">randomq":
        await message.add_reaction("<a:searching:1204038774066257950>")
        q = str(message.content)[8:]
        a = 3
        pt = ["popular","trending"]
        search = []
        for i in range(a):
            search += scratchattach.search_projects(query=q, mode=random.choice(pt), language="en", limit=40, offset=i)
        proj = search[random.randint(0,len(search))]
        pid = proj.id
        embed = project([None,int(pid)])
        await message.channel.send(embed=embed)
        await message.remove_reaction("<a:searching:1204038774066257950>", bot.user)
    if str(message.content)[0:8] == ">randome":
        await message.add_reaction("<a:searching:1204038774066257950>")
        q = str(message.content)[9:]
        a = 3
        search = []
        for i in range(a):
            search += scratchattach.explore_projects(query="*", mode=q, language="en", limit=40, offset=i)
        proj = search[random.randint(0,len(search))]
        pid = proj.id
        embed = project([None,int(pid)])
        await message.channel.send(embed=embed)
        await message.remove_reaction("<a:searching:1204038774066257950>", bot.user)
bot.run(TOKEN)