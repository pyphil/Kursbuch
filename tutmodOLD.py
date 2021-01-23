import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.scrollbarhelper import ScrollbarHelper
import calendar
import sqlite3


class Tutmod01App:
    def __init__(self, master=None):
        # build ui
        toplevel_1 = tk.Tk(master)
        frame_1 = ttk.Frame(toplevel_1)
        panedwindow_2 = ttk.Panedwindow(frame_1, orient='horizontal')
        frame_4 = ttk.Frame(panedwindow_2)
        labelframe_1 = ttk.Labelframe(frame_4)
        combobox_1 = ttk.Combobox(labelframe_1)
        combobox_1.pack(fill='x', side='top')
        labelframe_1.config(height='100', padding='5', text='Klasse')
        labelframe_1.pack(fill='x', side='top')
        space1 = ttk.Frame(frame_4)
        space1.config(height='8', width='200')
        space1.pack(side='top')
        labelframe_2 = ttk.Labelframe(frame_4)
        scrollbarhelper_1 = ScrollbarHelper(labelframe_2, scrolltype='both')
        treeview_2 = ttk.Treeview(scrollbarhelper_1.container)
        self.img_ = tk.PhotoImage(file='')
        self.img_ = tk.PhotoImage(file='')
        treeview_2_cols = ['column_2']
        treeview_2_dcols = ['column_2']
        treeview_2.configure(columns=treeview_2_cols, displaycolumns=treeview_2_dcols)
        treeview_2.column('#0', anchor='w',stretch='true',width='10',minwidth='10')
        treeview_2.column('column_2', anchor='w',stretch='true',width='200',minwidth='20')
        treeview_2.heading('#0', anchor='w',image=self.img_,text='Nr.')
        treeview_2.heading('column_2', anchor='w',image=self.img_,text='Name')
        treeview_2.pack(expand='true', fill='both', side='top')
        scrollbarhelper_1.add_child(treeview_2)
        # TODO - scrollbarhelper_1: code for custom option 'usemousewheel' not implemented.
        scrollbarhelper_1.pack(expand='true', fill='both', side='top')
        labelframe_2.config(height='200', padding='5', text='Schüler*innen', width='200')
        labelframe_2.pack(expand='true', fill='both', side='top')
        frame_4.pack(expand='true', fill='both', side='top')
        panedwindow_2.add(frame_4, weight='1')
        labelframe_3 = ttk.Labelframe(panedwindow_2)
        frame_6 = ttk.Frame(labelframe_3)
        self.label_top = ttk.Label(frame_6)
        self.label_top.config(font='{Segoe UI} 12 {bold}', padding='20', text='Fehlzeiten von ...')
        self.label_top.pack(side='top')
        frame_7 = ttk.Frame(frame_6)
        label_Jahr = ttk.Label(frame_7)
        label_Jahr.config(text='Jahr: ')
        label_Jahr.pack(side='left')
        self.combo_jahr = ttk.Combobox(frame_7)
        self.combo_jahr.config(values='"2020" "2021" "2022" "2023"', width='5')
        self.combo_jahr.pack(side='left')
        frame_8 = ttk.Frame(frame_7)
        frame_8.config(height='20', width='20')
        frame_8.pack(side='left')
        label_Monat = ttk.Label(frame_7)
        label_Monat.config(text='Monat: ')
        label_Monat.pack(side='left')
        self.combo_monat = ttk.Combobox(frame_7)
        self.combo_monat.config(values='"Januar" "Februar" "März" "April" "Mai" "Juni" "Juli" "August" "September" "Oktober" "November" "Dezember"', width='12')
        self.combo_monat.pack(side='left')
        frame_8_1 = ttk.Frame(frame_7)
        frame_8_1.config(height='20', width='20')
        frame_8_1.pack(side='left')
        self.button_month = ttk.Button(frame_7)
        self.button_month.config(text='OK', width='5')
        self.button_month.pack(side='top')
        self.button_month.configure(command=self.setMonth)
        frame_7.config(height='200', padding='10', width='200')
        frame_7.pack(side='top')
        frame_6.config(height='200', width='200')
        frame_6.pack(side='top')
        frame_9 = ttk.Frame(labelframe_3)
        button_weekbefore = tk.Button(frame_9)
        button_weekbefore.config(font='{Segoe UI Black} 16 {}', padx='5', relief='flat', text='◄')
        button_weekbefore.pack(padx='5', pady='5', side='left')
        button_weekbefore.configure(command=self.weekbefore)
        self.label_Woche = ttk.Label(frame_9)
        self.label_Woche.config(anchor='center', font='{Segoe UI} 10 {bold}', text='Woche vom 24.12. bis 24.12.', width='25')
        self.label_Woche.pack(padx='5', side='left')
        button_weekafter = tk.Button(frame_9)
        button_weekafter.config(font='{Segoe UI} 16 {}', padx='5', relief='flat', text='►')
        button_weekafter.pack(ipadx='2', padx='5', pady='5', side='left')
        button_weekafter.configure(command=self.weekafter)
        frame_9.config(height='80', width='500')
        frame_9.pack(side='top')
        frame_11 = ttk.Frame(labelframe_3)
        frame_1_2 = ttk.Frame(frame_11)
        label_Std = ttk.Label(frame_1_2)
        label_Std.config(text='Std.')
        label_Std.grid(padx='30', row='0')
        label_Std.rowconfigure('0', minsize='0', pad='0', uniform='None', weight='0')
        label_Std.columnconfigure('0', minsize='0')
        label_Mo = ttk.Label(frame_1_2)
        label_Mo.config(justify='center', text='Mo')
        label_Mo.grid(column='1', padx='5', row='0', sticky='n')
        label_Mo.rowconfigure('0', minsize='0', pad='0', uniform='None', weight='0')
        label_Mo.columnconfigure('1', minsize='0', pad='0')
        label_Mo.columnconfigure('5', minsize='50')
        self.label_Mo_date = ttk.Label(frame_1_2)
        self.label_Mo_date.config(anchor='center', justify='center', text='--', width='5')
        self.label_Mo_date.grid(column='1', padx='5', row='0', sticky='s')
        label_Di = ttk.Label(frame_1_2)
        label_Di.config(justify='center', text='Di', wraplength='40')
        label_Di.grid(column='2', padx='5', row='0', sticky='n')
        label_Di.rowconfigure('0', minsize='0', pad='0', uniform='None', weight='0')
        label_Di.columnconfigure('2', minsize='0')
        self.label_Di_date = ttk.Label(frame_1_2)
        self.label_Di_date.config(anchor='center', justify='center', text='--', width='5')
        self.label_Di_date.grid(column='2', row='0', sticky='s')
        label_Mi = ttk.Label(frame_1_2)
        label_Mi.config(justify='center', text='Mi')
        label_Mi.grid(column='3', padx='5', row='0', sticky='n')
        label_Mi.rowconfigure('0', minsize='0', pad='0', uniform='None', weight='0')
        label_Mi.columnconfigure('3', minsize='0')
        self.label_Mi_date = ttk.Label(frame_1_2)
        self.label_Mi_date.config(anchor='center', justify='center', text='--', width='5')
        self.label_Mi_date.grid(column='3', row='0', sticky='s')
        label_Do = ttk.Label(frame_1_2)
        label_Do.config(justify='center', text='Do', wraplength='40')
        label_Do.grid(column='4', padx='5', row='0', sticky='n')
        label_Do.rowconfigure('0', minsize='0', pad='0', uniform='None', weight='0')
        label_Do.columnconfigure('4', minsize='0')
        self.label_Do_date = ttk.Label(frame_1_2)
        self.label_Do_date.config(anchor='center', justify='center', text='--', width='5')
        self.label_Do_date.grid(column='4', row='0', sticky='s')
        label_Fr = ttk.Label(frame_1_2)
        label_Fr.config(justify='center', text='Fr\n')
        label_Fr.grid(column='5', padx='5', row='0', sticky='n')
        label_Fr.rowconfigure('0', minsize='0', pad='0', uniform='None', weight='0')
        label_Fr.columnconfigure('4', minsize='0')
        self.label_Fr_date = ttk.Label(frame_1_2)
        self.label_Fr_date.config(anchor='center', justify='center', text='--', width='5')
        self.label_Fr_date.grid(column='5', row='0', sticky='s')
        label_1Std = ttk.Label(frame_1_2)
        label_1Std.config(text='1')
        label_1Std.grid(column='0', pady='5', row='1')
        label_1Std.rowconfigure('1', pad='0')
        label_1Std.columnconfigure('0', minsize='0')
        self.button1_1 = tk.Button(frame_1_2)
        self.button1_1.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button1_1.grid(column='1', pady='5', row='1')
        self.button1_1.rowconfigure('1', pad='0')
        self.button1_1.columnconfigure('1', minsize='0', pad='0')
        self.button1_1.columnconfigure('5', minsize='50')
        self.button1_1.configure(command=self.set1_1)
        self.button1_2 = tk.Button(frame_1_2)
        self.button1_2.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button1_2.grid(column='2', padx='5', row='1')
        self.button1_2.rowconfigure('1', pad='0')
        self.button1_2.columnconfigure('2', minsize='0')
        self.button1_2.configure(command=self.set1_2)
        self.button1_3 = tk.Button(frame_1_2)
        self.button1_3.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button1_3.grid(column='3', padx='5', row='1')
        self.button1_3.rowconfigure('1', pad='0')
        self.button1_3.columnconfigure('3', minsize='0')
        self.button1_3.configure(command=self.set1_3)
        self.button1_4 = tk.Button(frame_1_2)
        self.button1_4.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button1_4.grid(column='4', padx='5', row='1')
        self.button1_4.rowconfigure('1', pad='0')
        self.button1_4.columnconfigure('4', minsize='0')
        self.button1_4.configure(command=self.set1_4)
        self.button1_5 = tk.Button(frame_1_2)
        self.button1_5.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button1_5.grid(column='5', padx='5', row='1')
        self.button1_5.rowconfigure('1', pad='0')
        self.button1_5.columnconfigure('5', minsize='0', pad='0', uniform='None', weight='0')
        self.button1_5.configure(command=self.set1_5)
        label_2Std = ttk.Label(frame_1_2)
        label_2Std.config(text='2')
        label_2Std.grid(column='0', row='2')
        label_2Std.rowconfigure('1', pad='10')
        label_2Std.rowconfigure('2', pad='0')
        label_2Std.columnconfigure('0', minsize='0')
        self.button2_1 = tk.Button(frame_1_2)
        self.button2_1.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button2_1.grid(column='1', pady='5', row='2')
        self.button2_1.rowconfigure('1', pad='10')
        self.button2_1.rowconfigure('2', pad='0')
        self.button2_1.columnconfigure('1', minsize='0', pad='0')
        self.button2_1.columnconfigure('5', minsize='50')
        self.button2_1.configure(command=self.set2_1)
        self.button2_2 = tk.Button(frame_1_2)
        self.button2_2.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button2_2.grid(column='2', pady='5', row='2')
        self.button2_2.rowconfigure('1', pad='10')
        self.button2_2.rowconfigure('2', pad='0')
        self.button2_2.columnconfigure('1', minsize='0', pad='0')
        self.button2_2.columnconfigure('5', minsize='50')
        self.button2_2.configure(command=self.set2_2)
        self.button2_3 = tk.Button(frame_1_2)
        self.button2_3.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button2_3.grid(column='3', pady='5', row='2')
        self.button2_3.rowconfigure('1', pad='10')
        self.button2_3.rowconfigure('2', pad='0')
        self.button2_3.columnconfigure('1', minsize='0', pad='0')
        self.button2_3.columnconfigure('5', minsize='50')
        self.button2_3.configure(command=self.set2_3)
        self.button2_4 = tk.Button(frame_1_2)
        self.button2_4.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button2_4.grid(column='4', pady='5', row='2')
        self.button2_4.rowconfigure('1', pad='10')
        self.button2_4.rowconfigure('2', pad='0')
        self.button2_4.columnconfigure('1', minsize='0', pad='0')
        self.button2_4.columnconfigure('5', minsize='50')
        self.button2_4.configure(command=self.set2_4)
        self.button2_5 = tk.Button(frame_1_2)
        self.button2_5.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button2_5.grid(column='5', pady='5', row='2')
        self.button2_5.rowconfigure('1', pad='10')
        self.button2_5.rowconfigure('2', pad='0')
        self.button2_5.columnconfigure('1', minsize='0', pad='0')
        self.button2_5.columnconfigure('5', minsize='50')
        self.button2_5.configure(command=self.set2_5)
        label_3Std = ttk.Label(frame_1_2)
        label_3Std.config(text='3')
        label_3Std.grid(column='0', row='3')
        label_3Std.rowconfigure('1', pad='10')
        label_3Std.rowconfigure('3', pad='0')
        label_3Std.columnconfigure('0', minsize='0')
        self.button3_1 = tk.Button(frame_1_2)
        self.button3_1.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button3_1.grid(column='1', pady='5', row='3')
        self.button3_1.rowconfigure('1', pad='10')
        self.button3_1.rowconfigure('3', pad='0')
        self.button3_1.columnconfigure('1', minsize='0', pad='0')
        self.button3_1.columnconfigure('5', minsize='50')
        self.button3_1.configure(command=self.set3_1)
        self.button3_2 = tk.Button(frame_1_2)
        self.button3_2.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button3_2.grid(column='2', pady='5', row='3')
        self.button3_2.rowconfigure('1', pad='10')
        self.button3_2.rowconfigure('3', pad='0')
        self.button3_2.columnconfigure('1', minsize='0', pad='0')
        self.button3_2.columnconfigure('5', minsize='50')
        self.button3_2.configure(command=self.set3_2)
        self.button3_3 = tk.Button(frame_1_2)
        self.button3_3.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button3_3.grid(column='3', pady='5', row='3')
        self.button3_3.rowconfigure('1', pad='10')
        self.button3_3.rowconfigure('3', pad='0')
        self.button3_3.columnconfigure('1', minsize='0', pad='0')
        self.button3_3.columnconfigure('5', minsize='50')
        self.button3_3.configure(command=self.set3_3)
        self.button3_4 = tk.Button(frame_1_2)
        self.button3_4.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button3_4.grid(column='4', pady='5', row='3')
        self.button3_4.rowconfigure('1', pad='10')
        self.button3_4.rowconfigure('3', pad='0')
        self.button3_4.columnconfigure('1', minsize='0', pad='0')
        self.button3_4.columnconfigure('5', minsize='50')
        self.button3_4.configure(command=self.set3_4)
        self.button3_5 = tk.Button(frame_1_2)
        self.button3_5.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button3_5.grid(column='5', pady='5', row='3')
        self.button3_5.rowconfigure('1', pad='10')
        self.button3_5.rowconfigure('3', pad='0')
        self.button3_5.columnconfigure('1', minsize='0', pad='0')
        self.button3_5.columnconfigure('5', minsize='50')
        self.button3_5.configure(command=self.set3_5)
        label_4Std = ttk.Label(frame_1_2)
        label_4Std.config(text='4')
        label_4Std.grid(column='0', row='4')
        label_4Std.rowconfigure('1', pad='10')
        label_4Std.rowconfigure('3', pad='10')
        label_4Std.rowconfigure('4', pad='0')
        label_4Std.columnconfigure('0', minsize='0')
        label_5Std = ttk.Label(frame_1_2)
        label_5Std.config(text='5')
        label_5Std.grid(column='0', row='5')
        label_5Std.rowconfigure('1', pad='10')
        label_5Std.rowconfigure('3', pad='10')
        label_5Std.rowconfigure('5', pad='0')
        label_5Std.columnconfigure('0', minsize='0')
        label_6Std = ttk.Label(frame_1_2)
        label_6Std.config(text='6')
        label_6Std.grid(column='0', row='6')
        label_6Std.rowconfigure('1', pad='10')
        label_6Std.rowconfigure('3', pad='10')
        label_6Std.rowconfigure('6', pad='0')
        label_6Std.columnconfigure('0', minsize='0')
        label_7Std = ttk.Label(frame_1_2)
        label_7Std.config(text='7')
        label_7Std.grid(column='0', row='7')
        label_7Std.rowconfigure('1', pad='10')
        label_7Std.rowconfigure('3', pad='10')
        label_7Std.rowconfigure('7', pad='0')
        label_7Std.columnconfigure('0', minsize='0')
        self.button4_1 = tk.Button(frame_1_2)
        self.button4_1.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button4_1.grid(column='1', pady='5', row='4')
        self.button4_1.rowconfigure('1', pad='10')
        self.button4_1.rowconfigure('3', pad='10')
        self.button4_1.rowconfigure('4', pad='0')
        self.button4_1.columnconfigure('1', minsize='0', pad='0')
        self.button4_1.columnconfigure('5', minsize='50')
        self.button4_1.configure(command=self.set4_1)
        self.button4_2 = tk.Button(frame_1_2)
        self.button4_2.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button4_2.grid(column='2', pady='5', row='4')
        self.button4_2.rowconfigure('1', pad='10')
        self.button4_2.rowconfigure('3', pad='10')
        self.button4_2.rowconfigure('4', pad='0')
        self.button4_2.columnconfigure('1', minsize='0', pad='0')
        self.button4_2.columnconfigure('5', minsize='50')
        self.button4_2.configure(command=self.set4_2)
        self.button4_3 = tk.Button(frame_1_2)
        self.button4_3.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button4_3.grid(column='3', pady='5', row='4')
        self.button4_3.rowconfigure('1', pad='10')
        self.button4_3.rowconfigure('3', pad='10')
        self.button4_3.rowconfigure('4', pad='0')
        self.button4_3.columnconfigure('1', minsize='0', pad='0')
        self.button4_3.columnconfigure('5', minsize='50')
        self.button4_3.configure(command=self.set4_3)
        self.button4_4 = tk.Button(frame_1_2)
        self.button4_4.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button4_4.grid(column='4', pady='5', row='4')
        self.button4_4.rowconfigure('1', pad='10')
        self.button4_4.rowconfigure('3', pad='10')
        self.button4_4.rowconfigure('4', pad='0')
        self.button4_4.columnconfigure('1', minsize='0', pad='0')
        self.button4_4.columnconfigure('5', minsize='50')
        self.button4_4.configure(command=self.set4_4)
        self.button4_5 = tk.Button(frame_1_2)
        self.button4_5.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button4_5.grid(column='5', pady='5', row='4')
        self.button4_5.rowconfigure('1', pad='10')
        self.button4_5.rowconfigure('3', pad='10')
        self.button4_5.rowconfigure('4', pad='0')
        self.button4_5.columnconfigure('1', minsize='0', pad='0')
        self.button4_5.columnconfigure('5', minsize='50')
        self.button4_5.configure(command=self.set4_5)
        self.button5_1 = tk.Button(frame_1_2)
        self.button5_1.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button5_1.grid(column='1', pady='5', row='5')
        self.button5_1.rowconfigure('1', pad='10')
        self.button5_1.rowconfigure('3', pad='10')
        self.button5_1.rowconfigure('5', pad='0')
        self.button5_1.columnconfigure('1', minsize='0', pad='0')
        self.button5_1.columnconfigure('5', minsize='50')
        self.button5_1.configure(command=self.set5_1)
        self.button5_2 = tk.Button(frame_1_2)
        self.button5_2.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button5_2.grid(column='2', pady='5', row='5')
        self.button5_2.rowconfigure('1', pad='10')
        self.button5_2.rowconfigure('3', pad='10')
        self.button5_2.rowconfigure('5', pad='0')
        self.button5_2.columnconfigure('1', minsize='0', pad='0')
        self.button5_2.columnconfigure('5', minsize='50')
        self.button5_2.configure(command=self.set5_2)
        self.button5_3 = tk.Button(frame_1_2)
        self.button5_3.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button5_3.grid(column='3', pady='5', row='5')
        self.button5_3.rowconfigure('1', pad='10')
        self.button5_3.rowconfigure('3', pad='10')
        self.button5_3.rowconfigure('5', pad='0')
        self.button5_3.columnconfigure('1', minsize='0', pad='0')
        self.button5_3.columnconfigure('5', minsize='50')
        self.button5_3.configure(command=self.set5_3)
        self.button5_4 = tk.Button(frame_1_2)
        self.button5_4.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button5_4.grid(column='4', pady='5', row='5')
        self.button5_4.rowconfigure('1', pad='10')
        self.button5_4.rowconfigure('3', pad='10')
        self.button5_4.rowconfigure('5', pad='0')
        self.button5_4.columnconfigure('1', minsize='0', pad='0')
        self.button5_4.columnconfigure('5', minsize='50')
        self.button5_4.configure(command=self.set5_4)
        self.button5_5 = tk.Button(frame_1_2)
        self.button5_5.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button5_5.grid(column='5', pady='5', row='5')
        self.button5_5.rowconfigure('1', pad='10')
        self.button5_5.rowconfigure('3', pad='10')
        self.button5_5.rowconfigure('5', pad='0')
        self.button5_5.columnconfigure('1', minsize='0', pad='0')
        self.button5_5.columnconfigure('5', minsize='50')
        self.button5_5.configure(command=self.set5_5)
        self.button6_1 = tk.Button(frame_1_2)
        self.button6_1.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button6_1.grid(column='1', pady='5', row='6')
        self.button6_1.rowconfigure('1', pad='10')
        self.button6_1.rowconfigure('3', pad='10')
        self.button6_1.rowconfigure('6', pad='0')
        self.button6_1.columnconfigure('1', minsize='0', pad='0')
        self.button6_1.columnconfigure('5', minsize='50')
        self.button6_1.configure(command=self.set6_1)
        self.button6_2 = tk.Button(frame_1_2)
        self.button6_2.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button6_2.grid(column='2', pady='5', row='6')
        self.button6_2.rowconfigure('1', pad='10')
        self.button6_2.rowconfigure('3', pad='10')
        self.button6_2.rowconfigure('6', pad='0')
        self.button6_2.columnconfigure('1', minsize='0', pad='0')
        self.button6_2.columnconfigure('5', minsize='50')
        self.button6_2.configure(command=self.set6_2)
        self.button6_3 = tk.Button(frame_1_2)
        self.button6_3.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button6_3.grid(column='3', pady='5', row='6')
        self.button6_3.rowconfigure('1', pad='10')
        self.button6_3.rowconfigure('3', pad='10')
        self.button6_3.rowconfigure('6', pad='0')
        self.button6_3.columnconfigure('1', minsize='0', pad='0')
        self.button6_3.columnconfigure('5', minsize='50')
        self.button6_3.configure(command=self.set6_3)
        self.button6_4 = tk.Button(frame_1_2)
        self.button6_4.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button6_4.grid(column='4', pady='5', row='6')
        self.button6_4.rowconfigure('1', pad='10')
        self.button6_4.rowconfigure('3', pad='10')
        self.button6_4.rowconfigure('6', pad='0')
        self.button6_4.columnconfigure('1', minsize='0', pad='0')
        self.button6_4.columnconfigure('5', minsize='50')
        self.button6_4.configure(command=self.set6_4)
        self.button6_5 = tk.Button(frame_1_2)
        self.button6_5.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button6_5.grid(column='5', pady='5', row='6')
        self.button6_5.rowconfigure('1', pad='10')
        self.button6_5.rowconfigure('3', pad='10')
        self.button6_5.rowconfigure('6', pad='0')
        self.button6_5.columnconfigure('1', minsize='0', pad='0')
        self.button6_5.columnconfigure('5', minsize='50')
        self.button6_5.configure(command=self.set6_5)
        self.button7_1 = tk.Button(frame_1_2)
        self.button7_1.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button7_1.grid(column='1', pady='5', row='7')
        self.button7_1.rowconfigure('1', pad='10')
        self.button7_1.rowconfigure('3', pad='10')
        self.button7_1.rowconfigure('7', pad='0')
        self.button7_1.columnconfigure('1', minsize='0', pad='0')
        self.button7_1.columnconfigure('5', minsize='50')
        self.button7_1.configure(command=self.set7_1)
        self.button7_2 = tk.Button(frame_1_2)
        self.button7_2.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button7_2.grid(column='2', pady='5', row='7')
        self.button7_2.rowconfigure('1', pad='10')
        self.button7_2.rowconfigure('3', pad='10')
        self.button7_2.rowconfigure('7', pad='0')
        self.button7_2.columnconfigure('1', minsize='0', pad='0')
        self.button7_2.columnconfigure('5', minsize='50')
        self.button7_2.configure(command=self.set7_2)
        self.button7_3 = tk.Button(frame_1_2)
        self.button7_3.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button7_3.grid(column='3', pady='5', row='7')
        self.button7_3.rowconfigure('1', pad='10')
        self.button7_3.rowconfigure('3', pad='10')
        self.button7_3.rowconfigure('7', pad='0')
        self.button7_3.columnconfigure('1', minsize='0', pad='0')
        self.button7_3.columnconfigure('5', minsize='50')
        self.button7_3.configure(command=self.set7_3)
        self.button7_4 = tk.Button(frame_1_2)
        self.button7_4.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button7_4.grid(column='4', pady='5', row='7')
        self.button7_4.rowconfigure('1', pad='10')
        self.button7_4.rowconfigure('3', pad='10')
        self.button7_4.rowconfigure('7', pad='0')
        self.button7_4.columnconfigure('1', minsize='0', pad='0')
        self.button7_4.columnconfigure('5', minsize='50')
        self.button7_4.configure(command=self.set7_4)
        self.button7_5 = tk.Button(frame_1_2)
        self.button7_5.config(background='#c0c0c0', justify='left', relief='groove', width='3')
        self.button7_5.grid(column='5', pady='5', row='7')
        self.button7_5.rowconfigure('1', pad='10')
        self.button7_5.rowconfigure('3', pad='10')
        self.button7_5.rowconfigure('7', pad='0')
        self.button7_5.columnconfigure('1', minsize='0', pad='0')
        self.button7_5.columnconfigure('5', minsize='50')
        self.button7_5.configure(command=self.set7_5)
        frame_1_2.config(height='200', width='200')
        frame_1_2.pack(side='left')
        abstand2 = ttk.Frame(frame_11)
        abstand2.config(height='200', width='30')
        abstand2.pack()
        frame_11.config(height='200', width='200')
        frame_11.pack(side='top')
        labelframe_3.config(height='200', text='Fehlzeiten', width='200')
        labelframe_3.pack(side='top')
        panedwindow_2.add(labelframe_3, weight='5')
        panedwindow_2.config(height='200', width='200')
        panedwindow_2.pack(expand='true', fill='both', side='top')
        frame_1.config(padding='5')
        frame_1.pack(expand='true', fill='both', side='top')
        toplevel_1.config(height='670', width='790')
        toplevel_1.geometry('790x670')
        toplevel_1.title('Tutorenmodus')

        # Main widget
        self.mainwindow = toplevel_1


    def setMonth(self):
        y = int(self.combo_jahr.get())
        self.m = int(self.combo_monat.current()+1)

        cal = calendar.Calendar()

        self.weeks = []

        for week in cal.monthdatescalendar(y,self.m):
            z = 1
            oneweek = []
            for date in week:
                if z <= 5:
                    #print(d)
                    oneweek.append(str(date))
                z += 1
            self.weeks.append(oneweek)
        self.weekno = -1
        self.weekafter()


    def weekbefore(self):
        self.resetButtons()
        self.weekno -= 1
        self.label_Woche.config(text=self.weeks[self.weekno][0].split("-")[2]+"."+self.weeks[self.weekno][0].split("-")[1]+"."+" bis "+self.weeks[self.weekno][4].split("-")[2]+"."+self.weeks[self.weekno][4].split("-")[1]+".")
        self.label_Mo_date.config(text=self.weeks[self.weekno][0].split("-")[2]+"."+self.weeks[self.weekno][0].split("-")[1]+".")
        self.label_Di_date.config(text=self.weeks[self.weekno][1].split("-")[2]+"."+self.weeks[self.weekno][1].split("-")[1]+".")
        self.label_Mi_date.config(text=self.weeks[self.weekno][2].split("-")[2]+"."+self.weeks[self.weekno][2].split("-")[1]+".")
        self.label_Do_date.config(text=self.weeks[self.weekno][3].split("-")[2]+"."+self.weeks[self.weekno][3].split("-")[1]+".")
        self.label_Fr_date.config(text=self.weeks[self.weekno][4].split("-")[2]+"."+self.weeks[self.weekno][4].split("-")[1]+".")

        self.set_fehlzeiten()

    def weekafter(self):
        self.resetButtons()
        self.weekno += 1
    
        if self.m != int(self.weeks[self.weekno][4].split("-")[1]):
            self.weekno += 1
        self.label_Woche.config(text=self.weeks[self.weekno][0].split("-")[2]+"."+self.weeks[self.weekno][0].split("-")[1]+"."+" bis "+self.weeks[self.weekno][4].split("-")[2]+"."+self.weeks[self.weekno][4].split("-")[1]+".")
        self.label_Mo_date.config(text=self.weeks[self.weekno][0].split("-")[2]+"."+self.weeks[self.weekno][0].split("-")[1]+".")
        self.label_Di_date.config(text=self.weeks[self.weekno][1].split("-")[2]+"."+self.weeks[self.weekno][1].split("-")[1]+".")
        self.label_Mi_date.config(text=self.weeks[self.weekno][2].split("-")[2]+"."+self.weeks[self.weekno][2].split("-")[1]+".")
        self.label_Do_date.config(text=self.weeks[self.weekno][3].split("-")[2]+"."+self.weeks[self.weekno][3].split("-")[1]+".")
        self.label_Fr_date.config(text=self.weeks[self.weekno][4].split("-")[2]+"."+self.weeks[self.weekno][4].split("-")[1]+".")

        self.set_fehlzeiten()

    def set_fehlzeiten(self):
        """Führt alle set-Methoden aus, indem vorher die Liste aus der db
        geholt wird und den Methoden u oder e oder ""? übergeben wird """
        # TODO Schüler-pk übergeben
        self.student_pk = 1

        # DB-Verbindung
        verbindung = sqlite3.connect("kurs.db")
        c = verbindung.cursor()

        # Liste generieren (wenn es das Datum+Std nicht gibt gibt sqlite das
        # Datum selbst zurück)
        setlist = []
        self.datelistweek = []

        for i in self.weeks[self.weekno]:
            fehlzlist = []
            datelist = []
            datelist.append('"'+i+"_1"'"')
            datelist.append('"'+i+"_2"'"')
            datelist.append('"'+i+"_3"'"')
            datelist.append('"'+i+"_4"'"')
            datelist.append('"'+i+"_5"'"')
            datelist.append('"'+i+"_6"'"')
            datelist.append('"'+i+"_7"'"')
            self.datelistweek.append(datelist)
            for d in datelist:
                item = list(c.execute("""SELECT """+d+""" 
                                                FROM "sus"
                                                WHERE pk = ?;
                                            """,
                                            (self.student_pk,)))
                fehlzlist.append(item)
            
            setlist.append(fehlzlist)
        
        # DB-Verindung schließen
        c.close()
        verbindung.close()
        
        #print(setlist[0][0][0][0])
        print(self.datelistweek)
        
        # set-Methoden aufrufen

        self.set1_1(setlist[0][0][0][0])
        self.set1_2(setlist[1][0][0][0])
        self.set1_3(setlist[2][0][0][0])
        self.set1_4(setlist[3][0][0][0])
        self.set1_5(setlist[4][0][0][0])
       
        self.set2_1(setlist[0][1][0][0])
        self.set2_2(setlist[1][1][0][0])
        self.set2_3(setlist[2][1][0][0])
        self.set2_4(setlist[3][1][0][0])
        self.set2_5(setlist[4][1][0][0])

        self.set3_1(setlist[0][2][0][0])
        self.set3_2(setlist[1][2][0][0])
        self.set3_3(setlist[2][2][0][0])
        self.set3_4(setlist[3][2][0][0])
        self.set3_5(setlist[4][2][0][0])

        self.set4_1(setlist[0][3][0][0])
        self.set4_2(setlist[1][3][0][0])
        self.set4_3(setlist[2][3][0][0])
        self.set4_4(setlist[3][3][0][0])
        self.set4_5(setlist[4][3][0][0])

        self.set5_1(setlist[0][4][0][0])
        self.set5_2(setlist[1][4][0][0])
        self.set5_3(setlist[2][4][0][0])
        self.set5_4(setlist[3][4][0][0])
        self.set5_5(setlist[4][4][0][0])

        self.set6_1(setlist[0][5][0][0])
        self.set6_2(setlist[1][5][0][0])
        self.set6_3(setlist[2][5][0][0])
        self.set6_4(setlist[3][5][0][0])
        self.set6_5(setlist[4][5][0][0])

        self.set7_1(setlist[0][6][0][0])
        self.set7_2(setlist[1][6][0][0])
        self.set7_3(setlist[2][6][0][0])
        self.set7_4(setlist[3][6][0][0])
        self.set7_5(setlist[4][6][0][0])


    def set1_1(self, val=None):
        if val == None:
            if self.button1_1.config('text')[4] == '':
                self.button1_1.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[0][0],1)
            elif self.button1_1.config('text')[4] == 'u':
                self.button1_1.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[0][0],2)
            elif self.button1_1.config('text')[4] == 'e':
                self.button1_1.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[0][0],3)
            elif self.button1_1.config('text')[4] == 'S':
                self.button1_1.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[0][0],0)
        else:
            if val == 1:
                self.button1_1.config(background='#f5010a', text='u')
            if val == 2:
                self.button1_1.config(background='#00e100', text='e')
            if val == 3:
                self.button1_1.config(background='#ffff80', text='S')
            else:
                pass
    def set1_2(self, val=None):
        if val == None:
            if self.button1_2.config('text')[4] == '':
                self.button1_2.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[1][0],1)
            elif self.button1_2.config('text')[4] == 'u':
                self.button1_2.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[1][0],2)
            elif self.button1_2.config('text')[4] == 'e':
                self.button1_2.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[1][0],3)
            elif self.button1_2.config('text')[4] == 'S':
                self.button1_2.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[1][0],0)
        else:
            if val == 1:
                self.button1_2.config(background='#f5010a', text='u')
            if val == 2:
                self.button1_2.config(background='#00e100', text='e')
            if val == 3:
                self.button1_2.config(background='#ffff80', text='S')
            else:
                pass                   
    def set1_3(self, val=None):
        if val == None:
            if self.button1_3.config('text')[4] == '':
                self.button1_3.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[2][0],1)
            elif self.button1_3.config('text')[4] == 'u':
                self.button1_3.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[2][0],2)
            elif self.button1_3.config('text')[4] == 'e':
                self.button1_3.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[2][0],3)
            elif self.button1_3.config('text')[4] == 'S':
                self.button1_3.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[2][0],0)
        else:
            if val == 1:
                self.button1_3.config(background='#f5010a', text='u')
            if val == 2:
                self.button1_3.config(background='#00e100', text='e')
            if val == 3:
                self.button1_3.config(background='#ffff80', text='S')
            else:
                pass                   
    def set1_4(self, val=None):
        if val == None:
            if self.button1_4.config('text')[4] == '':
                self.button1_4.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[3][0],1)
            elif self.button1_4.config('text')[4] == 'u':
                self.button1_4.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[3][0],2)
            elif self.button1_4.config('text')[4] == 'e':
                self.button1_4.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[3][0],3)
            elif self.button1_4.config('text')[4] == 'S':
                self.button1_4.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[3][0],0)
        else:
            if val == 1:
                self.button1_4.config(background='#f5010a', text='u')
            if val == 2:
                self.button1_4.config(background='#00e100', text='e')
            if val == 3:
                self.button1_4.config(background='#ffff80', text='S')
            else:
                pass                   
    def set1_5(self, val=None):
        if val == None:
            if self.button1_5.config('text')[4] == '':
                self.button1_5.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[4][0],1)
            elif self.button1_5.config('text')[4] == 'u':
                self.button1_5.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[4][0],2)
            elif self.button1_5.config('text')[4] == 'e':
                self.button1_5.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[4][0],3)
            elif self.button1_5.config('text')[4] == 'S':
                self.button1_5.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[4][0],0)
        else:
            if val == 1:
                self.button1_5.config(background='#f5010a', text='u')
            if val == 2:
                self.button1_5.config(background='#00e100', text='e')
            if val == 3:
                self.button1_5.config(background='#ffff80', text='S')
            else:
                pass                     
    def set2_1(self, val=None):
        if val == None:
            if self.button2_1.config('text')[4] == '':
                self.button2_1.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[0][1],1)
            elif self.button2_1.config('text')[4] == 'u':
                self.button2_1.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[0][1],2)
            elif self.button2_1.config('text')[4] == 'e':
                self.button2_1.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[0][1],3)
            elif self.button2_1.config('text')[4] == 'S':
                self.button2_1.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[0][1],0)
        else:
            if val == 1:
                self.button2_1.config(background='#f5010a', text='u')
            if val == 2:
                self.button2_1.config(background='#00e100', text='e')
            if val == 3:
                self.button2_1.config(background='#ffff80', text='S')
            else:
                pass                     
    def set2_2(self, val=None):
        if val == None:
            if self.button2_2.config('text')[4] == '':
                self.button2_2.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[1][1],1)
            elif self.button2_2.config('text')[4] == 'u':
                self.button2_2.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[1][1],2)
            elif self.button2_2.config('text')[4] == 'e':
                self.button2_2.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[1][1],3)
            elif self.button2_2.config('text')[4] == 'S':
                self.button2_2.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[1][1],0)
        else:
            if val == 1:
                self.button2_2.config(background='#f5010a', text='u')
            if val == 2:
                self.button2_2.config(background='#00e100', text='e')
            if val == 3:
                self.button2_2.config(background='#ffff80', text='S')
            else:
                pass                     
    def set2_3(self, val=None):
        if val == None:
            if self.button2_3.config('text')[4] == '':
                self.button2_3.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[2][1],1)
            elif self.button2_3.config('text')[4] == 'u':
                self.button2_3.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[2][1],2)
            elif self.button2_3.config('text')[4] == 'e':
                self.button2_3.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[2][1],3)
            elif self.button2_3.config('text')[4] == 'S':
                self.button2_3.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[2][1],0)
        else:
            if val == 1:
                self.button2_3.config(background='#f5010a', text='u')
            if val == 2:
                self.button2_3.config(background='#00e100', text='e')
            if val == 3:
                self.button2_3.config(background='#ffff80', text='S')
            else:
                pass                     
    def set2_4(self, val=None):
        if val == None:
            if self.button2_4.config('text')[4] == '':
                self.button2_4.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[3][1],1)
            elif self.button2_4.config('text')[4] == 'u':
                self.button2_4.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[3][1],2)
            elif self.button2_4.config('text')[4] == 'e':
                self.button2_4.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[3][1],3)
            elif self.button2_4.config('text')[4] == 'S':
                self.button2_4.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[3][1],0)
        else:
            if val == 1:
                self.button2_4.config(background='#f5010a', text='u')
            if val == 2:
                self.button2_4.config(background='#00e100', text='e')
            if val == 3:
                self.button2_4.config(background='#ffff80', text='S')
            else:
                pass                     
    def set2_5(self, val=None):
        if val == None:
            if self.button2_5.config('text')[4] == '':
                self.button2_5.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[4][1],1)
            elif self.button2_5.config('text')[4] == 'u':
                self.button2_5.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[4][1],2)
            elif self.button2_5.config('text')[4] == 'e':
                self.button2_5.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[4][1],3)
            elif self.button2_5.config('text')[4] == 'S':
                self.button2_5.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[4][1],0)
        else:
            if val == 1:
                self.button2_5.config(background='#f5010a', text='u')
            if val == 2:
                self.button2_5.config(background='#00e100', text='e')
            if val == 3:
                self.button2_5.config(background='#ffff80', text='S')
            else:
                pass                
    def set3_1(self, val=None):
        if val == None:
            if self.button3_1.config('text')[4] == '':
                self.button3_1.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[0][2],1)
            elif self.button3_1.config('text')[4] == 'u':
                self.button3_1.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[0][2],2)
            elif self.button3_1.config('text')[4] == 'e':
                self.button3_1.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[0][2],3)
            elif self.button3_1.config('text')[4] == 'S':
                self.button3_1.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[0][2],0)
        else:
            if val == 1:
                self.button3_1.config(background='#f5010a', text='u')
            if val == 2:
                self.button3_1.config(background='#00e100', text='e')
            if val == 3:
                self.button3_1.config(background='#ffff80', text='S')
            else:
                pass            
    def set3_2(self, val=None):
        if val == None:
            if self.button3_2.config('text')[4] == '':
                self.button3_2.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[1][2],1)
            elif self.button3_2.config('text')[4] == 'u':
                self.button3_2.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[1][2],2)
            elif self.button3_2.config('text')[4] == 'e':
                self.button3_2.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[1][2],3)
            elif self.button3_2.config('text')[4] == 'S':
                self.button3_2.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[1][2],0)
        else:
            if val == 1:
                self.button3_2.config(background='#f5010a', text='u')
            if val == 2:
                self.button3_2.config(background='#00e100', text='e')
            if val == 3:
                self.button3_2.config(background='#ffff80', text='S')
            else:
                pass                
    def set3_3(self, val=None):
        if val == None:
            if self.button3_3.config('text')[4] == '':
                self.button3_3.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[2][2],1)
            elif self.button3_3.config('text')[4] == 'u':
                self.button3_3.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[2][2],2)
            elif self.button3_3.config('text')[4] == 'e':
                self.button3_3.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[2][2],3)
            elif self.button3_3.config('text')[4] == 'S':
                self.button3_3.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[2][2],0)
        else:
            if val == 1:
                self.button3_3.config(background='#f5010a', text='u')
            if val == 2:
                self.button3_3.config(background='#00e100', text='e')
            if val == 3:
                self.button3_3.config(background='#ffff80', text='S')
            else:
                pass
    def set3_4(self, val=None):
        if val == None:
            if self.button3_4.config('text')[4] == '':
                self.button3_4.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[3][2],1)
            elif self.button3_4.config('text')[4] == 'u':
                self.button3_4.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[3][2],2)
            elif self.button3_4.config('text')[4] == 'e':
                self.button3_4.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[3][2],3)
            elif self.button3_4.config('text')[4] == 'S':
                self.button3_4.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[3][2],0)
        else:
            if val == 1:
                self.button3_4.config(background='#f5010a', text='u')
            if val == 2:
                self.button3_4.config(background='#00e100', text='e')
            if val == 3:
                self.button3_4.config(background='#ffff80', text='S')
            else:
                pass
    def set3_5(self, val=None):
        if val == None:
            if self.button3_5.config('text')[4] == '':
                self.button3_5.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[4][2],1)
            elif self.button3_5.config('text')[4] == 'u':
                self.button3_5.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[4][2],2)
            elif self.button3_5.config('text')[4] == 'e':
                self.button3_5.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[4][2],3)
            elif self.button3_5.config('text')[4] == 'S':
                self.button3_5.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[4][2],0)
        else:
            if val == 1:
                self.button3_5.config(background='#f5010a', text='u')
            if val == 2:
                self.button3_5.config(background='#00e100', text='e')
            if val == 3:
                self.button3_5.config(background='#ffff80', text='S')
            else:
                pass                
    def set4_1(self, val=None):
        if val == None:
            if self.button4_1.config('text')[4] == '':
                self.button4_1.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[0][3],1)
            elif self.button4_1.config('text')[4] == 'u':
                self.button4_1.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[0][3],2)
            elif self.button4_1.config('text')[4] == 'e':
                self.button4_1.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[0][3],3)
            elif self.button4_1.config('text')[4] == 'S':
                self.button4_1.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[0][3],0)
        else:
            if val == 1:
                self.button4_1.config(background='#f5010a', text='u')
            if val == 2:
                self.button4_1.config(background='#00e100', text='e')
            if val == 3:
                self.button4_1.config(background='#ffff80', text='S')
            else:
                pass                
    def set4_2(self, val=None):
        if val == None:
            if self.button4_2.config('text')[4] == '':
                self.button4_2.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[1][3],1)
            elif self.button4_2.config('text')[4] == 'u':
                self.button4_2.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[1][3],2)
            elif self.button4_2.config('text')[4] == 'e':
                self.button4_2.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[1][3],3)
            elif self.button4_2.config('text')[4] == 'S':
                self.button4_2.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[1][3],0)
        else:
            if val == 1:
                self.button4_2.config(background='#f5010a', text='u')
            if val == 2:
                self.button4_2.config(background='#00e100', text='e')
            if val == 3:
                self.button4_2.config(background='#ffff80', text='S')
            else:
                pass                     
    def set4_3(self, val=None):
        if val == None:
            if self.button4_3.config('text')[4] == '':
                self.button4_3.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[2][3],1)
            elif self.button4_3.config('text')[4] == 'u':
                self.button4_3.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[2][3],2)
            elif self.button4_3.config('text')[4] == 'e':
                self.button4_3.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[2][3],3)
            elif self.button4_3.config('text')[4] == 'S':
                self.button4_3.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[2][3],0)
        else:
            if val == 1:
                self.button4_3.config(background='#f5010a', text='u')
            if val == 2:
                self.button4_3.config(background='#00e100', text='e')
            if val == 3:
                self.button4_3.config(background='#ffff80', text='S')
            else:
                pass
    def set4_4(self, val=None):
        if val == None:
            if self.button4_4.config('text')[4] == '':
                self.button4_4.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[3][3],1)
            elif self.button4_4.config('text')[4] == 'u':
                self.button4_4.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[3][3],2)
            elif self.button4_4.config('text')[4] == 'e':
                self.button4_4.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[3][3],3)
            elif self.button4_4.config('text')[4] == 'S':
                self.button4_4.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[3][3],0)
        else:
            if val == 1:
                self.button4_4.config(background='#f5010a', text='u')
            if val == 2:
                self.button4_4.config(background='#00e100', text='e')
            if val == 3:
                self.button4_4.config(background='#ffff80', text='S')
            else:
                pass
    def set4_5(self, val=None):
        if val == None:
            if self.button4_5.config('text')[4] == '':
                self.button4_5.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[4][3],1)
            elif self.button4_5.config('text')[4] == 'u':
                self.button4_5.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[4][3],2)
            elif self.button4_5.config('text')[4] == 'e':
                self.button4_5.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[4][3],3)
            elif self.button4_5.config('text')[4] == 'S':
                self.button4_5.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[4][3],0)
        else:
            if val == 1:
                self.button4_5.config(background='#f5010a', text='u')
            if val == 2:
                self.button4_5.config(background='#00e100', text='e')
            if val == 3:
                self.button4_5.config(background='#ffff80', text='S')
            else:
                pass                     
    def set5_1(self, val=None):
        if val == None:
            if self.button5_1.config('text')[4] == '':
                self.button5_1.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[0][4],1)
            elif self.button5_1.config('text')[4] == 'u':
                self.button5_1.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[0][4],2)
            elif self.button5_1.config('text')[4] == 'e':
                self.button5_1.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[0][4],3)
            elif self.button5_1.config('text')[4] == 'S':
                self.button5_1.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[0][4],0)
        else:
            if val == 1:
                self.button5_1.config(background='#f5010a', text='u')
            if val == 2:
                self.button5_1.config(background='#00e100', text='e')
            if val == 3:
                self.button5_1.config(background='#ffff80', text='S')
            else:
                pass                     
    def set5_2(self, val=None):
        if val == None:
            if self.button5_2.config('text')[4] == '':
                self.button5_2.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[1][4],1)
            elif self.button5_2.config('text')[4] == 'u':
                self.button5_2.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[1][4],2)
            elif self.button5_2.config('text')[4] == 'e':
                self.button5_2.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[1][4],3)
            elif self.button5_2.config('text')[4] == 'S':
                self.button5_2.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[1][4],0)
        else:
            if val == 1:
                self.button5_2.config(background='#f5010a', text='u')
            if val == 2:
                self.button5_2.config(background='#00e100', text='e')
            if val == 3:
                self.button5_2.config(background='#ffff80', text='S')
            else:
                pass                         
    def set5_3(self, val=None):
        if val == None:
            if self.button5_3.config('text')[4] == '':
                self.button5_3.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[2][4],1)
            elif self.button5_3.config('text')[4] == 'u':
                self.button5_3.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[2][4],2)
            elif self.button5_3.config('text')[4] == 'e':
                self.button5_3.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[2][4],3)
            elif self.button5_3.config('text')[4] == 'S':
                self.button5_3.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[2][4],0)
        else:
            if val == 1:
                self.button5_3.config(background='#f5010a', text='u')
            if val == 2:
                self.button5_3.config(background='#00e100', text='e')
            if val == 3:
                self.button5_3.config(background='#ffff80', text='S')
            else:
                pass                         
    def set5_4(self, val=None):
        if val == None:
            if self.button5_4.config('text')[4] == '':
                self.button5_4.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[3][4],1)
            elif self.button5_4.config('text')[4] == 'u':
                self.button5_4.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[3][4],2)
            elif self.button5_4.config('text')[4] == 'e':
                self.button5_4.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[3][4],3)
            elif self.button5_4.config('text')[4] == 'S':
                self.button5_4.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[3][4],0)
        else:
            if val == 1:
                self.button5_4.config(background='#f5010a', text='u')
            if val == 2:
                self.button5_4.config(background='#00e100', text='e')
            if val == 3:
                self.button5_4.config(background='#ffff80', text='S')
            else:
                pass                         
    def set5_5(self, val=None):
        if val == None:
            if self.button5_5.config('text')[4] == '':
                self.button5_5.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[4][4],1)
            elif self.button5_5.config('text')[4] == 'u':
                self.button5_5.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[4][4],2)
            elif self.button5_5.config('text')[4] == 'e':
                self.button5_5.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[4][4],3)
            elif self.button5_5.config('text')[4] == 'S':
                self.button5_5.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[4][4],0)
        else:
            if val == 1:
                self.button5_5.config(background='#f5010a', text='u')
            if val == 2:
                self.button5_5.config(background='#00e100', text='e')
            if val == 3:
                self.button5_5.config(background='#ffff80', text='S')
            else:
                pass                         
    def set6_1(self, val=None):
        if val == None:
            if self.button6_1.config('text')[4] == '':
                self.button6_1.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[0][5],1)
            elif self.button6_1.config('text')[4] == 'u':
                self.button6_1.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[0][5],2)
            elif self.button6_1.config('text')[4] == 'e':
                self.button6_1.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[0][5],3)
            elif self.button6_1.config('text')[4] == 'S':
                self.button6_1.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[0][5],0)
        else:
            if val == 1:
                self.button6_1.config(background='#f5010a', text='u')
            if val == 2:
                self.button6_1.config(background='#00e100', text='e')
            if val == 3:
                self.button6_1.config(background='#ffff80', text='S')
            else:
                pass                         
    def set6_2(self, val=None):
        if val == None:
            if self.button6_2.config('text')[4] == '':
                self.button6_2.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[1][5],1)
            elif self.button6_2.config('text')[4] == 'u':
                self.button6_2.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[1][5],2)
            elif self.button6_2.config('text')[4] == 'e':
                self.button6_2.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[1][5],3)
            elif self.button6_2.config('text')[4] == 'S':
                self.button6_2.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[1][5],0)
        else:
            if val == 1:
                self.button6_2.config(background='#f5010a', text='u')
            if val == 2:
                self.button6_2.config(background='#00e100', text='e')
            if val == 3:
                self.button6_2.config(background='#ffff80', text='S')
            else:
                pass                          
    def set6_3(self, val=None):
        if val == None:
            if self.button6_3.config('text')[4] == '':
                self.button6_3.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[2][5],1)
            elif self.button6_3.config('text')[4] == 'u':
                self.button6_3.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[2][5],2)
            elif self.button6_3.config('text')[4] == 'e':
                self.button6_3.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[2][5],3)
            elif self.button6_3.config('text')[4] == 'S':
                self.button6_3.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[2][5],0)
        else:
            if val == 1:
                self.button6_3.config(background='#f5010a', text='u')
            if val == 2:
                self.button6_3.config(background='#00e100', text='e')
            if val == 3:
                self.button6_3.config(background='#ffff80', text='S')
            else:
                pass                          
    def set6_4(self, val=None):
        if val == None:
            if self.button6_4.config('text')[4] == '':
                self.button6_4.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[3][5],1)
            elif self.button6_4.config('text')[4] == 'u':
                self.button6_4.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[3][5],2)
            elif self.button6_4.config('text')[4] == 'e':
                self.button6_4.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[3][5],3)
            elif self.button6_4.config('text')[4] == 'S':
                self.button6_4.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[3][5],0)
        else:
            if val == 1:
                self.button6_4.config(background='#f5010a', text='u')
            if val == 2:
                self.button6_4.config(background='#00e100', text='e')
            if val == 3:
                self.button6_4.config(background='#ffff80', text='S')
            else:
                pass                          
    def set6_5(self, val=None):
        if val == None:
            if self.button6_5.config('text')[4] == '':
                self.button6_5.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[4][5],1)
            elif self.button6_5.config('text')[4] == 'u':
                self.button6_5.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[4][5],2)
            elif self.button6_5.config('text')[4] == 'e':
                self.button6_5.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[4][5],3)
            elif self.button6_5.config('text')[4] == 'S':
                self.button6_5.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[4][5],0)
        else:
            if val == 1:
                self.button6_5.config(background='#f5010a', text='u')
            if val == 2:
                self.button6_5.config(background='#00e100', text='e')
            if val == 3:
                self.button6_5.config(background='#ffff80', text='S')
            else:
                pass                          
    def set7_1(self, val=None):
        if val == None:
            if self.button7_1.config('text')[4] == '':
                self.button7_1.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[0][6],1)
            elif self.button7_1.config('text')[4] == 'u':
                self.button7_1.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[0][6],2)
            elif self.button7_1.config('text')[4] == 'e':
                self.button7_1.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[0][6],3)
            elif self.button7_1.config('text')[4] == 'S':
                self.button7_1.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[0][6],0)
        else:
            if val == 1:
                self.button7_1.config(background='#f5010a', text='u')
            if val == 2:
                self.button7_1.config(background='#00e100', text='e')
            if val == 3:
                self.button7_1.config(background='#ffff80', text='S')
            else:
                pass                          
    def set7_2(self, val=None):
        if val == None:
            if self.button7_2.config('text')[4] == '':
                self.button7_2.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[1][6],1)
            elif self.button7_2.config('text')[4] == 'u':
                self.button7_2.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[1][6],2)
            elif self.button7_2.config('text')[4] == 'e':
                self.button7_2.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[1][6],3)
            elif self.button7_2.config('text')[4] == 'S':
                self.button7_2.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[1][6],0)
        else:
            if val == 1:
                self.button7_2.config(background='#f5010a', text='u')
            if val == 2:
                self.button7_2.config(background='#00e100', text='e')
            if val == 3:
                self.button7_2.config(background='#ffff80', text='S')
            else:
                pass                          
    def set7_3(self, val=None):
        if val == None:
            if self.button7_3.config('text')[4] == '':
                self.button7_3.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[2][6],1)
            elif self.button7_3.config('text')[4] == 'u':
                self.button7_3.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[2][6],2)
            elif self.button7_3.config('text')[4] == 'e':
                self.button7_3.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[2][6],3)
            elif self.button7_3.config('text')[4] == 'S':
                self.button7_3.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[2][6],0)
        else:
            if val == 1:
                self.button7_3.config(background='#f5010a', text='u')
            if val == 2:
                self.button7_3.config(background='#00e100', text='e')
            if val == 3:
                self.button7_3.config(background='#ffff80', text='S')
            else:
                pass                      
    def set7_4(self, val=None):
        if val == None:
            if self.button7_4.config('text')[4] == '':
                self.button7_4.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[3][6],1)
            elif self.button7_4.config('text')[4] == 'u':
                self.button7_4.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[3][6],2)
            elif self.button7_4.config('text')[4] == 'e':
                self.button7_4.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[3][6],3)
            elif self.button7_4.config('text')[4] == 'S':
                self.button7_4.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[3][6],0)
        else:
            if val == 1:
                self.button7_4.config(background='#f5010a', text='u')
            if val == 2:
                self.button7_4.config(background='#00e100', text='e')
            if val == 3:
                self.button7_4.config(background='#ffff80', text='S')
            else:
                pass                  
    def set7_5(self, val=None):
        if val == None:
            if self.button7_5.config('text')[4] == '':
                self.button7_5.config(background='#f5010a', text='u')
                self.writeFehlzeit(self.datelistweek[4][6],1)
            elif self.button7_5.config('text')[4] == 'u':
                self.button7_5.config(background='#00e100', text='e')
                self.writeFehlzeit(self.datelistweek[4][6],2)
            elif self.button7_5.config('text')[4] == 'e':
                self.button7_5.config(background='#ffff80', text='S')
                self.writeFehlzeit(self.datelistweek[4][6],3)
            elif self.button7_5.config('text')[4] == 'S':
                self.button7_5.config(background='#c0c0c0', text='')
                self.writeFehlzeit(self.datelistweek[4][6],0)
        else:
            if val == 1:
                self.button7_5.config(background='#f5010a', text='u')
            if val == 2:
                self.button7_5.config(background='#00e100', text='e')
            if val == 3:
                self.button7_5.config(background='#ffff80', text='S')
            else:
                pass                  

    def writeFehlzeit(self, d, f):
        print(d,f)

        # DB-Verbindung
        verbindung = sqlite3.connect("kurs.db")
        c = verbindung.cursor()
        # TODO mit try exception abfangen und bei nicht existierender Spalte diese anlegen
        c.execute(""" UPDATE sus
                    SET """+d+""" = ?
                    WHERE pk = ?;
                    """,
                    (f,self.student_pk))
        verbindung.commit()

        # DB-Verbindung schließen
        c.close()
        verbindung.close()

    def resetButtons(self):
        self.button1_1.config(background='#c0c0c0', text='')
        self.button1_2.config(background='#c0c0c0', text='')
        self.button1_3.config(background='#c0c0c0', text='')
        self.button1_4.config(background='#c0c0c0', text='')
        self.button1_5.config(background='#c0c0c0', text='')
        
        self.button2_1.config(background='#c0c0c0', text='')
        self.button2_2.config(background='#c0c0c0', text='')
        self.button2_3.config(background='#c0c0c0', text='')
        self.button2_4.config(background='#c0c0c0', text='')
        self.button2_5.config(background='#c0c0c0', text='')
        
        self.button3_1.config(background='#c0c0c0', text='')
        self.button3_2.config(background='#c0c0c0', text='')
        self.button3_3.config(background='#c0c0c0', text='')
        self.button3_4.config(background='#c0c0c0', text='')
        self.button3_5.config(background='#c0c0c0', text='')
        
        self.button4_1.config(background='#c0c0c0', text='')
        self.button4_2.config(background='#c0c0c0', text='')
        self.button4_3.config(background='#c0c0c0', text='')
        self.button4_4.config(background='#c0c0c0', text='')
        self.button4_5.config(background='#c0c0c0', text='')
        
        self.button5_1.config(background='#c0c0c0', text='')
        self.button5_2.config(background='#c0c0c0', text='')
        self.button5_3.config(background='#c0c0c0', text='')
        self.button5_4.config(background='#c0c0c0', text='')
        self.button5_5.config(background='#c0c0c0', text='')
        
        self.button6_1.config(background='#c0c0c0', text='')
        self.button6_2.config(background='#c0c0c0', text='')
        self.button6_3.config(background='#c0c0c0', text='')
        self.button6_4.config(background='#c0c0c0', text='')
        self.button6_5.config(background='#c0c0c0', text='')
        
        self.button7_1.config(background='#c0c0c0', text='')
        self.button7_2.config(background='#c0c0c0', text='')
        self.button7_3.config(background='#c0c0c0', text='')
        self.button7_4.config(background='#c0c0c0', text='')
        self.button7_5.config(background='#c0c0c0', text='')



    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    app = Tutmod01App()
    app.run()

