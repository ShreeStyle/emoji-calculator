# app.py
from flask import Flask, render_template, request
import random
from emoji import emojize

app = Flask(__name__)

# Mapping of digits and operators to emojis and moods
mood_map = {
    "0": {"emoji": ":neutral_face:", "mood": "neutral"},
    "1": {"emoji": ":slightly_smiling_face:", "mood": "slightly happy"},
    "2": {"emoji": ":smiley:", "mood": "happy"},
    "3": {"emoji": ":partying_face:", "mood": "excited"},
    "4": {"emoji": ":heart_eyes:", "mood": "in love"},
    "5": {"emoji": ":star_struck:", "mood": "amazed"},
    "6": {"emoji": ":sunglasses:", "mood": "cool"},
    "7": {"emoji": ":nerd_face:", "mood": "nerdy"},
    "8": {"emoji": ":exploding_head:", "mood": "mind-blown"},
    "9": {"emoji": ":face_with_raised_eyebrow:", "mood": "suspicious"},
    "+": {"emoji": ":hugging_face:", "mood": "friendly"},
    "-": {"emoji": ":unamused:", "mood": "annoyed"},
    "*": {"emoji": ":zany_face:", "mood": "wild"},
    "/": {"emoji": ":grimacing:", "mood": "anxious"}
}

# Emoji art templates
emoji_art = {
    "happy": "☀️🌈😊🌻🎉",
    "sad": "☁️💧😢🌧️🕯️",
    "excited": "🎢🎡🎪🎉🎊",
    "angry": "🌋⚡🔥💥😠",
    "confused": "❓🤔🧩🔍🌀",
    "loving": "💖💕💞🌹💑",
    "adventurous": "🏔️🧗🌊🏄🌴",
    "relaxed": "🏖️☮️🧘🌅🍹"
}

def interpret_mood(score):
    if score < -10:
        return "angry"
    elif -10 <= score < 0:
        return "sad"
    elif 0 <= score < 5:
        return "confused"
    elif 5 <= score < 10:
        return "happy"
    elif 10 <= score < 20:
        return "excited"
    elif 20 <= score < 30:
        return "loving"
    elif 30 <= score < 40:
        return "adventurous"
    else:
        return "relaxed"

def generate_story(mood, expression, result):
    stories = {
        "angry": f"Oh no! Your calculation ({expression}) resulted in {result}, which made the numbers really angry! They're stomping around and causing quite a ruckus. Maybe try adding some happy numbers to calm them down?",
        "sad": f"Aw, your mathematical journey ({expression}) led to {result}, and now the numbers are feeling a bit blue. Perhaps they need a mathematical hug?",
        "confused": f"Well, that's odd! Your calculation ({expression}) gave {result}, and now the numbers are scratching their heads in confusion. They're not sure if they should celebrate or take a nap.",
        "happy": f"Yay! Your math adventure ({expression}) resulted in a cheerful {result}. The numbers are doing a little happy dance!",
        "excited": f"Wow! {expression} turned into an exhilarating {result}! The numbers are bouncing off the walls with excitement. They might need some chamomile tea to calm down.",
        "loving": f"Aww, how sweet! Your calculation ({expression}) blossomed into a loving {result}. The numbers are forming heart shapes and writing mathematical love poems.",
        "adventurous": f"Hold onto your calculators! {expression} transformed into a thrill-seeking {result}. The numbers are packing their bags for a mathematical expedition!",
        "relaxed": f"Aaah, bliss! Your serene calculation ({expression}) mellowed into a zen-like {result}. The numbers are lounging on geometric beaches, sipping on pi-ña coladas."
    }
    return stories[mood]

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    mood = ""
    story = ""
    emoji_expression = ""
    emoji_result = ""
    if request.method == "POST":
        expression = request.form.get("expression")
        try:
            # Convert expression to emoji and calculate mood score
            emoji_expression = ""
            mood_score = 0
            for char in expression:
                if char in mood_map:
                    emoji_expression += emojize(mood_map[char]["emoji"])
                    mood_score += list(mood_map.keys()).index(char) - 5  # Center the mood score around 0
                else:
                    emoji_expression += char
            
            # Evaluate the expression
            result = eval(expression)
            
            # Interpret the mood based on the result and mood score
            mood = interpret_mood(mood_score * result)
            
            # Generate emoji art
            emoji_result = emoji_art[mood]
            
            # Generate story
            story = generate_story(mood, expression, result)
            
        except Exception as e:
            result = "Error occurred..."
            emoji_result = emojize(":warning:")
            story = "Oops! The numbers got tangled up in a mathematical knot. Maybe try a different calculation?"
    
    return render_template("index.html", result=result, mood=mood, story=story, 
                           emoji_expression=emoji_expression, emoji_result=emoji_result, 
                           mood_map=mood_map)

if __name__ == '__main__':
    app.run(debug=True, port=5001)