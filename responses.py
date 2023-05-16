import random
import openai
import requests
import constants

openai.api_key = constants.OPENAI_API_KEY

#Setting context
gpt_messages = [ {"role": "system", "content": "You are a fashion assistant designed to suggest outfits based on weather. You should describe each every part of the outfit individually. The length of the prompt should not exceed 120 words."} ]

def handle_response(message) -> str:
    gender = ''
    print(message)
    if (message=='help'):
        return "Hi there! \nI am designed to suggest you outfits based on current weather in a city of your choice. \nYou can invoke me in the following way\n /[city_name] ['men'/'women']\nExample query:/London women"  
    elif(message.startswith('/')):
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
            print(api_link)
            response = requests.get(api_link).json()
            print(response)
            if(response['cod']=='404'):
                print('1')
                print(response['cod'])
                return "City not found. \nPlease try that again with a valid city name"            
            elif(response['cod']=='429'):
                print('2')
                print(response['cod'])
                return "You have exceeded the API call limit for now. \nPlease try again later"
            elif(response["weather"]):
                print('4')
                print('description ---------------- ',response["weather"][0]["description"])
                description = response["weather"][0]["description"]
                print('temp ---------------- ',response["main"]['temp'])
                temp = round(9 / 5 * (response["main"]['temp'] - 273.15) + 32, 3)
                feels_like = round(9 / 5 * (response["main"]['feels_like'] - 273.15) + 32, 3)
                
                content = "What would be the best outfit for "+gender+" to wear in "+message+" when the weather is "+description+" and the temperature is "+str(temp)+" Fahrenheit and it feels like "+str(feels_like)+" Fahrenheit. Give me the colors of the outfit as well."
                print('content ---------------- ',content)
                try:
                    if message:
                        gpt_messages.append(
                            {"role": "user", "content": content},
                        )
                        chat = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo", messages=gpt_messages
                        )
                    if(chat.choices[0].message.content):
                        reply = chat.choices[0].message.content
                        reply += "\n\n"+generate_dalle_image(reply)
                        return reply
                    else:
                        return "Sorry something went wrong :(. Please try that again."
                except:
                    return "Oops! Looks like GPT is not responding. Please try that again later"
            
            else:
                return "Oops! Something went wrong."
        else:
            return "Sorry I didn't get that.\n Please resend your request with the proper formatting and gender('men'/'women').\n\n/[city_name] ['men'/'women']\n\nExample query:/London women"

def generate_dalle_image(prompt):
    try:
        if prompt:
            response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size="512x512",
                )
            return response["data"][0]["url"]
    # except:
        # return "There was an issue in generating the image. Please try again later"
    except Exception as e: print(e)