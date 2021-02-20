# -*- coding: utf-8 -*-
#
#  mcpil.py
#  
#  Copyright 2020 Alvarito050506 <donfrutosgomez@gmail.com>
#  Copyright 2020 StealthHydrac/StealthHydra179/a1ma
#  Copyright 2020 JumpeR6790
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; version 2 of the License.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import signal

from typing import Dict

from proxy.proxy import Proxy

import launcher
import config

from splashes import SPLASHES
import random

from os import kill, killpg, getpid, getpgid
import platform
import threading

from subprocess import Popen

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror

from ttkthemes import ThemedTk

import webbrowser

'''
    Global variables.
'''

window: Tk

DESCRIPTIONS = [
    'Classic Minecraft Pi Edition. (Not Recommended)\nNo mods.',
    'Modded Minecraft Pi Edition.\nDefault MCPI-Reborn mods without Touch GUI.',
    'Minecraft Pocket Edition. (Recommended)\nDefault MCPI-Reborn mods.',
    'Custom Profile.\nModify its settings in the Features tab.',
]
current_selection = 0
description_text: StringVar

launch_button: ttk.Button

render_distances = [
    'Far',
    'Normal',
    'Short',
    'Tiny',
]
current_render_distance: StringVar
current_username: StringVar
current_features = []
feature_widgets: Dict[str, ttk.Checkbutton] = {}

current_process: Popen = None

current_config = {}

proxy_lock = threading.Lock()
proxy_thread: threading.Thread = None
proxy = Proxy()
current_ip: StringVar
current_port: StringVar

'''
    Helper classes.
'''

