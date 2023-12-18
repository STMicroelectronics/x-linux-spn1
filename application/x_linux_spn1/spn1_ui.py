#!/usr/bin/python3

# Copyright (c) 2023 STMicroelectronics. All rights reserved.
#
# This software component is licensed by ST under BSD 3-Clause license,
# the "License"; You may not use this file except in compliance with the
# License. You may obtain a copy of the License at:
#                     opensource.org/licenses/BSD-3-Clause


import sys
import gi
import os
import threading
import time

gi.require_version('Gtk','3.0')
from gi.repository import Gtk as gtk , Gdk,  GdkPixbuf

# For simulating UI on PC , please use
# the variable SIMULATE = 1
SIMULATE = 0
if SIMULATE > 0:
    #DEMO_PATH = os.environ['HOME']+"/Desktop/launcher"
    DEMO_PATH = "/home/ubuntu/root/local"
else:
    DEMO_PATH = "/usr/local/demo"
cc_count=5
close=0
error =0

img_logo=os.path.join(DEMO_PATH, "application/x_linux_spn1/pictures/Logo.png")
img_F= os.path.join(DEMO_PATH, "application/x_linux_spn1/pictures/Closed arrow_F.png")

img_B= os.path.join(DEMO_PATH, "application/x_linux_spn1/pictures/Closed arrow_B.png")
img_L= os.path.join(DEMO_PATH, "application/x_linux_spn1/pictures/Closed arrow_L.png")
img_R= os.path.join(DEMO_PATH, "application/x_linux_spn1/pictures/Closed arrow_R.png")
imagelogo=None
imager=None
imagel=None
imagef=None
imageb=None
z=1
popup_window=None
window1=None
gladeFile=None
img_IHM_12= os.path.join(DEMO_PATH, "application/x_linux_spn1/pictures/image_IHM_12.png")
img_IHM_15= os.path.join(DEMO_PATH, "application/x_linux_spn1/pictures/image_IHM_15.png")
img_F_G= os.path.join(DEMO_PATH, "application/x_linux_spn1/pictures/Closed arrow_F_Green.png")
img_B_G= os.path.join(DEMO_PATH, "application/x_linux_spn1/pictures/Closed arrow_B_Green.png")
img_L_G= os.path.join(DEMO_PATH, "application/x_linux_spn1/pictures/Closed arrow_L_Green.png")
img_R_G= os.path.join(DEMO_PATH, "application/x_linux_spn1/pictures/Closed arrow_R_Green.png")

new_pixbuf_IHM_12 = GdkPixbuf.Pixbuf.new_from_file(img_IHM_12)
new_pixbuf_IHM_15 = GdkPixbuf.Pixbuf.new_from_file(img_IHM_15)
new_pixbuf_F = GdkPixbuf.Pixbuf.new_from_file(img_F)
new_pixbuf_B = GdkPixbuf.Pixbuf.new_from_file(img_B)
new_pixbuf_R = GdkPixbuf.Pixbuf.new_from_file(img_R)
new_pixbuf_L = GdkPixbuf.Pixbuf.new_from_file(img_L)
new_pixbuf_B_G = GdkPixbuf.Pixbuf.new_from_file(img_B_G)
new_pixbuf_L_G = GdkPixbuf.Pixbuf.new_from_file(img_L_G)
new_pixbuf_R_G = GdkPixbuf.Pixbuf.new_from_file(img_R_G)
new_pixbuf_F_G = GdkPixbuf.Pixbuf.new_from_file(img_F_G)
motor =None
first_on=0
Board = None
module_12 =0
module_15 =0

def IHM_12_driver(x,y):

    global motor
    global Board
    if Board !="IHM_12":
        import application.x_linux_spn1.ihm12_api as motor

    Board="IHM_12"
   
    popup_window.destroy()
    

def IHM_15_driver(x,y):
    global motor
    global Board
    if Board != "IHM_15":
        try:
            import application.x_linux_spn1.ihm15_api as motor
        except:
            import ihm15_api as motor
     
    Board="IHM_15"
    popup_window.destroy()

def create_popup_window(parent_window, glade_file, width, height):
    builder = gtk.Builder()
    builder.add_from_file(glade_file)
    global popup_window
    popup_window = builder.get_object("Motor_driver_menu")
    popup_window.set_title("")
    popup_window.set_transient_for(parent_window)
    popup_window.set_modal(True)
    popup_window.set_default_size(width,height)

    IHM_12 = builder.get_object("IHM_12")
    IHM_12.connect("button_press_event",IHM_12_driver)
  
    image_widget_IHM_12 = builder.get_object("IHM_12_image")
    
    IHM_15 = builder.get_object("IHM_15")
    IHM_15.connect("button_press_event",IHM_15_driver)
 
    image_widget_IHM_15 = builder.get_object("IHM_15_image")
 
    image_widget_IHM_12.set_from_pixbuf(new_pixbuf_IHM_12)
    image_widget_IHM_15.set_from_pixbuf(new_pixbuf_IHM_15)
    popup_window.fullscreen()
    response = popup_window.run()

    popup_window.destroy()

