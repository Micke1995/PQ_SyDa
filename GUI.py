import tkinter 	as tk
from tkinter 							import filedialog, messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg 	import FigureCanvasTkAgg, NavigationToolbar2Tk
from PQmodel import PQ
import numpy as np
import csv
from scipy.io import savemat

catalog=['Pure sinusoidal', 'Sag', 'Swell','Interruption','Transient/Impulse/Spike',
         'Oscillatory transient','Harmonics','Harmonics with Sag', 'Harmonics with Swell',
         'Flicker', 'Flicker with Sag', 'Flicker with Swell', 'Sag with Oscillatory transient',
         'Swell with Oscillatory transient', 'Sag with Harmonics', 'Swell with Harmonics', 'Notch',
         'Harmonics with Sag with Flicker', 'Harmonics with Swell with Flicker',  'Sag with Harmonics with Flicker',
         'Swell with Harmonics with Flicker', 'Sag with Harmonics with Oscillatory transient',
         'Swell with Harmonics with Oscillatory transient', 'Harmonics with Sag with Oscillatory transient',
         'Harmonics with Swell with Oscillatory transient','Harmonics with Sag with Flicker with Oscillatory transient',
         'Harmonics with Swell with Flicker with Oscillatory transient', 'Sag with Harmonics with Flicker with Oscillatory transient',
         'Swell with Harmonics with Flicker with Oscillatory transient']

figs_size_font =24

