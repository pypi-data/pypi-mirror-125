def heater():
    



    from tkinter import *
    from tkinter import ttk
    from tkinter import _tkinter
    from gpiozero import Button, Button, LED
    from signal import pause
    import time
    import datetime as dt




    #Defining Buttons
    relay = LED(20)
    relay1 = LED(14)
    star= Button(3)
    pet = Button(2)
    die= Button(4)
    ker= Button(13)
    bit= Button(19)
    res= Button(26)
    lmtSwitch= Button(21)
    lmtSwitch1= Button(5)


    #Main Window and its properties
    Main_window = Tk()
    Main_window.title('OilSpecApp')
    Main_window.attributes("-fullscreen", True)
    Main_window.configure(bg='white')


    #Logos
    canvas = Canvas(Main_window, width = 101, height = 101, borderwidth=0, highlightthickness=0, bg="white", highlightbackground="white")      
    canvas.grid(row=0, column=0)
    global img
    img = PhotoImage(file="unnamed1.ppm")      
    canvas.create_image(1,1, anchor=NW, image=img)  

    canvas1 = Canvas(Main_window, width = 167, height = 40, borderwidth=0, highlightthickness=0, bg="white", highlightbackground="white")      
    canvas1.place(x=420)
    global img1
    img1 = PhotoImage(file="K1.ppm")      
    canvas1.create_image(1,1, anchor=NW, image=img1)

    #Thermo

    canvas2 = Canvas(Main_window, width = 90, height = 297, borderwidth=0, highlightthickness=0, bg='white', highlightbackground="white")       

    canvas2.place(x=450, y=70)

    global img2

    img2 = PhotoImage(file="thermo3.ppm")      

    canvas2.create_image(1,1, anchor=NW, image=img2)




    #Bottom Labels: V and T
    Label(Main_window, text = "V:4.0", font=("Arial", 11),bg="white").place(y=426)
    Label(Main_window, text = "F300", font=("Arial", 11),bg="white").place(x=558,y=426)

    # Labels                                                                                    #Sizes and Pos

    Label(Main_window, text = "Settings   ", font=("Arial Bold",13),bg="#F8F9FA").place(x=40,y=290)

    Label(Main_window, text = "User", font=("Arial",11),bg="white").place(x=40,y=325)

    Label(Main_window, text = "Administrator", font=("Arial",11),bg="white").place(x=120,y=325)

    Label(Main_window, text = "Method", font=("Arial",11),bg="white").place(x=40,y=355)

    Label(Main_window, text = "Freezing Point", font=("Arial",11),bg="white").place(x=120,y=355)

    Label(Main_window, text = "Mode", font=("Arial",11),bg="white").place(x=40,y=385)

    Label(Main_window, text = "Freezing", font=("Arial",11),bg="white").place(x=120,y=385) #

    Label(Main_window, text = "Fuel", font=("Arial",12),bg="white").place(x=280,y=325)

    Label(Main_window, text = "Made in", font=("Arial Bold",13),bg="white").place(x=280,y=360)#

    Label(Main_window, text = "Pakistan", font=("Arial Bold",13),bg="white").place(x=360,y=360) ##

    Label(Main_window, text = "KidZania ADNOC", font=("Arial Bold",17), bg="white").place(x=165,y=20)

    Label(Main_window, text = "Freezer", font=("Arial Bold",17), bg="white").place(x=210,y=54)  #Spectrometer to Freezer and Pos. Changed

    Label(Main_window, text = "Freezing Point             0.00 °C", font=("Arial Bold",14),bg="white").place(x=40,y=220) ##

    Label(Main_window, text = "Room Temperature     24.0 °C", font=("Arial Bold",14),bg="white").place(x=40,y=250) ##

    Label(Main_window, text = "°C", font=("Arial Bold",20),bg="white").place(x=300,y=170)

    Label(Main_window, text=f"{dt.datetime.now():%a, %b %d %Y}", bg="white", font=("Arial", 12)).place(x=330,y=424)


    #For Time
    time1 = ''
    clock = Label(Main_window, font=('Arial', 12), bg='white')
    clock.place(x=130,y=424)
    
    def tick():
        global time1
        # get the current local time from the PC
        time2 = time.strftime('%H:%M:%S')
        # if time string has changed, update it
        if time2 != time1:
            time1 = time2
            clock.config(text=time2)
        # calls itself every 200 milliseconds
        # to update the time display as needed
        # could use >200 ms, but display gets jerky
        clock.after(200, tick)
        
    tick()


    #Text Variables
    my_text = "Press to start..."
    my_text1 = "IMAD IS BEST"


    #Labels to be varied
    my_label= Label(Main_window)
    G= Label(Main_window)
    Result=Label(Main_window)

    space=Label(Main_window)
    space1=Label(Main_window)
    space2=Label(Main_window)
    space3=Label(Main_window)
    space4=Label(Main_window)
    space5=Label(Main_window)
    space6=Label(Main_window)
    space7=Label(Main_window)
    space8=Label(Main_window)
    space9=Label(Main_window)
    space10=Label(Main_window)
    space11=Label(Main_window)
    space12=Label(Main_window)

    #Functions for pages
    def startpage():

        def flash():

                bg = my_label.cget("background")

                fg = my_label.cget("foreground")

                my_label.configure(background=fg, foreground=bg)

                my_label.after(500, flash)



        global my_label

        global G

        global Result
        global space
        global space1
        global space2
        global space3
        global space4
        global space5
        global space6
        global space7
        global space8
        global space9
        global space10
        global space11
        global space12

        space.destroy()
        space1.destroy()
        space2.destroy()
        space3.destroy()
        space4.destroy()
        space5.destroy()
        space6.destroy()
        space7.destroy()
        space8.destroy()
        space9.destroy()
        space10.destroy()
        space11.destroy()
        space12.destroy()
        

        my_label.destroy()

        G.destroy()

        Result.destroy()

        

     #my_label= Label(Main_window, text = "Select Fuel:",  font=("Arial Bold", 24), fg="#0959A8", bg="white")

     # my_label.place(x=170,y=110)

        global I
        global j
        
        if lmtSwitch.is_pressed==0:
            if lmtSwitch1.is_pressed==0:
                j=0
            elif lmtSwitch1.is_pressed==1:
                j=1
                my_label= Label(Main_window, text = "Please, close the door!",  font=("Arial Bold", 20), fg="#0959A8", bg="white")
                my_label.place(x=120,y=110)
            I=0
        if lmtSwitch.is_pressed:
            I=1
            if lmtSwitch1.is_pressed==0:
                my_label.destroy()
                my_label= Label(Main_window, text = "Press reset",  font=("Arial Bold", 24), fg="#0959A8", bg="white")
                my_label.place(x=170,y=110)
                res.when_pressed=rest
                j=0
            elif lmtSwitch1.is_pressed==1:
                my_label= Label(Main_window, text = "Select Fuel:",  font=("Arial Bold", 24), fg="#0959A8", bg="white")
                my_label.place(x=170,y=110)
                pet.when_pressed = petrolpts
                die.when_pressed = dieselpts
                ker.when_pressed = kerosenepts
                bit.when_pressed = bitumenpts
                j=1
        G= Label(Main_window, text = "None", font=("Arial",12),bg="white")
        Result= Label(Main_window, text="0.00", font=("Arial",30),bg="white")
        
        

        space=Label(Main_window,text="   ",fg="#ED1C24",bg="#ED1C24",  font=("Arial", 18),)
        space.place(x=473,y=302)
        space1=Label(Main_window,text="   ",fg="#ED1C24",bg="#ED1C24",  font=("Arial", 18),)
        space1.place(x=473,y=287)
        space2=Label(Main_window,text="   ",fg="#ED1C24",bg="#ED1C24",  font=("Arial", 18),)
        space2.place(x=473,y=257)
        space3=Label(Main_window,text="   ",fg="#ED1C24",bg="#ED1C24",  font=("Arial", 18),)
        space3.place(x=473,y=247)
        space4=Label(Main_window,text="   ",fg="#ED1C24",bg="#ED1C24",  font=("Arial", 18),)
        space4.place(x=473,y=237)
        space5=Label(Main_window,text="   ",fg="#ED1C24",bg="#ED1C24",  font=("Arial", 18),)
        space5.place(x=473,y=227)
        space6=Label(Main_window,text="   ",fg="#ED1C24",bg="#ED1C24",  font=("Arial", 18),)
        space6.place(x=473,y=207)
        space7=Label(Main_window,text="   ",fg="#ED1C24",bg="#ED1C24",  font=("Arial", 18),)
        space7.place(x=473,y=194)
        space8=Label(Main_window,text="   ",fg="#ED1C24",bg="#ED1C24",  font=("Arial", 18),)
        space8.place(x=473,y=182)
        space9=Label(Main_window,text="   ",fg="#ED1C24",bg="#ED1C24",  font=("Arial", 18),)
        space9.place(x=473,y=151)
        space10=Label(Main_window,text="   ",fg="#ED1C24",bg="#ED1C24",  font=("Arial", 18),)
        space10.place(x=473,y=137)
        space11=Label(Main_window,text="   ",fg="#ED1C24",bg="#ED1C24",  font=("Arial", 18),)
        space11.place(x=473,y=130)
        space12=Label(Main_window,text="   ",fg="#ED1C24",bg="#ED1C24",  font=("Arial", 18),)
        space12.place(x=473,y=125)
        #Positions for Labels
        
        G.place(x=360,y=325)
        Result.place(x=200, y=160)
        flash()
        
        
        lmtSwitch.when_released = old  
        lmtSwitch.when_pressed = new


        lmtSwitch1.when_released = old1 
        lmtSwitch1.when_pressed = new1
            
        
                
        
        #Buttons Integration


    def ajeeb():
        global I
        global my_label
        global j
        def flash():
            bg = my_label.cget("background")
            fg = my_label.cget("foreground")
            my_label.configure(background=fg, foreground=bg)
            my_label.after(500, flash)
    
        if I==0:
            my_label.destroy()
            my_label= Label(Main_window, text = "Please, close the door!",  font=("Arial Bold", 20), fg="#0959A8", bg="white")
            my_label.place(x=120,y=110)
            print(I)
            pet.when_pressed = ajeeb
            die.when_pressed = ajeeb
            ker.when_pressed = ajeeb
            bit.when_pressed = ajeeb
            star.when_pressed = ajeeb
            flash()
        elif I==1:
            print(I)
            
            if  j==0:
                print(j)
                my_label.destroy()
                my_label= Label(Main_window, text = "Press reset",  font=("Arial Bold", 24), fg="#0959A8", bg="white")
                my_label.place(x=170,y=110)
                pet.when_pressed = ajeeb
                die.when_pressed = ajeeb
                ker.when_pressed = ajeeb
                bit.when_pressed = ajeeb
                star.when_pressed = ajeeb
                res.when_pressed = rest
                
            if j==1:
                my_label.destroy()
                my_label= Label(Main_window, text = "Select Fuel",  font=("Arial Bold", 24), fg="#0959A8", bg="white")
                my_label.place(x=170,y=110)
                pet.when_pressed = petrolpts
                die.when_pressed = dieselpts
                ker.when_pressed = kerosenepts
                bit.when_pressed = bitumenpts

        flash()

    
    def new():
        global I
        I=1
        ajeeb()


    
    def old():
        global I
        I=0
        ajeeb()

    def new1():
        print("new1")
        global j
        j=1
        ajeeb()


    
    def old1():
        global j
        j=0
        ajeeb()
    
    def start():
        
        if (a==1):
                
                print(a)
                star.when_pressed = petrol
            
        if (a==2):
            star.when_pressed = diesel
        if (a==3):
            star.when_pressed = kerosene
        if (a==4):
            star.when_pressed = bitumen

    def petrolpts():

	
        global my_text
        global my_text1
        global my_label
        global G
        
        my_label.destroy()
        G.destroy()
        
        my_label= Label(Main_window, text = "Press to Start",  font=("Arial Bold", 24), fg="black", bg="white")
        G= Label(Main_window, text = "Petrol", font=("Arial",12),bg="white")
        
        my_label.place(x=155,y=110)
        G.place(x=360,y=325)
        
        global a
        a=1
        star.when_pressed = petrol


    def petrol():

        global space
        global space1
        global space2
        global space3
        global space4
        global space5
        global space6
        global space7
        global space8
        global space9
        global space10
        global space11
        global space12

        
        global my_text
        global my_text1
        global my_label
        global Result
        
        Result.destroy()
        my_label.destroy()
        my_label= Label(Main_window, text = "Processing",  font=("Arial Bold", 24), fg="black", bg="white")
        my_label.place(x=170,y=100)
        
        
        
        relay.on()
        space12.destroy()
        time.sleep(4)
        space11.destroy()
        time.sleep(4)
        space10.destroy()
        time.sleep(4)
        space9.destroy()
        time.sleep(4)
        space8.destroy()
        time.sleep(4)
        space7.destroy()
        time.sleep(4)
        space6.destroy()
        time.sleep(4)
        space5.destroy()
        time.sleep(4)
        space4.destroy()
        time.sleep(4)
        space3.destroy()
        time.sleep(4)
        space2.destroy()
        time.sleep(4)
        space1.destroy()
        time.sleep(4)
        
        
        f=10
        relay.off()
        print(f)
        my_label.destroy()
        Result= Label(Main_window, text="-60", font=("Arial Bold",30),bg="white")
        Result.place(x=200, y=160)
        my_label= Label(Main_window, text = "Freezing Point",  font=("Arial Bold", 24), fg="black", bg="white")
        my_label.place(x=170,y=100)

        res.when_pressed= rest


    def dieselpts():
	
        global my_text
        global my_text1
        global my_label
        global G
        
        my_label.destroy()
        G.destroy()

        
        my_label= Label(Main_window, text = "Press to Start",  font=("Arial Bold", 24), fg="black", bg="white")
        G= Label(Main_window, text = "Diesel", font=("Arial",12),bg="white")
        
        my_label.place(x=155,y=110)
        G.place(x=360,y=325)

        global a
        a=2
        start()

    def diesel():
        
        global space
        global space1
        global space2
        global space3
        global space4
        global space5
        global space6
        global space7
        global space8
        global space9
        global space10
        global space11
        global space12

        
        global my_text
        global my_text1
        global my_label
        global Result
        
        Result.destroy()
        my_label.destroy()
        my_label= Label(Main_window, text = "Processing",  font=("Arial Bold", 24), fg="black", bg="white")
        my_label.place(x=170,y=100)
        
        

        relay.on()
        space12.destroy()
        time.sleep(4)
        space11.destroy()
        time.sleep(4)
        space10.destroy()
        time.sleep(4)
        space9.destroy()
        time.sleep(4)
        space8.destroy()
        time.sleep(4)
        
        
        
        
        f=10
        relay.off()
        
        my_label.destroy()
        Result= Label(Main_window, text="-8.1", font=("Arial Bold",30),bg="white")
        Result.place(x=200, y=160)
        my_label= Label(Main_window, text = "Freezing Point",  font=("Arial Bold", 24), fg="black", bg="white")
        my_label.place(x=170,y=100)

        
        res.when_pressed= rest
        
    def kerosenepts():

	
        global my_text
        global my_text1
        global my_label
        global G
        
        my_label.destroy()
        G.destroy()
        
        my_label= Label(Main_window, text = "Press to Start",  font=("Arial Bold", 24), fg="black", bg="white")
        G= Label(Main_window, text = "Kerosene", font=("Arial",12),bg="white")
        
        my_label.place(x=155,y=110)
        G.place(x=360,y=325)
        
        global a
        a=3
        start()
        

    def kerosene():
        
        global space
        global space1
        global space2
        global space3
        global space4
        global space5
        global space6
        global space7
        global space8
        global space9
        global space10
        global space11
        global space12
        
        global my_text
        global my_text1
        global my_label
        global Result
        
        Result.destroy()
        my_label.destroy()
        my_label= Label(Main_window, text = "Processing",  font=("Arial Bold", 24), fg="black", bg="white")
        my_label.place(x=170,y=100)
        
        

        relay.on()
        space12.destroy()
        time.sleep(4)
        space11.destroy()
        time.sleep(4)
        space10.destroy()
        time.sleep(4)
        space9.destroy()
        time.sleep(4)
        space8.destroy()
        time.sleep(4)
        space7.destroy()
        time.sleep(4)
        space6.destroy()
        time.sleep(4)
        space5.destroy()
        time.sleep(4)
        space4.destroy()
        time.sleep(4)
        
        
        
        
        f=10
        relay.off()
        
        my_label.destroy()
        Result= Label(Main_window, text="-47", font=("Arial Bold",30),bg="white")
        Result.place(x=200, y=160)
        my_label= Label(Main_window, text = "Freezing Point",  font=("Arial Bold", 24), fg="black", bg="white")
        my_label.place(x=170,y=100)

        
        

        res.when_pressed= rest
        
        
        
    def bitumenpts():
	
        global my_text
        global my_text1
        global my_label
        global G

        
        my_label.destroy()
        G.destroy()

        
        my_label= Label(Main_window, text = "Press to Start",  font=("Arial Bold", 24), fg="black", bg="white")
        G= Label(Main_window, text = "Bitumen", font=("Arial",12),bg="white")
        
        my_label.place(x=155,y=110)
        G.place(x=360,y=325)

        global a
        a=4
        start()


    def bitumen():

        global space
        global space1
        global space2
        global space3
        global space4
        global space5
        global space6
        global space7
        global space8
        global space9
        global space10
        global space11
        global space12
        global my_text
        global my_text1
        global my_label
        global Result
        
        Result.destroy()
        my_label.destroy()
        my_label= Label(Main_window, text = "Processing",  font=("Arial Bold", 24), fg="black", bg="white")
        my_label.place(x=170,y=100)
        
        

        relay.on()
        space12.destroy()
        time.sleep(4)
        space11.destroy()
        time.sleep(4)
        space10.destroy()
        time.sleep(4)
        space9.destroy()
        time.sleep(4)
        
        
        
        
        
        f=10
        relay.off()
        
        my_label.destroy()
        Result= Label(Main_window, text="-4.7", font=("Arial Bold",30),bg="white")
        Result.place(x=200, y=160)
        my_label= Label(Main_window, text = "Freezing Point",  font=("Arial Bold", 24), fg="black", bg="white")
        my_label.place(x=170,y=100)
        
        res.when_pressed= rest

    def rest():
        global my_label
        my_label.destroy()
        my_label= Label(Main_window, text = "Resetting! Please Wait",  font=("Arial Bold", 22), fg="#0959A8", bg="white")
        my_label.place(x=110,y=110)
        #res relay on
        relay1.on()
        if lmtSwitch1.is_pressed==0:
            print("Imad")
            rest()
        elif lmtSwitch1.is_pressed==1:
            print("ANYTHIN")
            startpage()
            #res relay off
            relay1.off()
            print("OK")




    #Buttons Integration


    #Start Page on start
    startpage()         



    # Starting the GUI
    Main_window.mainloop()


heater()
