import pyautogui
import time
import os
import tkinter
import threading
import random
import datetime
import winsound
import sys
import pygubu
from desktopmagic.screengrab_win32 import (
getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
getRectAsImage, getDisplaysAsImages)

pyautogui.screenshot = getScreenAsImage()

def str_to_col(str_input):
    str_input = str_input.split('(')
    str_input = str_input[1].split(')')
    str_input = str_input[0].split(',')
    str_input = (int(str_input[0]), int(str_input[1]), int(str_input[2]))
    return str_input


settings_file = open('cfg.ini').read()  # Opens config
settingsOrig = settings_file.split('\n')
settings = []

for s in settingsOrig:
    settings.append(s.split('=')[1])

# for ss in settings:
#    print(ss)

window_height = int(settings[0])
window_width = int(settings[1])
heal_spell_x = int(settings[2])
heal_spell_y = int(settings[3])
heal_spell_col = settings[4]
heal_spell_col = str_to_col(heal_spell_col)
heal_spell_key = settings[5]
mana_train_x = int(settings[6])
mana_train_y = int(settings[7])
mana_train_col = settings[8]
mana_train_col = str_to_col(mana_train_col)
mana_train_key = settings[9]
mana_pot_x = int(settings[10])
mana_pot_y = int(settings[11])
mana_pot_col = settings[12]
mana_pot_col = str_to_col(mana_pot_col)
mana_pot_key = settings[13]
heal_pot_x = int(settings[14])
heal_pot_y = int(settings[15])
heal_pot_col = settings[16]
heal_pot_col = str_to_col(heal_pot_col)
heal_pot_key = settings[17]
food_key = settings[18]
attack_x = int(settings[19])
attack_y = int(settings[20])
attack_col = settings[21]
attack_col = str_to_col(attack_col)
loot_x = int(settings[22])
loot_y = int(settings[23])

attack_status = 'off'
heal_status = 'off'
manatrain_status = 'off'
manapot_status = 'off'
healpot_status = 'off'
food_status = 'off'
loot_status = 'off'


def current_time():  # Makes sure the log frame isn't flooded and returns current time.
    log_count = int(app.builder.get_object('text_logframe').index('end-1c').split('.')[0])
    if log_count > 9:
        app.builder.get_object('text_logframe').delete("end-1c linestart", "end")
    return datetime.datetime.now().strftime("%H:%M:%S")


def rand_sleep(to_int):
    time.sleep(random.randint(1, to_int))


def attack_start():
    global attack_status
    var_name = 'attack_status'
    var = app.builder.get_variable(var_name)
    if var.get() == "off":  # Enable
        log_add("Starting attack, put cursor on first battle list target.")
        newlabel = 'on'
        attack_status = 'on'
        var.set(newlabel)
    else:
        log_add("Stopping attack")
        newlabel = 'off'
        attack_status = 'off'
        var.set(newlabel)


def log_add(message):  # Adds message to log frame and log file
    log_message = current_time() + " " + message + "\n"
    log_file_name = "log-" + datetime.datetime.now().strftime("%d-%m-%Y") + ".txt"
    log_file = open(log_file_name, 'a+')
    log_file.write(log_message)
    app.builder.get_object('text_logframe').insert('1.0', log_message)


def setup_attack():
    attack_thread = threading.Thread(target=set_attack_thread)
    attack_thread.start()


def set_attack_thread():
    global attack_x, attack_y, attack_col
    # print("old variables" + str(attack_x) + str(attack_y) + str(attack_col))
    log_add("Picking attack in 5, put cursor near mana value")
    time.sleep(1)
    log_add("Picking attack in 4")
    time.sleep(1)
    log_add("Picking attack in 3")
    time.sleep(1)
    log_add("Picking attack in 2")
    time.sleep(1)
    log_add("Picking attack in 1")
    time.sleep(1)
    attack_x2, attack_y2 = pyautogui.position()
    im = pyautogui.screenshot
    attack_col2 = im.getpixel((attack_x2, attack_y2))
    cfg = open("cfg.ini").read()
    cfg = cfg.replace("attackCol=" + str(settings[21]), "attackCol=" + str(attack_col2))
    cfg = cfg.replace("attackX=" + str(attack_x), "attackX=" + str(attack_x2))
    cfg = cfg.replace("attackY=" + str(attack_y), "attackY=" + str(attack_y2))
    new_cfg = open("cfg.ini", 'w')
    new_cfg.write(cfg)
    new_cfg.close()
    attack_col = attack_col2
    attack_x = attack_x2
    attack_y = attack_y2
    # print("new variables" + str(attack_x) + str(attack_y) + str(attack_col))
    log_add("attack picked and saved")


