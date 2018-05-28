#The AGNES Project

import pip
import speech_recognition as speechRecog
import pyttsx3
from playsound import playsound
import random
import bs4
from urllib.request import urlopen as urlReq
import urllib
from bs4 import BeautifulSoup as soup
import datetime
import webbrowser
import os
import platform
import sqlite3

#Global variables
microphoneExistFlag = False #It is false by default, no microphone will be detected
firstQuestionFlag = True    #To greet with a random message
lyrics_url = "http://www.metrolyrics.com/"  #In order to fetch lyrincs (do not change)
weather_url = "https://weather.com/en-IN/weather/today/l/INGJ0568:1:IN"     #For ahmedabad only (you can change the city by going to www.weather.com)
conn = sqlite3.connect('userData.db')   #To store username and several other data
dataCursor = conn.cursor()
userName = ""   #Set to blank initially and later fetch it from db

#All the dictionaries with data (You can add more data too)
endChatDict = {1: "See you soon ", 2: "Catch you later ", 3: "Bye bye ", 4: "Good bye ", 5: "Be back soon ", 6: "Stay safe "}
questionDict = {1: "\nHow can I help you?",
	    2: "\nIs there anything I can assist you with?",
	    3: "\nWhat do you need?",
	    4: "\nHow may I help you?",
	    5: "\nYour wish is my command",
	    6: "\nWhat assistance do you require?",
        7: "\nDo you need anything?",
        8: "\nYou called and here I am",
	    9: "\nHow else can I be of service?",
	    10: "\nCan I help you with anything else?",
	    11: "\nWhat else can I help you with?",
        12: "\nIs there anything else I can help you with?",
	    13: "\nDo you need my help with anything else?",
        14: "\nNow that that's out of the way, do you need anything else?",
        15: "\nAnything you need?"}
windDirectionTable = {"N" : "North",
        "NNE" : "North to North East",
        "NE" : "North East",
        "ENE" : "East to North East",
        "E" : "East",
        "ESE" : "East to South East",
        "SE" : "South East",
        "SSE" : "South to South East",
        "S" : "South",
        "SSW" : "South to South West",
        "SW" : "South West",
        "WSW" : "West to South West",
        "W" : "West",
        "WNW" : "West to North West",
        "NW" : "North West",
        "NNW" : "North to North West"}
weatherDict = {1: "Checking the weather online",
        2: "I'll check what it says online",
        3: "Let me check on weather.com",
        4: "Getting the weather from weather.com",
        5: "I'll look it up online",
        6: "Let me just look it up online",
        7: "One moment"}
jokeDictionary = {1: "Do not be racist; be like Mario. He's an Italian plumber, who was made by the Japanese, speaks English, looks like a Mexican, jumps like a black man, and grabs coins like a Jew!",
        2: "Why couldn't the blonde add 10 + 5 on a calculator? Because she couldn't find the 10 button",
        3: "A SEO couple had twins. For the first time they were happy with duplicate content.",
        4: "Why was the JavaScript developer sad? Because he didn't Node how to Express himself",
        5: "Why do java developers wear glasses? Because they can't C#",
        6: "Why did the developer go broke? Because he used up all his cache",
        7: "I would tell you a UDP joke, but you might not get it.",
        8: "There's a band called 1023MB. They haven't had any gigs yet.",
        9: "Algorithm. Word used by programmers when they don't want to explain what they did.",
        10: "I was once living very actively - playing football, tennis, participating into car races. Sometimes I would play poker and pool. But later somebody stole my PC and that was it.",
        11: "If debugging is the process of removing software bugs, then programming must be the process of putting them in.",
        12: "My friend thinks he is smart. He told me an onion is the only food that makes you cry, so I threw a coconut at his face.",
        13: "If tomatoes are a fruit, isn't ketchup a smoothie?",
        14: "What happens to a frog's car when it breaks down? It gets toad away.",
        15: "Why was six scared of seven? Because seven 'ate' nine.",
        16: "Why did Adele cross the road? To sing, 'Hello from the other side!'",
        17: "Chuck Norris doesn't throw up if he drinks too much. Chuck Norris throws down!",
        18: "A movie scene depicting Chuck Norris losing a fight with Bruce Lee was the product of history's most expensive visual effect. When adjusted for inflation, the effect cost more than the Gross National Product of Paraguay.",
        19: "Chuck Norris can spawn threads that complete before they are started.",
        20: "What do you call a belt made out of watches? A waist of time.",
        21: "What do you call a programmer from Finland? A nerdic",
        22: "A foo walks into a bar, takes a look around and says... Hello world",
        23: "Two bytes meet. The first byte asks, 'Are you ill?' The second byte replies, 'No, just feeling a bit off.'",
        24: "A SQL query goes into a bar, walks up to two tables and asks... can I join you?",
        25: "What's the object-oriented way to become wealthy? Inheritance",
        26: "Why can't bicycles stand on their own? Because they're two tired",
        27: "How many lips does a flower have? Tulips",
        28: "What did the fish say when it hit the wall? Damn",
        29: "Why did the programmer quit his job? Because he didn't get arrays",
        30: "What do you call a singing Laptop? A Dell"}
