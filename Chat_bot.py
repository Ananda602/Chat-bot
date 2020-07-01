import random
import speech_recognition as sr
import datetime
import calendar
import time
import webbrowser
import wikipedia
from gtts import gTTS
import playsound
import os
import win10toast
from bs4 import BeautifulSoup
import requests
import re
import nltk
from googletrans import Translator
import sports
from newspaper import Article


bot_name = "Rag2020"
bot_template = "{0}"
user_template = "{1}"

def send_message(message):
    response = respond(message)
    alex_speak(bot_template.format(response))


def respond(message):
    if message in responses:
        bot_message = random.choice(responses[message])
    elif 'Search' in message:
        search = record_audio("Specify the word")
        url = "https://google.com/search?q=" +search
        bot_message = webbrowser.get().open(url)
    elif message == "Find Location":
        location = record_audio("City name")
        url = "https://google.ml/maps/place/" + location +'/&amp;'
        bot_message = webbrowser.get().open(url)
    elif message == "Calculate":
        m = record_audio("What you have to compute")
        bot_message = calculate(m)
    elif 'who is' in message:
        person = person_name(message)
        bot_message = wikipedia.summary(person, sentences=2)
    elif message == "Set An Remainder":
        bot_message = remainder()
    elif message == "Set An Alarm":
        bot_message = alarm()
    elif message == "Play Me A Song":
        bot_message = melody()
    elif message == "Weather":
        bot_message = weather_manager()
    elif message == "Wikipedia":
        bot_message = scrap()
    elif message == "Translate":
        bot_message = trans()
    elif message == "Headlines":
        bot_message = news_scrap()
    elif message == "Live Score":
        bot_message = sport_score()
    elif message == "Exit":
        breakpoint()
    else:
        bot_message = random.choice(responses["Default"])

    return bot_message


def date_and_time():
    now = datetime.datetime.now()
    today = datetime.datetime.today()
    weekday = calendar.day_name[today.weekday()]
    month = now.month
    day = now.day
    month_list = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']

    Numbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th',
               '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24th', '25th', '26th', '27th',
               '28th', '29th', '30th', '31st']

    return "Today is "+weekday + ' '+month_list[month-1]+' the ' + Numbers[day-1]


def month():
    now = datetime.datetime.now()
    month = now.month

    month_list = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']

    return month_list[month-1]


def current_time():
    local_time = time.ctime()
    return local_time


def calculate(message):
    message = message.split()
    i = 0
    request_d = {}
    for req in message:
        request_d[i] = req
        i = i + 1
    for key,value in request_d.items():
        if value == '+':
            return int(request_d[key - 1]) + int(request_d[key + 1])
        if value == '-':
            return int(request_d[key - 1]) - int(request_d[key + 1])
        if value == '*':
            return int(request_d[key - 1]) * int(request_d[key + 1])
        if value == '/':
            return int(request_d[key - 1]) / int(request_d[key + 1])



def person_name(text):
    name = text.split()
    for i in range(0, len(name)):
        if i + 3 <= len(name)-1 and name[i].lower == 'who' and name[i+1].lower == 'is':
            return name[i+2]+ ' '+ name[i+3]


def remainder():
    Remainder_message = record_audio("Enter the remainder message:")
    time = str(input("Enter the timing in format HH:MM"))
    date = str(input("Enter the remainder date in format DD/MM/YYYY"))
    time = time.split(":")
    date = date.split("/")
    timings = str(input("Enter AM or PM"))
    timings = timings.lower()
    alarmHour = int(time[0])
    alarmMinute = int(time[1])
    rem_date = int(date[0])
    rem_month = int(date[1])
    rem_year = int(date[2])
    if timings == "pm":
        alarmHour = alarmHour + 12

    while True:
        if alarmHour == datetime.datetime.now().hour and alarmMinute == datetime.datetime.now().minute and rem_date == datetime.datetime.now().day and rem_month == datetime.datetime.now().month and rem_year == datetime.datetime.now().year:
            toaster = win10toast.ToastNotifier()
            notification_message = toaster.show_toast("Pycharm", Remainder_message, duration=10)
            return notification_message


