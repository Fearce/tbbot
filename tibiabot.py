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

#for ss in settings:
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


attack_status = 'off'
heal_status = 'off'
manatrain_status = 'off'
manapot_status = 'off'
healpot_status = 'off'
food_status = 'off'


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
    log_file_name = "log-" + datetime.datetime.now().strftime("%d-%m-%Y")+".txt"
    log_file = open(log_file_name, 'a+')
    log_file.write(log_message)
    app.builder.get_object('text_logframe').insert('1.0', log_message)


def setup_attack():
    print('not implemented')

def attack_do():
    #print(attack_col)
    #print(attack_x)
    #print(attack_y)
    if not pyautogui.pixelMatchesColor(attack_x, attack_y, attack_col):
        if not pyautogui.pixelMatchesColor(attack_x, attack_y, (77, 77, 77)):
            pyautogui.click(attack_x, attack_y)


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


def setup_healpot():
    print('not implemented')


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
    #print("trying mana train")
    if pyautogui.pixelMatchesColor(mana_train_x, mana_train_y, mana_train_col):
        #print("doing mana train")
        log_add("Casting mana training spell")
        pyautogui.hotkey(str(mana_train_key))


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
    print('not implemented')


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
    time.sleep(1)
    mana_train_x2, mana_train_y2 = pyautogui.position()
    im = pyautogui.screenshot()
    mana_train_col2 = im.getpixel((mana_train_x2, mana_train_y2))
    cfg = open("cfg.ini").read()
    cfg = cfg.replace(str(settings[8]), str(mana_train_col2))
    cfg = cfg.replace(str(mana_train_x), str(mana_train_x2))
    cfg = cfg.replace(str(mana_train_y), str(mana_train_y2))
    new_cfg = open("cfg.ini", 'w')
    new_cfg.write(cfg)
    new_cfg.close()
    mana_train_col = mana_train_col2
    mana_train_x = mana_train_x2
    mana_train_y = mana_train_y2
    # print("new variables" + str(mana_train_x) + str(mana_train_y) + str(mana_train_col))
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


def setup_manapot():
    print('not implemented')


def setup_heal():
    print('not implemented')
    
    
def start_all():
    global attack_status, manatrain_status, food_status, heal_status, healpot_status, manapot_status
    if attack_status == 'off':
        attack_start()
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
        
        
def stop_all():
    global attack_status, manatrain_status, food_status, heal_status, healpot_status, manapot_status
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
        }

        builder.connect_callbacks(callbacks)


def program():
    global attack_status, manatrain_status, food_status, heal_status, healpot_status, manapot_status
    print("starting")
    pyautogui.FAILSAFE = True
    while True:
        if attack_status == 'on':
            attack_thread = threading.Thread(target=attack_do)
            attack_thread.start()
        if manatrain_status == 'on':
            manatrain_thread = threading.Thread(target=manatrain_do)
            manatrain_thread.start()
        if food_status == 'on':
            food_thread = threading.Thread(target=food_do)
            food_thread.start()
        rand_sleep(5)


if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    threading.stack_size(200000000)
    thread = threading.Thread(target=program)
    thread.start()
    root = tkinter.Tk()
    app = Application(root)
    #print(app.builder.get_variable('attack_status'))
    #test_variable()
    #print(app.builder.get_variable('attack_status'))
    root.mainloop()

