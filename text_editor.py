from tkinter import Tk,scrolledtext,Menu,filedialog,END,messagebox

import tkinter.scrolledtext as ScrolledText 
import mysql.connector
Editor_title="Untitled"
row_size=0
win=Tk(className=" Untitled")

#use you own database details 
mydb = mysql.connector.connect(host="Localhost",user="root",passwd="rishabh@123")
cursor = mydb.cursor()
cursor.execute("use MY_TEXT_EDITOR")

def Create_Table():
        global Editor_title,row_size
        x=Editor_title+"DT"
        y=Editor_title+"_Save"
        k="Create table {} (Sno int,data varchar(500))".format(Editor_title)
        j="Create table {} (Lineno int, data varchar(500))".format(y)
        l="Create table {} (File_Name varchar(30) , Date DATE,Time TIME )".format(x)
        cursor.execute(k)
        cursor.execute(j)
        cursor.execute(l)
        data=textArea.get('1.0',END+'-1c')
        k=data.split('\n')
        for i in k:
                row_size=row_size+1
                cursor.execute('insert into {} (Sno,data) values(%s,%s)'.format(Editor_title),(row_size,i))
                mydb.commit()
        print("data reached in first table")
        print(row_size)

def insert(data):
        global Editor_title,row_size
        data=textArea.get('1.0',END+'-1c')
        k=data.split('\n')
        name=Editor_title+"_Save"
        try:
                cursor.execute("select data from {}".format(Editor_title))
                previous_data=cursor.fetchall()
                #table1=len(k)
                #print(table1)
                #table2=len(previous_data)
                #print(table2)

                #for i in previous_data:
                #        print(i[0])
                ii=0 
                jj=0
                while(jj<len(previous_data) and ii<len(k)):
                        if previous_data[jj][0] != k[ii]:
                                cursor.execute('insert into {} (Lineno,data) values(%s,%s)'.format(name),(jj,previous_data[jj][0]))        
                                mydb.commit()
                                cursor.execute('update {} set data=%s where Sno=%s'.format(Editor_title),(k[ii],ii+1))

                                mydb.commit()
                        jj+=1
                        ii+=1
                while(jj<len(previous_data)):
                        cursor.execute('insert into {} (Lineno,data) values(%s,%s)'.format(name),(jj+1,previous_data[jj][0]))
                        mydb.commit()
                        del_query='Delete from {} where Sno={}'.format(Editor_title,jj)
                        cursor.execute(del_query)
                        mydb.commit()
                        jj+=1
                        if( jj== len(previous_data)-1):
                                del_query='Delete from {} where Sno={}'.format(Editor_title,jj)

                while(ii<len(k)):
                        cursor.execute('insert into {} (Sno,data) values(%s,%s)'.format(Editor_title),(ii+1,k[ii]))
                        mydb.commit()
                        ii+=1
                print("Data reached in second table")
        except:
                Create_Table()

# Text Area
textArea=ScrolledText.ScrolledText(win,width=600,height=1000)
textArea.pack()

def openFile():        
        global Editor_title,row_size
        file=filedialog.askopenfile(parent=win, mode='rb',title="Select a text file")
        name=file.name.split('/')
        Editor_title=name[-1]
        if file !=None:
                contents = file.read()
                textArea.delete('1.0', END)
                textArea.insert(END, contents)
                file.close()
        win.title(Editor_title)


def saveFile():
        global Editor_title,row_size
        file=filedialog.asksaveasfile(mode='w')
        name=file.name
        name=name.split('/')
        name=name[-1]
        Editor_title=name.split('.')
        Editor_title=Editor_title[0]
        if file!=None:
                data =textArea.get('1.0',END+'-1c')
                k=data.split('\n')
                file.write(data)
                file.close()
        insert(k)
        win.title(Editor_title)
                
def New():
        if len(textArea.get('1.0',END+'-1c')) >=0:
                if messagebox.askyesno("Save?","Do you want to save it"):
                        saveFile()
                else:
                        textArea.delete('1.0',END)
        win.title("Undefined")

def About():
        messagebox.showinfo("About","Text editor")

def Help():
        messagebox.showinfo("Help","There is nothing for you do it yourself")

def Exit():
        if messagebox.askyesno("Quit","Are you sure you want to Quit?"):
                win.destroy()

#MenuBar
menu = Menu(win)
win.config(menu=menu)
fileMenu = Menu(menu)
menu.add_cascade(label="File",menu=fileMenu)
fileMenu.add_command(label="New",command=New)
fileMenu.add_command(label="Open",command=openFile)
fileMenu.add_command(label="Save",command=saveFile)
fileMenu.add_command(label="Exit",command=Exit)

helpmenu = Menu(menu)
menu.add_command(label="Help",command=Help)
menu.add_command(label="About",command=About)

win.mainloop()
