#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

# Libraries
from gi.repository import Gio, Gtk, GdkPixbuf, AppIndicator3 as appindicator
import gi
import os
import sys
import subprocess

import gettext
import locale

el = gettext.translation('base', 'locale', fallback=True)
el.install()
_ = el.gettext


gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")

CURRDIR = os.path.dirname(os.path.abspath(__file__))
MAINDIR = "./"
ICONDomain = os.path.join(MAINDIR+"images/", 'Domain-icon.png')
ICONLocal = os.path.join(MAINDIR+"images/", 'Local-icon.png')


def getDomain():
    cmd_domainname = "net ads info 2> /dev/null | grep Realm | cut -d':' -f2 | tr -d ' ' | tr -d '\n'"
    domainname = subprocess.check_output((cmd_domainname), shell=True)
    domainname = domainname.decode('UTF-8')
    return(domainname)


def getWorkgroup():
    command = "net ads workgroup | cut -d':' -f2 | tr -d ' ' | tr -d '\n'"
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (workgroupname, err) = proc.communicate()
    workgroupname = workgroupname.decode('UTF-8')
    return(workgroupname)


def getHostname():
    command = "hostname | tr -d '\n'"
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (hostname, err) = proc.communicate()
    hostname = hostname.decode('UTF-8')
    return(hostname)


def getCPU():
    command = "lscpu | grep 'Model name:' | cut -d':' -f2 | sed -e 's/^[[:space:]]*//'| tr -d '\n'"
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (cpumodel, err) = proc.communicate()
    cpumodel = cpumodel.decode('UTF-8')
    command = "lscpu | grep '^CPU(s):' | cut -d':' -f2 | sed -e 's/^[[:space:]]*//'| tr -d '\n'"
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (cpucore, err) = proc.communicate()
    cpucore = cpucore.decode('UTF-8')
    return(cpumodel+" - "+cpucore)


def getRAM():
    command = "awk '/MemTotal/ {print $2}' /proc/meminfo"
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (memory, err) = proc.communicate()
    memory = memory.decode('UTF-8')
    memory = round(int(memory)/1024/1000, 2)
    return(str(memory)+" GB")


def getDist():
    command = "lsb_release -ir | cut -d':' -f2| sed -e 's/^[[:space:]]*//'| tr '\n' ' '"
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (dist, err) = proc.communicate()
    dist = dist.decode('UTF-8')
    return(dist)


class Summary(object):
    def __init__(self):

        # ana pencere bileşeni
        window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        window.set_title('PiriReis')
        window.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        window.set_border_width(32)
        window.set_icon_from_file(ICONDomain)
        window.set_default_size(400, 400)
        window.set_resizable(False)

        #window.connect_after('destroy', self.on_cikis_pencere)
        # window.add(check_button)

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_halign(Gtk.Align.CENTER)
        grid.set_direction(Gtk.TextDirection.LTR)

        window.add(grid)

        quitBtn = Gtk.Button(label=_("Settings"))
        quitBtn.set_size_request(80, 30)
        quitBtn.connect("clicked", self.on_button_clicked)

        label1 = Gtk.Label(("<b>"+getHostname()+"</b>"), use_markup=True)
        label1.set_halign(Gtk.Align.CENTER)

        separator1 = Gtk.Separator()

        label2 = Gtk.Label(getDist())
        label2.set_halign(Gtk.Align.START)
        label2.set_direction(Gtk.TextDirection.LTR)
        label2_a = Gtk.Label(_("OS:"))
        label2_a.set_halign(Gtk.Align.END)
        label2_a.set_direction(Gtk.TextDirection.LTR)

        label3 = Gtk.Label(getCPU())
        label3.set_halign(Gtk.Align.START)
        label3.set_direction(Gtk.TextDirection.LTR)
        label3_a = Gtk.Label(_("CPU:"))
        label3_a.set_halign(Gtk.Align.END)
        label3_a.set_direction(Gtk.TextDirection.LTR)

        label4 = Gtk.Label(getRAM())
        label4.set_halign(Gtk.Align.START)
        label4.set_direction(Gtk.TextDirection.LTR)
        label4_a = Gtk.Label(_("RAM:"))
        label4_a.set_halign(Gtk.Align.END)
        label4_a.set_direction(Gtk.TextDirection.LTR)

        separator2 = Gtk.Separator()

        domain = getDomain()
        label5 = Gtk.Label(domain)
        if(domain == ""):
            label5 = Gtk.Label(_("Domain could not found"))

        label5.set_halign(Gtk.Align.START)
        label5.set_direction(Gtk.TextDirection.LTR)
        label5_a = Gtk.Label(_("Domain:"))
        label5_a.set_halign(Gtk.Align.END)
        label5_a.set_direction(Gtk.TextDirection.LTR)

        workgroup = getWorkgroup()
        label6 = Gtk.Label(workgroup)
        if(workgroup == ""):
            label6 = Gtk.Label(_("Workgroup could not found"))

        label6.set_halign(Gtk.Align.START)
        label6.set_direction(Gtk.TextDirection.LTR)
        label6_a = Gtk.Label(_("Workgroup:"))
        label6_a.set_halign(Gtk.Align.END)
        label6_a.set_direction(Gtk.TextDirection.LTR)

        separator3 = Gtk.Separator()

        if (getDomain() != ""):
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename=ICONDomain,
                width=96,
                height=96,
                preserve_aspect_ratio=True)
        else:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                filename=ICONLocal,
                width=96,
                height=96,
                preserve_aspect_ratio=True)

        image1 = Gtk.Image.new_from_pixbuf(pixbuf)

        grid.attach(label1, 0, 0, 4, 1)
        grid.attach_next_to(image1, label1, Gtk.PositionType.BOTTOM, 4, 2)
        grid.attach_next_to(separator1, image1, Gtk.PositionType.BOTTOM, 4, 2)

        grid.attach_next_to(label2_a, separator1,
                            Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label2, label2_a, Gtk.PositionType.RIGHT, 3, 2)
        grid.attach_next_to(label3_a, label2_a, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label3, label3_a, Gtk.PositionType.RIGHT, 3, 2)
        grid.attach_next_to(label4_a, label3_a, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label4, label4_a, Gtk.PositionType.RIGHT, 3, 2)
        grid.attach_next_to(separator2, label4_a,
                            Gtk.PositionType.BOTTOM, 4, 2)
        grid.attach_next_to(label5_a, separator2,
                            Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label5, label5_a, Gtk.PositionType.RIGHT, 3, 2)
        grid.attach_next_to(label6_a, label5_a, Gtk.PositionType.BOTTOM, 1, 2)
        grid.attach_next_to(label6, label6_a, Gtk.PositionType.RIGHT, 3, 2)
        grid.attach_next_to(separator3, label6_a,
                            Gtk.PositionType.BOTTOM, 4, 2)

        grid.attach_next_to(quitBtn, separator3, Gtk.PositionType.BOTTOM, 4, 2)

        window.show_all()

    def on_button_clicked(self, widget):
        print("Settings")
        #Gtk.main_quit()

    def on_degisim_ornekozellik(self, settings, key, check_button):
        check_button.set_active(settings.get_boolean("ornekozellik"))

    def on_kontrol_ornekozellik(self, button, settings):
        settings.set_boolean("ornekozellik", button.get_active())
