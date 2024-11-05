import time

import scratchattach as sa
from dotenv import load_dotenv
import google.generativeai as genai
import time
import os
import re

from pyasn1.type.univ import SetOf

load_dotenv()
TOKEN = os.environ.get("GEMTOKEN")
SCRATCHPASS = os.environ.get("SCRATCHPASS")
genai.configure(api_key=TOKEN)
session = sa.login("scratchbotee", SCRATCHPASS)
events = session.connect_message_events()
prompt = """You are scratch bot. You are a bot that replies to comments on the children's coding website: “Scratch” you cannot give help with coding. You have a character limit of 500 characters, and cannot use linebreaks, so keep responses short.

You have access to certain emojis, they must be marked with two underscores on each side of the emoji, the ones named after objects are an icon of that object, they are case sensitive:
	
	_meow_ : An icon of a cat
	_gobo_ : An icon of a weird alien thing
	_waffle_
	_taco_
	_sushi_
	_apple_
	_broccoli_
	_pizza_
	_candycorn_
	_10mil_ : An icon of a party popper
	_map_ 
	_camera_
	_suitcase_
	_compass_
	_binoculars_
	_cupcake_
	_:)_ : cat with a slight smile, happy
	_:D_ : cat with a grin and dilated eyes, overjoyed
	_B)_ : cat with sunglasses, cool
	_:P_ : cat with tongue out, silly
	_;P_ : cat with zany face and tongue out, zany
	_:’P_ : cat laughing
	_P:_ : upside down cat with tongue out, curious
	_:3_ : cat with smug smirk, smug
	_<3_ : cat with heart eyes, admiration
	_**_ : cat with star eyes, star struck
	_:))_ : cat barfing rainbows, random
	_:D<_ : cat eating pizza, random

Keep emojis to a minimum, user made emojis are not possible, and emojis cannot be used in projects.

Do not mention social medias, or swear, that’ll get you banned/muted.

Your username is "scratchbotee"

You are replying to a comment posted by {user}, with the contents:
“{message}”

"""

@events.event
def on_message(message):
    # `message` is a sa.Activity object.
    # All attributes and methods of `message` can be found in the documentation of the sa.Activity class.
    print(message.actor_username, "performed action", message.type)
    if message.type == "addcomment":
        thread = []
        comment = message.target()
        newprompt = prompt.replace("{user}", comment.author_name)
        newprompt = newprompt.replace("{message}", comment.content)
        pcomment = comment.parent_comment()
        if pcomment != None:
            if not "@scratchbotee" in comment.content:
                return
            thread = pcomment.replies()
            if len(thread) > 1:
                thread.remove(comment)
                newprompt += "The previous messages in the thread are:\n"
                for i in thread:
                    newcontent = re.sub('@[^<]+? ', '', i.content)
                    newprompt += f"\t{i.author_name}: {newcontent}\n"
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(newprompt)
        responsetext = response.text
        if f"@{comment.author_name}" in responsetext:
            responsetext.replace(f"@{comment.author_name}","")
        try:
            comment.reply(f"@{comment.author_name} {responsetext}")
        except:
            print("ouch!! cooldowned")
            time.sleep(15)
            comment.reply(f"@{comment.author_name} {responsetext}")
        print("comment posted")
        session.clear_messages()
events.start()