class Checkbox(ttk.Checkbutton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = BooleanVar(self)
        self.configure(variable=self.state)

    def checked(self):
        return self.state.get()

    def check(self, val):
        return self.state.set(val)

class HyperLink(ttk.Label):
    def __init__(self, parent, url, text=None, cursor=None, *args, **kwargs):
        self.url = url
        super().__init__(parent, text=(text or url), cursor=(cursor or 'hand2'), *args, **kwargs)
        self.bind('<Button-1>', self.web_open)

    def web_open(self, event):
        return webbrowser.open(self.url)

class ScrollableFrame(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.canvas = Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.grid(row=0, column=1, sticky='NSE')
        self.canvas.grid(row=0, column=0, sticky='NSEW')

        self.scrollable_frame = ttk.Frame(self.canvas)
        scrollable_frame_id = self.canvas.create_window(0, 0, window=self.scrollable_frame, anchor='nw')

        def configure_scrollable_frame(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.scrollable_frame.bind('<Configure>', configure_scrollable_frame)

        def configure_canvas(event):
            self.canvas.itemconfig(scrollable_frame_id, width=event.width, height=(self.scrollable_frame.winfo_height() if self.scrollable_frame.winfo_height() > event.height else event.height))

        self.canvas.bind('<Configure>', configure_canvas)

'''
    Helper functions and back-end.
'''

def basename(path):
    return path.split('/')[-1]

# Convert Dict Of Features To List Of Enabled Features
def features_dict_to_list(features: Dict[str, bool]):
    out = []
    for key in features:
        if features[key]:
            out.append(key)
    return out

# Get Features From Selected Mode
def get_features() -> list:
    global current_selection, current_features
    if current_selection == 0:
        # No Mods
        return []
    elif current_selection == 1:
        # Default Mods Minus Touch GUI
        mods = launcher.AVAILABLE_FEATURES.copy()
        mods['Touch GUI'] = False
        return features_dict_to_list(mods)
    elif current_selection == 2:
        # Default Mods
        return features_dict_to_list(launcher.AVAILABLE_FEATURES.copy())
    elif current_selection == 3:
        # Custom Features (Use Features Tab)
        return current_features

# Launch Minecraft
def launch():
    global current_render_distance, current_username, current_process
    launch_button.config(state=DISABLED)
    if current_process is None or current_process.poll() is not None:
        current_process = launcher.run(get_features(), current_render_distance.get(), current_username.get())
    return 0

# Update Launch ttk.Button
def update_launch_button():
    global launch_button
    if (current_process is None or current_process.poll() is not None) and launch_button['state'] == DISABLED:
        launch_button.config(state=NORMAL)
    launch_button.after(10, update_launch_button)

# Close MCPIL
def quit():
    global current_process
    if current_process is not None and current_process.poll() is None:
        killpg(getpgid(current_process.pid), signal.SIGTERM)

    window.destroy()
    kill(getpid(), signal.SIGTERM)
    return 0

# Start/Stop Proxy
def update_proxy():
    global proxy, proxy_thread, proxy_lock, current_ip, current_port
    proxy_lock.acquire()
    if proxy_thread is not None:
        proxy.stop()
        proxy_thread.join()
    try:
        proxy.set_option("src_addr", current_ip.get())
        proxy.set_option("src_port", int(current_port.get()))
        proxy_thread = threading.Thread(target=lambda *args: proxy.run())
        proxy_thread.start()
    except ValueError:
        # Invalid Port
        pass
    proxy_lock.release()

# Save/Load Config
def load():
    global current_config, current_render_distance, current_username, current_features, feature_widgets
    current_config = config.load()
    current_render_distance.set(current_config['general']['render-distance'])
    current_username.set(current_config['general']['username'])
    current_features = current_config['general']['custom-features'].copy()
    for key in feature_widgets:
        feature_widgets[key].state(['!alternate'])
        if key in current_features:
            feature_widgets[key].state(['selected'])
        else:
            feature_widgets[key].state(['!selected'])
    current_ip.set(current_config['server']['ip'])
    current_port.set(current_config['server']['port'])
    update_proxy()
def save():
    global current_config, current_render_distance, current_username, current_features
    current_config['general']['render-distance'] = current_render_distance.get()
    current_config['general']['username'] = current_username.get()
    current_config['general']['custom-features'] = current_features.copy()
    current_config['server']['ip'] = current_ip.get()
    current_config['server']['port'] = current_port.get()
    config.save(current_config)

# Update Features From Widgets
def update_features():
    global current_features, feature_widgets
    current_features = []
    for key in feature_widgets:
        if feature_widgets[key].instate(['selected']):
            current_features.append(key)

'''
    Event handlers.
'''

def select_version(version: int):
    global current_selection
    try:
        current_selection = version
        description_text.set(DESCRIPTIONS[int(current_selection)])
    except IndexError:
        pass
    except Exception as err:
        return 'Critical error {}'.format(err)
def on_select_versions(event):
    select_version(event.widget.selection()[0])
    return 0

'''
    Tabs.
'''

def play_tab(parent):
    global description_text, launch_button

    tab = ttk.Frame(parent)

    title = ttk.Label(tab, text='Minecraft Pi Launcher')
    title.config(font=('', 24))
    title.grid(row=0)

    splash_text = ttk.Label(tab, text=random.choice(SPLASHES), foreground='yellow')
    splash_text.grid(row=1, pady=4)

    choose_text = ttk.Label(tab, text='Choose a Minecraft version to launch.')
    choose_text.grid(row=2, pady=(0, 16))

    versions_frame = ttk.Frame(tab)

    tab.columnconfigure(0, weight=1)
    versions_frame.columnconfigure(0, weight=1)
    tab.rowconfigure(2, weight=1)
    versions_frame.rowconfigure(0, weight=1)

    description_text = StringVar(versions_frame)
    description_text_label = ttk.Label(versions_frame, textvariable=description_text, wraplength=256, anchor='center', justify='center')

    versions = ttk.Treeview(versions_frame, selectmode='browse', show='tree')
    versions.insert('', 'end', text='Classic MCPI', iid=0)
    versions.insert('', 'end', text='Modded MCPI', iid=1)
    versions.insert('', 'end', text='Classic MCPE', iid=2)
    versions.insert('', 'end', text='Custom Profile', iid=3)
    versions.bind('<<TreeviewSelect>>', on_select_versions)
    versions.grid(row=0, column=0, sticky='NSEW')
    versions.selection_set(2)
    select_version(versions.selection()[0])

    description_text_label.grid(row=0, column=1, pady=48, padx=48, sticky='NSE')

    versions_frame.grid(row=3, sticky='NSEW')

    launch_frame = ttk.Frame(tab)
    launch_button = ttk.Button(launch_frame, text='Launch', command=launch)
    launch_button.pack(side=RIGHT, anchor=S)
    launch_frame.grid(row=4, sticky='SE')

    launch_button.after(0, update_launch_button)

    return tab

def settings_tab(parent):
    global current_render_distance, current_username

    tab = ttk.Frame(parent)

    tab.rowconfigure(0, weight=1)
    tab.columnconfigure(0, weight=1)

    main_frame = ttk.Frame(tab)

    main_frame.columnconfigure(1, weight=1)

    render_distance_label = ttk.Label(main_frame, text='Render Distance:')
    render_distance_label.grid(row=0, column=0, padx=6, pady=6, sticky='W')
    current_render_distance = StringVar(main_frame)
    render_distance = ttk.Combobox(main_frame, textvariable=current_render_distance, values=render_distances, width=24)
    render_distance.state(['readonly'])
    render_distance.grid(row=0, column=1, padx=6, pady=6, sticky='EW')

    username_label = ttk.Label(main_frame, text='Username:')
    username_label.grid(row=1, column=0, padx=6, pady=6, sticky='W')
    current_username = StringVar(main_frame)
    username = ttk.Entry(main_frame, width=24, textvariable=current_username)
    username.grid(row=1, column=1, padx=6, pady=6, sticky='EW')

    main_frame.grid(row=0, sticky='NEW')

    save_frame = ttk.Frame(tab)
    save_button = ttk.Button(save_frame, text='Save', command=save)
    save_button.pack(side=RIGHT, anchor=S)
    save_frame.grid(row=1, sticky='SE')

    return tab

def features_tab(parent):
    global feature_widgets

    tab = ttk.Frame(parent)

    tab.rowconfigure(0, weight=1)
    tab.columnconfigure(0, weight=1)

    main_frame = ScrollableFrame(tab)

    main_frame.scrollable_frame.columnconfigure(1, weight=1)

    row = 0
    for key in launcher.AVAILABLE_FEATURES:
        check = ttk.Checkbutton(main_frame.scrollable_frame, command=update_features, text=key)
        check.pack(padx=6, pady=6, anchor='w')
        feature_widgets[key] = check

        row += 1

    main_frame.grid(row=0, sticky='NSEW')

    save_frame = ttk.Frame(tab)
    save_button = ttk.Button(save_frame, text='Save', command=save)
    save_button.pack(side=RIGHT, anchor=S)
    save_frame.grid(row=1, sticky='SE')

    return tab

def multiplayer_tab(parent):
    global current_ip, current_port

    tab = ttk.Frame(parent)

    tab.rowconfigure(0, weight=1)
    tab.columnconfigure(0, weight=1)

    main_frame = ttk.Frame(tab)

    main_frame.columnconfigure(1, weight=1)

    ip_label = ttk.Label(main_frame, text='IP:')
    ip_label.grid(row=0, column=0, padx=6, pady=6, sticky='W')
    current_ip = StringVar(main_frame)
    current_ip.trace('w', lambda *args: update_proxy())
    ip = ttk.Entry(main_frame, width=24, textvariable=current_ip)
    ip.grid(row=0, column=1, padx=6, pady=6, sticky='EW')

    port_label = ttk.Label(main_frame, text='Port:')
    port_label.grid(row=1, column=0, padx=6, pady=6, sticky='W')
    current_port = StringVar(main_frame)
    current_port.trace('w', lambda *args: update_proxy())
    port = ttk.Entry(main_frame, width=24, textvariable=current_port)
    port.grid(row=1, column=1, padx=6, pady=6, sticky='EW')

    main_frame.grid(row=0, sticky='NEW')

    save_frame = ttk.Frame(tab)
    save_button = ttk.Button(save_frame, text='Save', command=save)
    save_button.pack(side=RIGHT, anchor=S)
    save_frame.grid(row=1, sticky='SE')

    return tab

# Get Version
def get_version() -> str:
    try:
        with open('/opt/mcpil/VERSION', 'r') as file:
            return 'v' + file.readline().strip()
    except OSError:
        # File Does Not Exists Or Is Inaccessible
        pass
    return 'Unknown Version'

def about_tab(parent):
    tab = ttk.Frame(parent)

    main_frame = ttk.Frame(tab)

    main_frame.columnconfigure(0, weight=1)

    title = ttk.Label(main_frame, text='Minecraft Pi Launcher', anchor='center')
    title.config(font=('', 24))
    title.grid(row=0, sticky='NSEW')

    version = ttk.Label(main_frame, text=get_version(), anchor='center')
    version.config(font=('', 10))
    version.grid(row=1, sticky='NSEW')

    authors = HyperLink(main_frame, 'https://github.com/MCPI-Revival/MCPIL/graphs/contributors', text='by all its contributors', anchor='center')
    authors.config(font=('', 10))
    authors.grid(row=2, sticky='NSEW')

    url = HyperLink(main_frame, 'https://github.com/MCPI-Revival/MCPIL', anchor='center', foreground='blue')
    url.config(font=('', 10))
    url.grid(row=3, sticky='NSEW')

    main_frame.pack(expand=True)

    return tab

def main():
    if platform.system() != 'Linux':
        showerror('Error', 'Linux Is Required')
        return 1

    global window

    window = ThemedTk(theme='equilux', className='mcpil')
    window.title('MCPIL')
    window.geometry('512x400')
    window.resizable(True, True)

    tabs = ttk.Notebook(window)
    tabs.add(play_tab(tabs), text='Play')
    tabs.add(features_tab(tabs), text='Features')
    tabs.add(multiplayer_tab(tabs), text='Multiplayer')
    tabs.add(settings_tab(tabs), text='Settings')
    tabs.add(about_tab(tabs), text='About')
    tabs.pack(fill=BOTH, expand=True)

    load()
    save()

    window.wm_protocol('WM_DELETE_WINDOW', quit)
    signal.signal(signal.SIGINT, lambda *args: quit())

    try:
        window.mainloop()
    except KeyboardInterrupt:
        quit()

    return 0

if __name__ == '__main__':
    sys.exit(main())
