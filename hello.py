# app.py
from flask import Flask, render_template, request
import random
from emoji import emojize

app = Flask(__name__)

# Mapping of digits and operators to emojis and moods
mood_map = {
    "0": {"emoji": "😐", "mood": "neutral"},
    "1": {"emoji": "🙂", "mood": "slightly happy"},
    "2": {"emoji": "😃", "mood": "happy"},
    "3": {"emoji": "🥳", "mood": "excited"},
    "4": {"emoji": "😍", "mood": "in love"},
    "5": {"emoji": "🤩", "mood": "amazed"},
    "6": {"emoji": "😎", "mood": "cool"},
    "7": {"emoji": "🤓", "mood": "nerdy"},
    "8": {"emoji": "🤯", "mood": "mind-blown"},
    "9": {"emoji": "🤨", "mood": "suspicious"},
    "+": {"emoji": "+", "mood": "friendly"},
    "-": {"emoji": "-", "mood": "annoyed"},
    "*": {"emoji": "×", "mood": "wild"},
    "/": {"emoji": "÷", "mood": "anxious"}
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

def evaluate_mood_combo(expression, result):
    parts = []
    for char in str(expression):
        if char in mood_map:
            # For operators, add the symbol, for operands add the mood word
            if char in "+-*/":
                if char == '+': parts.append("plus")
                elif char == '-': parts.append("minus")
                elif char == '*': parts.append("multiplied by")
                elif char == '/': parts.append("divided by")
            else:
                parts.append(mood_map[char]["mood"])
    
    meaningful_expr = " ".join(parts)
    
    # Specific fun overrides
    if "happy plus happy" in meaningful_expr:
        return "joyful", "👯‍♀️💖✨", f"Happy plus happy always equals joyful! Your calculation resulted in {result}. These numbers are best friends spreading positive vibes everywhere."
    
    if "angry" in meaningful_expr or "annoyed" in meaningful_expr:
        if result > 0:
            return "calmed down", "😌🍵🌿", f"Even though things started negative with '{meaningful_expr}', the result is a positive {result}. The numbers drank some tea and calmed down."
        else:
            return "furious", "🌋🤬💥", f"Oh no, '{meaningful_expr}' ended up at {result}. The numbers are absolutely furious and starting a riot!"

    if result == 0:
        return "peaceful", "🧘‍♀️🕊️🍃", f"'{meaningful_expr}' balances perfectly to zero. The numbers have achieved true inner peace and zen."
    elif result < 0:
        return "grumpy", "🌩️😠📉", f"'{meaningful_expr}' led to a negative space ({result}). The numbers are quite grumpy about being less than nothing!"
    elif 1 <= result <= 5:
        return "joyful", "😊🎈🌻", f"'{meaningful_expr}' adds up nicely to {result}. It's a small but joyful step into happiness."
    elif 6 <= result <= 15:
        return "thrilled", "🥳🎆🎢", f"Wow! '{meaningful_expr}' skyrocketed to {result}! The numbers are thrilled and having a massive celebration!"
    elif result > 15:
        return "mind-blown", "🤯🚀🌌", f"Incredible! '{meaningful_expr}' reached an astronomical {result}. The numbers are absolutely mind-blown by this math!"
    else:
        return "confused", "🌀🤔🧩", f"'{meaningful_expr}' resulted in {result}. The numbers are scratching their heads in confusion."

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
            # Convert expression to emoji string for display
            emoji_expression = ""
            for char in expression:
                if char in mood_map:
                    emoji_expression += mood_map[char]["emoji"]
                else:
                    emoji_expression += char
            
            # Evaluate the expression
            result = eval(expression)
            
            # Interpret the mood based on combinations
            mood, emoji_result, story = evaluate_mood_combo(expression, result)
            
        except Exception as e:
            result = "Error"
            emoji_result = "⚠️"
            story = "Oops! The numbers got tangled up in a mathematical knot. Please ensure you enter a valid calculation!"
    
    return render_template("index.html", result=result, mood=mood, story=story, 
                           emoji_expression=emoji_expression, emoji_result=emoji_result, 
                           mood_map=mood_map)

if __name__ == '__main__':
    app.run(debug=True, port=5001)