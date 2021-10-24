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
import sqlite3
import requests
from underthesea import pos_tag
from bs4 import BeautifulSoup
import urllib.request
import wikipedia as wi
import gc
wi.set_lang("vi")
conn = sqlite3.connect('chatbotdb')
cursor = conn.cursor()
print("Database created and Successfully Connected to SQLite")

stopword = ['là gì','là ai', 'như thế nào', 'chưa hiểu', 'muốn biết về', 'ở đâu']
xinchao = ['hello', 'hey yo', 'hey', 'hi', 'nice to meet you', 'hello my friend', 'alo', 'hi buddy', 'yo']
gioi_thieuten = ['chatbot?', 'who are you', 'info']
camon = ['tks', 'thank you', 'i got it', 'ok', 'perfect', 'briliant', 'wah', 'oh']

class ask_bomon_gv(Action):
    def name(self) -> Text:
        return "ask_bomon_gv"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        bomon = '%'+tracker.latest_message['entities'][0].get('value').lower()
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
        sqlite_select_Query = 'SELECT * from giaoVien where lower(mon) like ' + '"'+bomon+'"'
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        if record:
            try:
                if len(record) >= 2:
                    dispatcher.utter_message('bộ môn ' + tracker.latest_message['entities'][0].get('value') + ' có ' + str(len(record)) + ' giáo viên là:') 
                for i in record:
                    dispatcher.utter_message(i[4]) 
            except:
                dispatcher.utter_message("Không có giáo viên bạn cần tìm trong khoa!!!")
        else: dispatcher.utter_message("Không có giáo viên bạn cần tìm trong khoa!!!")


class action_dinhnghia(Action):
    def name(self) -> Text:
        return "action_dinhnghia"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
        ent = []
        h = 0
        for i in tracker.latest_message['entities']:
            s = i.get('value').lower()
            s = s.replace(' và', '')
            s = s.replace('và ', '')
            ent.append(s)
            h += 1
        check = 0
        print(ent)
        for i in ent:
            sqlite_select_Query = 'SELECT * from quyChe where lower(entity) = ' + '"'+i+'"'
            cursor.execute(sqlite_select_Query)
            print(sqlite_select_Query)
            record = cursor.fetchall()
            check += len(record)
            print(ent)
            for result in record:
                dispatcher.utter_message(result[2])
        if check == 0: action_unknown.run2(dispatcher, tracker, domain)

class ask_vitri(Action):
    def name(self) -> Text:
        return "ask_vitri"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = tracker.latest_message['text']
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
        text_input = text.lower()
        ent = ['','']
        h = 0
        for i in tracker.latest_message['entities']:
            ent[h] =  '%'+i.get('value').lower()
            h += 1
        check = 0
        print(ent)
        for i in ent:
            sqlite_select_Query = 'SELECT * from phongHoc where lower(entity) like ' + '"'+i+'"'
            cursor.execute(sqlite_select_Query)
            print(sqlite_select_Query)
            record = cursor.fetchall()
            check += len(record)
            print(ent)
            for result in record:
                dispatcher.utter_message(result[2])
        if check == 0: action_unknown.run2(dispatcher, tracker, domain)

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
                dispatcher.utter_message("Xin lỗi, mình không biết giáo viên bạn muốn tìm!")
        else:
            for result in record:
                name = result[1].lower()
                if ent[1:].lower() in name:
                    check = True
                    dispatcher.utter_message(result[4])   
            if not check :
                dispatcher.utter_message("Xin lỗi, mình không biết giáo viên bạn muốn tìm!")

class ask_thoitiet(Action):
    def name(self) -> Text:
        return "ask_thoitiet"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Accept-Language': 'vi'}
        city= 'cantho'
        city = city+'+weather'
        res = requests.get(f'https://www.google.com/search?q={city}&oq={city}&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        location = soup.select('#wob_loc')[0].getText().strip()
        time = soup.select('#wob_dts')[0].getText().strip()
        info = soup.select('#wob_dc')[0].getText().strip()
        weather = soup.select('#wob_tm')[0].getText().strip()
        dispatcher.utter_message(location)
        dispatcher.utter_message(info + ' vào lúc: '+ time.lower())
        dispatcher.utter_message('Nhiệt độ trung bình: '+weather+"°C")

class ask_gvname(Action):
    def name(self) -> Text:
        return "ask_gvname"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('[%s] <- %s' % (self.name(), tracker.latest_message['text']))
        if 'cô' in tracker.latest_message['text']:
            gioitinh = 'cô'
        elif 'thầy' in tracker.latest_message['text']:
            gioitinh = 'thầy'
        else: gioitinh = '%'
        ten = '%'+tracker.latest_message['entities'][0].get('value')
        sqlite_select_Query = 'SELECT * from giaoVien where ten like ' + '"'+ten+'"' + 'and gioitinh like ' + '"' + gioitinh+ '"'
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        if record:
            try:
                if len(record) >= 2:
                    dispatcher.utter_message('Có ' + str(len(record))+' giáo viên tên ' + tracker.latest_message['entities'][0].get('value') + ' tại Khoa') 
                for i in record:
                    dispatcher.utter_message(i[4]) 
            except:
                dispatcher.utter_message("Xin lỗi, mình không biết giáo viên bạn muốn tìm!")
        else: dispatcher.utter_message("Xin lỗi, mình không biết giáo viên bạn muốn tìm!")

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
        slot = tracker.get_slot('nganh_hoc')
        ent = ['','']
        if slot:
            ent[0] = '%'+slot
        else: 
            h = 0
            ent = ['','']
            for i in tracker.latest_message['entities']:
                ent[h] =  '%'+i.get('value').lower()
                h += 1

        intent = tracker.latest_message['intent'].get('name')
        print('[%s] <- %s' % (self.name(), intent))
        print(ent)
        check = 0
        for i in ent:
            sqlite_select_Query = 'SELECT * from ' + intent + ' where entity like ' + '"'+i+'"'
            cursor.execute(sqlite_select_Query)
            print(sqlite_select_Query)
            record = cursor.fetchall()
            check += len(record)
            for result in record:
                dispatcher.utter_message(result[2]) 
        if check == 0: action_unknown.run2(dispatcher, tracker, domain)


class action_unknown(Action):
    def name(self) -> Text:
        return "action_unknown"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        texttt = (tracker.latest_message['text']).lower()
        print('[%s] <- %s' % (self.name(), texttt))
        for i in stopword:
            s = texttt.replace(i, '')
            texttt = s
        try:
            s = wi.summary(texttt, sentences='1', auto_suggest = False)
            s1 = wi.page(texttt)
            dispatcher.utter_message(s)
            dispatcher.utter_message(s1.url)
        except:
            dispatcher.utter_message(
                text="Xin lỗi bạn vì hiện tại mình chưa hiểu bạn muốn gì!")
    @staticmethod
    def run2(dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        texttt = (tracker.latest_message['text'])
        for i in stopword:
            s = texttt.replace(i, '')
            texttt = s
        try:
            s = wi.summary(texttt, sentences='1', auto_suggest = False)
            s1 = wi.page(texttt)
            dispatcher.utter_message(s)
            dispatcher.utter_message(s1.url)
        except:
            dispatcher.utter_message(text="Xin lỗi bạn vì hiện tại mình chưa hiểu bạn muốn gì!")