morningMessageDict = {1: "Good morning", 2: "Hello there, good morning", 3: "Have an energetic day today!"}
afternoonMessageDict = {1: "Good afternoon", 2: "Good afternoon, I hope you had lunch", 3: "Its noon, I hope you're having a good day"}
eveningMessageDict = {1: "Good evening", 2: "Just a few hours till dinner", 3: "It'll be time to head home soon, I hope you had a great day"}
nightMessageDict = {1: "You should be asleep at this hour", 2: "I would advise you to call it a day", 3: "Oh hello, I was just about to go to sleep"}
calculateMessageDict = {1: "I think the answer should be: ", 2: "According to my math, it should be: ", 3: "My processor says its: "}
notCapableMessageDict = {1: "Umm, I can't do that yet. Maybe in the future", 2: "I'm not trained for that yet", 3: "I'm not sure I'm that powerful yet", 4: "Oh, hopefully my maker will teach me that one day"}
speakAgainDict = {1: "Can you say that again?", 2: "Didn't get that, you might have to repeat that", 3: "Sorry, I didn't get you. Try again"}
noLyricsMessageDict = {1: "Sorry, I didn't find the lyrics for this song online", 2: "Can you check the name of the song and the artist again?", 3: "No such song found on metrolyrics.com", 4: "I guess MetroLyrics will add this soon"}
whereAreYouMessageDict = {1: "I'm inside your machine. Just not in the creepy way you'd imagine", 2: "Oh me? I'm in this device", 3: "I live in this device", 4: "Duh, the device you use is my home"}
whoAreYouMessageDict = {1: "My maker named me Agnes, and my goal is to help you", 2: "Oh you didn't know me? I'm Agnes", 3: "Hey there, my name is Agnes, its good to meet you", 4: "My name is Agnes. I'm here to assist you", 5: "I'm Agnes and my goal is to help you"}
agnesMeaningDict = {1: "AGNES stands for A Gossiping Non Energetic System", 2: "Bluntly put, it means A Gossiping Non Energetic System", 3: "Well, it means A Gossiping Non Energetic System, but I'd prefer you call me as AGNES"}
whatCanYouDoDict = {1: "I can get you the lyrics of a song, calculate, tell you the date, time, joke or weather", 2: "Lyrics, weather, calculations, youtube - you name it!", 3: "Oh, I thought you knew. Well I can tell you a joke, tell you the weather, do some calculations and a lot more", 4: "Type in anything, if I can do it, I'll tell you"}
whoAmIDict = {1: "You told me your name was ", 2: "My database says you are ", 3: "You should know your name, well it's ", 4: "I think you forgot your name, it's "}
noUserMessageDict = {1: "Hello there, I'm Agnes, what's your name?", 2: "Welcome, can I get to know your name?", 3: "Hi, I'm Agnes, what is your name?", 4: "Can we be friends? Let's begin with names. I'm Agnes, and you are?"}

#Takes input as speech if mic is available else by text
def takeInput():
    global firstQuestionFlag
    while(1):
        if microphoneExistFlag:
            recognizor = speechRecog.Recognizer()
            with speechRecog.Microphone() as source:
                randomQuestionMessage()
                firstQuestionFlag = False
                audio = recognizor.listen(source)

            try:
                query = recognizor.recognize_google(audio)
                print("You: \n" + query)
            except speechRecog.UnknownValueError:
                speak(speakAgainDict[random.randint(1,3)])
            except speechRecog.RequestError:
                speak("Could not request results. The internet might be a little slow")
        else:
            randomQuestionMessage()
            firstQuestionFlag = False
            query = input("You: ")

        if(query == "exit" or query == "quit" or "bye" in query or "go away" in query or "see you" in query or "close" == query):
            endSession()
            break
        else:
            processQuery(query.lower())

#Speaks a random question message from the dictionary
def randomQuestionMessage():
	if firstQuestionFlag:
		speak(questionDict[random.randint(1,8)])
	else:
		speak(questionDict[random.randint(8,len(questionDict))])

#Implementation of pyttsx engine for speaking from text
def speak(sentence):
    print(sentence)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate+18)
    engine.setProperty('voice', voices[1].id)
    engine.say(sentence)
    engine.runAndWait()

