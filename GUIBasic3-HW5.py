# GUIBasic3-HW5.py
from tkinter import *   #import * คือการ import package ทั้งหมดของ tkinter
from tkinter import ttk, messagebox  # ttk is theme ของ Tk
import csv
from datetime import datetime
import os.path

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย v.1.0 by tanavadee')    # กำหนด title ของ GUI
GUI.geometry('600x600+50+100')  #กำหนดความกว้างxสูง+ตำแหน่งจากซ้าย+ตำแหน่งจากด้านบน

# สร้างเมนูบาร์ให้โปรแกรม
menubar = Menu(GUI) 
GUI.config(menu=menubar) 

# File Menu
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File',menu=filemenu) # Add Menu เข้าไปใน Menubar
filemenu.add_command(label='Import CSV')    # Add SubMenu เข้าไปใน Menu File

# Help 
def About():
    print('About Menu')
    messagebox.showinfo('About','สวัสดี...............')

helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu) # Add Menu เข้าไปใน Menubar
helpmenu.add_command(label='About',command=About) 


# Donate 
donatemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemenu) # Add Menu เข้าไปใน Menubar


################################

# การใส่ Tab 
Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH,expand=1)    # fill คือการขยับให้เต็มพื้นที่ BOTH = ทั้งแกนXและY , expand = 1 คือการบอกให้ขยาย ใช้ร่วมกับ fill

T1pic = PhotoImage(file='expense.png').subsample(20)    # ใส่รูปภาพ ใช้เป็น .png ได้เท่านั้น .subsample เพื่อลดขนาดกี่เท่าจากขนาดรูปจริง
Tab.add(T1,text=f'{"Add Expense": ^50s}',image=T1pic,compound='top')    # f'{}' คือ การจัดให้ระยะห่างเท่ากัน, compound คือการจัดตำแหน่งของรูปภาพ

T2pic = PhotoImage(file='list.png').subsample(20)
Tab.add(T2,text=f'{"Expense List": ^50s}',image=T2pic,compound='top')


# GUI > Tab > T1 > F1 > Button
F1 = Frame(T1, width=500,height=500)                 # เอา Frame ไปแปะใน GUI หรือ ใน T1 (Tab)
F1.pack() #F1.place(x=130,y=10)

F2 = Frame(T2, width=500,height=500)
F2.pack() 


days = {'Mon':'จันทร์' ,
        'Tue':'อังคาร' ,
        'Wed':'พุธ' ,
        'Thu':'พฤหัส' ,
        'Fri':'ศุกร์' ,
        'Sat':'เสาร์' ,
        'Sun':'อาทิตย์'}

# Function Save
def Save(event=None):
    expense = v_expense.get()   # .get คือการดึงค่ามาจาก v_expense
    price = v_price.get()
    qty = v_qty.get()

    if expense == '':
        print('No Data')
        messagebox.showwarning('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
        return
    elif price == '':
        messagebox.showwarning('Error','กรุณากรอกข้อมูลราคา')
        return
    elif qty == '':
        qty = 1

    try:
        total = float(price)*float(qty)     #  ต้องแปลงเป็นfloat ก่อนนำมาคำนวณ

        today = datetime.now().strftime('%a')   # ต้องการรู้ว่าเป็นวันไหน
        dt = datetime.now().strftime('%Y-%m-%d-{} %H:%M:%S'.format(days[today]))   # กำหนดวันที่-เวลาปัจจุบัน และ กำหนด format วันที่

        print(dt)
        print('รายการ: {} ราคา {:,.2f} บาท'.format(expense,float(price)))
        print('จำนวน {} รวม {:,.2f} บาท'.format(qty,total))

        text = 'รายการ: {} ราคา {:,.2f} บาท\n'.format(expense,float(price))
        text = text + 'จำนวน {} รวม {:,.2f} บาท'.format(qty,total)
        v_result.set(text)

        # Clear ข้อมูลเก่า เป็นการกำหนดค่าให้ 
        v_expense.set('')
        v_price.set('')
        v_qty.set('')

        # บันทึกข้อมูลลง .csv อย่าลืม import csv ด้วย
        with open('savedata4.csv','a',encoding='utf-8',newline='') as f:
            # 'a' คือการเพิ่มข้อมูลต่อจากข้อมูลเก่า,​ 'w' คือการเขียนใหม่ตลอด
            # encoding='utf-8'เพื่อให้สามารถบันทึกภาษาไทยได้
            # newline='' คือทำให้ข้อมูลไม่มีบรรทัดว่าง
            fw = csv.writer(f)      # สร้าง function สำหรับเขียนข้อมูล
            data = [dt,expense,price,qty,str(total)]
            fw.writerow(data)

        E1.focus()      # ทำให้ cursor กลับไปช่องกรอก E1
        update_record()
        update_table()
    except Exception as e:
        print('Error')
        #messagebox.showwarning('ERROR','กรุณากรอกข้อมูลใหม่ \nคุณกรอกตัวเลขผิด')    # ชื่อpopup, ข้อความในpopup
        messagebox.showwarning('ERROR',e)
        v_expense.set('')
        v_price.set('')
        v_qty.set('')
    
# ทำให้สามารถกด Enter ได้
GUI.bind('<Return>',Save)   #ต้องเพิ่มใน def Save(event=None) ด้วย
# <Return> คือปุ่มEnter, Save คือชื่อFunction

# กำหนด Font Family (None หรือ Angsana New), ขนาด
FONT1 = (None,20)
FONT2 = ('Angsana New',14)

# รูปภาพ Background
bg = PhotoImage(file='wallet.png').subsample(6)     # ใส่รูปภาพ ใช้เป็น .png ได้เท่านั้น .subsample เพื่อลดขนาดกี่เท่าจากขนาดรูปจริง
walletpic = ttk.Label(F1,image=bg)
walletpic.pack (pady=20)

#------text1--------
L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1).pack() # การใส่ Label ข้อความ
v_expense = StringVar()
# StringVar() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT2)
E1.pack()
#-------------------
#------text2--------
L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1).pack() # การใส่ Label ข้อความ
v_price = StringVar()
# StringVar() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT2)
E2.pack()
#-------------------
#------text3--------
L = ttk.Label(F1,text='จำนวน (ชิ้น)',font=FONT1).pack() # การใส่ Label ข้อความ
v_qty = StringVar()
# StringVar() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E3 = ttk.Entry(F1,textvariable=v_qty,font=FONT2)
E3.pack()
#-------------------