class Window1():

	# Main window

	global font_text
	font_text = 'Calibri'

	global color0, color1, color2, color3
	color0 = 'SteelBlue4'
	color1 = 'black'
	color2 = 'grey24'
	color3 = 'snow'


	def __init__(self, master):
		self.master = master
		self.master.title('PQ event Toolbox')
		self.master.geometry('1300x800')
		self.master.configure(bg = color1)
		self.frame = tk.Frame(self.master)
		self.frame.pack()
		self.Model = None
		self.Create_Widgets()
		self.Signals = []

		


	def Create_Widgets(self):

		# MASTER
		title = 'PQ event generator'
		self.Title = tk.Label(self.master, text = title, font = (font_text, 14), fg = 'white', bg = color0, anchor = tk.CENTER)
		self.Title.pack(fill = 'x')

		self.Infobtn = tk.Label(self.master, text = 'i', font = ('Times', 14, 'italic'), fg = 'white', bg = color1, anchor = tk.CENTER)
		self.Infobtn.place(relx = 1.00, rely = 0.0, height = 30, width = 30,  anchor = tk.NE)
		self.Infobtn.bind('<Button-1>', self.Info)
        # ========================================  Inizialize model Button's ======================================== #
		self.btn1 = tk.Button(self.master, text = 'Initialize model', font = (font_text, 10), anchor = tk.CENTER,command=self.clickInizializeModel)
		self.btn1.place(relx = 0.012, y = 45.0, height = 24, relwidth = 0.080)
		
		self.Cicles_val = tk.DoubleVar()
		self.CiclesLabel = tk.Label(self.master, text = 'Cycles:', font = (font_text, 10), anchor = tk.CENTER,fg='white', bg = color1)
		self.CiclesLabel.place(relx = 0.095, y = 45.0, height = 20)		
		self.Cicles_val.set(10)

		self.CiclesEnt = tk.Entry(self.master, fg = 'white', font = (font_text, 10), bg = color2,textvariable=self.Cicles_val)
		self.CiclesEnt.place(relx = 0.135, y = 45.0, height = 24, relwidth = 0.03)

		self.Freq_val = tk.DoubleVar()
		self.FreqLabel = tk.Label(self.master, text = 'Frequency:', font = (font_text, 10), anchor = tk.CENTER,fg='white', bg = color1)
		self.FreqLabel.place(relx = 0.175, y = 45.0, height = 20)
		self.Freq_val.set(60)		
		
		self.FreqEnt = tk.Entry(self.master, fg = 'white', font = (font_text, 10), bg = color2,textvariable=self.Freq_val)
		self.FreqEnt.place(relx = 0.225, y = 45.0, height = 24, relwidth = 0.03)

		self.FS_val =tk.DoubleVar()
		self.FSLabel = tk.Label(self.master, text = 'Fs:', font = (font_text, 10), anchor = tk.CENTER,fg='white', bg = color1)
		self.FSLabel.place(relx = 0.27, y = 45.0, height = 20)		
		self.FS_val.set(16000)
		self.FSEnt = tk.Entry(self.master, fg = 'white', font = (font_text, 10), bg = color2,textvariable=self.FS_val)
		self.FSEnt.place(relx = 0.288, y = 45.0, height = 24, relwidth = 0.045)
		
        
		self.DurationLabel = tk.Label(self.master, text = 'Duration:', font = (font_text, 10), anchor = tk.CENTER,fg='white', bg = color1)
		self.DurationLabel.place(relx = 0.34, y = 45.0, height = 20)		
		self.Duration_val = tk.DoubleVar()
		self.DurationEnt = tk.Entry(self.master, fg = 'white', font = (font_text, 10), bg = color2,textvariable=self.Duration_val)
		self.DurationEnt.place(relx = 0.385, y = 45.0, height = 24, relwidth = 0.03)
		self.Duration_val.set(5)      


		self.StartLabel = tk.Label(self.master, text = 'Start:', font = (font_text, 10), anchor = tk.CENTER,fg='white', bg = color1)
		self.StartLabel.place(relx = 0.42, y = 45.0, height = 20)		
		self.Start_val = tk.DoubleVar()
		self.StartEnt = tk.Entry(self.master, fg = 'white', font = (font_text, 10), bg = color2,textvariable=self.Start_val)
		self.StartEnt.place(relx = 0.448, y = 45.0, height = 24, relwidth = 0.03)
		self.Start_val.set(0)   
		
		RandomStar =[self.StartEnt,self.DurationEnt]
		self.val_RandomStart = tk.BooleanVar()
		self.val_RandomStart.set(True)
		self.RandomStart = tk.Checkbutton(self.master, variable = self.val_RandomStart, text = 'Random	(Cycles) [Duration][Start]', 
			onvalue = True, offvalue = False, fg = 'white', bg = color1, anchor = tk.NE,command=lambda e=RandomStar, v=self.val_RandomStart: self.AcivateDeactivate(e,v))
		self.RandomStart.config(selectcolor='#000000')
		self.RandomStart.place(relx = 0.65, y = 45.0, height = 24, relwidth = 0.16, anchor = tk.NE)
		self.AcivateDeactivate(RandomStar,self.val_RandomStart)                     
		        
        # ======================================== GENERAL BUTTON'S ======================================== #
		# self.CLEAR = tk.Button(self.master, text = 'CLEAR ALL', font = (font_text, 12), anchor = tk.CENTER)
		# self.CLEAR.place(relx = 0.62, y = 50, height = 30, relwidth = 0.11)

		self.RUN = tk.Button(self.master, text = 'RUN', font = (font_text, 12), anchor = tk.CENTER,command=self.clickRUN)
		self.RUN.place(relx = 0.74, y = 50, height = 30, relwidth = 0.11)

		self.RUN = tk.Button(self.master, text = 'EXIT', font = (font_text, 12), anchor = tk.CENTER,command= self.click_EXIT)
		self.RUN.place(relx = 0.86, y = 50, height = 30, relwidth = 0.11)

		# ======================================== SETTINGS FRAME ======================================== #

		self.SttgFrame = tk.LabelFrame(self.master, text = 'Settings', font = (font_text, 10), fg = 'white', bg = color1)
		self.SttgFrame.place(x = 10, y = 80, height = 122, relwidth = 0.980, anchor = tk.NW)

		self.PQLb = tk.Label(self.SttgFrame, text = 'PQ Event:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.NE)
		self.PQLb.place(relx = 0.00001, y = 2, height = 24, relwidth = 0.05, anchor = tk.NW)

		self.Refreshsttbtn = tk.Button(self.SttgFrame, text = 'Set Parameters', font = (font_text, 10), anchor = tk.CENTER,command=self.SetParam)
		self.Refreshsttbtn.place(relx = 0.2, y = 64, height = 24, relwidth = 0.1, anchor = tk.NW)		

		self.val_PQ = tk.StringVar()
		self.val_PQ.set(catalog[0])
		self.PQmenu = tk.OptionMenu(self.SttgFrame, self.val_PQ, *catalog)
		self.PQmenu.place(relx = 0.06, y = 2, height = 24, relwidth = 0.28, anchor = tk.NW)
		style = ttk.Style(self.SttgFrame)
		style.configure('lefttab.TNotebook',tabposition='wn',font = (font_text, 7))
		#style.configure('TNotebook.Tab', padding=(20, 15, 30, 5))
    
		self.tbsettings = ttk.Notebook(self.SttgFrame)#,style='lefttab.TNotebook')
		self.tbsettings.place(relx = 0.44, rely = 0.00, relwidth = 0.55, relheight = 0.99, anchor = tk.NW)

		self.tab0 = tk.Frame(self.tbsettings, background = color1)
		self.tab1 = tk.Frame(self.tbsettings, background = color1)
		self.tab2 = tk.Frame(self.tbsettings, background = color1)
		self.tab3 = tk.Frame(self.tbsettings, background = color1)
		self.tab4 = tk.Frame(self.tbsettings, background = color1)
		self.tab5 = tk.Frame(self.tbsettings, background = color1)
		self.tab6 = tk.Frame(self.tbsettings, background = color1)		

		self.tbsettings.add(self.tab0, text ='General')
		self.tbsettings.add(self.tab1, text ='Harmonics')
		self.tbsettings.add(self.tab2, text ='Sag/Swell')
		self.tbsettings.add(self.tab3, text ='Oscillatory')
		self.tbsettings.add(self.tab4, text ='Flicker')		
		self.tbsettings.add(self.tab5, text ='Notch')
		self.tbsettings.add(self.tab6, text ='Transient')		

		# ======================================== FOR ALL SIGNALS ======================================================== #
		self.GenLb = tk.Label(self.tab0, text = 'Parameters for all signals:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.GenLb.place(relx = 0.3, y = 2, height = 24, relwidth = 2, anchor = tk.NE)
		
		self.Har1stLb = tk.Label(self.tab0, text = 'Phase [Min][Max]:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.Har1stLb.place(relx = 0.2, y = 30, height = 24, relwidth = 0.2, anchor = tk.NE)
    
		self.val_Phasemin = tk.DoubleVar()
		self.ent_Phasemin = tk.Entry(self.tab0, textvariable = self.val_Phasemin, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Phasemin.place(relx = 0.22, y = 30, height = 24, relwidth = 0.08)

		self.val_Phasemax = tk.DoubleVar()
		self.ent_Phasemax = tk.Entry(self.tab0, textvariable = self.val_Phasemax, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Phasemax.place(relx = 0.35, y = 30, height = 24, relwidth = 0.08)	

        # ======================================== HARMONICS RELATED SETTINGS FRAME ======================================== #
		self.HarMagLb = tk.Label(self.tab1, text = 'Magnitude:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.HarMagLb.place(relx = 0.12, y = 2, height = 24, relwidth = 0.8, anchor = tk.NE)
		
		self.Har1stLb = tk.Label(self.tab1, text = '1st Ord :', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.Har1stLb.place(relx = 0.2, y = 20, height = 24, relwidth = 0.2, anchor = tk.NE)
    
		self.val_Har1st = tk.DoubleVar()
		self.ent_Har1st = tk.Entry(self.tab1, textvariable = self.val_Har1st, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Har1st.place(relx = 0.22, y = 20, height = 24, relwidth = 0.08)

		# self.val_Har1stmax = tk.DoubleVar()
		# self.ent_Har1stmax = tk.Entry(self.tab1, textvariable = self.val_Har1stmax, fg = 'white', font = (font_text, 10), bg = color2)
		# self.ent_Har1stmax.place(relx = 0.35, y = 20, height = 24, relwidth = 0.08)		
		
		self.Har3thLb = tk.Label(self.tab1, text = '3th Ord [Min][Max]:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.Har3thLb.place(relx = 0.2, y = 50, height = 24, relwidth = 0.2, anchor = tk.NE)
    
		self.val_Har3thmin = tk.DoubleVar()
		self.ent_Har3thmin = tk.Entry(self.tab1, textvariable = self.val_Har3thmin, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Har3thmin.place(relx = 0.22, y = 50, height = 24, relwidth = 0.08)   

		self.val_Har3thmax = tk.DoubleVar()
		self.ent_Har3thmax = tk.Entry(self.tab1, textvariable = self.val_Har3thmax, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Har3thmax.place(relx = 0.35, y = 50, height = 24, relwidth = 0.08)     

		self.Har5thLb = tk.Label(self.tab1, text = '5th Ord [Min][Max]:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.Har5thLb.place(relx = 0.65, y = 20, height = 24, relwidth = 0.2, anchor = tk.NE)
    
		self.val_Har5thmin = tk.DoubleVar()
		self.ent_Har5thmin = tk.Entry(self.tab1, textvariable = self.val_Har5thmin, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Har5thmin.place(relx = 0.67, y = 20, height = 24, relwidth = 0.08)

		self.val_Har5thmax = tk.DoubleVar()
		self.ent_Har5thmax = tk.Entry(self.tab1, textvariable = self.val_Har5thmax, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Har5thmax.place(relx = 0.8, y = 20, height = 24, relwidth = 0.08)		
		
		self.Har7thLb = tk.Label(self.tab1, text = '7th Ord [Min][Max]:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.Har7thLb.place(relx = 0.65, y = 50, height = 24, relwidth = 0.2, anchor = tk.NE)

		self.val_Har7thmin = tk.DoubleVar()
		self.ent_Har7thmin = tk.Entry(self.tab1, textvariable = self.val_Har7thmin, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Har7thmin.place(relx = 0.67, y = 50, height = 24, relwidth = 0.08)
    
		self.val_Har7thmax = tk.DoubleVar()
		self.ent_Har7thmax = tk.Entry(self.tab1, textvariable = self.val_Har7thmax, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Har7thmax.place(relx = 0.8, y = 50, height = 24, relwidth = 0.08)  

		# =============================== NOTCH RELATED SETTINGS FRAME  =============================== #
		
		self.NotchLb = tk.Label(self.tab5, text = 'Notch parameters:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.NotchLb.place(relx = 0.17, y = 2, height = 24, relwidth = 0.2, anchor = tk.NE)

		self.KLb = tk.Label(self.tab5, text = 'K[Min][Max]:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.KLb.place(relx = 0.22, y = 20, height = 24, relwidth = 0.2, anchor = tk.NE)
    
		self.val_Kmin = tk.DoubleVar()
		self.ent_Kmin = tk.Entry(self.tab5, textvariable = self.val_Kmin, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Kmin.place(relx = 0.32, y = 20, height = 24, relwidth = 0.08, anchor = tk.NE)

		self.val_Kmax = tk.DoubleVar()
		self.ent_Kmax = tk.Entry(self.tab5, textvariable = self.val_Kmin, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Kmax.place(relx = 0.35, y = 20, height = 24, relwidth = 0.08)		

		self.CLb = tk.Label(self.tab5, text = 'Notches[1,2,4,6]:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.CLb.place(relx = 0.22, y = 50, height = 24, relwidth = 0.2, anchor = tk.NE)
    
		self.val_C = tk.DoubleVar()
		self.ent_C = tk.Entry(self.tab5, textvariable = self.val_C, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_C.place(relx = 0.24, y = 50, height = 24, relwidth = 0.08)

	

				
        # ======================================== SAG/SWELL RELATED SETTINGS FRAME ======================================== #
		self.SAGLb = tk.Label(self.tab2, text = 'Parameters:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.SAGLb.place(relx = 0.12, y = 2, height = 24, relwidth = 0.8, anchor = tk.NE)
		
		self.AlphaLb = tk.Label(self.tab2, text = 'Alpha[Min][Max]:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.AlphaLb.place(relx = 0.22, y = 20, height = 24, relwidth = 0.15, anchor = tk.NE)
    
		self.val_Alphamin = tk.DoubleVar()
		self.ent_Alphamin = tk.Entry(self.tab2, textvariable = self.val_Alphamin, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Alphamin.place(relx = 0.23, y = 20, height = 24, relwidth = 0.05)		

		self.val_Alphamax = tk.DoubleVar()
		self.ent_Alphamax = tk.Entry(self.tab2, textvariable = self.val_Alphamax, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Alphamax.place(relx = 0.3, y = 20, height = 24, relwidth = 0.05)			

		self.BetaLb = tk.Label(self.tab2, text = 'Beta[Min][Max]:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.BetaLb.place(relx = 0.22, y = 50, height = 24, relwidth = 0.15, anchor = tk.NE)
    
		self.val_Betamin = tk.DoubleVar()
		self.ent_Betamin = tk.Entry(self.tab2, textvariable = self.val_Betamin, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Betamin.place(relx = 0.23, y = 50, height = 24, relwidth = 0.05)	

		self.val_Betamax = tk.DoubleVar()
		self.ent_Betamax = tk.Entry(self.tab2, textvariable = self.val_Betamax, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Betamax.place(relx = 0.3, y = 50, height = 24, relwidth = 0.05)		

		self.RhoLb = tk.Label(self.tab2, text = 'Rho[Min][Max]:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.RhoLb.place(relx = 0.5, y = 20, height = 24, relwidth = 0.15, anchor = tk.NE)
    
		self.val_Rhomin = tk.DoubleVar()
		self.ent_Rhomin = tk.Entry(self.tab2, textvariable = self.val_Rhomin, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Rhomin.place(relx = 0.52, y = 20, height = 24, relwidth = 0.05)    

		self.val_Rhomax = tk.DoubleVar()
		self.ent_Rhomax = tk.Entry(self.tab2, textvariable = self.val_Rhomax, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Rhomax.place(relx = 0.59, y = 20, height = 24, relwidth = 0.05)   

        # ======================================== Oscillatory transient RELATED SETTINGS FRAME ======================================== #       
           	
		self.OscLb = tk.Label(self.tab3, text = 'Parameters:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.OscLb.place(relx = 0.12, y = 2, height = 24, relwidth = 0.8, anchor = tk.NE)
		
		self.TauLb = tk.Label(self.tab3, text = 'Tau [Min][Max]:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.TauLb.place(relx = 0.22, y = 20, height = 24, relwidth = 0.15, anchor = tk.NE)
    
		self.val_Taumin = tk.DoubleVar()
		self.ent_Taumin = tk.Entry(self.tab3, textvariable = self.val_Taumin, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Taumin.place(relx = 0.23, y = 20, height = 24, relwidth = 0.05)	

		self.val_Taumax = tk.DoubleVar()
		self.ent_Taumax = tk.Entry(self.tab3, textvariable = self.val_Taumax, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Taumax.place(relx = 0.3, y = 20, height = 24, relwidth = 0.05)	

		self.PeriodLb = tk.Label(self.tab3, text = 'Period [Min][Max]:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.PeriodLb.place(relx = 0.22, y = 50, height = 24, relwidth = 0.16, anchor = tk.NE)
    
		self.val_Periodmin = tk.DoubleVar()
		self.ent_Periodmin = tk.Entry(self.tab3, textvariable = self.val_Periodmin, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Periodmin.place(relx = 0.23, y = 50, height = 24, relwidth = 0.05)
    
		self.val_Periodmax = tk.DoubleVar()
		self.ent_Periodmax = tk.Entry(self.tab3, textvariable = self.val_Periodmax, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Periodmax.place(relx = 0.3, y = 50, height = 24, relwidth = 0.05)		

		self.FnLb = tk.Label(self.tab3, text = 'Fn [Min][Max]:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.FnLb.place(relx = 0.5, y = 20, height = 24, relwidth = 0.15, anchor = tk.NE)
    
		self.val_Fnmin = tk.DoubleVar()
		self.ent_Fnmin = tk.Entry(self.tab3, textvariable = self.val_Fnmin, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Fnmin.place(relx = 0.52, y = 20, height = 24, relwidth = 0.05)

		self.val_Fnmax = tk.DoubleVar()
		self.ent_Fnmax = tk.Entry(self.tab3, textvariable = self.val_Fnmax, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Fnmax.place(relx = 0.59, y = 20, height = 24, relwidth = 0.05)		

        # ======================================== FLICKER RELATED SETTINGS FRAME ======================================== #
		
		self.FlkLb = tk.Label(self.tab4, text = 'Parameters:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.FlkLb.place(relx = 0.12, y = 2, height = 24, relwidth = 0.8, anchor = tk.NE)
		
		self.FfLb = tk.Label(self.tab4, text = 'Flicker Frecuency [Min][Max] :', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.FfLb.place(relx = 0.27, y = 20, height = 24, relwidth = 0.25, anchor = tk.NE)
    
		self.val_Ffmin = tk.DoubleVar()
		self.ent_Ffmin = tk.Entry(self.tab4, textvariable = self.val_Ffmin, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Ffmin.place(relx = 0.28, y = 20, height = 24, relwidth = 0.05)		

		self.val_Ffmax = tk.DoubleVar()
		self.ent_Ffmax = tk.Entry(self.tab4, textvariable = self.val_Ffmax, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Ffmax.place(relx = 0.35, y = 20, height = 24, relwidth = 0.05)	

		self.LamndaLb = tk.Label(self.tab4, text = 'Lambda [Min][Max] :', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.LamndaLb.place(relx = 0.27, y = 50, height = 24, relwidth = 0.2, anchor = tk.NE)
    
		self.val_Lamndamin = tk.DoubleVar()
		self.ent_Lamndamin = tk.Entry(self.tab4, textvariable = self.val_Lamndamin, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Lamndamin.place(relx = 0.28, y = 50, height = 24, relwidth = 0.05)		

		self.val_Lamndamax = tk.DoubleVar()
		self.ent_Lamndamax = tk.Entry(self.tab4, textvariable = self.val_Lamndamax, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Lamndamax.place(relx = 0.35, y = 50, height = 24, relwidth = 0.05)


        # ======================================== TRANSIENT RELATED SETTINGS FRAME ======================================== #
		
		self.TrsnLb = tk.Label(self.tab6, text = 'Parameters:', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.TrsnLb.place(relx = 0.12, y = 2, height = 24, relwidth = 0.8, anchor = tk.NE)
		
		self.PsiLb = tk.Label(self.tab6, text = 'Psi [Min][Max] :', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.PsiLb.place(relx = 0.27, y = 20, height = 24, relwidth = 0.25, anchor = tk.NE)
    
		self.val_Psimin = tk.DoubleVar()
		self.ent_Psimin = tk.Entry(self.tab6, textvariable = self.val_Psimin, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Psimin.place(relx = 0.28, y = 20, height = 24, relwidth = 0.05)		

		self.val_Psimax = tk.DoubleVar()
		self.ent_Psimax = tk.Entry(self.tab6, textvariable = self.val_Psimax, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Psimax.place(relx = 0.35, y = 20, height = 24, relwidth = 0.05)	

		self.PerdLb = tk.Label(self.tab6, text = 'Lambda [Min][Max] :', font = (font_text, 10), fg = 'white', bg = color1,  anchor = tk.E)
		self.PerdLb.place(relx = 0.27, y = 50, height = 24, relwidth = 0.2, anchor = tk.NE)
    
		self.val_Perdmin = tk.DoubleVar()
		self.ent_Perdmin = tk.Entry(self.tab6, textvariable = self.val_Perdmin, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Perdmin.place(relx = 0.28, y = 50, height = 24, relwidth = 0.05)		

		self.val_Perdmax = tk.DoubleVar()
		self.ent_Perdmax = tk.Entry(self.tab6, textvariable = self.val_Perdmax, fg = 'white', font = (font_text, 10), bg = color2)
		self.ent_Perdmax.place(relx = 0.35, y = 50, height = 24, relwidth = 0.05)		

        # ======================================== CHECKBOX FOR DEFAULT PARAMETERS ======================================== #
		ParametersPQ = [self.ent_Perdmax,self.ent_Perdmin,self.ent_Psimax,self.ent_Psimin,self.ent_Alphamax,self.ent_Alphamin,self.ent_Betamax,self.ent_Betamin,self.ent_C,
				  		self.ent_Ffmax,self.ent_Ffmin,self.ent_Fnmax,self.ent_Fnmin,self.ent_Lamndamax,self.ent_Lamndamin,self.ent_Har1st,
						self.ent_Har3thmax,self.ent_Har3thmin,self.ent_Har5thmax,self.ent_Har5thmin,self.ent_Har7thmax,self.ent_Har7thmin,self.ent_Kmax,self.ent_Kmin,self.ent_Periodmax,
						self.ent_Periodmin,self.ent_Phasemax,self.ent_Phasemin,self.ent_Taumax,self.ent_Taumin,self.ent_Rhomax,self.ent_Rhomin]
				
		self.val_Random = tk.BooleanVar()
		self.Check_PQ = tk.Checkbutton(self.SttgFrame, variable = self.val_Random, text = 'Default parameters [All]',
			onvalue = True, offvalue = False, fg = 'white', bg = color1, anchor = tk.NE, command=lambda e=ParametersPQ, v=self.val_Random: self.AcivateDeactivate(e,v))
		self.Check_PQ.config(selectcolor=color1)
		self.Check_PQ.place(relx = 0.13, y = 40, height = 24, relwidth = 0.125, anchor = tk.NE)
		self.val_Random.set(True)
		self.AcivateDeactivate(ParametersPQ,self.val_Random)
		


		# =============================== SIMULATION ======================================= #
		self.Simulation = tk.LabelFrame(self.master, text = 'Simulation', font = (font_text, 10), fg = 'white', bg = color1)
		self.Simulation.place(x = 10, y = 205, relheight = 0.74, relwidth = 0.980, anchor = tk.NW)

		self.Refresh = tk.Button(self.Simulation, text = 'Refresh', font = (font_text, 10),command = self.clickrefresh, anchor = tk.CENTER)
		self.Refresh.place(relx = 0.44, rely = 0.0, height = 24, relwidth = 0.092, anchor = tk.NW)

		self.Export = tk.Button(self.Simulation, text = 'Export', font = (font_text, 10), anchor = tk.CENTER,command=self.click_EXPORT)
		self.Export.place(relx = 0.64, rely = 0.0, height = 24,  relwidth = 0.092, anchor = tk.NW)

		# NOTEBOOK FOR GRAPHICS
		self.Notebook = ttk.Notebook(self.Simulation)
		self.Notebook.place(relx = 0.005, rely = 0.06, relwidth = 0.99, relheight = 0.93, anchor = tk.NW)
		self.tab1 = tk.Frame(self.Notebook, background = 'white')
		self.Notebook.add(self.tab1, text ='Signal vizualitation')
			
	def Fig_Signals(self):

		try:
			self.canvas_sig.get_tk_widget().destroy()
			self.toolbar_sig.destroy()
		except:
			pass

		plt.style.use('dark_background')
		plt.rcParams.update({'font.size': figs_size_font})
		self.fig = plt.Figure(dpi = 100) 
		ax = self.fig.add_subplot(111)
		ax.set_xlabel('Time (s)')
		ax.set_ylabel('Magnitude')
		ax.set_facecolor('k')
		self.fig.subplots_adjust(left = 0.1, bottom = 0.23, right = 0.96, top = 0.9)
		self.canvas_sig = FigureCanvasTkAgg(self.fig, self.tab1)
		self.canvas_sig.draw() 
		self.canvas_sig.get_tk_widget().place(relheight = 1.00, relwidth = 1.00)
		self.toolbar_sig = NavigationToolbar2Tk(self.canvas_sig, self.tab1)
		self.toolbar_sig.place(relx = 0.50, rely = 1.00, relwidth = 1.00, anchor = tk.S)
		self.toolbar_sig.update()
		Signal_index = catalog.index(self.val_PQ.get())
		t = np.arange(0,self.Model.n/self.Model.f+1,1/self.Model.fs)
		if self.Model!=None:
			ax.plot(t[:len(self.Signals[0,Signal_index])],self.Signals[0,Signal_index])


	def Info(self, event = None):

		info_text =  ('''
Reference:


Authors:
Miguel Gabriel Juarez Jimenez
Alejandro Zamora Mendez
Jaime Cerda	Jacobo			

Version 0.0
June 11th, 2024
		''')
		tk.messagebox.showinfo('Information', info_text)
		

	def clickrefresh(self):
		
		self.Fig_Signals()
		
			
	def clickInizializeModel(self):
		
		if self.Cicles_val.get()< self.Duration_val.get():
			tk.messagebox.showerror('Error','The duration of event must not be greater that the duration of the signal')
		elif int(self.Cicles_val.get())-(int(self.Duration_val.get())+int(self.Start_val.get()))<0:
			tk.messagebox.showerror('Error','The start of the event must be set in order to be during the period of the signal')
		elif self.val_RandomStart.get() == False :	
			self.Model =PQ(Cicles=int(self.Cicles_val.get()),Frecuency=int(self.Freq_val.get()),FS=int(self.FS_val.get()),InicioDisturbio=int(self.Start_val.get()),PeriodoDisturbio=int(self.Duration_val.get()))	
			self.Signals =self.Model.PQaleatorio(1)
		else:
			self.Model = PQ(Cicles=int(self.Cicles_val.get()),Frecuency=int(self.Freq_val.get()),FS=int(self.FS_val.get()))
			self.Signals =self.Model.PQaleatorio(1)
		

	def clickRUN(self):
		if self.Model!=None:
			self.Fig_Signals()
			self.Signals = self.Model.PQaleatorio(1)
		else:
			tk.messagebox.showerror('Error','The model is not inizialized yet')
			self.master.lift()


	def AcivateDeactivate(self,Entradas,Variable):
		if Variable.get()==True:
			for v in Entradas:
				v.config(state='disabled')
		else:
			for v in Entradas:	
				v.config(state='normal')	

	def SetParam(self):
		ParametersPQ_val = [self.val_Phasemin.get(),self.val_Phasemax.get(),self.val_Alphamin.get(),self.val_Alphamax.get(),self.val_Betamin.get(),self.val_Betamax.get(),self.val_Rhomin.get(),self.val_Rhomax.get(),
					  self.val_Psimin.get(),self.val_Psimax.get(),self.val_Ffmin.get(),self.val_Ffmax.get(),self.val_Lamndamin.get(),self.val_Lamndamax.get(),self.val_Taumin.get(),self.val_Taumax.get(),self.val_Fnmin.get(),
					  self.val_Fnmax.get(),self.val_Perdmin.get(),self.val_Perdmax.get(),self.val_Har1st.get(),self.val_Har3thmin.get(),self.val_Har3thmax.get(),self.val_Har5thmin.get(),
					  self.val_Har5thmax.get(),self.val_Har7thmin.get(),self.val_Har7thmax.get(),self.val_Kmin.get(),self.val_Kmax.get(),self.val_C.get()]

		if self.Model!=None:
			if self.val_Random.get():
				pass
			else:
				if self.val_C.get() == 0:
					tk.messagebox.showerror('Error','The number of notches must be differet of Zero ')
					self.master.lift()
				else:
					self.Model.change_values(ParametersPQ_val)

		else:
			tk.messagebox.showerror('Error','You shoud inizialize the model before you change their values')
			self.master.destroy()

	def click_EXPORT(self):
			Window3(tk.Toplevel(self.master),model=self.Model)

	def click_EXIT(self):
		self.master.destroy()
	

class Window3():

	def __init__(self, master,model = None):

		self.master = master
		self.master.title('Export')
		self.master.geometry('1200x800')
		self.master.configure(bg = color1)
		self.frame = tk.Frame(self.master)
		self.numberSignals = None
		self.Signals = []
		self.Create_Widgets()
		self.Model = model


	def Create_Widgets(self):
		
		self.Title = tk.Label(self.master, text = 'Export', font = (font_text, 14), fg = 'white', bg = color0, anchor = tk.CENTER)
		self.Title.pack(fill = tk.X)
		self.Check_Val = {}
		self.Check_S={}

		for v in catalog:
			self.Check_Val[v] = tk.BooleanVar()
			self.Check_Val[v].set(True)
			self.Check_S[v] = tk.Checkbutton(self.master, variable = self.Check_Val[v], text = v,
				onvalue = True, offvalue = False, fg = 'white', bg = color1, anchor = tk.W)
			self.Check_S[v].config(selectcolor=color1)
			self.Check_S[v].pack(side=tk.TOP,anchor = tk.W)

		self.SignalspE = tk.Label(self.master, text = 'Signals per event :', font = (font_text, 14), fg = 'white', bg = color1)
		self.SignalspE.place(relx = 0.57, rely = 0.5, height = 24, relwidth = 0.2, anchor = tk.CENTER)
    
		self.SignalspE = tk.Entry(self.master, font = (font_text, 10))
		self.SignalspE.place(relx = 0.50, rely = 0.55, relwidth = 0.20, anchor = tk.W, height = 24) 	
		self.SignalspE.insert(0, 'Signals per event...')

		self.Save = tk.Button(self.master, text = 'SAVE', font = (font_text, 10),command = lambda:self.checkVa(self.Check_Val,False), anchor = tk.CENTER)
		self.Save.place(relx = 0.50, rely = 0.6, relwidth = 0.20, anchor = tk.W) 	

		self.Saveas = tk.Button(self.master, text = 'SAVE AS', font = (font_text, 10),command = lambda:self.checkVa(self.Check_Val,True), anchor = tk.CENTER)
		self.Saveas.place(relx = 0.50, rely = 0.65, relwidth = 0.20, anchor = tk.W) 

		# options_exp = [".npy", ".xmls", ".mat", ".csv",".txt"]
		# self.value_inside = tk.StringVar(self.master)
		# self.value_inside.set("Select Format")
		# self.question_menu = tk.OptionMenu(self.master,self.value_inside, *options_exp) 
		# self.question_menu.place(relx = 0.50, rely = 0.70, relwidth = 0.20, anchor = tk.W) 		
		


	def checkVa(self,check,withpath):
		try: 
			self.numberSignals = int(self.SignalspE.get())

		except:
			tk.messagebox.showerror('Error','The number of signals per event is incorrect')
			self.master.lift()
			return 0
			
		if isinstance(self. numberSignals, int) and self.Model != None:
			for v in catalog:
				if check[v].get():
					self.Signals += [catalog.index(v)]
			Allsig = None
			if len(self.Signals)!=29:
				Allsig = self.Model.PQselectivo(self.numberSignals,self.Signals)
			else:
				Allsig = self.Model.PQaleatorio(self.numberSignals)
				
			if withpath:
				files = [('Numpy Array', '*.npy'), 
						('Text Document', '*.txt'),
						('CSV file','*.csv'),
						('Matlab file','*.mat'),
						('Compress Numpy Array','*.npz'),
						('All Files', '*.*')] 
				file = filedialog.asksaveasfile(filetypes = files, defaultextension = files) 
				if file.name.endswith('.txt'):
					with open(file.name,'w') as outfile:
						for slice_2d in Allsig:
							np.savetxt(outfile, slice_2d)
				if file.name.endswith('.csv'):
					with open(file.name,'w', newline='') as outfile:
						writer=csv.writer(outfile, delimiter=',')
						writer.writerows(Allsig.tolist())
				if file.name.endswith('.npy'):
					np.save(file.name,Allsig)
				if file.name.endswith('.mat'):
					savemat(file.name, {'Allsig': Allsig})
				if file.name.endswith('.npz'):
					np.savez(file.name,Allsig)	
			else:
				file = filedialog.asksaveasfile(mode='w', defaultextension=".npy") 
				if file:
					np.save(file.name,Allsig)
			self.master.lift()
		else:
			tk.messagebox.showerror('Error','The model is not inizialized yet')
			self.master.destroy()


	
			

		

			

		
def main():
	root = tk.Tk()
	app	= Window1(root)
	root.mainloop()


if __name__ == '__main__':
	main()