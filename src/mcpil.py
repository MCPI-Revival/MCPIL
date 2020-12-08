#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  mcpil.py
#  
#  Copyright 2020 Alvarito050506 <donfrutosgomez@gmail.com>
#  Copyright 2020 StealthHydrac/StealthHydra179
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
#  

import signal


from os import kill, getpid

from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename

'''
	Global variables.
'''

descriptions = [
	"Classic Miecraft Pi Edition.\nNo mods.",
	"Modded Miecraft Pi Edition.\nModPi + MCPI-Docker mods without Survival or Touch GUI.",
	"Minecraft Pocket Edition.\nMCPI-Docker mods.",
	"Custom Profile.\nModify its settings in the Profile tab.",
];

'''
	Helper classes.
'''

class Checkbox(ttk.Checkbutton):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs);
		self.state = BooleanVar(self);
		self.configure(variable=self.state);

	def checked(self):
		return self.state.get();

	def check(self, val):
		return self.state.set(val);

class HyperLink(Label):
	def __init__(self, parent, url, text=None, fg=None, cursor=None, *args, **kwargs):
		self.url = url;
		super().__init__(parent, text=(text or url), fg=(fg or "blue"), cursor=(cursor or "hand2"), *args, **kwargs);
		self.bind("<Button-1>", self.web_open);

	def web_open(self, event):
		return webbrowser.open(self.url);

'''
	Helper functions and back-end.
'''

def basename(path):
	return path.split("/")[-1];

def launch():
	return 0;

def pre_launch():
	return launch();

def bye():
	window.destroy();
	kill(getpid(), signal.SIGTERM);
	return 0;

'''
	Event handlers.
'''

def on_select_versions(event):
	global current_selection;
	try:
		current_selection = event.widget.curselection()[0];
		description_text["text"] = descriptions[current_selection];
	except IndexError:
		pass;
	except Exception, err:
		return "Critical error {}".format(err);
	return 0;

'''
	Tabs.
'''

def play_tab(parent):
	global description_text;

	tab = Frame(parent);

	title = Label(tab, text="Minecraft Pi Launcher");
	title.config(font=("", 24));
	title.pack();

	choose_text = Label(tab, text="Choose a Minecraft version to launch.");
	choose_text.pack(pady=16);

	versions_frame = Frame(tab);
	versions = Listbox(versions_frame, selectmode=SINGLE, width=22);
	versions.insert(0, " Classic MCPI ");
	versions.insert(1, " Modded MCPI ");
	versions.insert(2, " Classic MCPE ");
	versions.insert(3, " Custom Profile ");
	versions.bind('<<ListboxSelect>>', on_select_versions);
	versions.pack(side=LEFT);

	description_text = Label(versions_frame, text="", wraplength=256);
	description_text.pack(pady=48);

	versions_frame.pack(fill=BOTH, expand=True);

	launch_frame = Frame(tab);
	launch_button = Button(launch_frame, text="Launch!", command=pre_launch);
	launch_button.pack(side=RIGHT, anchor=S);
	launch_frame.pack(fill=BOTH, expand=True);
	return tab;

def about_tab(parent):
	tab = Frame(parent);

	title = Label(tab, text="Minecraft Pi Launcher");
	title.config(font=("", 24));
	title.pack();

	version = Label(tab, text="v0.8.0");
	version.config(font=("", 10));
	version.pack();

	authors = HyperLink(tab, "https://github.com/MCPI-Devs/MCPIL/graphs/contributors", text="by all its contributors", fg="black");
	authors.config(font=("", 10));
	authors.pack();

	url = HyperLink(tab, "https://github.com/MCPI-Devs/MCPIL-R");
	url.config(font=("", 10));
	url.pack();
	return tab;

def main(args):
	global window;

	window = Tk();
	window.title("MCPI Laucher - Rebooted");
	window.geometry("512x400");
	window.resizable(False, False);

	tabs = ttk.Notebook(window);
	tabs.add(play_tab(tabs), text="Play");
	tabs.add(about_tab(tabs), text="About");
	tabs.pack(fill=BOTH, expand=True);

	window.wm_protocol("WM_DELETE_WINDOW", bye);

	try:
		window.mainloop();
	except KeyboardInterrupt:
		bye();
	return 0;

if __name__ == "__main__":
	sys.exit(main(sys.argv));

