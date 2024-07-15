from customtkinter import * 
from tkinter 							import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg 	import FigureCanvasTkAgg, NavigationToolbar2Tk
from PQmodel import PQ
import numpy as np
from scipy.io import savemat
from pandas import DataFrame
from sklearn.model_selection import train_test_split 
import joblib
from keras.models import load_model
from CTkMessagebox import CTkMessagebox
from Tools import *
from os.path import splitext


catalog=['Pure sinusoidal', 'Sag', 'Swell','Interruption','Spike',
         'Oscillatory transient','Harmonics','Harmonics with Sag', 'Harmonics with Swell',
         'Flicker', 'Flicker with Sag', 'Flicker with Swell', 'Sag with Oscillatory transient',
         'Swell with Oscillatory transient', 'Sag with Harmonics', 'Swell with Harmonics', 'Notch',
         'Harmonics with Sag with Flicker', 'Harmonics with Swell with Flicker',  'Sag with Harmonics with Flicker',
         'Swell with Harmonics with Flicker', 'Sag with Harmonics with Oscillatory transient',
         'Swell with Harmonics with Oscillatory transient', 'Harmonics with Sag with Oscillatory transient',
         'Harmonics with Swell with Oscillatory transient','Harmonics with Sag with Flicker with Oscillatory transient',
         'Harmonics with Swell with Flicker with Oscillatory transient', 'Sag with Harmonics with Flicker with Oscillatory transient',
         'Swell with Harmonics with Flicker with Oscillatory transient']

figs_size_font = 20
index=-1
tetx = ''

