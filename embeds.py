import scratchattach
from datetime import datetime
import html
import discord
import re

from scratchattach import get_project


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
    remixparent = project.remix_parent
    remixroot = project.remix_root
    if remixparent != None:
        remix = get_project(remixparent)
        rname = remix.title
        rauthor = remix.author()
        authname = rauthor.name
        embed.add_field(name="Remix of:", value=f"[{rname}](https://scratch.mit.edu/projects/{remix.id}/) by [{authname}](https://scratch.mit.edu/users/{authname}/)")
    if remixroot != None and remixroot != remixparent:
        remix = get_project(remixroot)
        rname = remix.title
        rauthor = remix.author()
        authname = rauthor.name
        embed.add_field(name="Original project:", value=f"[{rname}](https://scratch.mit.edu/projects/{remix.id}/) by [{authname}](https://scratch.mit.edu/users/{authname}/)")
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
    user = studio.host()
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
    #embed.set_thumbnail(url=thumb)
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
    remixparent = project.remix_parent
    remixroot = project.remix_root
    if remixparent != None:
        remix = get_project(remixparent)
        rname = remix.title
        rauthor = remix.author()
        authname = rauthor.name
        embed.add_field(name="Remix of:",
        value=f"[{rname}](https://scratch.mit.edu/projects/{remix.id}/) by [{authname}](https://scratch.mit.edu/users/{authname}/)")
    if remixroot != None and remixroot != remixparent:
        remix = get_project(remixroot)
        rname = remix.title
        rauthor = remix.author()
        authname = rauthor.name
        embed.add_field(name="Original project:",
        value=f"[{rname}](https://scratch.mit.edu/projects/{remix.id}/) by [{authname}](https://scratch.mit.edu/users/{authname}/)")
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