def news_scrap():
    url = 'https://www.indiatoday.in/top-stories'
    article = Article(url)

    article.download()
    article.parse()
    nltk.download('punkt')
    article.nlp()

    return article.text


def sport_score():
    import sports
    matches = sports.all_matches()
    match_invoked = record_audio("Enter the game you want to search")
    if match_invoked == 'Cricket':
        cricket = matches['cricket']
    elif match_invoked == 'Football':
        cricket = matches['football']
    else:
        cricket = "no matches found"

    return cricket

def trans():
    trans = Translator()
    text = record_audio("Specify the sentence or word to be translated:")
    source = record_audio("From Languages:")
    source = source.lower()
    source = source[0:2]
    desti = record_audio("To Languages:")
    desti = desti.lower()
    desti = desti[0:2]

    t = trans.translate(
        text, src=source, dest=desti
    )

    return t.text


def scrap():
    search = record_audio("Enter the word")
    url = f"https://en.wikipedia.org/wiki/{search}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    text = ""
    for paragraph in soup.find_all('p'):
        text += paragraph.text
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\d', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    sentences = nltk.sent_tokenize(text)
    return (sentences[0],sentences[1])

def alarm():
    time = record_audio("Enter the Time in the format HH:MM")
    time = time.split(":")
    alarmHour = int(time[0])
    alarmMinute = int(time[1])
    timings_module = str(input("Mention PM or AM"))
    timings_module = timings_module.lower()
    if timings_module == "pm":
        alarmHour = alarmHour + 12
    while True:
        if alarmHour == datetime.datetime.now().hour and alarmMinute == datetime.datetime.now().minute:
            from playsound import playsound
            alarm = playsound('C:/Users/Anandatirtha/PycharmProjects/Chat_ananda/the-purge-siren-ringtone.mp3')
            return alarm


def melody():
    from playsound import playsound
    melody = playsound('C:/Users/Anandatirtha/PycharmProjects/Chat_ananda/nature-alarm-sounds.mp3')
    return melody

def weather_manager():
    place = record_audio("Enter the name of place")
    search = f"Weather in {place}"
    url = f"https://www.google.com/search?&q={search}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    update = soup.find("div", class_="BNeawe").text
    weather_report = "The current temperature in {0} is {1}".format(place, update)
    return weather_report

