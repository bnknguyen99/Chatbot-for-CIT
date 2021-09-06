# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from typing import Text, List, Dict, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json
import re
import sqlite3
from underthesea import pos_tag
from bs4 import BeautifulSoup
import urllib.request
import wikipedia as wi
import gc
wi.set_lang("vi")

conn = sqlite3.connect('chatbotdb')
cursor = conn.cursor()
print("Database created and Successfully Connected to SQLite")

def nocheck(dispatcher: CollectingDispatcher, tracker: Tracker,):
    texttt = (tracker.latest_message['text']).lower()
    try:
        s = wi.summary(texttt, sentences='1')
        s1 = wi.page(texttt)
        return (s,s1.url)
    except:
        text = "Xin lỗi bạn vì hiện tại mình chưa hiểu bạn muốn gì! Bạn hãy bấm vào đây để  nhờ chị Google giải đáp nhé: https://www.google.com.vn/search?q=" + tracker.latest_message['text'].replace(" ", "%20") 
        return text

class ask_bomon_gv(Action):
    def name(self) -> Text:
        return "ask_bomon_gv"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = tracker.latest_message['text']
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
        text_input = text.lower()
        sqlite_select_Query = "SELECT * from giaoVien"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        check = False
        print(text_input)
        for result in record:
            subject = result[3].lower()
            if subject in text_input:
                check = True
                dispatcher.utter_message(result[4])       
        if not check:
            dispatcher.utter_message("Không có bộ môn bạn cần tìm trong khoa!!!")

class action_dinhnghia(Action):
    def name(self) -> Text:
        return "action_dinhnghia"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = tracker.latest_message['text']
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
        text_input = text.lower()
        sqlite_select_Query = "SELECT * from quyChe"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        check = False
        print(text_input)
        for result in record:
            name = result[1].lower()
            define = result[2]
            if name in text_input:
                check = True
                dispatcher.utter_message(define)       
        if not check:
            dispatcher.utter_message(
            text="Xin lỗi bạn vì hiện tại mình chưa hiểu bạn muốn gì! Bạn hãy bấm vào đây để  nhờ chị Google giải đáp nhé: https://www.google.com.vn/search?q=" +
                 tracker.latest_message['text'].replace(" ", "%20") )

class ask_vitri(Action):
    def name(self) -> Text:
        return "ask_vitri"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = tracker.latest_message['text']
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
        text_input = text.lower()
        sqlite_select_Query = "SELECT * from phongHoc"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        check = False
        print(text_input)
        for result in record:
            name = result[1].lower()
            define = result[2]
            if name in text_input:
                check = True
                dispatcher.utter_message(define)       
        if not check:
            kq = nocheck( CollectingDispatcher, tracker)
            for i in kq:
                dispatcher.utter_message(i)

class ask_gvfullname(Action):
    def name(self) -> Text:
        return "ask_gvfullname"    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ent = '' #tracker.latest_message['entities'][0]['value'].lower()
        for i in  tracker.latest_message['entities']:
            ent += (' '+i['value'])
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
        sqlite_select_Query = "SELECT * from giaoVien"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        check = False
        if not ent: 
            for result in record:
                name = result[1].lower()
                if tracker.latest_message['text'].lower() in name:
                    check = True
                    dispatcher.utter_message(result[4])   
            if not check :
                dispatcher.utter_message("Không có giáo viên bạn cần tìm trong khoa!!!")
        else:
            for result in record:
                name = result[1].lower()
                if ent[1:].lower() in name:
                    check = True
                    dispatcher.utter_message(result[4])   
            if not check :
                dispatcher.utter_message("Không có giáo viên bạn cần tìm trong khoa!!!")

class ask_gvname(Action):
    def name(self) -> Text:
        return "ask_gvname"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = tracker.latest_message['text']
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
        for x in text.split(' '):
            if x == 'Cô':
                x = 'cô'
            if x == 'Thầy':
                x = 'thầy'
        text_input = text.lower()
        sqlite_select_Query = "SELECT * from giaoVien"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        check = False
        gvname=''
        countsex=0
        j=0
        for i in range(len(pos_tag(text))):
            for x in pos_tag(text)[i]:
                if x == 'Np':
                    gvname=pos_tag(text)[i][0]
                    countsex+=1
                    j=i
                gvsex=pos_tag(text)[j-countsex][0].lower()
        if  gvname == '':
            dispatcher.utter_message("Không có giáo viên bạn cần tìm trong khoa!!!")
        else:
            print(gvsex)
            for result in record:
                name = result[1]
                sex = result[2].lower()
                info = result[4].lower()
                if name.split(' ')[len(name.split(' '))-1] in gvname[0:len(gvname)] and sex==gvsex:
                    check = True
                    dispatcher.utter_message(result[4])   
            if not check :
                dispatcher.utter_message("Không có giáo viên bạn cần tìm trong khoa!!!")

class action_whatnew(Action):

    def name(self) -> Text:
        return "action_whatnew"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url =  'https://www.ctu.edu.vn/tin-tuc.html'
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        new_feeds = soup.find('div', class_='content').find_all('div', class_='items-row')
        dispatcher.utter_message('Thông tin mới nhất từ trang thông tin Đại học Cần Thơ:')
        for feed in list(new_feeds):
            feed_result= feed.find('a')
            title = feed_result.contents[0]
            link = feed_result.get('href')
            dispatcher.utter_message('{} \nChi tiết: {}'.format(title, url+link))


class action_ask(Action):
    def name(self) -> Text:
        return "action_ask"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ent = ''
        for j in tracker.latest_message['entities']:
            ent += (' '+ j['value'])
        intent= tracker.latest_message['intent'].get('name')
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
        print('[%s] <- %s' % (self.name(), intent))
        sqlite_select_Query = "SELECT * from " + intent
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        check = False
        for result in record:
            name = result[1].lower()
            define = result[2]
            if name in ent[1:].lower():
                check = True
                dispatcher.utter_message(define) 
        if not check:
            dispatcher.utter_message(
            text="Xin lỗi bạn vì hiện tại mình chưa hiểu bạn muốn gì! Bạn hãy bấm vào đây để  nhờ chị Google giải đáp nhé: https://www.google.com.vn/search?q=" +
                 tracker.latest_message['text'].replace(" ", "%20") )



class action_unknown(Action):

    def name(self) -> Text:
        return "action_unknown"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        texttt = (tracker.latest_message['text']).lower()
        print('[%s] <- %s' % (self.name(), texttt))
        try:
            s = wi.summary(texttt, sentences='1')
            s1 = wi.page(texttt)
            dispatcher.utter_message(s)
            dispatcher.utter_message(s1.url)
        except:
            dispatcher.utter_message(
                text="Xin lỗi bạn vì hiện tại mình chưa hiểu bạn muốn gì! Bạn hãy bấm vào đây để  nhờ chị Google giải đáp nhé: https://www.google.com.vn/search?q=" +
                    tracker.latest_message['text'].replace(" ", "%20") )