def loot_do():
    loot_positions = [(loot_x, loot_y-40),
                      (loot_x, loot_y+50),
                      (loot_x+40, loot_y+50),
                      (loot_x - 50, loot_y + 50),
                      (loot_x + 40, loot_y),
                      (loot_x - 50, loot_y),
                      (loot_x - 50, loot_y - 40),
                      (loot_x + 40, loot_y - 40)]
    for pos in loot_positions:
        pyautogui.click(pos, button='right')
        time.sleep(0.01)


def attack_do():
    # print(attack_col)
    # print(attack_x)
    # print(attack_y)
    if pyautogui.pixelMatchesColor(attack_x, attack_y, attack_col):
        if not pyautogui.pixelMatchesColor(attack_x, attack_y, (77, 77, 77)):
            pyautogui.click(attack_x, attack_y)
            loot_do()
            pyautogui.moveTo(attack_x, attack_y, 1)


def heal_start():
    global heal_status
    var_name = 'heal_status'
    var = app.builder.get_variable(var_name)
    if var.get() == "off":  # Enable
        heal_status = 'on'
        log_add("Starting heal")
        newlabel = 'on'
        var.set(newlabel)
    else:
        heal_status = 'off'
        log_add("Stopping heal")
        newlabel = 'off'
        var.set(newlabel)


def manatrain_start():
    global manatrain_status
    var_name = 'manatrain_status'
    var = app.builder.get_variable(var_name)
    if var.get() == "off":  # Enable
        log_add("Starting mana training")
        manatrain_status = 'on'
        newlabel = 'on'
        var.set(newlabel)
    else:
        log_add("Stopping mana training")
        manatrain_status = 'off'
        newlabel = 'off'
        var.set(newlabel)


def manatrain_do():
    if pyautogui.pixelMatchesColor(mana_train_x, mana_train_y, mana_train_col):
        # print("doing mana train")
        log_add("Casting mana training spell")
        pyautogui.hotkey(str(mana_train_key))


def healpot_do():
    if not pyautogui.pixelMatchesColor(heal_pot_x, heal_pot_y, heal_pot_col):
        log_add("Using healing potion")
        pyautogui.hotkey(str(heal_pot_key))


def manapot_do():
    if not pyautogui.pixelMatchesColor(mana_pot_x, mana_pot_y, mana_pot_col):
        log_add("Using mana potion")
        pyautogui.hotkey(str(mana_pot_key))


def heal_do():
    if not pyautogui.pixelMatchesColor(heal_spell_x, heal_spell_y, heal_spell_col):
        log_add("Casting healing spell")
        pyautogui.hotkey(str(heal_spell_key))


def manapot_start():
    global manapot_status
    var_name = 'manapot_status'
    var = app.builder.get_variable(var_name)
    if var.get() == "off":  # Enable
        log_add("Starting mana pots")
        manapot_status = 'on'
        newlabel = 'on'
        var.set(newlabel)
    else:
        log_add("Stopping mana pots")
        manapot_status = 'off'
        newlabel = 'off'
        var.set(newlabel)


def deposit_start():
    deposit_thread = threading.Thread(target=deposit_do)
    deposit_thread.start()


def deposit_do():
    log_add("Starting deposit")
    rand_sleep(1)
    pyautogui.typewrite('Hi', interval=0.1)
    pyautogui.hotkey('enter')
    rand_sleep(1)
    pyautogui.typewrite('deposit all', interval=0.07)
    pyautogui.hotkey('enter')
    rand_sleep(1)
    pyautogui.typewrite('yes', interval=0.09)
    pyautogui.hotkey('enter')
    log_add("Deposit done")