#The mind of the program, where all text queries are processed
def processQuery(query):
    if "lyrics for" in query or "lyrics of" in query:
        songName = query.split("lyrics")[1].split(" ")
        lyricQuery = ""
        for i in songName[2:]:
            if i != "by":
                lyricQuery += i + "-"
            else:
                lyricQuery += "lyrics-"
        getLyricsForSong(lyricQuery[:-1])
    elif "toss a coin" in query or ("can you toss" in query):
        speak("Heads") if random.randint(1,2) == 1 else speak("Tails it is")
    elif "where are you" in query or "where do you live" in query:
        speak(whereAreYouMessageDict[random.randint(1,len(whereAreYouMessageDict))])
    elif "who are you" in query or "what is your name" in query:
        speak(whoAreYouMessageDict[random.randint(1,len(whoAreYouMessageDict))])
    elif "agnes" in query and "mean" in query and ("what" in query or "can you tell" in query):
        speak(agnesMeaningDict[random.randint(1,len(agnesMeaningDict))])
    elif "time" in query and ("can" in query or "what" in query or "get me" in query or "tell me" in query) or "current" in query:
        tellTime()
    elif "weather" in query and ("can" in query or "what" in query or "get me" in query or "tell me" in query) or "current" in query:
        tellWeather()
    elif "you do" in query and ("can" in query or "what" in query):
        speak(whatCanYouDoDict[random.randint(1, len(whatCanYouDoDict))])
    elif "joke" in query and ("can" in query or "tell" in query or "say" in query):
        tellAJoke()
    elif "news" in query and ("can" in query or "get me" in query):
        getNews()
    elif "youtube" in query or "video" in query or "videos" in query and ("show" in query or "get me" in query or "start" in query):
        openYoutube()
    elif "cls" in query or "clear" in query or "clear screen" in query or "clean display" in query or "clear terminal" in query or "clean terminal" in query or "clean the screen" in query or "clear the screen" in query or "clean the terminal" in query or "clear the terminal" in query:
        clearDisplay()
    elif "date" in query or "today" in query and ("can" in query or "what" in query or "get me" in query or "tell me" in query)  or "current" in query:
        tellDate()
    elif "start" in query or "open" in query:
        if "start" in query:
            appName = query.split("start")[1].split()[0]
        elif "open" in query:
            appName = query.split("open")[1].split()[0]
        startApp(appName)
    elif "music" in query or "song" in query and ("start" in query or "play" in query or "put on" in query):
        playMusic()
    elif "+" in query or "-" in query or "*" in query or "/" in query:
        queryTokens = query.split()
        operation = ""
        started = False
        startIndex, lastIndex = 0,0
        for i in range(len(queryTokens)):
            for j in queryTokens[i]:
                if j.isdigit() and not started:
                    started = True
                    startIndex = i
        if lastIndex == 0:
            lastIndex = len(queryTokens)
        operation = " ".join(queryTokens[startIndex:lastIndex])
        calculate(operation)
    elif "my name" in query:
        if "who am i" in query or "what is my name" in query or "can you tell me" in query:
            whoAmI()
        elif "change name" in query or "change my name" in query:
            changeUserName()
    elif "where is" in query or "map of" in query or "map for" in query:
        location = ""
        if "where is" in query:
            location = query.split()[2:]
        elif "show map" in query:
            location = query.split()[3]
        if "of" in location or "for" in location or "the" in location or len(location) == 0:
            speak("I didn't get the location, can you specify the location name again?")
            location = input().strip()
        showOnMap(location)
    else:
        speak(notCapableMessageDict[random.randint(1, len(notCapableMessageDict))])

#To start an application
def startApp(appName):
    speak("Starting " + appName + " now")
    os.system("start " + appName)

#When the user types 'bye' or 'exit'
def endSession():
    speak(endChatDict[random.randint(1,4)] + userName)
    conn.commit()
    conn.close()

#In order to play music from Spotify
def playMusic():
    speak("Starting a music app now")
    os.system("start spotify")

#Tells the current time
def tellTime():
    if datetime.datetime.now().hour < 12:
            speak("It's " + str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) + " in the morning")
    elif datetime.datetime.now().hour >= 12 and datetime.datetime.now().hour < 16:
        speak("It's " + str(datetime.datetime.now().hour - 12) + ":" + str(datetime.datetime.now().minute) + " in the noon")
    elif datetime.datetime.now().hour >= 16 and datetime.datetime.now().hour < 20:
        speak("It's " + str(datetime.datetime.now().hour - 12) + ":" + str(datetime.datetime.now().minute) + " in the evening")
    else:
        speak("It's " + str(datetime.datetime.now().hour - 12) + ":" + str(datetime.datetime.now().minute) + " in the night")

#Tells the current date
def tellDate():
    today = datetime.datetime.now()
    speak("It is a " + str(today.strftime("%A")) + " today and the date is " + str(today.strftime("%d %B %Y")))

