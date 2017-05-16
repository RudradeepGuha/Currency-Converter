# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 22:04:10 2017

@author: RudradeepGuha
"""

import bs4
import requests

#URL from which live rates are being scraped
url = "http://www.xe.com/?c=CHF"

#This function takes care of the conversion after scraping the live rates 
#off the URL and accepting the amount to convert as a parameter.
def convert(frm, to, amt):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
    c_rates = requests.get(url, headers = headers)
    c_rates.raise_for_status()
    c_soup = bs4.BeautifulSoup(c_rates.text)
    
    #Finds all <a> tags in the HTML code and check if they contain the string 
    #"currency-we-want-to-convert-from, currency-we-want-to-convert-to"
    rate = c_soup.find('a', attrs = {'rel': lambda x: x and to+","+frm in x[:7]})
    if rate == None: #if exchange rate of two currencies is not explicitly provided...
    #We first convert the currency to US Dollars and then convert that amount to the desired currency,
    #since exchange rates between USD and all others are available.
        from_usd = float(c_soup.find('a', attrs = {'rel': lambda x: x and "USD,"+frm in x[:7]}).contents[0])
        to_usd = float(c_soup.find('a', attrs = {'rel': lambda x: x and "USD,"+to in x[:7]}).contents[0])
        desired_currency_rate = from_usd/to_usd
        a = desired_currency_rate*amt
        return "{0:.2f}".format(round(a, 2)) #Round off to 2 decimal points
    else:
        a = float(rate.contents[0])*amt     #Most currencies have readily available exchange rates so we just extract the contents of the correct <a> tag
        return "{0:.2f}".format(round(a, 2))
    
import tkinter as tk
#from PIL import Image, ImageTk

win = tk.Tk()
win.title("Currency Coverter")
win.resizable(width=False, height=False)  #Disallow resizing ability of window
win.geometry('{}x{}'.format(550, 350))    #Dimensions of GUI window
win.configure(background='white')

#Code for adding a background to the GUI window
#image = Image.open("background_image.jpg")
#bg_image = ImageTk.PhotoImage(image)
#bg_label = tk.Label(win, image=bg_image)
#bg_label.place(x=0, y=0, relwidth=1, relheight=1)
#bg_label.image = bg_image

#Adds a message in the tezt box which disappears when the widget is clicked on 
def click(event):
    current_widget = amt_field.get('1.0', 'end')
    if current_widget == 'Enter Amount\n':
        amt_field.delete('1.0', "end") 

amt_field = tk.Text(height = 3, width = 16)
amt_field.grid(row=1, column=1, padx=10, pady=20)
amt_field.config(font=("Times New Roman", 11), bg='white', highlightthickness=2, highlightbackground='black', relief='flat')
amt_field.insert('end', "Enter Amount")
amt_field.bind("<FocusIn>", click)     #Binds the click function to the amt_field text widget
amt_field.tag_configure('center', justify = 'center')
amt_field.tag_add('center', '1.0', 'end')
    
currencies = ["USD", "GBP", "CAD", "EUR", "AUD", "INR", "JPY", "ZAR", "CHF", "NZD"]
    
from_menu = tk.StringVar(win)           #Keeps track of the current value of the menu
from_menu.set("Choose Currency")        #What the drop down menu shows in the beginning
f = tk.OptionMenu(win, from_menu, *currencies)
f.config(background='white', highlightthickness=2, highlightbackground='black', width=15, relief='flat')
f.grid(row=2, column=1, padx=50, pady=10)

to_menu = tk.StringVar(win)
to_menu.set("Choose Currency")
t = tk.OptionMenu(win, to_menu, *currencies)
t.config(background='white', highlightthickness=2, highlightbackground='black', width=15, relief='flat')
t.grid(row=2, column=3, padx=50, pady=10)
       
#Updates labels to show results of conversion or error messages
def update_label():
    try:
        if from_menu.get() == to_menu.get():
            if from_menu.get() == "Choose Currency":
                label.configure(text="No currency chosen", font=("Times New Roman", 16))
            elif amt_field.get('1.0', 'end') == "Enter Amount\n" or amt_field.get('1.0', 'end') == "\n":
                label.configure(text="Please enter valid amount", font=("Times New Roman", 12))
            else:
                label.configure(text=str(amt_field.get('1.0', 'end')), font=("Times New Roman", 24))
        else:     #Call convert function, passing values obtained from the text and OptionMenu widgets as parameters
            label.configure(text=str(convert(from_menu.get(), to_menu.get(), float(amt_field.get('1.0', 'end')))), font=("Times New Roman", 24))
    except ValueError:   #if the user enters a string or other invalid characters
        label.configure(text="Please enter valid amount", font=("Times New Roman", 12))
    except AttributeError:   #if a currency is not chosen in the OptionMenu
        label.configure(text="Please fill all fields", font=("Times New Roman", 12))        
        
     
    label.grid(row=1, column=3)
    
#Function that exchanges the value of the two OptionMenus
def interchange():
    a = from_menu.get()
    b = to_menu.get()
    from_menu.set(b)
    to_menu.set(a)
    update_label()
  
#Create Interchange button, which calls interchange function 
exchange_button = tk.Button(win, text="Interchange", command=interchange)
exchange_button.grid(row=2, column=2, padx=4, pady=4)
#cursor argument changes the cursor when it hovers over the Interchange button
exchange_button.config(bg='black', borderwidth=0, fg='white', height=2, width=9, cursor='exchange')

#Create Convert button, which calls update_label function 
convert_btn = tk.Button(win, text="Convert", command=update_label)
convert_btn.grid(row=3, column=2, padx=4, pady=4)
convert_btn.config(bg='black', borderwidth=0, fg='white', height=2, width=9)

#Creates the initial label that is shown
label = tk.Label(win, text="0")
label.config(font=("Times New Roman", 24), bg='white')
label.grid(row=1, column=3, padx=4, pady=4)
    
win.mainloop()