class Window1():

	# Main window

	global font_text
	font_text = 'TimesNewRoman'


	def __init__(self, master):
		self.master = master
		self.master.title('PQ event Toolbox')
		self.master.geometry('1300x800')
		#self.master.configure(bg = color1)
		#self.frame = CTkFrame(self.master)
		#self.frame.pack()
		self.Model = None
		self.Create_Widgets()
		self.Signals = []
		self.MLmodel = None
		self.MLpath = '' 
		self.messagPrediction = '!'

	
	def Create_Widgets(self):

		# TITLE AND INFO
		self.Title = CTkLabel(self.master, text =  'Generating Synthetic Power Quality Events Dataset', font = (font_text, 24), height = 30)
		self.Title.place(relx = 0.5, rely = 0.03,anchor =CENTER)

		self.Infobtn = CTkLabel(self.master, text = 'i', height = 30, width = 30)
		self.Infobtn.place(relx = 1.00, rely = 0.0,  anchor = NE)
		self.Infobtn.bind('<Button-1>', self.Info)
		# ======================================== SETTINGS FRAME ======================================== #
		
		self.SttgFrame = CTkFrame(self.master, height = 250) # , text = 'Settings', font = (font_text, 14)
		self.SttgFrame.place(x = 14, y = 40, relwidth = 0.980, anchor = NW)

        # ========================================  Inizialize model Button's ======================================== #
		
		self.Cicles_val = DoubleVar()
		self.CiclesLabel = CTkLabel(self.SttgFrame, text = 'Event length (Cycles):', font = (font_text, 14), height = 20)
		self.CiclesLabel.place(relx = 0.005, y = 15.0)		
		self.Cicles_val.set(10)

		self.CiclesEnt = CTkEntry(self.SttgFrame, font = (font_text, 14),textvariable=self.Cicles_val)
		self.CiclesEnt.place(relx = 0.115, y = 10.0, relwidth = 0.03)

		self.Freq_val = DoubleVar()
		self.FreqLabel = CTkLabel(self.SttgFrame, height = 20, text = 'Fund. freq. (Hz):', font = (font_text, 14))
		self.FreqLabel.place(relx = 0.15, y = 15.0)
		self.Freq_val.set(60)		
		
		self.FreqEnt = CTkEntry(self.SttgFrame, font = (font_text, 14),textvariable=self.Freq_val)
		self.FreqEnt.place(relx = 0.232, y = 10.0, relwidth = 0.03)

		self.FS_val = DoubleVar()
		self.FSLabel = CTkLabel(self.SttgFrame, height = 20, text = 'Sampling rate (Hz):', font = (font_text, 14))
		self.FSLabel.place(relx = 0.27, y = 15.0)		
		self.FS_val.set(3600)
		self.FSEnt = CTkEntry(self.SttgFrame, font = (font_text, 14),textvariable=self.FS_val)
		self.FSEnt.place(relx = 0.37, y = 10.0, relwidth = 0.045)
		
        
		self.DurationLabel = CTkLabel(self.SttgFrame, height = 20, text = 'Disturbance duration (Cycles):', font = (font_text, 14))
		self.DurationLabel.place(relx = 0.64, y = 15.0)		
		self.Duration_val = DoubleVar()
		self.DurationEnt = CTkEntry(self.SttgFrame, font = (font_text, 14),textvariable=self.Duration_val)
		self.DurationEnt.place(relx = 0.795, y = 10.0, relwidth = 0.03)
		self.Duration_val.set(5)      


		self.StartLabel = CTkLabel(self.SttgFrame, height = 20, text = 'Disturbance starting time (Cycles):', font = (font_text, 14))
		self.StartLabel.place(relx = 0.425, y = 15.0)		
		self.Start_val = DoubleVar()
		self.StartEnt = CTkEntry(self.SttgFrame, font = (font_text, 14),textvariable=self.Start_val)
		self.StartEnt.place(relx = 0.6, y = 10.0, relwidth = 0.03)
		self.Start_val.set(0)   
		
		RandomStar =[self.StartEnt,self.DurationEnt]
		self.val_RandomStart = BooleanVar()
		self.val_RandomStart.set(True)
		self.RandomStart = CTkCheckBox(self.SttgFrame, variable = self.val_RandomStart, text ='Random [Disturbance Related]',# 'Random	[Duration][Starting]', # 
			onvalue = True, offvalue = False,command=lambda e=RandomStar, v=self.val_RandomStart: self.AcivateDeactivate(e,v))
		self.RandomStart.place(relx = 0.992, y = 10.0, anchor = NE)
		self.AcivateDeactivate(RandomStar,self.val_RandomStart)                     
		        
        # ======================================== GENERAL BUTTON'S ======================================== #
		#Mover Der
		self.RUN = CTkButton(self.SttgFrame, text = 'RUN', font = (font_text, 14), height = 30,command=self.clickRUN)
		self.RUN.place(relx = 0.735, y = 75, relwidth = 0.2)
		#Mover Izq
		self.Init = CTkButton(self.SttgFrame, text = 'INITIALIZE MODEL', font = (font_text, 14),command=self.clickInizializeModel)#Initialize
		self.Init.place(relx = 0.015, y = 75)

		self.PQLb = CTkLabel(self.SttgFrame, text = 'PQ Event:', font = (font_text, 14),  anchor = NE)
		self.PQLb.place(relx = 0.735, y = 130, anchor = NW)

		self.val_PQ = StringVar()
		self.val_PQ.set(catalog[0])
		self.PQmenu = CTkOptionMenu(self.SttgFrame, variable = self.val_PQ, values = catalog,font=(font_text,14))
		self.PQmenu.place(relx = 0.735, y = 158,relwidth=0.26, anchor = NW)	


		self.Refresh = CTkButton(self.SttgFrame, text = 'REFRESH', font = (font_text, 14),command = self.clickrefresh, anchor = CENTER)
		self.Refresh.place(relx = 0.735, y =208, relwidth = 0.092, anchor = NW)

		self.Export = CTkButton(self.SttgFrame, text = 'EXPORT', font = (font_text, 14), anchor = CENTER,command=self.click_EXPORT)
		self.Export.place(relx = 0.855, y = 208,  relwidth = 0.092, anchor = NW)		


		self.tbsettings = CTkTabview(self.SttgFrame)
		self.tbsettings.place(relx = 0.18, rely = 0.25, relwidth = 0.54, relheight = 0.66, anchor = NW)		

		self.tbsettings.add( 'General')
		self.tbsettings.add( 'Harmonics')
		self.tbsettings.add( 'Sag/Swell')
		self.tbsettings.add( 'Oscillatory')
		self.tbsettings.add( 'Flicker')		
		self.tbsettings.add( 'Notch')
		self.tbsettings.add( 'Transient')		

		# ======================================== FOR ALL SIGNALS ======================================================== #
		self.GenLb = CTkLabel(master=self.tbsettings.tab( 'General'), text = 'Parameters for all signals:', font = (font_text, 14))
		self.GenLb.place(relx = 0.3, y = 2, relwidth = 2, anchor = NE)
		
		self.PhaseLb = CTkLabel(self.tbsettings.tab( 'General'), text = 'Phase [Min][Max]:', font = (font_text, 14))
		self.PhaseLb.place(relx = 0.2, y = 30, relwidth = 0.2, anchor = NE)
    
		self.val_Phasemin = DoubleVar()
		self.ent_Phasemin = CTkEntry(self.tbsettings.tab( 'General'), textvariable = self.val_Phasemin, font = (font_text, 14))
		self.ent_Phasemin.place(relx = 0.22, y = 30, relwidth = 0.1)

		self.val_Phasemax = DoubleVar()
		self.ent_Phasemax = CTkEntry(self.tbsettings.tab( 'General'), textvariable = self.val_Phasemax, font = (font_text, 14))
		self.ent_Phasemax.place(relx = 0.35, y = 30, relwidth = 0.1)	

        # ======================================== HARMONICS RELATED SETTINGS FRAME ======================================== #
		self.HarMagLb = CTkLabel(self.tbsettings.tab( 'Harmonics'), text = 'Magnitude:', font = (font_text, 14))
		self.HarMagLb.place(relx = 0.12, y = 2, relwidth = 0.8, anchor = NE)
		
		self.Har1stLb = CTkLabel(self.tbsettings.tab( 'Harmonics'), text = '1st Ord :', font = (font_text, 14))
		self.Har1stLb.place(relx = 0.2, y = 20, relwidth = 0.2, anchor = NE)
    
		self.val_Har1st = DoubleVar()
		self.ent_Har1st = CTkEntry(self.tbsettings.tab( 'Harmonics'), textvariable = self.val_Har1st, font = (font_text, 14))
		self.ent_Har1st.place(relx = 0.22, y = 20, relwidth = 0.08)

		# self.val_Har1stmax = tk.DoubleVar()
		# self.ent_Har1stmax = tk.Entry( textvariable = self.val_Har1stmax, font = (font_text, 14))
		# self.ent_Har1stmax.place(relx = 0.35, y = 20, relwidth = 0.08)		
		
		self.Har3thLb = CTkLabel(self.tbsettings.tab( 'Harmonics'), text = '3th Ord [Min][Max]:', font = (font_text, 14))
		self.Har3thLb.place(relx = 0.2, y = 50, relwidth = 0.2, anchor = NE)
    
		self.val_Har3thmin = DoubleVar()
		self.ent_Har3thmin = CTkEntry(self.tbsettings.tab( 'Harmonics'), textvariable = self.val_Har3thmin, font = (font_text, 14))
		self.ent_Har3thmin.place(relx = 0.22, y = 50, relwidth = 0.08)   

		self.val_Har3thmax = DoubleVar()
		self.ent_Har3thmax = CTkEntry(self.tbsettings.tab( 'Harmonics'), textvariable = self.val_Har3thmax, font = (font_text, 14))
		self.ent_Har3thmax.place(relx = 0.35, y = 50, relwidth = 0.08)     

		self.Har5thLb = CTkLabel(self.tbsettings.tab( 'Harmonics'), text = '5th Ord [Min][Max]:', font = (font_text, 14))
		self.Har5thLb.place(relx = 0.65, y = 20, relwidth = 0.2, anchor = NE)
    
		self.val_Har5thmin = DoubleVar()
		self.ent_Har5thmin = CTkEntry(self.tbsettings.tab( 'Harmonics'), textvariable = self.val_Har5thmin, font = (font_text, 14))
		self.ent_Har5thmin.place(relx = 0.67, y = 20, relwidth = 0.08)

		self.val_Har5thmax = DoubleVar()
		self.ent_Har5thmax = CTkEntry(self.tbsettings.tab( 'Harmonics'), textvariable = self.val_Har5thmax, font = (font_text, 14))
		self.ent_Har5thmax.place(relx = 0.8, y = 20, relwidth = 0.08)		
		
		self.Har7thLb = CTkLabel(self.tbsettings.tab( 'Harmonics'), text = '7th Ord [Min][Max]:', font = (font_text, 14))
		self.Har7thLb.place(relx = 0.65, y = 50, relwidth = 0.2, anchor = NE)

		self.val_Har7thmin = DoubleVar()
		self.ent_Har7thmin = CTkEntry(self.tbsettings.tab( 'Harmonics'), textvariable = self.val_Har7thmin, font = (font_text, 14))
		self.ent_Har7thmin.place(relx = 0.67, y = 50, relwidth = 0.08)
    
		self.val_Har7thmax = DoubleVar()
		self.ent_Har7thmax = CTkEntry(self.tbsettings.tab( 'Harmonics'), textvariable = self.val_Har7thmax, font = (font_text, 14))
		self.ent_Har7thmax.place(relx = 0.8, y = 50, relwidth = 0.08)  

		# =============================== NOTCH RELATED SETTINGS FRAME  =============================== #
		
		self.NotchLb = CTkLabel(self.tbsettings.tab( 'Notch'), text = 'Notch parameters:', font = (font_text, 14))
		self.NotchLb.place(relx = 0.2, y = 2, anchor = NE)

		self.KLb = CTkLabel(self.tbsettings.tab( 'Notch'), text = 'K[Min][Max]:', font = (font_text, 14))
		self.KLb.place(relx = 0.22, y = 22, relwidth = 0.2, anchor = NE)
    
		self.val_Kmin = DoubleVar()
		self.ent_Kmin = CTkEntry(self.tbsettings.tab( 'Notch'), textvariable = self.val_Kmin, font = (font_text, 14))
		self.ent_Kmin.place(relx = 0.32, y = 22, relwidth = 0.08, anchor = NE)

		self.val_Kmax = DoubleVar()
		self.ent_Kmax = CTkEntry(self.tbsettings.tab( 'Notch'), textvariable = self.val_Kmin, font = (font_text, 14))
		self.ent_Kmax.place(relx = 0.35, y = 22, relwidth = 0.08)		

		self.CLb = CTkLabel(self.tbsettings.tab( 'Notch'), text = 'Notches[1,2,4,6]:', font = (font_text, 14))
		self.CLb.place(relx = 0.22, y = 52, relwidth = 0.2, anchor = NE)
    
		self.val_C = DoubleVar()
		self.ent_C = CTkEntry(self.tbsettings.tab( 'Notch'), textvariable = self.val_C, font = (font_text, 14))
		self.ent_C.place(relx = 0.24, y = 50, relwidth = 0.08)

	

				
        # ======================================== SAG/SWELL RELATED SETTINGS FRAME ======================================== #
		self.SAGLb = CTkLabel(self.tbsettings.tab( 'Sag/Swell'), text = 'Parameters:', font = (font_text, 14))
		self.SAGLb.place(relx = 0.12, y = 2, relwidth = 0.8, anchor = NE)
		
		self.AlphaLb = CTkLabel(self.tbsettings.tab( 'Sag/Swell'), text = 'σ [Min][Max]:', font = (font_text, 14))
		self.AlphaLb.place(relx = 0.22, y = 20, relwidth = 0.15, anchor = NE)
    
		self.val_Alphamin = DoubleVar()
		self.ent_Alphamin = CTkEntry(self.tbsettings.tab( 'Sag/Swell'), textvariable = self.val_Alphamin, font = (font_text, 14))
		self.ent_Alphamin.place(relx = 0.23, y = 20, relwidth = 0.09)		

		self.val_Alphamax = DoubleVar()
		self.ent_Alphamax = CTkEntry(self.tbsettings.tab( 'Sag/Swell'), textvariable = self.val_Alphamax, font = (font_text, 14))
		self.ent_Alphamax.place(relx = 0.35, y = 20, relwidth = 0.09)			

		self.BetaLb = CTkLabel(self.tbsettings.tab( 'Sag/Swell'), text = 'β [Min][Max]:', font = (font_text, 14))
		self.BetaLb.place(relx = 0.22, y = 50, relwidth = 0.15, anchor = NE)
    
		self.val_Betamin = DoubleVar()
		self.ent_Betamin = CTkEntry(self.tbsettings.tab( 'Sag/Swell'), textvariable = self.val_Betamin, font = (font_text, 14))
		self.ent_Betamin.place(relx = 0.23, y = 50, relwidth = 0.09)	

		self.val_Betamax = DoubleVar()
		self.ent_Betamax = CTkEntry(self.tbsettings.tab( 'Sag/Swell'), textvariable = self.val_Betamax, font = (font_text, 14))
		self.ent_Betamax.place(relx = 0.35, y = 50, relwidth = 0.09)		

		self.RhoLb = CTkLabel(self.tbsettings.tab( 'Sag/Swell'), text = 'ρ [Min][Max]:', font = (font_text, 14))
		self.RhoLb.place(relx = 0.6, y = 20, relwidth = 0.15, anchor = NE)
    
		self.val_Rhomin = DoubleVar()
		self.ent_Rhomin = CTkEntry(self.tbsettings.tab( 'Sag/Swell'), textvariable = self.val_Rhomin, font = (font_text, 14))
		self.ent_Rhomin.place(relx = 0.62, y = 20, relwidth = 0.09)    

		self.val_Rhomax = DoubleVar()
		self.ent_Rhomax = CTkEntry(self.tbsettings.tab( 'Sag/Swell'), textvariable = self.val_Rhomax, font = (font_text, 14))
		self.ent_Rhomax.place(relx = 0.72, y = 20, relwidth = 0.09)   

        # ======================================== Oscillatory transient RELATED SETTINGS FRAME ======================================== #       
           	
		self.OscLb = CTkLabel(self.tbsettings.tab( 'Oscillatory'), text = 'Parameters:', font = (font_text, 14))
		self.OscLb.place(relx = 0.12, y = 2, relwidth = 0.8, anchor = NE)
		
		self.TauLb = CTkLabel(self.tbsettings.tab( 'Oscillatory'), text = 'τ [Min][Max]:', font = (font_text, 14))
		self.TauLb.place(relx = 0.22, y = 20, relwidth = 0.15, anchor = NE)
    
		self.val_Taumin = DoubleVar()
		self.ent_Taumin = CTkEntry(self.tbsettings.tab( 'Oscillatory'), textvariable = self.val_Taumin, font = (font_text, 14))
		self.ent_Taumin.place(relx = 0.23, y = 20, relwidth = 0.09)	

		self.val_Taumax = DoubleVar()
		self.ent_Taumax = CTkEntry(self.tbsettings.tab( 'Oscillatory'), textvariable = self.val_Taumax, font = (font_text, 14))
		self.ent_Taumax.place(relx = 0.33, y = 20, relwidth = 0.09)	

		self.PeriodLb = CTkLabel(self.tbsettings.tab( 'Oscillatory'), text = 'Period [Min][Max]:', font = (font_text, 14))
		self.PeriodLb.place(relx = 0.22, y = 50, anchor = NE)
    
		self.val_Periodmin = DoubleVar()
		self.ent_Periodmin = CTkEntry(self.tbsettings.tab( 'Oscillatory'), textvariable = self.val_Periodmin, font = (font_text, 14))
		self.ent_Periodmin.place(relx = 0.23, y = 50, relwidth = 0.09)
    
		self.val_Periodmax = DoubleVar()
		self.ent_Periodmax =CTkEntry(self.tbsettings.tab( 'Oscillatory'), textvariable = self.val_Periodmax, font = (font_text, 14))
		self.ent_Periodmax.place(relx = 0.33, y = 50, relwidth = 0.09)		

		self.FnLb = CTkLabel(self.tbsettings.tab( 'Oscillatory'), text = 'Fn [Min][Max]:', font = (font_text, 14))
		self.FnLb.place(relx = 0.6, y = 20, relwidth = 0.15, anchor = NE)
    
		self.val_Fnmin = DoubleVar()
		self.ent_Fnmin = CTkEntry(self.tbsettings.tab( 'Oscillatory'), textvariable = self.val_Fnmin, font = (font_text, 14))
		self.ent_Fnmin.place(relx = 0.62, y = 20, relwidth = 0.09)

		self.val_Fnmax = DoubleVar()
		self.ent_Fnmax = CTkEntry(self.tbsettings.tab( 'Oscillatory'), textvariable = self.val_Fnmax, font = (font_text, 14))
		self.ent_Fnmax.place(relx = 0.72, y = 20, relwidth = 0.09)		

        # ======================================== FLICKER RELATED SETTINGS FRAME ======================================== #
		
		self.FlkLb = CTkLabel(self.tbsettings.tab( 'Flicker'), text = 'Parameters:', font = (font_text, 14))
		self.FlkLb.place(relx = 0.12, y = 2, relwidth = 0.8, anchor = NE)
		
		self.FfLb = CTkLabel(self.tbsettings.tab( 'Flicker'), text = 'Flicker Frecuency [Min][Max] :', font = (font_text, 14))
		self.FfLb.place(relx = 0.3, y = 20, anchor = NE)
    
		self.val_Ffmin =  DoubleVar()
		self.ent_Ffmin = CTkEntry(self.tbsettings.tab( 'Flicker'), textvariable = self.val_Ffmin, font = (font_text, 14))
		self.ent_Ffmin.place(relx = 0.31, y = 20, relwidth = 0.09)		

		self.val_Ffmax = DoubleVar()
		self.ent_Ffmax = CTkEntry(self.tbsettings.tab( 'Flicker'), textvariable = self.val_Ffmax, font = (font_text, 14))
		self.ent_Ffmax.place(relx = 0.41, y = 20, relwidth = 0.09)	

		self.LamndaLb = CTkLabel(self.tbsettings.tab( 'Flicker'), text = 'λ [Min][Max] :', font = (font_text, 14))
		self.LamndaLb.place(relx = 0.3, y = 50, anchor = NE)
    
		self.val_Lamndamin =  DoubleVar()
		self.ent_Lamndamin = CTkEntry(self.tbsettings.tab( 'Flicker'), textvariable = self.val_Lamndamin, font = (font_text, 14))
		self.ent_Lamndamin.place(relx = 0.31, y = 50, relwidth = 0.09)		

		self.val_Lamndamax =  DoubleVar()
		self.ent_Lamndamax = CTkEntry(self.tbsettings.tab( 'Flicker'), textvariable = self.val_Lamndamax, font = (font_text, 14))
		self.ent_Lamndamax.place(relx = 0.41, y = 50, relwidth = 0.09)


        # ======================================== TRANSIENT RELATED SETTINGS FRAME ======================================== #
		
		self.TrsnLb = CTkLabel(self.tbsettings.tab( 'Transient'), text = 'Parameters:', font = (font_text, 14))
		self.TrsnLb.place(relx = 0.12, y = 2, relwidth = 0.8, anchor = NE)
		
		self.PsiLb = CTkLabel(self.tbsettings.tab( 'Transient'), text = 'ψ [Min][Max] :', font = (font_text, 14))
		self.PsiLb.place(relx = 0.27, y = 20, relwidth = 0.25, anchor = NE)
    
		self.val_Psimin =  DoubleVar()
		self.ent_Psimin = CTkEntry(self.tbsettings.tab( 'Transient'), textvariable = self.val_Psimin, font = (font_text, 14))
		self.ent_Psimin.place(relx = 0.28, y = 20, relwidth = 0.09)		

		self.val_Psimax =  DoubleVar()
		self.ent_Psimax = CTkEntry(self.tbsettings.tab( 'Transient'), textvariable = self.val_Psimax, font = (font_text, 14))
		self.ent_Psimax.place(relx = 0.38, y = 20, relwidth = 0.09)	

		self.PerdLb = CTkLabel(self.tbsettings.tab( 'Transient'), text = 'Period [Min][Max] :', font = (font_text, 14))
		self.PerdLb.place(relx = 0.27, y = 50, relwidth = 0.2, anchor = NE)
    
		self.val_Perdmin = DoubleVar()
		self.ent_Perdmin = CTkEntry(self.tbsettings.tab( 'Transient'), textvariable = self.val_Perdmin, font = (font_text, 14))
		self.ent_Perdmin.place(relx = 0.28, y = 50, relwidth = 0.09)		

		self.val_Perdmax =  DoubleVar()
		self.ent_Perdmax = CTkEntry(self.tbsettings.tab( 'Transient'), textvariable = self.val_Perdmax, font = (font_text, 14))
		self.ent_Perdmax.place(relx = 0.38, y = 50, relwidth = 0.09)		

        # ======================================== CHECKBOX FOR DEFAULT PARAMETERS ======================================== #
		ParametersPQ = [self.ent_Perdmax,self.ent_Perdmin,self.ent_Psimax,self.ent_Psimin,self.ent_Alphamax,self.ent_Alphamin,self.ent_Betamax,self.ent_Betamin,self.ent_C,
				  		self.ent_Ffmax,self.ent_Ffmin,self.ent_Fnmax,self.ent_Fnmin,self.ent_Lamndamax,self.ent_Lamndamin,self.ent_Har1st,
						self.ent_Har3thmax,self.ent_Har3thmin,self.ent_Har5thmax,self.ent_Har5thmin,self.ent_Har7thmax,self.ent_Har7thmin,self.ent_Kmax,self.ent_Kmin,self.ent_Periodmax,
						self.ent_Periodmin,self.ent_Phasemax,self.ent_Phasemin,self.ent_Taumax,self.ent_Taumin,self.ent_Rhomax,self.ent_Rhomin]
		#Mover Izq		
		self.val_Random =  BooleanVar()
		self.Check_PQ = CTkCheckBox(self.SttgFrame, variable = self.val_Random, text = 'Default parameters',
			onvalue = True, offvalue = False, command=lambda e=ParametersPQ, v=self.val_Random: self.AcivateDeactivate(e,v),font=(font_text,14))
		self.Check_PQ.place(relx = 0.15, y = 125, anchor = NE)
		self.val_Random.set(True)
		self.AcivateDeactivate(ParametersPQ,self.val_Random)
		#Mover Izq
		self.Refreshsttbtn = CTkButton(self.SttgFrame, text = 'CHANGE PARAMETERS', font = (font_text, 14), anchor = CENTER,command=self.ChangeParam)
		self.Refreshsttbtn.place(relx = 0.015, y = 170, anchor = NW)			


		# # =============================== SIMULATION ======================================= #

		# NOTEBOOK FOR GRAPHICS
		self.Notebook = CTkTabview(self.master)
		self.Notebook.place(x = 14, y = 290, relheight = 0.63, relwidth = 0.980, anchor = NW)
		self.Notebook.add( 'Signal vizualitation')
		self.Notebook.add( 'FFT')
		self.Notebook.add( 'Machine Learning')

		self.FileMLModel = CTkButton(self.Notebook.tab('Machine Learning'), text = 'File', font = (font_text, 14), anchor = CENTER,command=self.LoadPredictML)
		self.FileMLModel.place(relx = 0.075, y = 10, anchor = NW)		

		self.val_entModel =  StringVar()
		self.entModel = CTkEntry(self.Notebook.tab('Machine Learning'), font = (font_text, 14),textvariable = self.val_entModel)
		self.entModel.place(relx = 0.2, y = 10, relwidth = 0.45)
		self.val_entModel.set('Select machine learning file...')

		self.PredictModel = CTkButton(self.Notebook.tab('Machine Learning'), text = 'Predict', font = (font_text, 14), anchor = CENTER,command=self.clickpredictML)
		self.PredictModel.place(relx = 0.77, y = 10, anchor = NW)

		self.PredLbl = CTkLabel(self.Notebook.tab('Machine Learning'),text =' ', font = (font_text, 22))
		self.PredLbl.place(relx = 0.05, y = 80, anchor = NW)

	def clickpredictML(self):
		self.PredLbl.configure(text='')
		if self.Model!=None and self.MLmodel !=None:
			Signal_index = catalog.index(self.val_PQ.get())
			if self.MLpath.endswith('.pkl'):
				Pred = int(self.MLmodel.predict(FeatExtraction(self.Signals[0,Signal_index]).reshape(1,6)))
				self.messagPrediction ='The type of event the signal contains is ' + catalog[Pred] +' you can vizualise the signal in the window tab \"Signal vizualization\"' #'The type of event the signal contains is ' # catalog[Pred] #
				self.slide()

			if self.MLpath.endswith('.h5'):
				Signal_List = [1,2,3,4,5,6,9,16] 
				Pred = Signal_List[int(np.argmax(self.MLmodel.predict(self.Signals[0,Signal_index].reshape(1,-1,1))))]
				self.messagPrediction ='The type of event the signal contains is ' + catalog[Pred] +' you can vizualise the signal in the window tab \"Signal vizualization\"' #'The type of event the signal contains is ' # catalog[Pred] #
				self.slide()				
		else:
			CTkMessagebox(title="Error", 
                  message="The PQ model or the Machine Learning model are not inizialized yet",
				  icon='cancel')
			
	def slide(self):
		global index,tetx
		if index>=len(self.messagPrediction)-1:
			index=-1
			tetx = ' '
		else:
			tetx += self.messagPrediction[index+1]
			self.PredLbl.configure(text=tetx)
			index+=1
			self.PredLbl.after(60,self.slide)
	
	def LoadPredictML(self):

		self.MLpath = filedialog.askopenfilename(title		='Select a Machine Learning Model',
		                          	   		   filetype		=[('Machine Learning files', '*.pkl'),('Tensor Flow files', '*.h5')])
				
		self.val_entModel.set(self.MLpath)
		if self.MLpath.endswith('.pkl'):
			self.MLmodel = joblib.load(self.MLpath)			
		elif self.MLpath.endswith('.h5'):
			self.MLmodel = load_model(self.MLpath)
		else:
			CTkMessagebox(title="Error", 
                  message="The format is not supported",
				  icon='cancel')
			
	def Fig_Signals(self):

		try:
			self.canvas_sig.get_tk_widget().destroy()
			self.toolbar_sig.destroy()
		except:
			pass

		plt.style.use('dark_background')
		plt.rcParams.update({'font.size': figs_size_font})
		self.fig = plt.Figure(dpi = 140) 
		ax = self.fig.add_subplot(111)
		ax.set_xlabel('Time (s)')
		ax.set_ylabel('Magnitude')
		ax.set_facecolor('k')
		self.fig.subplots_adjust(left = 0.1, bottom = 0.23, right = 0.96, top = 0.9)
		self.canvas_sig = FigureCanvasTkAgg(self.fig,self.Notebook.tab('Signal vizualitation')) 
		self.canvas_sig.draw() 
		self.canvas_sig.get_tk_widget().place(relheight = 1.00, relwidth = 1.00)
		self.toolbar_sig = NavigationToolbar2Tk(self.canvas_sig,self.Notebook.tab('Signal vizualitation')) 
		self.toolbar_sig.place(relx = 0.50, rely = 1.00, relwidth = 1.00, anchor = S)
		self.toolbar_sig.update()
		Signal_index = catalog.index(self.val_PQ.get())
		t = self.Model.t # np.arange(0,self.Model.n/self.Model.f+1,1/self.Model.fs)
		if self.Model!=None:
			ax.grid( linestyle = '--', linewidth = 0.5)
			ax.plot(t[:len(self.Signals[0,Signal_index])],self.Signals[0,Signal_index])

	def Fig_FFT(self):

		try:
			self.canvas_fft.get_tk_widget().destroy()
			self.toolbar_fft.destroy()
		except:
			pass

		plt.style.use('dark_background')
		plt.rcParams.update({'font.size': figs_size_font})
		self.fft = plt.Figure(dpi = 140) 
		ax = self.fft.add_subplot(111)
		ax.set_xlabel('Frequency (Hz)')
		ax.set_ylabel('Amplitude')
		ax.set_facecolor('k')
		self.fft.subplots_adjust(left = 0.1, bottom = 0.23, right = 0.96, top = 0.9)
		self.canvas_fft = FigureCanvasTkAgg(self.fft,self.Notebook.tab('FFT')) 
		self.canvas_fft.draw() 
		self.canvas_fft.get_tk_widget().place(relheight = 1.00, relwidth = 1.00)
		self.toolbar_fft = NavigationToolbar2Tk(self.canvas_fft,self.Notebook.tab('FFT')) 
		self.toolbar_fft.place(relx = 0.50, rely = 1.00, relwidth = 1.00, anchor = S)
		self.toolbar_fft.update()
		Signal_index = catalog.index(self.val_PQ.get())
		t = self.Model.t # np.arange(0,self.Model.n/self.Model.f+1,1/self.Model.fs)
		if self.Model!=None:
			X = np.abs(np.fft.fft(self.Signals[0,Signal_index]))
			N = len(X)
			n = np.arange(N)
			T= N/self.Model.fs
			freq = n/T
			ax.grid(color = 'green', linestyle = '--', linewidth = 0.5)
			ax.stem(freq,X/(N/2),"g" ,\
			basefmt="-g")
			ax.set_xlim([0,self.Model.f*8])


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
		messagebox.showinfo('Information', info_text)
		

	def clickrefresh(self):
		self.Fig_FFT()
		self.Fig_Signals()
		
			
	def clickInizializeModel(self):
		
		if self.Cicles_val.get()< self.Duration_val.get():
			messagebox.showerror('Error','The duration of event must not be greater that the duration of the signal')
		elif int(self.Cicles_val.get())-(int(self.Duration_val.get())+int(self.Start_val.get()))<0:
			messagebox.showerror('Error','The start of the event must be set in order to be during the period of the signal')
		elif self.val_RandomStart.get() :
			self.Model = PQ(Cicles=int(self.Cicles_val.get()),Frecuency=int(self.Freq_val.get()),FS=int(self.FS_val.get()))
			self.Signals =self.Model.PQaleatorio(1)	
			self.SetParam()
		else:
			self.Model =PQ(Cicles=int(self.Cicles_val.get()),Frecuency=int(self.Freq_val.get()),FS=int(self.FS_val.get()),InicioDisturbio=int(self.Start_val.get()),PeriodoDisturbio=int(self.Duration_val.get()))	
			self.Signals =self.Model.PQaleatorio(1)
			self.SetParam()
		

	def clickRUN(self):
		if self.Model!=None:
			self.Signals = self.Model.PQaleatorio(1)
			self.Fig_Signals()
			self.Fig_FFT()			
		else:
			messagebox.showerror('Error','The model is not inizialized yet')
			# self.master.lift()


	def AcivateDeactivate(self,Entradas,Variable):
		if Variable.get()==True:
			for v in Entradas:
				v.configure(state='disabled')
		else:
			for v in Entradas:	
				v.configure(state='normal')	

	def SetParam(self):
		self.val_Phasemin.set(self.Model.phase_min)
		self.val_Phasemax.set(self.Model.phase_max)
		self.val_Alphamin.set(self.Model.alpha_min)
		self.val_Alphamax.set(self.Model.alpha_max)
		self.val_Betamin.set(self.Model.beta_min)
		self.val_Betamax.set(self.Model.beta_max)
		self.val_Rhomin.set(self.Model.rho_min)
		self.val_Rhomax.set(self.Model.rho_max)
		self.val_Psimin.set(self.Model.psi_min)
		self.val_Psimax.set(self.Model.psi_max)
		self.val_Ffmin.set(self.Model.ff_min)
		self.val_Ffmax.set(self.Model.ff_max)
		self.val_Lamndamin.set(self.Model.lambda_min)
		self.val_Lamndamax.set(self.Model.lambda_max)
		self.val_Taumin.set(self.Model.tau_min)
		self.val_Taumax.set(self.Model.tau_max)
		self.val_Fnmin.set(self.Model.fn_min)
		self.val_Fnmax.set(self.Model.fn_max)
		self.val_Perdmin.set(self.Model.taPeriod_min)
		self.val_Perdmax.set(self.Model.taPeriod_max)
		self.val_Periodmin.set(self.Model.periodMinOT)
		self.val_Periodmax.set(self.Model.periodMaxOT)
		self.val_Har1st.set(self.Model.alpha1)
		self.val_Har3thmin.set(self.Model.alpha3_min)
		self.val_Har3thmax.set(self.Model.alpha3_max)
		self.val_Har5thmin.set(self.Model.alpha5_min)
		self.val_Har5thmax.set(self.Model.alpha5_max)
		self.val_Har7thmin.set(self.Model.alpha7_min)
		self.val_Har7thmax.set(self.Model.alpha7_max)
		self.val_Kmin.set(self.Model.k_min)
		self.val_Kmax.set(self.Model.k_max)
		#self.val_C.set(self.Model.c)
					

	def ChangeParam(self):
		ParametersPQ_val = [self.val_Phasemin.get(),self.val_Phasemax.get(),self.val_Alphamin.get(),self.val_Alphamax.get(),self.val_Betamin.get(),self.val_Betamax.get(),self.val_Rhomin.get(),self.val_Rhomax.get(),
					  self.val_Psimin.get(),self.val_Psimax.get(),self.val_Ffmin.get(),self.val_Ffmax.get(),self.val_Lamndamin.get(),self.val_Lamndamax.get(),self.val_Taumin.get(),self.val_Taumax.get(),self.val_Fnmin.get(),
					  self.val_Fnmax.get(),self.val_Periodmin.get(),self.val_Periodmax.get(),self.val_Har1st.get(),self.val_Har3thmin.get(),self.val_Har3thmax.get(),self.val_Har5thmin.get(),
					  self.val_Har5thmax.get(),self.val_Har7thmin.get(),self.val_Har7thmax.get(),self.val_Kmin.get(),self.val_Kmax.get(),self.val_C.get(),self.val_Perdmin.get(),
					  self.val_Perdmax.get()]

		if self.Model!=None:
			if self.val_Random.get():
				pass
			else:
				if self.val_C.get() == 0:
					messagebox.showerror('Error','The number of notches must be differet of Zero ')
				else:
					self.Model.change_values(ParametersPQ_val)

		else:
			messagebox.showerror('Error','You shoud inizialize the model before you change their values')
			self.master.destroy()

	def click_EXPORT(self):
			Window3(CTkToplevel(self.master),model=self.Model)
	