#Gets the lyrics from metroLyrics using web scraping
def getLyricsForSong(songName):
    try:
        uClient = urlReq(lyrics_url + songName + ".html")
        page_html = uClient.read()
        uClient.close()

        page_soup = soup(page_html, "html.parser")
        containers = page_soup.findAll("p", {"class":"verse"})

        speak("Here are the lyrics for that song\n")
        for container in containers:
            print(container.text)
    except urllib.error.HTTPError:
        speak(noLyricsMessageDict[random.randint(1,len(noLyricsMessageDict))])

#Similar to cls or clear
def clearDisplay():
    speak("Clearing screen now")
    if platform.system() == 'Windows':
        os.system("cls")
    elif platform.system() == 'Linux':
        os.system("clear")

#Scrapes the weather data from www.weather.com
def tellWeather():
    try:
        speak(weatherDict[random.randint(1,len(weatherDict))])
        uClient = urlReq(weather_url)
        page_html = uClient.read()
        uClient.close()

        page_soup = soup(page_html, "html.parser")
        tempValue = page_soup.find("div", {"class":"today_nowcard-temp"})
        currentTemperature = tempValue.span.text
        sideTable = page_soup.find("div", {"class" : "today_nowcard-sidecar component panel"}).table.tbody.tr.td.span
        wind = sideTable.text
        windDirection = wind.split()[0]
        windSpeed = wind.split()[1] + wind.split()[2]

        speak("It's " + currentTemperature + "C currently with a wind speed of " + windSpeed + " in the direction " + windDirectionTable[windDirection])
    except urllib.error.HTTPError:
        speak("It seems the weather server is ignoring me. Can you try this later?")

#Returns the value of an expression in input
def calculate(expression):
    speak(calculateMessageDict[random.randint(1,len(calculateMessageDict))] + " " + str(format(eval(expression), '.3f')))

#Opens news.google.com
def getNews():
    speak("Opening Google News in the browser")
    webbrowser.open_new_tab("https://news.google.com")
    speak("Here you go")

#Opens Youtube in a browser
def openYoutube():
    webbrowser.open_new_tab("https://www.youtube.com")
    speak("Done")

#Tells a random joke from the dictionary
def tellAJoke():
    speak(jokeDictionary[random.randint(1,len(jokeDictionary))])

#Displays a greeting message according to the current time
def greetForCurrentTime():
    if(datetime.datetime.now().hour < 12):
        speak(morningMessageDict[random.randint(1,len(morningMessageDict))] + " " + userName)
    elif(datetime.datetime.now().hour >= 12 and datetime.datetime.now().hour <= 16):
        speak(afternoonMessageDict[random.randint(1,len(afternoonMessageDict))] + " " + userName)
    elif(datetime.datetime.now().hour > 16 and datetime.datetime.now().hour <= 22):
        speak(eveningMessageDict[random.randint(1,len(eveningMessageDict))] + " " + userName)
    else:
        speak(nightMessageDict[random.randint(1,len(nightMessageDict))])

#Responses to when asked "Who am I"
def whoAmI():
    speak(whoAmIDict[random.randint(1,len(whoAmIDict))] + userName)

#Inputs the name of the user and stores it in the databases
def inputAndSaveUser():
    global userName
    speak(noUserMessageDict[random.randint(1, len(noUserMessageDict))])
    userName = input().strip()
    dataCursor.execute("INSERT INTO Users(name) VALUES(?)", (userName, ))
    conn.commit()

#Method to change the currently saved username
def changeUserName():
    global userName
    speak("What should I call you?")
    newName = input("You: ").strip()
    dataCursor.execute("UPDATE Users SET name = '" + newName + "' WHERE name = '" + userName + "';")
    conn.commit()
    userName = newName

#Shows a specified location on the map
def showOnMap(locationQuery):
    speak("Let me search it on the maps for you")
    webbrowser.open_new_tab("https://www.google.com/maps/place/" + " ".join(locationQuery) + "/&amp;")

#The main method
def main():
    global userName
    dataCursor.execute("CREATE TABLE IF NOT EXISTS Users(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    dataCursor.execute("SELECT * FROM Users")
    fetchedData = dataCursor.fetchone()
    if fetchedData == None:
        inputAndSaveUser()
        os.system("pip install -r requirements.txt")
    else:
        userName = fetchedData[1]
    greetForCurrentTime()
    global microphoneExistFlag
    try:
        speechRecog.Microphone()
        microphoneExistFlag = False
    except OSError:
        #speak("I'm sorry but I didn't detect a microphone. You'll need to use the keyboard")
        microphoneExistFlag = False

    takeInput()

if __name__ == "__main__":
    main()