def setup_manatrain():
    manatrain_thread = threading.Thread(target=set_manatrain_thread)
    manatrain_thread.start()


def set_manatrain_thread():
    global mana_train_x, mana_train_y, mana_train_col
    # print("old variables" + str(mana_train_x) + str(mana_train_y) + str(mana_train_col))
    log_add("Picking mana train in 5, put cursor near mana value")
    time.sleep(1)
    log_add("Picking mana train in 4")
    time.sleep(1)
    log_add("Picking mana train in 3")
    time.sleep(1)
    log_add("Picking mana train in 2")
    time.sleep(1)
    log_add("Picking mana train in 1")
    print("pos")
    time.sleep(1)
    print("pos")
    mana_train_x2, mana_train_y2 = pyautogui.position()
    print("grabbing screen")
    im = pyautogui.screenshot
    print("grabbed")
    mana_train_col2 = im.getpixel((mana_train_x2, mana_train_y2))
    print(mana_train_col2)
    cfg = open("cfg.ini").read()
    cfg = cfg.replace("manatrainCol=" + str(settings[8]), "manatrainCol=" + str(mana_train_col2))
    cfg = cfg.replace("manatrainX=" + str(mana_train_x), "manatrainX=" + str(mana_train_x2))
    cfg = cfg.replace("manatrainY=" + str(mana_train_y), "manatrainY=" + str(mana_train_y2))
    new_cfg = open("cfg.ini", 'w')
    new_cfg.write(cfg)
    new_cfg.close()
    mana_train_col = mana_train_col2
    mana_train_x = mana_train_x2
    mana_train_y = mana_train_y2
    print("new variables" + str(mana_train_x) + str(mana_train_y) + str(mana_train_col))
    log_add("Mana train picked and saved")


def healpot_start():
    global healpot_status
    var_name = 'healpot_status'
    var = app.builder.get_variable(var_name)
    if var.get() == "off":  # Enable
        log_add("Starting heal pots")
        healpot_status = 'on'
        newlabel = 'on'
        var.set(newlabel)
    else:
        log_add("Stopping heal pots")
        healpot_status = 'off'
        newlabel = 'off'
        var.set(newlabel)


def loot_start():
    global loot_status
    var_name = 'loot_status'
    var = app.builder.get_variable(var_name)
    if var.get() == "off":  # Enable
        log_add("Starting auto loot")
        loot_status = 'on'
        newlabel = 'on'
        var.set(newlabel)
    else:
        log_add("Stopping auto loot")
        loot_status = 'off'
        newlabel = 'off'
        var.set(newlabel)
        

def setup_manapot():
    manapot_thread = threading.Thread(target=set_manapot_thread)
    manapot_thread.start()


def set_manapot_thread():
    global mana_pot_x, mana_pot_y, mana_pot_col
    # print("old variables" + str(mana_train_x) + str(mana_train_y) + str(mana_train_col))
    log_add("Picking mana pot in 5, put cursor near mana value")
    time.sleep(1)
    log_add("Picking mana pot in 4")
    time.sleep(1)
    log_add("Picking mana pot in 3")
    time.sleep(1)
    log_add("Picking mana pot in 2")
    time.sleep(1)
    log_add("Picking mana pot in 1")
    time.sleep(1)
    mana_pot_x2, mana_pot_y2 = pyautogui.position()
    im = pyautogui.screenshot
    mana_pot_col2 = im.getpixel((mana_pot_x2, mana_pot_y2))
    cfg = open("cfg.ini").read()
    cfg = cfg.replace("manapotCol=" + str(settings[12]), "manapotCol=" + str(mana_pot_col2))
    cfg = cfg.replace("manapotX=" + str(mana_pot_x), "manapotX=" + str(mana_pot_x2))
    cfg = cfg.replace("manapotY=" + str(mana_pot_y), "manapotY=" + str(mana_pot_y2))
    new_cfg = open("cfg.ini", 'w')
    new_cfg.write(cfg)
    new_cfg.close()
    mana_pot_col = mana_pot_col2
    mana_pot_x = mana_pot_x2
    mana_pot_y = mana_pot_y2
    # print("new variables" + str(mana_pot_x) + str(mana_pot_y) + str(mana_pot_col))
    log_add("Mana pot picked and saved")