count_start =0

class Main(gtk.Window):
    def __init__(self, parent):
        global gladeFile
        gladeFile = os.path.join(DEMO_PATH, "application/x_linux_spn1/spn1_ui.glade")
        self.builder=gtk.Builder()
        self.builder.add_from_file(gladeFile)
        global imagef
        global imageb
        global imagel
        global imager
        global imagelogo
        #logo
        Logo = self.builder.get_object("St_logo")
        imagelogo = gtk.Image.new_from_file(img_logo)
        Logo.add(imagelogo)
        
        img= os.path.join(DEMO_PATH, "application/x_linux_spn1/pictures/Close.png")
        
        dtry = self.builder.get_object("dtry")
        image = gtk.Image.new_from_file(img)
        dtry.add(image)
        
        img_RD= os.path.join(DEMO_PATH, "application/x_linux_spn1/pictures/Reload.png")
        Reset = self.builder.get_object("Reset")
        image = gtk.Image.new_from_file(img_RD)
        Reset.add(image)
        Reset.connect("button_press_event",self.Reload)
        #buttons for movement
        F_button = self.builder.get_object("F_button")
        imagef = gtk.Image.new_from_file(img_F)
        F_button.add(imagef)
        F_button.connect("button_press_event",self.printTextF)
       
        # Set button background color using CSS
        css_provider =gtk.CssProvider()
        css_path= os.path.join(DEMO_PATH, "application/x_linux_spn1/spn1_ui.css")
        css_provider.load_from_path(css_path) #load css file
        
        context =F_button.get_style_context()
        context.add_provider(css_provider, gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        context.add_class("custom")


       

        context =dtry.get_style_context()
        context.add_provider(css_provider, gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        context.add_class("custom")
        global error
        if error==1:
            Error_msg= self.builder.get_object("Error_msg")
            Error_msg.set_label("Fault detected, To reset please restart the Board")


        # buttons for movement
        B_button = self.builder.get_object("B_button")
        B_button.connect("button_press_event",self.printTextB)
      
        imageb = gtk.Image.new_from_file(img_B)
        B_button.add(imageb)
       


        L_button = self.builder.get_object("L_button")
        L_button.connect("button_press_event",self.printTextL)
       
        imagel = gtk.Image.new_from_file(img_L)
        L_button.add(imagel)
       
        R_button = self.builder.get_object("R_button")
        R_button.connect("button_press_event",self.printTextR)
    
        imager = gtk.Image.new_from_file(img_R)
        R_button.add(imager)
       

        #labels to show duty % in realtime
        L_label =self.builder.get_object("L_duty")
        L_label.set_label("50%")

        
       

       
        
        L_scale_button = self.builder.get_object("L_scale")
        L_scale_button.connect("value-changed", self.L_on_scale_value_changed)
        L_scale_button.set_value(50)

        R_scale_button = self.builder.get_object("R_scale")
        R_scale_button.connect("value-changed", self.R_on_scale_value_changed)
        R_scale_button.set_value(50)



        #CSS on button
        #1
        context =B_button.get_style_context()
        context.add_provider(css_provider, gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        context.add_class("custom")

        #2
        context =L_button.get_style_context()
        context.add_provider(css_provider, gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        context.add_class("custom")
        #3
        context =R_button.get_style_context()
        context.add_provider(css_provider, gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        context.add_class("custom")
       
       

        # switch(on/off)
        Switch = self.builder.get_object("Switch")
        Switch.connect("toggled",self.printTextON)
        Switch.set_label("Off")
        context1 =Switch.get_style_context()
        context1.add_provider(css_provider, gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        context1.add_class("custom1") 
        global count_start
        global window1   
        if count_start==0:
            create_popup_window(window1, gladeFile, parent.get_size()[0], parent.get_size()[1])  
        count_start=1

        
        if Board =="IHM_12":
            Board_name=self.builder.get_object("Board_name")
            Board_name.set_label("X-NUCLEO-IHM12A1")    
        elif Board=="IHM_15":
            Board_name=self.builder.get_object("Board_name")
            Board_name.set_label("X-NUCLEO-IHM15A1") 



        window1 = self.builder.get_object('window1')

        dtry.connect("button_press_event",self.Wclose)

        #Show window   
        window1.connect("delete-event",gtk.main_quit) 
        window1 .set_default_size(parent.get_size()[0], parent.get_size()[1])
        #window1.fullscreen()
        
        window1.set_decorated(False)
        window1.show_all()
        global close
        close=0
        my_thread = threading.Thread(target=self.Current_check_ui)
        my_thread.start()
       
    def Wclose(x,widget,event):
        global motor
        global first_on
        global close
        close=1
        first_on=0
        motor.reset()
        motor.end()
        
        window1.destroy()
      
        

    
    def R_on_scale_value_changed(self,widget):
        value = widget.get_value()
        R_label =self.builder.get_object("R_duty")
        R_label.set_label("%d%%" %(100- value))
    
    def L_on_scale_value_changed(self,widget):
        value = widget.get_value()
        L_label =self.builder.get_object("L_duty")
        L_label.set_label("%d%%" %(100- value))
    def Current_check_ui(self):
        global error
        global cc_count
        global close
        while(1):
            if (motor.Current_check() == 0):
                time.sleep(1)
                if (error == 0 and motor.Current_check() == 0):
                    Error_msg= self.builder.get_object("Error_msg")
                    Error_msg.set_label("Fault detected, To reset please restart the Board")
                    error=1
                    while(motor.Current_check()==0):
                        if close==1:
                            return   
                      
            if (motor.Current_check()==1 and error==1):
                Error_msg= self.builder.get_object("Error_msg")
                Error_msg.set_label("")
                error=0

            time.sleep(5)

            if close==1:
                return      

    def printTextON(self, widget):

        global z
        global error
        if z==1 and error==0:
            global first_on
            if first_on==0:

                imagef.set_from_pixbuf(new_pixbuf_F_G)
                imageb.set_from_pixbuf(new_pixbuf_B)
                imager.set_from_pixbuf(new_pixbuf_R)
                imagel.set_from_pixbuf(new_pixbuf_L)
                first_on=1     
            motor.start()
            


            z=0
            Switch = self.builder.get_object("Switch")
            Switch.set_label("On")
              
        else:
            if error==0:
                z=1
                motor.stop()
                Switch = self.builder.get_object("Switch")
                Switch.set_label("Off")

    def printTextLU(self, widget,event):
        global y
        if y+10 < 101:
            y=y+10

        L_label =self.builder.get_object("L_duty")
        L_label.set_label("%d%%" % y)

    def printTextRD(self, widget):
        global x
        if x-10> -1:
            x=x-10

        R_label =self.builder.get_object("R_duty")
        R_label.set_label("%d%%" % x)

    def Reload(self, widget,event):
        imagef.set_from_pixbuf(new_pixbuf_F)
        imageb.set_from_pixbuf(new_pixbuf_B)
        imager.set_from_pixbuf(new_pixbuf_R)
        imagel.set_from_pixbuf(new_pixbuf_L)
        motor.reset()
        global z
        global error
        z=1
        error =0
        global first_on
        first_on=0
        Switch = self.builder.get_object("Switch")
        Switch.set_label("Off")
        L_scale_button = self.builder.get_object("L_scale")
        L_scale_button.connect("value-changed", self.L_on_scale_value_changed)
        L_scale_button.set_value(50)

        R_scale_button = self.builder.get_object("R_scale")
        R_scale_button.connect("value-changed", self.R_on_scale_value_changed)
        R_scale_button.set_value(50)



#motor controller functions
    def printTextF(self, widget,event):
        imagef.set_from_pixbuf(new_pixbuf_F_G)
        imageb.set_from_pixbuf(new_pixbuf_B)
        imager.set_from_pixbuf(new_pixbuf_R)
        imagel.set_from_pixbuf(new_pixbuf_L)
        
        motor.forward()
    
    def printTextB(self, widget,event):
        imageb.set_from_pixbuf(new_pixbuf_B_G)
        imagef.set_from_pixbuf(new_pixbuf_F)
        imager.set_from_pixbuf(new_pixbuf_R)
        imagel.set_from_pixbuf(new_pixbuf_L)
        motor.backward()


    def printTextL(self, widget,event):
        imagel.set_from_pixbuf(new_pixbuf_L_G)
        imagef.set_from_pixbuf(new_pixbuf_F)
        imageb.set_from_pixbuf(new_pixbuf_B)
        imager.set_from_pixbuf(new_pixbuf_R)
        
        motor.left()
    def printTextR(self, widget,event):
        imager.set_from_pixbuf(new_pixbuf_R_G)
        imagef.set_from_pixbuf(new_pixbuf_F)
        imageb.set_from_pixbuf(new_pixbuf_B)
        imagel.set_from_pixbuf(new_pixbuf_L)
        motor.right()


def create_subdialogwindow(parent):
    gtk.init()
    _window = Main(parent)


#for testing purpose
class TestUIWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self, title="X-LINUX-SPN1")
        create_subdialogwindow(self)
        self.show_all()

if __name__=='__main__':
    win = TestUIWindow()
    win.connect("delete-event", gtk.main_quit)
    win.show_all()
