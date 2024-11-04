import scratchattach as sa
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()
TOKEN = os.environ.get("GEMTOKEN")
genai.configure(api_key=TOKEN)
session = sa.login("scratchbotee", "a0547300")
events = session.connect_message_events()
prompt = """You are scratch bot. You are a bot that replies to comments on the children's coding website: “Scratch” you cannot give help with coding. You have a character limit of 500 characters, so keep responses short.

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

Keep emojis to a minimum, and user made emojis are not possible.

Do not mention social medias, or swear, that’ll get you banned/muted.

You are replying to a comment posted by {user}, with the contents:
“{message}”
"""

@events.event
def on_ready():
    print("what")
@events.event
def on_message(message):
    # `message` is a sa.Activity object.
    # All attributes and methods of `message` can be found in the documentation of the sa.Activity class.
    if message.type == "addcomment":
        thread = []
        comment = message.target()
        pcomment = comment.parent_comment()
        if pcomment != None:
            thread = pcomment.replies()
        model = genai.GenerativeModel("gemini-1.5-flash")
        newprompt = prompt.replace("{user}",comment.author_name)
        newprompt = newprompt.replace("{message}",comment.content)
        response = model.generate_content(newprompt)

        comment.reply(f"@{comment.author_name} {response}")
        print(thread)
    print(message.actor_username, "performed action", message.type)

events.start()