def setup_heal():
    heal_thread = threading.Thread(target=set_heal_thread)
    heal_thread.start()


def set_heal_thread():
    global heal_spell_x, heal_spell_y, heal_spell_col
    # print("old variables" + str(mana_train_x) + str(mana_train_y) + str(mana_train_col))
    log_add("Picking heal spell in 5, put cursor near mana value")
    time.sleep(1)
    log_add("Picking heal spell in 4")
    time.sleep(1)
    log_add("Picking heal spell in 3")
    time.sleep(1)
    log_add("Picking heal spell in 2")
    time.sleep(1)
    log_add("Picking heal spell in 1")
    time.sleep(1)
    heal_spell_x2, heal_spell_y2 = pyautogui.position()
    im = pyautogui.screenshot
    heal_spell_col2 = im.getpixel((heal_spell_x2, heal_spell_y2))
    cfg = open("cfg.ini").read()
    cfg = cfg.replace("healspellCol=" + str(settings[4]), "healspellCol=" + str(heal_spell_col2))
    cfg = cfg.replace("healspellX=" + str(heal_spell_x), "healspellX=" + str(heal_spell_x2))
    cfg = cfg.replace("healspellY=" + str(heal_spell_y), "healspellY=" + str(heal_spell_y2))
    new_cfg = open("cfg.ini", 'w')
    new_cfg.write(cfg)
    new_cfg.close()
    heal_spell_col = heal_spell_col2
    heal_spell_x = heal_spell_x2
    heal_spell_y = heal_spell_y2
    # print("new variables" + str(heal_spell_x) + str(heal_spell_y) + str(heal_spell_col))
    log_add("heal spell picked and saved")


def setup_loot():
    loot_thread = threading.Thread(target=set_loot_thread)
    loot_thread.start()


def set_loot_thread():
    global loot_x, loot_y
    # print("old variables" + str(mana_train_x) + str(mana_train_y) + str(mana_train_col))
    log_add("Picking loot in 5, put cursor at middle char")
    time.sleep(1)
    log_add("Picking loot in 4")
    time.sleep(1)
    log_add("Picking loot in 3")
    time.sleep(1)
    log_add("Picking loot in 2")
    time.sleep(1)
    log_add("Picking loot in 1")
    time.sleep(1)
    loot_x2, loot_y2 = pyautogui.position()
    im = pyautogui.screenshot
    loot_col2 = im.getpixel((loot_x2, loot_y2))
    cfg = open("cfg.ini").read()
    cfg = cfg.replace("lootX=" + str(loot_x), "lootX=" + str(loot_x2))
    cfg = cfg.replace("lootY=" + str(loot_y), "lootY=" + str(loot_y2))
    new_cfg = open("cfg.ini", 'w')
    new_cfg.write(cfg)
    new_cfg.close()
    loot_col = loot_col2
    loot_x = loot_x2
    loot_y = loot_y2
    # print("new variables" + str(loot_x) + str(loot_y) + str(loot_col))
    log_add("loot pos picked and saved")


