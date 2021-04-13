import vk_api
import json
import shutil
# from YANDEX_LY.data.db_session import global_init, create_session
from YANDEX_LY.data.VKusers import VKuser
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import vk_api.keyboard
from YANDEX_LY.data.db_session import global_init, create_session
import datetime
import fitz
import os
import requests
from PIL import Image
import threading
from threading import Thread

boxOfImages = []
update_hours_list = [6, 16, 18, 20]
url_today = ''
url_to_download = ''
list_with_checklists = []
todaydata = int(datetime.datetime.today().day)
nextdaydata = todaydata + 1
downloading_checklist_now = False


class Schedule:
    def __init__(self, FILENAMEpdf):
        self.FILENAMEpdf = FILENAMEpdf

    def download_pdf(self):
        def check_url(checking_url):
            return checking_url[-1] == "f"

        def get_new_url():
            global html, ind, url_list, flag_url
            new_url = URL
            if ROADFOLDER in html:
                len_html = len(html)
                html = html[html.index(ROADFOLDER):]
                for item in range(len_html):
                    if html[item] != chr(34):
                        new_url += html[item]
                    else:
                        if check_url(new_url):
                            if flag_url:
                                url_list.append(new_url)
                                html = html[item + 1:]
                                get_new_url()
                        else:
                            break

        def check_urls(url_list_in, todaydata1, nextdaydata1):
            string_from_urls = ''.join(url_list_in)
            if str(nextdaydata1) in string_from_urls:
                return 1
            elif str(todaydata1) in string_from_urls:
                return 2
            else:
                return 0

        global html, ind, url_list, flag_url, list_with_checklists, url_to_download, url_today, todaydata, nextdaydata
        flag_url = True
        url_list = list()
        URL = 'https://school.kco27.ru//'
        ROADFOLDER = 'wp-content/uploads/shedule/'
        html = requests.get(URL).text
        ind = html.index(ROADFOLDER)
        html = html[ind:]
        get_new_url()
        check_res = check_urls(url_list, todaydata, nextdaydata)
        if check_res == 1:
            for item in url_list:
                if str(nextdaydata) in item:
                    url_to_download = item
                    break
        elif check_res == 2:
            for item in url_list:
                if str(todaydata) in item:
                    url_to_download = item
                    break
        else:
            url_today = url_today
        try:
            request = requests.get(url_to_download, stream=True)
            with open(self.FILENAMEpdf, 'wb') as file:
                file.write(request.content)
        except ValueError:
            print(str(ValueError))

    def delete_pdf_imades(self):
        pass

    def get_classes(self):
        text = self.get_text_pdf()
        box = []
        for i in text.split('\n'):
            if '.' in i:
                iq = i.replace('/', '').replace('.', '').replace(' ', '')
                if any([j.isdigit() for j in (iq)]) and iq.isalnum():
                    if len(i.replace(' ', '')) < 8:
                        if len(i.split('.')) == 2 and len(i.split('.')[0]) == 2 and len(i.split('.')[1]) == 2:
                            pass
                        else:
                            if int(i.split('.')[0]) > 9:
                                box.append(i.strip())
                            else:
                                i = i.split()[0]
                                box.append('.'.join(i.replace('.', ' ').strip().split()))
        return box

    def get_class_groupes(self, clas):
        lst = []
        for i in self.get_classes():
            if i.startswith(clas):
                lst.append(i)
        return lst

    def get_phooto_path(self, clas):
        pass

    def get_num_of_borders(self, text):
        numOfborders = 0
        if 'кабинет' in text.lower() or 'каб.' in text.lower():
            numOfborders += 1
        if 'учитель' in text.lower() or 'уч.' in text.lower():
            numOfborders += 1
        return numOfborders

    def get_text_pdf(self):
        txt = ''
        pdf_document = self.FILENAMEpdf
        doc = fitz.open(pdf_document)
        page1 = doc.loadPage(0)
        txt += '\n' + page1.getText("text")
        page1 = doc.loadPage(1)
        txt += '\n' + page1.getText("text")
        page1 = doc.loadPage(2)
        txt += '\n' + page1.getText("text")
        page1 = doc.loadPage(3)
        txt += '\n' + page1.getText("text")
        return txt

    def get_indent(self, pixMap, width, height):
        box = []
        for i in range(height):
            tok = 0
            for j in range(width):
                if pixMap[j, i] == (0, 0, 0):
                    tok += 1
            if tok > 500:
                box.append(i)
        return (box[0], box[-1])

    def make_lessonslists(self, classes, filePath, pdffile):
        global boxOfImages
        try:
            os.makedirs("data")
        except:
            pass

        doc = None
        file = pdffile
        doc = fitz.open(file)
        for i in range(len(doc)):
            first_page = doc[i]

            image_matrix = fitz.Matrix(fitz.Identity)
            image_matrix.preScale(2, 2)

            pix = first_page.getPixmap(alpha=False, matrix=image_matrix)
            boxOfImages.append(f'{i}.jpg')
            pix.writePNG(f'data/{i}.jpg')

        NUMBEROFCLASS = 0
        for _filename_ in boxOfImages:
            img = Image.open(f"{filePath}{_filename_}")
            pixMap = img.load()
            width, height = img.size

            listTemplates = []
            boxTime2 = [False]
            FIRSTindent, SECONDindent = self.get_indent(pixMap, width, height)
            for i in range(FIRSTindent, SECONDindent):
                boxTime = []
                tok = 0
                for j in range(width):
                    if pixMap[j, i] != (0, 0, 0):
                        boxTime.append(True)
                    else:
                        tok += 1
                        boxTime.append(False)
                # print(boxTime)
                if (not all(boxTime2) and all(boxTime)) or (all(boxTime2) and not all(boxTime)):
                    listTemplates.append(i)
                boxTime2 = boxTime.copy()
            listTemplates.extend([FIRSTindent, SECONDindent])
            listTemplates.sort()

            try:
                os.makedirs("data/data")
            except:
                pass

            def getY(y):
                chek = 0
                border = set()
                variableBorder = None
                for i in range(width):
                    if pixMap[i, y] == (0, 0, 0):
                        variableBorder = i
                    elif variableBorder:
                        border.add(variableBorder)
                return sorted(list(border))

            BORDERNUM = self.get_num_of_borders(self.get_text_pdf())
            for i in range(len(listTemplates) // 2):
                try:
                    if 1:
                        y0 = listTemplates[i * 2]
                        y1 = listTemplates[i * 2 + 1]
                        boxBorder = getY(y0 + 3)
                        im0 = img.crop((boxBorder[0], y0, boxBorder[2], y1))
                        for k in range((len(boxBorder) - 3) // BORDERNUM + 1):

                            # print(boxBorder)
                            x0 = boxBorder[k * (BORDERNUM + 1) + 2]
                            x1 = boxBorder[k * (BORDERNUM + 1) + 3 + BORDERNUM]
                            # print(x0, x1)
                            im1 = img.crop((x0, y0, x1 + 1, y1))
                            new_im = Image.new('RGB', (im0.size[0] + im1.size[0], im0.size[1]))
                            new_im.paste(im0, (0, 0))
                            new_im.paste(im1, (im0.size[0], 0))
                            new_im.save('data/data/' + str(classes[NUMBEROFCLASS]) + '.jpg')
                            NUMBEROFCLASS += 1
                except Exception:
                    pass


class_list = {'5': ['1', '2', '3'],
              '6': ['1', '2', '3', '4', '5'],
              '7': ['1', '2', '3', '4', '5', '6.1', '6.2', '7.1', '7.2'],
              '8': ['1', '2', '3.1', '3.2'],
              '9': ['1', '2', '3', '4.1', '4.2', '5'],
              '10': ['1 ен', '1 т', '2 гум', '2 сэ'],
              '11': ['1', '2 гум', '2 ен', '2 сэ'],
              }
vk_session = vk_api.VkApi(token='30b12320d099fcf622461de8875d3526b105e8e70863a79d290e90e075d5cde48c582aa6261fdab0ab8a0')
vk = vk_session.get_api()
longpol = VkLongPoll(vk_session)
Flag_msg = False
userclass = {}


def get_button(text, color):
    return {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"" + "3" + "\"}",
            "label": f"{text}"
        },
        "color": f"{color}"
    }


def get_keyboard(buttonslist, one_time_flag=True):
    keyboard = {
        "one_time": one_time_flag,
        "buttons": [
            buttonslist
        ]
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard


def get_big_keyboard(buttonlist):
    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
    len_buttons_list = len(buttonlist)
    if len_buttons_list % 3 == 0:
        flag = 0
        for buttongroupind in range(len_buttons_list):
            if flag != 0 and flag % 3 == 0:
                keyboard.add_line()
            keyboard.add_button(buttonlist[buttongroupind]['action']['label'],
                                color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
            flag += 1
    if len_buttons_list == 4:
        keyboard.add_button(buttonlist[0]['action']['label'],
                            color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
        keyboard.add_button(buttonlist[1]['action']['label'],
                            color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(buttonlist[2]['action']['label'],
                            color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
        keyboard.add_button(buttonlist[3]['action']['label'],
                            color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
    if len_buttons_list == 5:
        keyboard.add_button(buttonlist[0]['action']['label'],
                            color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
        keyboard.add_button(buttonlist[1]['action']['label'],
                            color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(buttonlist[2]['action']['label'],
                            color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
        keyboard.add_button(buttonlist[3]['action']['label'],
                            color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(buttonlist[4]['action']['label'],
                            color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
    if len_buttons_list == 7:
        keyboard.add_button(buttonlist[0]['action']['label'],
                            color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
        keyboard.add_button(buttonlist[1]['action']['label'],
                            color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(buttonlist[2]['action']['label'],
                            color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
        keyboard.add_button(buttonlist[3]['action']['label'],
                            color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(buttonlist[4]['action']['label'],
                            color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
        keyboard.add_button(buttonlist[5]['action']['label'],
                            color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(buttonlist[6]['action']['label'],
                            color=vk_api.keyboard.VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()


def messegeoperator(userid, text, keyboardflag=False, buttons=None, sizekeyboard=False):
    if keyboardflag:
        if sizekeyboard:
            vk_session.method('messages.send',
                              {'user_id': userid, 'message': text, 'random_id': 0,
                               'keyboard': get_big_keyboard(buttons)})
        else:
            vk_session.method('messages.send',
                              {'user_id': userid, 'message': text, 'random_id': 0,
                               'keyboard': get_keyboard(buttons)})
    else:
        vk_session.method('messages.send',
                          {'user_id': userid, 'message': text, 'random_id': 0})


def upload_photo(upload, photo):
    response = upload.photo_messages(photo)[0]
    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']
    print(owner_id, photo_id, access_key)
    return owner_id, photo_id, access_key


def send_photo(peer_id, owner_id, photo_id, access_key):
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk.messages.send(
        random_id=get_random_id(),
        peer_id=peer_id,
        attachment=attachment
    )


def digitinstr(string):
    for char in string:
        if char.isdigit():
            return True
    return False


def newuser(usid):
    global userclass
    if usid in userclass:
        pass
    else:
        userclass[usid] = {}
        userclass[usid]['table'] = None
        userclass[usid]['grouplist'] = None
        userclass[usid]['firstdate'] = True


def get_group(classname):
    for char in classname:
        if char == ".":
            return classname[classname.index(char):]


def chek_user(idd):
    global_init('YANDEX_LY/db/data.db')
    db_sess = create_session()
    if db_sess.query(VKuser).filter(VKuser.Uvk_id == idd).first():
        return True
    return False


def add_user(idd, clas, string=None):
    if chek_user(idd):
        global_init('YANDEX_LY/db/data.db')
        db_sess = create_session()
        user = db_sess.query(VKuser).filter(VKuser.Uvk_id == idd).first()
        print(user, user.Uclass)
        user.Uclass = clas
        db_sess.commit()
        print(user, user.Uclass)
    else:
        global_init('YANDEX_LY/db/data.db')
        db_sess = create_session()
        u = VKuser()
        u.Uvk_id = idd
        u.Uclass = clas
        u.Uclass_profile = string
        db_sess.add(u)
        db_sess.commit()


def get_class_user(idd):
    global_init('YANDEX_LY/db/data.db')
    db_sess = create_session()
    if db_sess.query(VKuser).filter(VKuser.Uvk_id == idd).first():
        return db_sess.query(VKuser).filter(VKuser.Uvk_id == idd).first().Uclass
    return None


def main():
    global Flag_msg, userclass, class_list
    for event in longpol.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                userid = event.user_id
                msg = event.text.lower()
                newuser(userid)
                print(userid, msg)
                print(type(userid))
                if msg == "расписание":
                    upload = VkUpload(vk)
                    url = str(get_class_user(userid))
                    send_photo(userid, *upload_photo(upload, f'data/data/{url.upper()}.jpg'))
                    messegeoperator(userid, 'Что вы хотите?',
                                    keyboardflag=True, buttons=[get_button('Расписание', 'primary'),
                                                                get_button('Сменить класс', 'primary')])
                if userclass[userid]['firstdate']:
                    userclass[userid]['firstdate'] = False
                if msg == "начать" or msg == "сменить класс":
                    messegeoperator(userid, 'Привет! Ты в какую организацию?',
                                    keyboardflag=True, buttons=[get_button('КЦО', 'primary'),
                                                                get_button('IT_cube', 'positive')])
                    continue
                if msg == "кцо":
                    messegeoperator(userid, 'В каком вы классе?', keyboardflag=True,
                                    buttons=[get_button('5', 'primary'),
                                             get_button('6', 'primary'),
                                             get_button('7', 'primary'),
                                             get_button('8', 'primary'),
                                             get_button('9', 'primary'),
                                             get_button('10', 'primary'),
                                             get_button('11', 'primary')], sizekeyboard=True)
                    Flag_msg = False
                    continue
                if digitinstr(msg):
                    if not Flag_msg:
                        if int(msg) in range(5, 12):
                            userclass[userid]['table'] = msg
                            userclass[userid]['grouplist'] = []
                            buttonsgroup = []
                            for group in class_list[msg]:
                                userclass[userid]['grouplist'].append(group)
                                buttonsgroup.append(get_button(userclass[userid]['table'] + "." + group, 'primary'))
                            messegeoperator(userid, 'В какой ты группе?', keyboardflag=True,
                                            buttons=buttonsgroup, sizekeyboard=True)
                            Flag_msg = True
                            continue
                    if Flag_msg:
                        userclass[userid]['table'] += get_group(msg)
                        print(userclass[userid])
                        Flag_msg = False
                        userclass[userid]['grouplist'] = []
                        upload = VkUpload(vk)
                        url = userclass[userid]['table']
                        send_photo(userid, *upload_photo(upload, f'data/data/{url.upper()}.jpg'))
                        add_user(userid, userclass[userid]['table'])
                        messegeoperator(userid, 'Вы добавлeны в базу данных')
                        print(userclass)
                        messegeoperator(userid, 'Что вы хотите?',
                                        keyboardflag=True, buttons=[get_button('Расписание', 'primary'),
                                                                    get_button('Сменить класс', 'primary')])
                if msg == "it_cube":
                    messegeoperator(userid, 'Пока расписаний нет!')


def get_all_class_users():
    box = dict()
    global_init('YANDEX_LY/db/data.db')
    db_sess = create_session()
    for item in db_sess.query(VKuser).all():
        print(item.Uclass, item.Uvk_id)
        if item.Uclass not in box:
            box[item.Uclass] = []
        if item.Uvk_id not in box[item.Uclass]:
            box[item.Uclass].append(item.Uvk_id)
    return box


def automatic_notification():
    users_list = get_all_class_users()
    print(users_list)
    for item in users_list.items():
        upload = VkUpload(vk)
        user_class = item[0]
        for user_name in users_list[user_class]:
            print(user_name)
            send_photo(int(user_name), *upload_photo(upload, f'data/data/{str(user_class).upper()}.jpg'))


def vk_bot_work():
    while True:
        main()


flag_url1 = True
url_list1 = list()
MAIN_URL = 'http://school.kco27.ru//'
ROADFOLDERNEW = 'wp-content/uploads/shedule/'
new_html = requests.get(MAIN_URL).text
indexi = new_html.index(ROADFOLDERNEW)
html = new_html[indexi:]


def check_url_from_system():
    global url_list1, todaydata, nextdaydata, flag_url1

    def check_url(checking_url):
        return checking_url[-1] == "f"

    def get_new_url():
        global new_html, ROADFOLDERNEW
        new_url = MAIN_URL
        if ROADFOLDERNEW in new_html:
            len_html = len(new_html)
            new_html = new_html[new_html.index(ROADFOLDERNEW):]
            for item in range(len_html):
                if new_html[item] != chr(34):
                    new_url += new_html[item]
                else:
                    if check_url(new_url):
                        if flag_url1:
                            url_list1.append(new_url)
                            new_html = new_html[item + 1:]
                            get_new_url()
                    else:
                        break

    def check_urls(url_list_in, todaydata1, nextdaydata1):
        string_from_urls = ''.join(url_list_in)
        if str(nextdaydata1) in string_from_urls:
            return 1
        elif str(todaydata1) in string_from_urls:
            return 2
        else:
            return 0

    get_new_url()
    print(url_list1)
    check_res = check_urls(url_list1, todaydata, nextdaydata)
    return check_res


def updater_work():
    global downloading_checklist_now
    while True:
        time_now = int(datetime.datetime.today().time().hour)
        minut_now = int(datetime.datetime.today().time().minute)
        second_now = int(datetime.datetime.today().time().second)
        if time_now in update_hours_list and minut_now == 1 and second_now in range(0, 5):
            if check_url_from_system() == 1:
                if os.path.isdir('data'):
                    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
                    shutil.rmtree(path)
                if downloading_checklist_now:
                    print("downloading_checklist")
                    sch = Schedule('q.pdf')
                    sch.download_pdf()
                    sch.make_lessonslists(sch.get_classes(), 'data/', 'q.pdf')
                    automatic_notification()
                    print("downloaded_checklist")
                    print(f"url_checklist_to_downloud: {url_to_download}")
                    downloading_checklist_now = False
                else:
                    downloading_checklist_now = True
                    print("start_downloading")


thread1 = Thread(target=vk_bot_work)
thread2 = Thread(target=updater_work)
thread1.start()
thread2.start()
thread1.join()
thread2.join()