class Window3():

	def __init__(self, master,model = None):

		self.master = master
		self.master.title('Export')
		self.master.geometry('1200x800')
		self.numberSignals = None
		self.Signals = []
		self.Create_Widgets()
		self.Model = model
		self.master.attributes('-topmost',0)
		self.master.grab_set()
		


	def Create_Widgets(self):
		
		self.Title = CTkLabel(self.master, text = 'Export', font = (font_text, 14))
		self.Title.pack(fill = X)
		self.Check_Val = {}
		self.Check_S={}

		for v in catalog:
			self.Check_Val[v] = BooleanVar()
			self.Check_Val[v].set(True)
			self.Check_S[v] = CTkCheckBox(self.master, variable = self.Check_Val[v], text = v,
				onvalue = True, offvalue = False)
			
			self.Check_S[v].pack(padx= 20,pady=1,side= TOP,anchor = W)

		self.SignalspE = CTkLabel(self.master, text = 'Signals per event :', font = (font_text, 14))
		self.SignalspE.place(relx = 0.57, rely = 0.5, relwidth = 0.2, anchor = CENTER)
    
		self.SignalspE = CTkEntry(self.master, font = (font_text, 14))
		self.SignalspE.place(relx = 0.50, rely = 0.55, relwidth = 0.20, anchor = W) 	
		self.SignalspE.insert(0, 'Signals per event...')

		self.SignalspE = CTkEntry(self.master, font = (font_text, 14))
		self.SignalspE.place(relx = 0.50, rely = 0.55, relwidth = 0.20, anchor = W) 	
		self.SignalspE.insert(0, 'Signals per event...')

		self.Split = CTkLabel(self.master, text = 'Split percentage :', font = (font_text, 14))
		self.Split.place(relx = 0.57, rely = 0.4, relwidth = 0.2, anchor = CENTER)
		self.Split_val = DoubleVar()
		self.Split_entry = CTkEntry(self.master, font = (font_text, 14),textvariable=self.Split_val)
		self.Split_entry.place(relx = 0.50, rely = 0.45, relwidth = 0.20, anchor = W) 	
		self.Split_val.set(1.0)

		self.Save = CTkButton(self.master, text = 'SAVE', font = (font_text, 14),command = lambda:self.checkVa(self.Check_Val,False), anchor = CENTER)
		self.Save.place(relx = 0.50, rely = 0.6, relwidth = 0.20, anchor = W) 	

		self.Saveas = CTkButton(self.master, text = 'SAVE AS', font = (font_text, 14),command = lambda:self.checkVa(self.Check_Val,True), anchor = CENTER)
		self.Saveas.place(relx = 0.50, rely = 0.65, relwidth = 0.20, anchor = W) 
		
		
		self.Select = CTkButton(self.master, text = 'Select All', font = (font_text, 14),command = lambda:self.dnsall(True), anchor = CENTER)
		self.Select.place(relx = 0.50, rely = 0.3, relwidth = 0.20, anchor = W) 	

		self.Deselect = CTkButton(self.master, text = 'Deselect All', font = (font_text, 14),command = lambda:self.dnsall(False), anchor = CENTER)
		self.Deselect.place(relx = 0.50, rely = 0.35, relwidth = 0.20, anchor = W)

	def checkVa(self,check,withpath):
		try: 
			self.numberSignals = int(self.SignalspE.get())
			splt = int(self.Split_val.get())

		except:
			messagebox.showerror('Error','The number of signals per event is incorrect')
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

			a,b,c=Allsig.shape

			Allsig = Allsig.reshape(a*b,c)
			Dataset = DataFrame(Allsig)
			labels = DataFrame( self.Signals*self.numberSignals)
			Dataset.insert(0,'Label',labels,True)

			train, test = train_test_split(Dataset, test_size = splt)

			if withpath:
				files = [('Numpy Array', '*.npy'), 
						('Text Document', '*.txt'),
						('CSV file','*.csv'),
						('Matlab file','*.mat'),
						('Compress Numpy Array','*.npz'),
						('All Files', '*.*')] 
				file = filedialog.asksaveasfile(filetypes = files, defaultextension = files,initialfile='Test_') 
				if file.name.endswith('.txt'):
					path_test = splitext(file.name)[0]+'_test.csv'
					path_train = splitext(file.name)[0]+'_train.csv'
					np.savetxt(file.name,Dataset)
					np.savetxt(path_test,test)
					np.savetxt(path_train,train)
				
				if file.name.endswith('.csv'):
					Dataset.to_csv(file.name,header=None,index=False)
					path_test = splitext(file.name)[0]+'_test.csv'
					path_train = splitext(file.name)[0]+'_train.csv'
					frame_test = DataFrame(test)
					frame_train = DataFrame(train)
					frame_test.to_csv(path_test,header=None,index=False)
					frame_train.to_csv(path_train,header=None,index=False)
		
				if file.name.endswith('.npy'):
					path_test = splitext(file.name)[0]+'_test.npy'
					path_train = splitext(file.name)[0]+'_train.npy'
					np.save(path_test, test)
					np.save(path_train, train)
					np.save(file.name,Dataset)
	

				if file.name.endswith('.mat'):
					path_test = splitext(file.name)[0]+'_test.npy'
					path_train = splitext(file.name)[0]+'_train.npy'
					savemat(file.name, {'Allsig': Dataset})
					savemat(path_test, {'test':test})
					savemat(path_train, {'train':train})					


				if file.name.endswith('.npz'):						
					path_test = splitext(file.name)[0]+'_test.npy'
					path_train = splitext(file.name)[0]+'_train.npy'
					np.savez(path_test, test)
					np.savez(path_train, train)
					np.savez(file.name,Dataset)	
									
			else:
				file = filedialog.asksaveasfile(mode='w', defaultextension=".npy") 
				if file:
					path_test = splitext(file.name)[0]+'_test.npy'
					path_train = splitext(file.name)[0]+'_train.npy'
					np.save(path_test, test)
					np.save(path_train, train)
					np.save(file.name,Dataset)
		else:
			messagebox.showerror('Error','The model is not inizialized yet')
			self.master.destroy()

	def dnsall(self,value):
		for v in catalog:
			self.Check_Val[v].set(value)		



	
		
def main():
	set_appearance_mode("System") 
	set_default_color_theme("Themes\metal.json")
	root = CTk()
	app	= Window1(root)
	root.mainloop()


if __name__ == '__main__':
	main()