savepic = PhotoImage(file='save.png').subsample(40)
B2 = ttk.Button(F1,text='บันทึก',image=savepic,command=Save,compound='left')   #ใช้ปุ่มของ ttk แปะไว้ที่ Frame F1, command คือการเรียกใช้ Function                       
B2.pack(ipadx=20,ipady=20,pady=10)  # ipadx, ipady คือ internal padding ส่วน padx,pady คือ padding ด้านนอก

# การใส่ Label แสดงผลลัพธ์
v_result = StringVar()
v_result.set('---------ผลลัพธ์---------')
result = ttk.Label(F1,textvariable=v_result,font=FONT1,foreground='yellow')
#result = Label(F1,textvariable=v_result,font=FONT1,fg='green')
result.pack(pady=20)

####################### TAB 2 ########################

def read_csv():
    # Function สำหรับอ่านไฟล์ .csv
    with open('savedata4.csv',newline='',encoding='utf-8') as f:   # Function with มีไว้สำหรับเปิดและปิดไฟล์
        # Mode 'a', 'w' ไม่ต้องใส่เพราะใช้กับ writer เท่านั้น
        # encoding='utf-8'เพื่อให้สามารถอ่านภาษาไทยได้
        # newline='' คือทำให้ข้อมูลไม่มีบรรทัดว่าง
        fr = csv.reader(f) # fr เป็นตัวแปร สำหรับ File reader
        data = list(fr)
    return data   # return data ออกมา

def update_record():
    getdata = read_csv()
    v_list.set('')
    text = ''
    for d in getdata:
        txt = '{}---{}---{}---{}---{}\n'.format(d[0],d[1],d[2],d[3],d[4])
        text = text + txt
    v_list.set(text)


# Tab 2 (T2) > Frame2 (F2)
v_list = StringVar()
v_list.set('All record')
elist = ttk.Label(F2,textvariable=v_list,font=FONT2,foreground='green')
elist.pack(pady=20)


L = ttk.Label(F2,text='ตารางแสดงผลลัพธ์ทั้งหมด',font=FONT1).pack() # การใส่ Label ข้อความ
# TreeView สร้าง Table 
header = ['วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']  # กำหนด Header ของตาราง
resultTable = ttk.Treeview(F2, columns=header,show='headings',height=10)  # height คือการกำหนดว่าให้แสดงกี่บรรทัด
resultTable.pack()

# การกำหนด Header ให้กับ Table
for hd in header:
    resultTable.heading(hd,text=hd)

# การกำหนดขนาดแต่ละ Column
headerwidth = [200,100,80,80,80]
for hd,W in zip(header,headerwidth):
    resultTable.column(hd,width=W)

#resultTable.insert('','end',value=['a','b',3,1,3]) # value คือชุดข้อมูลที่ต้องเท่ากับคอลัมน์

def update_table():
    resultTable.delete(*resultTable.get_children()) # * เป็นการสั่งให้ทำคำสั่งซ้ำบรรทัดนี้จนหมด
    # เทียบเท่า
    # for c in resulttable.get_children():
    #   resulttable.delete(c)

    getdata = read_csv()
    for rd in getdata:
        resultTable.insert('',0,value=[rd[0],rd[1],rd[2],rd[3],rd[4]])
        # value คือชุดข้อมูลที่ต้องเท่ากับคอลัมน์
        # 'end' คือให้ invsert ที่รายการสุดท้าย ถ้าจะให้แสดงรายการล่าสุดอยู่บรรทัดบนสุดให้ใส่ 0


update_table()
update_record()

GUI.mainloop()  # ต้องมีอยู่บรรทัดสุดท้ายเสมอ ใส่เพื่อให้โปรแกรม run ตลอดเวลา
