import random
import openai
import requests
import constants

openai.api_key = constants.OPENAI_API_KEY

#Setting context
messages = [ {"role": "system", "content": "You are a fashion assistant designed to suggest outfits based on weather and create a dalle prompt that generates images with 4 or more panels depicting those outfits. You should describe each every part of the outfit clearly. The length of the prompt should not exceed 120 words."} ]

def handle_response(message) -> str:
    gender = ''
    if(message.startswith('/')):
        print(message)
        if(message.endswith("women")):
            message = message[:-6]
            gender = 'women'
            
        elif(message.endswith(" men")):
            message = message[:-4]
            gender = 'men'
        
        message = message.lower().replace(" ", "%20").replace("/", "")
        print(message)
        if(gender):
            link = "https://api.openweathermap.org/data/2.5/weather?q="+message+"&appid="+constants.WEATHER_API_KEY
            api_link = link.replace(" ", "%20")
            response = requests.get(api_link).json()
            print(api_link)
            print(type(response))
            print('description ---------------- ',response["weather"][0]["description"])
            description = response["weather"][0]["description"]
            print('temp ---------------- ',response["main"]['temp'])
            temp = round(9 / 5 * (response["main"]['temp'] - 273.15) + 32, 3)
            feels_like = round(9 / 5 * (response["main"]['feels_like'] - 273.15) + 32, 3)
            
            content = "What would be the best outfit for "+gender+" to wear in "+message+" when the weather is "+description+" and the temperature is "+str(temp)+" Fahrenheit and it feels like "+str(feels_like)+" Fahrenheit. Give me the colors of the outfit as well."
            print('content ---------------- ',content)
            if message:
                messages.append(
                    {"role": "user", "content": content},
                )
                chat = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=messages
                )
            
            reply = chat.choices[0].message.content
            reply += "\n\n"+generate_dalle_image(reply)
            return reply
        else:
            return "Sorry I didn't get it. Please resend your request with the proper formatting and gender('men'/'women').\nExample query:/London women"

def generate_dalle_image(prompt):
    if prompt:
        response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024",
            )
        return response["data"][0]["url"]