responses = {
    "Hey Alex": ["Your bot is activating..."," Bot is Launcing 3 2 1"],
    "Good Morning": ["Good Morning have a great day", "great day ahead", "have a wonderful day", "Good Morning"],
    "Hi": ["Hi", "Hello", "Hola", "Hi there", "what's special today"],
    "Default": ["I can't get you", "sorry one more time", "Sorry! again"],
    "Who Created You": ["I was developed by Anandatirtha", "By Anandatirtha", "I was developed by Anandatirtha as a demo bot"],
    "What Is Your Name": ["My name is {0}".format(bot_name), "Call me {0}".format(bot_name)],
    "Good Afternoon": ["Good Afternoon", "Good Afternoon after your great meal", "Good Afternoon don't forget to check notifications"],
    "Good Night": ["Good Night", "Good Night !! Sweet dreams", "Good Night we will meet Next day"],
    "What Is Today Date": [date_and_time()],
    "What Is The Month": [month()],
    "What Is The Time Now": [ time.ctime()],
    "Thank You": ["Welcome", "It's nice to hear from you"],
    "When Is Your Birthday": ["It's on June 2nd 2020", "It's on June 2nd 2020 at Rag labs"],
    "Happy Birthday Rag": ["Thank you for your wishes","Thak you so much for thinking of me", "Thanks for making me feel special on my birthday",
                          "I can't tell you how I enjoyed hearing from you"],
    "I Feel Stressed": ["Here are some tips to get rid of stress:\n 1) Avoid Caffine and Alcohol \n 2) Get more sleep \n 3)Talk to someone who cares you",
                             "Here are few tips to get rid of stress:\n 1) Listen some melody songs \n 2) Exercise regularly \n 3) Get enough sleep and rest",
                             "Follow these tips:\n 1) Make time for hobbies\n 2) Avoid using Mobile Phone \n 3) Get advise from mental health professional\n "
                             "4) Be positive"],
    "Feels Stressed": ["Here are some tips to get rid of stress:\n 1) Avoid Caffine and Alcohol \n 2) Get more sleep \n 3)Talk to someone who cares you",
                        "Here are few tips to get rid of stress:\n 1) Listen some melody songs \n 2) Exercise regularly \n 3) Get enough sleep and rest",
                        "Follow these tips:\n 1) Make time for hobbies\n 2) Avoid using Mobile Phone \n 3) Get advise from mental health professional\n "
                        "4) Be positive"],
    "How To Relieve Stress": ["Here are some tips to get rid of stress:\n 1) Avoid Caffine and Alcohol \n 2) Get more sleep \n 3)Talk to someone who cares you",
                              "Here are few tips to get rid of stress:\n 1) Listen some melody songs \n 2) Exercise regularly \n 3) Get enough sleep and rest",
                              "Follow these tips:\n 1) Make time for hobbies\n 2) Avoid using Mobile Phone \n 3) Get advise from mental health professional\n "
                              "4) Be positive"],
    "I Feel Bored": ["Here Some Melody songs", "I tired to play music but vain", "Sleep well"],
    # Medical field questions
    "Cold": ["The common cold is medically referred to as a viral upper respiratory tract infection. "
             "Symptoms of the common cold may include cough, sore throat, low-grade fever, nasal congestion, runny nose, and sneezing."],
    "I Have Cold": ["Sad to har from you", "Please, take rest from you", "Properly take medicines",
                        "Consult doctor before it becomes complicated"],
    "Symptoms For Cold": ["Here are results \n 1)Runny nose \n 2)Sore throat \n 3)Cough \n 4)Congestion \n 5)Body Achnes \n 6)Sneezing \n 7) Fever"],
    "How To Prevent From Cold": ["Here are some Prevention methods \n 1. Wash your hands properly \n 2. Disinfect your stuff \n 3. Avoid touching your eyes,nose and mouth \n 4. Stay away"],
    "Symptoms For Fever": ["1)Sweating 2)Headaches 3)Muscle aches 4) Loss of appetite 5)Dehydration"],
    "Symptoms For Throat Pain": ["1) Scratchy sensation in the throat \n 2)Difficulty in Swallowing \n 3)Sore"],
    "Symptoms For Acidity": ["1)Bloating \n 2) Burping \n 3)Dry Cough \n 4)Sore throat"],
     #Political questions
    "The 11Th President Of India": ["Abdul Kalam Azad"],
    "Member Of Rajya Sabha": ["Selected by elected members of Legislative Assembly"],
    "Current Prime Minister of India":["Narendra Damodardas Modi"],
    "Chief Minister Of Andhra Pradesh": ["Y.S Jaganmohan Reddy"],
    "Chief Minister Of Arunachal Pradesh": ["Pema Khandu"],
    "Chief Minister Of Assam": ["Sarbananda Sonowal"],
    "Chief Minister Of Bihar": ["Nitesh Kumar"],
    "Chief Minister Of Chhattisgarh": ["Bhupesh Baghel"],
    "Chief Minister Of Delhi": ["Arvind Kejriwal"],
    "Chief Minister Of Goa": ["Pramod Sawant"],
    "Chief Minister Of Gujarat": ["Vijay Rupani"],
    "Chief Minister Of Haryana": ["Manohar Lal Khattar"],
    "Chief Minister Of Himachal Pradesh": ["Jai Ram Thakur"],
    "Chief Minister Of Jammu and Kashmir": ["President's rule"],
    "Chief Minister Of Jharkhand": ["Hemant Soren"],
    "Chief Minister Of Karnataka": ["B. S. Yediyurappa"],
    "Chief Minister Of Kerala": ["Pinarayi Vijayan"],
    "Chief Minister Of Madhya Pradesh": ["Shivraj Singh Chouhan"],
    "Chief Minister Of Maharashtra": ["Uddhav Thackeray"],
    "Chief Minister Of Manipur": ["N. Biren Singh"],
    "Chief Minister Of Meghalaya": ["Conrad Sangma"],
    "Chief Minister Of Mizoram": ["Zoramthanga"],
    "Chief Minister Of Nagaland": ["Neiphiu Rio"],
    "Chief Minister Of Odisha": ["Naveen Patnaik"],
    "Chief Minister Of Puducherry": ["V. Narayanasamy"],
    "Chief Minister Of Punjab": ["Amarinder Singh"],
    "Chief Minister Of Rajasthan": ["Ashok Gehlot"],
    "Chief Minister Of Sikkim": ["Prem Singh Tamang"],
    "Chief Minister Of Tamil Nadu": ["Edappadi K. Palaniswami"],
    "Chief Minister Of Telangana": ["K. Chandrashekhar Rao"],
    "Chief Minister Of Tripura": ["Biplab Kumar Deb"],
    "Chief Minister Of Uttar Pradesh": ["Yogi Adityanath"],
    "Chief Minister Of Uttarakhand": ["Trivendra Singh Rawat"],
    "Chief Minister Of West Bengal": ["Mamata Banerjee"],
    "Defence Minster Of India": ["Shri.Raj Nath Singh"],
    "Ministry Of Home Affairs": ["Amit Shah"],
    #capital of States in India
    "Capital Of Tripura": ["Agartala"],
    "Capital Of Rajasthan": ["Jaipur"],
    "Capital Of Sikkim": ["Gangtok"],
    "Capital Of Arunachal Pradesh": ["Itanagar"],
    "Capital Of Maharasthtra": ["Mumbai"],
    "Capital Of Mizoram": ["Aizawl"],
    "Capital Of Chhattisgarh": ["Raipur"],
    "Capital Of Telangana": [" Hyderabad"],
    "Capital Of Assam": ["Dispur"],
    "Capital Of Uttar Pradesh": ["Lucknow"],
    "Capital Of Himachal Pradesh": ["Shimla"],
    "Capital Of Gujarat": ["Gandhinagar"],
    "Capital Of Bihar": ["Patna"],
    "Capital Of Haryana": ["Chandigarh"],
    "Capital Of Jammu & Kashmir": [" Srinagar & Jammu"],
    "Capital Of Uttaranchal": ["Dehradun"],
    "Capital Of Nagaland": ["Kohima"],
    "Capital Of Tamil Nadu": ["Chennai"],
    "Capital Of Meghalaya": ["Shillong"],
    #national games
    "What Is The National Game Of Bangladesh": ["Kabaddi"],
    "What Is The National Game Of Argentina": ["Pato"],
    "What Is The National Game Of United States": ["Baseball"],
    "What Is The National Game Of Afghanistan": ["Buzkashi"],
    "What Is The National Game Of Bhutan": [" Archery"],
    "What Is The National Game Of Sri Lanka": ["Volley ball"],
    "What Is The National Game Of Turkey": ["Oil Wrestling"],
    "What Is The National Game Of India": [" Field Hockey"],
    "What Is The National Game Of England": ["Cricket"],
    "What Is The National Game Of Scotland": ["Golf"],
    "What Is The National Game Of Iran": ["Wrestling"],
    "What Is The National Game Of Hungary": [" Water Polo"],
    "What Is The National Game Of Cuba": ["Baseball"],
    "What Is The National Game Of Pakistan": ["Field Hockey"],
    "What Is The National Game Of Brazil": ["Football"],
    "What Is The National Game Of Russia": ["Bandy"],
    "What Is The National Game Of Canada in Summer ": ["Lacrosse"],
    "What Is The National Game Of Canada in Winter": ["Ice Hockey"],
    "What Is The National Game Of Spain": ["Bull Fighting"],

}


def record_audio(ask=False):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        if ask:
            alex_speak(ask)

        audio = r.listen(source)
        data = ''
        try:
            data = r.recognize_google(audio)
        except sr.UnknownValueError():
            alex_speak("Error")
        except sr.RequestError():
            alex_speak("Error 1")

        return data

def alex_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' +str(r)+'.mp4'
    tts.save(audio_file)
    print(audio_string)
    playsound.playsound(audio_file)
    os.remove(audio_file)

alex_speak("What can I do for you")
while True:
    message = record_audio()
    send_message(message.title())