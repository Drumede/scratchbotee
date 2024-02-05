# bot.py
import os
import random
import main
import scratchattach

import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.environ.get("TOKEN")
GUILD = "just bonus emojis for nitro people (2/2)"
print(TOKEN)
#intents = discord.Intents.default()
#intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
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
        return embed
    def studio(id):
        studio = scratchattach.get_studio(id[1])
        title = studio.title
        desc = studio.description
        thumb = studio.image_url
        fol = studio.follower_count
        proj = studio.project_count
        surl = "https://scratch.mit.edu/studios/" + str(id[1])
        if len(desc) > 300:
            desc = desc[0:300] + "..."
        embed = discord.Embed(title=title, url=surl,
                              #                              description=ins + "/n" + note,
                              color=0x885CD4)
        embed.set_thumbnail(url=thumb)
        embed.add_field(name="Description", value=desc,
                        inline=False)
        embed.set_footer(text="👤️ " + str(fol) + " 🗳️️ " + str(proj))
        return embed
    if "https://" in message.content:
        links = message.content.split("https://")
        links.remove("")
        embedlist = []
        if len(links) == 1:
            id = main.parse(message.content)
            if type(id) is list:
                if id[0] == "pro":
                    embed = project(id)
                    await message.channel.send(embed=embed)
                elif id[0] == "use":
                    embed = user(id)
                    print(embed)
                    await message.channel.send(embed=embed)
                elif id[0] == "stu":
                    embed = studio(id)
                    await message.channel.send(embed=embed)
        else:
            for i in range(len(links)):
                id = main.parse("https://"+links[i])
                if type(id) is list:
                    if id[0] == "pro":
                        embed = project(id)
                        embedlist.append(embed)
                    elif id[0] == "use":
                        embed = user(id)
                        print(embed)
                        embedlist.append(embed)
                    elif id[0] == "stu":
                        embed = studio(id)
                        embedlist.append(embed)
            await message.channel.send(embeds=embedlist)
    elif str(message.content)[0:7] == ">search":
        ctx = message.content[7:].split(",")
        search = scratchattach.search_projects(query=ctx[0], mode=ctx[2], language=ctx[3], limit=int(ctx[1]), offset=0)
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
                embedlist.append(embed)
            await message.channel.send(embeds=embedlist)
        else:
            await message.channel.send("no search results returned")
    if str(message.content)[0:7] == ">invite":
        await message.channel.send("[invite link](https://discord.com/api/oauth2/authorize?client_id=1203706530818564196&permissions=1067299752000&scope=bot)")

bot.run(TOKEN)