def set_healpot_thread():
    global heal_pot_x, heal_pot_y, heal_pot_col
    # print("old variables" + str(heal_train_x) + str(heal_train_y) + str(heal_train_col))
    log_add("Picking heal pot in 5, put cursor near heal value")
    time.sleep(1)
    log_add("Picking heal pot in 4")
    time.sleep(1)
    log_add("Picking heal pot in 3")
    time.sleep(1)
    log_add("Picking heal pot in 2")
    time.sleep(1)
    log_add("Picking heal pot in 1")
    time.sleep(1)
    heal_pot_x2, heal_pot_y2 = pyautogui.position()
    im = pyautogui.screenshot
    heal_pot_col2 = im.getpixel((heal_pot_x2, heal_pot_y2))
    cfg = open("cfg.ini").read()
    cfg = cfg.replace("healpotCol=" + str(settings[16]), "healpotCol=" + str(heal_pot_col2))
    cfg = cfg.replace("healpotX=" + str(heal_pot_x), "healpotX=" + str(heal_pot_x2))
    cfg = cfg.replace("healpotY=" + str(heal_pot_y), "healpotY=" + str(heal_pot_y2))
    new_cfg = open("cfg.ini", 'w')
    new_cfg.write(cfg)
    new_cfg.close()
    heal_pot_col = heal_pot_col2
    heal_pot_x = heal_pot_x2
    heal_pot_y = heal_pot_y2
    # print("new variables" + str(heal_pot_x) + str(heal_pot_y) + str(heal_pot_col))
    log_add("heal pot picked and saved")


def setup_healpot():
    healpot_thread = threading.Thread(target=set_healpot_thread)
    healpot_thread.start()


def start_all():
    global attack_status, manatrain_status, food_status, heal_status, healpot_status, manapot_status, loot_status
    # if attack_status == 'off':
        # attack_start()
    if manatrain_status == 'off':
        manatrain_start()
    if food_status == 'off':
        food_start()
    if heal_status == 'off':
        heal_start()
    if healpot_status == 'off':
        healpot_start()
    if manapot_status == 'off':
        manapot_start()
    # if loot_status == 'off':
        # loot_start()


def stop_all():
    global attack_status, manatrain_status, food_status, heal_status, healpot_status, manapot_status, loot_status
    if attack_status == 'on':
        attack_start()
    if manatrain_status == 'on':
        manatrain_start()
    if food_status == 'on':
        food_start()
    if heal_status == 'on':
        heal_start()
    if healpot_status == 'on':
        healpot_start()
    if manapot_status == 'on':
        manapot_start()
    if loot_status == 'on':
        loot_start()


def food_start():
    global food_status
    var_name = 'food_status'
    var = app.builder.get_variable(var_name)
    if var.get() == "off":  # Enable
        log_add("Starting eating.")
        newlabel = 'on'
        food_status = 'on'
        var.set(newlabel)
    else:
        log_add("Stopping eating")
        newlabel = 'off'
        food_status = 'off'
        var.set(newlabel)


def food_do():
    pyautogui.hotkey(str(food_key))


class Application:
    def __init__(self, master):
        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file('tbgui.ui')

        # 3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('tbb_frame', master)

        # Configure callbacks
        callbacks = {
            'attack_start': attack_start,
            'setup_attack': setup_attack,
            'heal_start': heal_start,
            'setup_healpot': setup_healpot,
            'manatrain_start': manatrain_start,
            'manapot_start': manapot_start,
            'deposit_start': deposit_start,
            'setup_manatrain': setup_manatrain,
            'healpot_start': healpot_start,
            'setup_manapot': setup_manapot,
            'setup_heal': setup_heal,
            'food_start': food_start,
            'start_all': start_all,
            'stop_all': stop_all,
            'loot_start': loot_start,
            'setup_loot': setup_loot,
        }

        builder.connect_callbacks(callbacks)


def program():
    global attack_status, manatrain_status, food_status, heal_status, healpot_status, manapot_status
    print("starting")
    pyautogui.FAILSAFE = True
    while True:
        if attack_status == 'on':
            attack_do()
        if manatrain_status == 'on':
            manatrain_do()
        if food_status == 'on':
            food_do()
        if heal_status == 'on':
            heal_do()
        if healpot_status == 'on':
            healpot_do()
        if manapot_status == 'on':
            manapot_do()
        rand_sleep(5)


if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    threading.stack_size(200000000)
    thread = threading.Thread(target=program)
    thread.start()
    root = tkinter.Tk()
    app = Application(root)
    # print(app.builder.get_variable('attack_status'))
    # test_variable()
    # print(app.builder.get_variable('attack_status'))
    root.mainloop()
