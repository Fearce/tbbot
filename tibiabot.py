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

settings_file = open('cfg.ini').read()  # Opens config
settingsOrig = settings_file.split('\n')
settings = []

for s in settingsOrig:
    settings.append(s.split('=')[1])

#for ss in settings:
#    print(ss)

window_height = settings[0]
window_width = settings[1]
heal_spell_x = settings[2]
heal_spell_y = settings[3]
heal_spell_col = settings[4]
heal_spell_key = settings[5]
mana_train_x = settings[6]
mana_train_y = settings[7]
mana_train_col = settings[8]
mana_train_key = settings[9]
mana_pot_x = settings[10]
mana_pot_y = settings[11]
mana_pot_col = settings[12]
mana_pot_key = settings[13]
heal_pot_x = settings[14]
heal_pot_y = settings[15]
heal_pot_col = settings[16]
heal_pot_key = settings[17]
food_key = settings[18]
attack_x = settings[19]
attack_y = settings[20]
attack_col = settings[21]

attack_status = 'off'


def current_time():
    return datetime.datetime.now().strftime("%H:%M:%S")


def attack_start():
    global attack_status
    var_name = 'attack_status'
    var = app.builder.get_variable(var_name)
    if var.get() == "off":  # Enable
        newlabel = 'on'
        attack_status = 'on'
        var.set(newlabel)
    else:
        newlabel = 'off'
        attack_status = 'off'
        var.set(newlabel)


def setup_attack():
    print('not implemented')

def attack_do():
    print("attacking")
    app.builder.get_object('text_logframe').insert('1.0', current_time() + " Picking play again in 5\n")
    time.sleep(1)


def heal_start():
    var_name = 'heal_status'
    var = app.builder.get_variable(var_name)
    if var.get() == "off":  # Enable
        newlabel = 'on'
        var.set(newlabel)
    else:
        newlabel = 'off'
        var.set(newlabel)


def setup_healpot():
    print('not implemented')


def manatrain_start():
    var_name = 'manatrain_status'
    var = app.builder.get_variable(var_name)
    if var.get() == "off":  # Enable
        newlabel = 'on'
        var.set(newlabel)
    else:
        newlabel = 'off'
        var.set(newlabel)


def manapot_start():
    var_name = 'manapot_status'
    var = app.builder.get_variable(var_name)
    if var.get() == "off":  # Enable
        newlabel = 'on'
        var.set(newlabel)
    else:
        newlabel = 'off'
        var.set(newlabel)


def deposit_start():
    print('not implemented')


def setup_manatrain():
    print('not implemented')


def healpot_start():
    var_name = 'healpot_status'
    var = app.builder.get_variable(var_name)
    if var.get() == "off":  # Enable
        newlabel = 'on'
        var.set(newlabel)
    else:
        newlabel = 'off'
        var.set(newlabel)


def setup_manapot():
    print('not implemented')


def setup_heal():
    print('not implemented')


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
        }

        builder.connect_callbacks(callbacks)



def program():
    global attack_status
    print("starting")
    pyautogui.FAILSAFE = True
    while True:
        if attack_status == 'on':
           attack_do()




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

