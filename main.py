#!/usr/bin/env python


#############################################################################################################
#############################################################################################################
########       Copyright  Karl Grammer Department of Anthropology/ University of Vienna         #############
#############################################################################################################
########                                                                                        #############
########                       MOULAY ISMAEL THE BLOODTHIRSTY      1.5                          #############
########                                                                                        #############
########                developped on OS X 10.8 Python 2.72 ( not tested under Windows)          #############
########                            GNU General Public License                                  #############
########                            Programmed in Komodo by Active State                        #############
#############################################################################################################
#############################################################################################################
########  There are two models implemented:                                                     #############
########  Random: females are selected randomly from a pool of haremsize - the results          #############
########          are number of copulations a day which are necessary to reach the number       #############
########          of children  (R)                                                              #############
########  Harem:  simulates the complete reproductive live span on a day to day basis           #############
########          with a given number of copulations  a day                                     #############
########          - women's cycles are also updated - the result is  the number of children (H) #############
#############################################################################################################
#############################################################################################################
########                                      VARIABLES                                         #############
########                                                                                        #############
########     self.tabu                        Number of days where sex is tabu (R,H)            #############
########     self.detection_probability       Probability of Ovulationdetection 0-100 (R,H)     #############
########     self.fertile                     Female Fertility rate 0-100  (R,H)                #############
########     self.survival                    Probability of child survival 0-100  (R,H)        #############
########     self.iterations                  Number of iterations in simulation (R,H)          #############
########     self.children                    Number of children  (R,H)                         #############
########     self.miss                        Misscariage rate (R,H)                            #############
########     self.reproductive_span           Reproductive span in years  (R,H)                 #############
########     self.haremsize                   Haremsize (H)                                     #############
########     self.ovusync                     Percentage of synchronized females in harem 0-100 (H)  ########
########     self.relationshipprob            Probability that a relationship starts  (H)       #############
########     self.relationshipdur             Relationshipduration in days (H)                  #############
########     self.favouritesprob              Probability that a woman becomes a favourite (H)  #############
########     self.favouritesnum               Number of favourites allowed (usually seven) (H)  #############
########     self.copaday                     Number of copulations a day (H)                   #############
########     self.spermvitality               Sperm vitality  (H)    0.7% a year                #############
########     self.coppreg                     Copulations during pregnancy - days (H)           #############
########     self.lact                        lactation time - no fertile cycles  (H)           #############
########     self.spermlifetime               sperm fertility decrasse 1.52% per year (H)       #############
#############################################################################################################
#############################################################################################################
######### Wilcox conception probabilities
######### self.concprobW = [0.0, 0.0, 0.0, 0.00, 0.00, 0.00, 0.00, 0.00, 0.10, 0.16, 0.14, 0.27,  0.31,  0.33,  0.01,  0.00,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
######### Joechle conception probabilities
######### self.concprobR = [0.0, 0.0, 0.0, 0.00, 0.17, 0.17, 0.30, 0.30, 0.24, 0.30, 0.33, 0.41, 0.28,  0.27,  0.11,  0.05,  0.03,0.03,0.03,0.02,0.05,0.05,0.01,0.0,0.0,0.0,0.0]
######### Barret Marshal conception probabilities
######### self.concprobS = [0.0, 0.0, 0.0, 0.00, 0.00, 0.00, 0.00, 0.00, 0.04, 0.14, 0.20, 0.20, 0.34,  0.14,  0.07,  0.00,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]



from Tkinter import *
import Tkinter, tkFileDialog
import os
import string
import tkMessageBox
import math
import random
import matplotlib.pyplot as plt
import numpy as np
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import rcParams
# rcParams.update( {
# 'font.name' : 'Verdana'
# })



window_title="MOULAY"
class App:
    def __init__(self, master,window_title):
        
        self.framebg="#999999"
        self.listextfg="#000000"
        self.buttonfg="#000000"
        self.listfont='Verdana'
        self.listfontsize=9
        self.labelfont='Verdana'
        self.labelfontsize=9
        self.buttonfont='Verdana'
        self.buttonfontsize=9
        
        
        
        self.master = master
        self.frame = Tkinter.Frame(master, relief=Tkinter.GROOVE, borderwidth=2)
        self.frame.grid(row=1,column=1, sticky=Tkinter.E+Tkinter.W+Tkinter.N+Tkinter.S)
        
        self.frame_1 = Tkinter.Frame(master, relief=Tkinter.GROOVE, borderwidth=2)
        self.frame_1.grid(row=0,column=0, sticky=Tkinter.E+Tkinter.W+Tkinter.N+Tkinter.S)
        
        self.frame_2 = Tkinter.Frame(master, relief=Tkinter.GROOVE, borderwidth=2, bg=self.framebg)
        self.frame_2.grid(row=0,column=1, sticky=Tkinter.E+Tkinter.W+Tkinter.N+Tkinter.S)
        
        self.frame_3 = Tkinter.Frame(master, relief=Tkinter.GROOVE, borderwidth=2, bg=self.framebg)
        self.frame_3.grid(row=0,column=3, sticky=Tkinter.E+Tkinter.W+Tkinter.N+Tkinter.S)
        
        
        self.frame_4 = Tkinter.Frame(self.frame_2, relief=Tkinter.GROOVE, borderwidth=2, bg=self.framebg)
        self.frame_4.grid(row=12,column=0, columnspan =10, sticky=S)
        
        self.frame_5 = Tkinter.Frame(self.frame_2, relief=Tkinter.GROOVE, borderwidth=2, bg=self.framebg)
        self.frame_5.grid(row=22,column=0, columnspan =10, sticky=S)
        
        #######################################################################################BUTTONS
        
        self.ButtonOpen = Tkinter.Button(self.frame_1, height=2,width = 10, text="QUIT", command=self.Quit, font=(self.buttonfont,self.buttonfontsize,'bold'))
        self.ButtonOpen.grid(row =20, column=1, padx=1, pady=4,sticky=Tkinter.W)
        
        ############ test random model results in average copulations a day for number of children
        self.ButtonProcess_1 = Tkinter.Button(self.frame_1, height=2,width = 10, text="OPEN POOL", command=self.moulay, font=(self.buttonfont,self.buttonfontsize,'bold')) ############ test random model results in average copulations a day for number of children
        self.ButtonProcess_1.grid(row =1, column=1, padx=1, pady=4,sticky=Tkinter.W)
        
        ############ test a life cycle with n copulations a day
        self.ButtonProcess_1 = Tkinter.Button(self.frame_1, height=2,width = 10, text="HAREM POOL", command=self.moulay_harem, font=(self.buttonfont,self.buttonfontsize,'bold')) 
        self.ButtonProcess_1.grid(row =2, column=1, padx=1, pady=4,sticky=Tkinter.W)

        

        ####################################################################################### BASIC  ENTRIES
        ####################################################################################### BASIC  ENTRIES
        ####################################################################################### BASIC  ENTRIES  
        #######################################################################################LABELS
        self.literations=Label(self.frame_2,text='ITERATIONS',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold'))               ########## Iterations of the simulation - the more the better - (BOTH)
        self.lchildren=Label(self.frame_2,text='CHILDREN',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold'))                   ########## Number of children to produce (OPEN POOL) 
        self.lreproductive_span=Label(self.frame_2,text='REPRODUCTIVE SPAN',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold')) ########## Reproductive Span in years    (HAREM)   
        self.ltabu=Label(self.frame_2,text='TABU 1-27',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold'))                      ########## Days of copulation avoidance during menses (BOTH)
        self.ldetection=Label(self.frame_2,text='OVULATION DETECTION 0-100',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold')) ########## Probability of Ovulation detection (BOTH)
        self.lmiss=Label(self.frame_2,text='MISSCARRIAGE 0-100',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold'))             ########## Probability of misscarriage (BOTH)
        self.lfertile=Label(self.frame_2,text='FERTILE 0-100',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold'))               ########## Probability of misscarriage  (BOTH)
        self.lsurvival=Label(self.frame_2,text='SURVIVAL 0-100',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold'))             ########## Probability of children survival the first two years (BOTH)
       
        
        #######################################################################################LABELSGRID
        self.literations.grid(row =1, column=2, padx=2, pady=1,sticky=N)
        self.lchildren.grid(row =2, column=2, padx=2, pady=1,sticky=N)
        self.lreproductive_span.grid(row =4, column=2, padx=2, pady=1,sticky=N) 
        
        self.ltabu.grid(row =1, column=4, padx=2, pady=1,sticky=N)
        self.ldetection.grid(row =2, column=4, padx=2, pady=1,sticky=N)
        self.lfertile.grid(row =3, column=4, padx=2, pady=1,sticky=N)
        self.lmiss.grid(row =4, column=4, padx=2, pady=1,sticky=N)
        self.lsurvival.grid(row =5, column=4, padx=2, pady=1,sticky=N)   
        
        
         #######################################################################################ENTRIES
        self.entryshadow=Entry(self.frame_1,width=5,font=(self.labelfont,self.labelfontsize))
        self.eiterations=Entry(self.frame_2,width=5,font=(self.labelfont,self.labelfontsize,'bold'))
        self.echildren=Entry(self.frame_2,width=5,font=(self.labelfont,self.labelfontsize,'bold'))
        self.ereproductive_span=Entry(self.frame_2,width=5,font=(self.labelfont,self.labelfontsize,'bold'))
        
        self.etabu=Entry(self.frame_2,width=5,font=(self.labelfont,self.labelfontsize,'bold'))
        self.edetection=Entry(self.frame_2,width=5,font=(self.labelfont,self.labelfontsize,'bold'))
        self.efertile=Entry(self.frame_2,width=5,font=(self.labelfont,self.labelfontsize,'bold'))
        self.emiss=Entry(self.frame_2,width=5,font=(self.labelfont,self.labelfontsize,'bold'))
        self.esurvival=Entry(self.frame_2,width=5,font=(self.labelfont,self.labelfontsize,'bold'))
       
        
         #######################################################################################ENTRIES GRID
        self.eiterations.grid(row =1, column=3, padx=2, pady=1,sticky=N)
        self.echildren.grid(row =2, column=3, padx=2, pady=1,sticky=N)
        self.ereproductive_span.grid(row =4, column=3, padx=2, pady=1,sticky=N) 
        
        self.etabu.grid(row =1, column=5, padx=2, pady=1,sticky=N)
        self.edetection.grid(row =2, column=5, padx=2, pady=1,sticky=N)
        self.efertile.grid(row =3, column=5, padx=2, pady=1,sticky=N)
        self.emiss.grid(row =4, column=5, padx=2, pady=1,sticky=N) 
        self.esurvival.grid(row =5, column=5, padx=2, pady=1,sticky=N)  
        
        
       #######################################################################################ENTRIES INSERT START VALUES
        self.eiterations.insert(END, '10')
        self.echildren.insert(END, '1171')
        self.ereproductive_span.insert(END, '32')
        
        self.etabu.insert(END, '0')
        self.edetection.insert(END, '0')
        self.efertile.insert(END, '100')
        self.emiss.insert(END, '100')
        self.esurvival.insert(END, '100')
      
        
        ############################################################################################# Harem entries
        ############################################################################################# Harem entries
        ############################################################################################# Harem entries
        ############################################################################################# Harem entries
        
        self.lharemsize=Label(self.frame_5,text='HAREMSIZE',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold'))                    ################## Haremsize affects both simulations !!!!!! (BOTH)
        self.lovusync=Label(self.frame_5,text='OVU SYNC 0-100',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold'))                 ################## Percentage of how many females are synchronized (HAREM)
        self.lrelationshipprop=Label(self.frame_5,text='RELATIONSHIP PROB',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold'))     ################## Probability that a long term relation is started (HAREM)
        self.lrelationshipdur=Label(self.frame_5,text='RELATIONSHIP DUR',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold'))       ################## Long term relation - girls are preferred in any case (HAREM)
        self.lfavouritesprob=Label(self.frame_5,text='FAVOURITES PROB',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold'))         ################## Probability that a girl becomes favourite (HAREM)
        self.lfavouritesnum=Label(self.frame_5,text='FAVOURITES NUM',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold'))           ################## Number of possible favourites in the harem  (HAREM) 
        self.lspermvitality=Label(self.frame_5,text='SPERM CYCLE < 100',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold'))     ################## Values <100 trigger 0.7 decreas in sperm vitality a year  (HAREM) 
        self.lcopaday=Label(self.frame_5,text='COPULATIONS/DAY',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold'))                ################## Copulations a day (HAREM)
        self.lcoppreg=Label(self.frame_5,text='COP_PREGNANCY/DAYS',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold'))             ################## Copulations  during pregnancy (HAREM)
        self.llact=Label(self.frame_5,text='LACTATION/MONTHS',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold'))                         ################## Lacatation - n fertile cycle (HAREM)
        self.lspermlifetime=Label(self.frame_5,text='SPERM AGING (1.52%)',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold'))  
        
        
        self.eharemsize=Entry(self.frame_5,width=5,font=(self.labelfont,self.labelfontsize,'bold'))
        self.eovosync=Entry(self.frame_5,width=5,font=(self.labelfont,self.labelfontsize,'bold'))
        self.erelationshipprob=Entry(self.frame_5,width=5,font=(self.labelfont,self.labelfontsize,'bold'))
        self.erelationshipdur=Entry(self.frame_5,width=5,font=(self.labelfont,self.labelfontsize,'bold'))
        self.efavouritesprob=Entry(self.frame_5,width=5,font=(self.labelfont,self.labelfontsize,'bold'))    
        self.efavouritesnum=Entry(self.frame_5,width=5,font=(self.labelfont,self.labelfontsize,'bold'))
        self.espermvitality=Entry(self.frame_5,width=5,font=(self.labelfont,self.labelfontsize,'bold'))
        self.ecopaday=Entry(self.frame_5,width=5,font=(self.labelfont,self.labelfontsize,'bold'))
        self.ecoppreg=Entry(self.frame_5,width=5,font=(self.labelfont,self.labelfontsize,'bold'))
        self.elact=Entry(self.frame_5,width=5,font=(self.labelfont,self.labelfontsize,'bold'))
        self.espermlifetime=Entry(self.frame_5,width=5,font=(self.labelfont,self.labelfontsize,'bold'))
           
        self.lharemsize.grid(row =0, column=0, padx=2, pady=1,sticky=N)      
        self.eharemsize.grid(row =0, column=1, padx=2, pady=1,sticky=N)
        self.lovusync.grid(row =0, column=2, padx=2, pady=1,sticky=N)
        self.eovosync.grid(row =0, column=3, padx=2, pady=1,sticky=N) 
        self.lrelationshipprop.grid(row =1, column=0, padx=2, pady=1,sticky=N)
        self.erelationshipprob.grid(row =1, column=1, padx=2, pady=1,sticky=N)
        self.lrelationshipdur.grid(row =1, column=2, padx=2, pady=1,sticky=N)
        self.erelationshipdur.grid(row =1, column=3, padx=2, pady=1,sticky=N)
        self.lfavouritesprob.grid(row =3, column=0, padx=2, pady=1,sticky=N)
        self.efavouritesprob.grid(row =3, column=1, padx=2, pady=1,sticky=N)
        self.lfavouritesnum.grid(row =3, column=2, padx=2, pady=1,sticky=N)
        self.efavouritesnum.grid(row =3, column=3, padx=2, pady=1,sticky=N)
        self.lspermvitality.grid(row =4, column=0, padx=2, pady=1,sticky=N)
        self.espermvitality.grid(row =4, column=1, padx=2, pady=1,sticky=N)
        self.lcopaday.grid(row =4, column=2, padx=2, pady=1,sticky=N)
        self.ecopaday.grid(row =4, column=3, padx=2, pady=1,sticky=N)
        self.lcoppreg.grid(row =5, column=2, padx=2, pady=1,sticky=N)
        self.ecoppreg.grid(row =5, column=3, padx=2, pady=1,sticky=N)
        self.llact.grid(row =5, column=0, padx=2, pady=1,sticky=N)
        self.elact.grid(row =5, column=1, padx=2, pady=1,sticky=N)
        self.lspermlifetime.grid(row =6, column=0, padx=2, pady=1,sticky=N)
        self.espermlifetime.grid(row =6, column=1, padx=2, pady=1,sticky=N)
       
        
        self.eharemsize.insert(END, '504')
        self.eovosync.insert(END, '0')
        self.erelationshipprob.insert(END, '0')
        self.erelationshipdur.insert(END, '0')
        self.efavouritesprob.insert(END, '0')
        self.efavouritesnum.insert(END, '0')     
        self.espermvitality.insert(END, '100')
        self.ecopaday.insert(END, '1')
        self.ecoppreg.insert(END, '0')
        self.elact.insert(END, '0')
        self.espermlifetime.insert(END, '0.0')
        
       
        
        # ##########################################################################################  place a graph somewhere here 
        self.f = Figure(figsize=(7,4), dpi=72)
        
        self.f_2 = Figure(figsize=(6,2), dpi=72)
        self.f_3 = Figure(figsize=(6,2), dpi=72)
        self.f_4 = Figure(figsize=(6,2), dpi=72)
        self.f_5 = Figure(figsize=(6,2), dpi=72)
        
        self.canvas = FigureCanvasTkAgg(self.f, master= self.frame_4) 
        self.canvas.show()
        self.canvas.get_tk_widget().grid (row=10, column=0)
        
        
        self.canvas_3 = FigureCanvasTkAgg(self.f_3, master= self.frame_3) 
        self.canvas_3.show()
        self.canvas_3.get_tk_widget().grid (row=2, column=0,padx=2, pady=2)
        
        self.canvas_2 = FigureCanvasTkAgg(self.f_2, master= self.frame_3) 
        self.canvas_2.show()
        self.canvas_2.get_tk_widget().grid (row=3, column=0,padx=2, pady=2)
        
        self.canvas_4 = FigureCanvasTkAgg(self.f_4, master= self.frame_3) 
        self.canvas_4.show()
        self.canvas_4.get_tk_widget().grid (row=4, column=0,padx=2, pady=2)
        
        
        self.canvas_5 = FigureCanvasTkAgg(self.f_5, master= self.frame_3) 
        self.canvas_5.show()
        self.canvas_5.get_tk_widget().grid (row=5, column=0,padx=2, pady=2)
          
        ########################################################################################### check buttons for plotting
        self.cplot_mean=Checkbutton(self.frame_4, text='PLOT MEAN',font=(self.labelfont,self.labelfontsize,'bold'), bg=self.framebg,command = self.Check_Plotmean)
        self.cplot_range=Checkbutton(self.frame_4, text='PLOT RANGE',font=(self.labelfont,self.labelfontsize,'bold'),bg=self.framebg,command = self.Check_Plotrange)


        self.cplot_mean.grid(row =20, column=0, padx=2, pady=1,sticky=W)
        self.cplot_range.grid(row =20, column=0, padx=2, pady=1,sticky=E)

        
        self.plothist=0
        self.plotmean=0
        self.plotrange=0
        self.plotpool=0
        ########################################################################################### radio buttons for modelselction
        self.lmodelselect=Label(self.frame_4,text='MODEL',bg=self.framebg,font=(self.labelfont,self.labelfontsize,'bold'))
        self.lmodelselect.grid(row =1, column=0, padx=2, pady=5,sticky=W)
        
        self.rbc=IntVar()
        self.rbc.set(1)
        self.cwilcox=Radiobutton(self.frame_4, text='WILCOX',font=(self.labelfont,self.labelfontsize,'bold'), bg=self.framebg,variable=self.rbc, value=1,command=self.Check_Rbc)
        self.croyton=Radiobutton(self.frame_4, text='JOECHLE',font=(self.labelfont,self.labelfontsize,'bold'), bg=self.framebg,variable=self.rbc, value=2,command=self.Check_Rbc)
        self.csbm=Radiobutton(self.frame_4, text='SBM',font=(self.labelfont,self.labelfontsize,'bold'), bg=self.framebg,variable=self.rbc, value=3,command=self.Check_Rbc)

        self.cwilcox.grid(row =2, column=0, padx=2, pady=3,sticky=W)
        self.croyton.grid(row =2, column=0, padx=2, pady=3,)
        self.csbm.grid(row =2, column=0, padx=2, pady=3,sticky=E)
        self.modelselect=1
       
        self.rbplot=IntVar()
        self.rbplot.set(1)
        
        self.cnone=Radiobutton(self.frame_3, text='NO PLOT',font=(self.labelfont,self.labelfontsize,'bold'), bg=self.framebg,variable=self.rbplot, value=1,command=self.Check_Rbplot)
        self.cinside=Radiobutton(self.frame_3, text='LIVE PLOT',font=(self.labelfont,self.labelfontsize,'bold'), bg=self.framebg,variable=self.rbplot, value=2,command=self.Check_Rbplot)
        self.coutside=Radiobutton(self.frame_3, text='RESULT PLOT',font=(self.labelfont,self.labelfontsize,'bold'), bg=self.framebg,variable=self.rbplot, value=3,command=self.Check_Rbplot)

        self.cnone.grid(row =10, column=0, padx=2, pady=3,sticky=E)
        self.cinside.grid(row =10, column=0, padx=2, pady=3)
        self.coutside.grid(row =10, column=0, padx=2, pady=3,sticky=W)
       
            
        
        ##########################################-9   -8     -7   -6    -5     -4    -3    -2    -1    0     1     2 MODELS OF basic conception data
        
        self.concprobW = [0.0, 0.0, 0.0, 0.00, 0.00, 0.00, 0.00, 0.00, 0.10, 0.16, 0.14, 0.27,  0.31,  0.33,  0.01,  0.00,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]        ###### WILCOXON MODEL
        self.concprobR = [0.0, 0.0, 0.0, 0.00, 0.17, 0.17, 0.30, 0.30, 0.24, 0.30, 0.33, 0.41, 0.28,  0.27,  0.11,  0.05,  0.03,0.03,0.03,0.02,0.05,0.05,0.01,0.0,0.0,0.0,0.0]  ###### JOECHLE MODEL
        self.concprobS = [0.0, 0.0, 0.0, 0.00, 0.00, 0.00, 0.00, 0.00, 0.04, 0.14, 0.20, 0.20, 0.34,  0.14,  0.07,  0.00,  0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]         ###### SMB MODEL
    
       
        self.conception_window=[10,11,12,13,14,15,16] 
        
        ############################################################ SET BASIC VARIABLES
        self.iterations=10                       ########### Block 1
        self.children=1171
        self.reproductive_span=32
        ############################################################
        self.tabu=0                              ########### Block 2
        self.detection_probability=0
        self.fertile=100
        self.miss=100
        self.survival=100
        ############################################################
        self.haremsize=504                       ########### Block 3
        self.relationshipprob=0
        self.favouritesprob=0
        self.spermvitality=100
        self.lact=0
        self.spermlifetime=0.0
        ############################################################
        self.ovusync=0                           ########### Block 4
        self.relationshipdur=0
        self.favouritesnum=0
        self.copaday=1
        self.coppreg=0


        self.mean=0.0
        self.plotselection=1
        random.seed()
        self.type='1'                             ############ used only in batchmode version 
      
        
        
        
    def clearentries(self):
        ############################################################
        self.eiterations.delete('0',END)         ########### Block 1
        self.echildren.delete('0',END)
        self.ereproductive_span.delete('0',END)
        ############################################################
        self.etabu.delete('0',END)               ########### Block 2
        self.edetection.delete('0',END)
        self.efertile.delete('0',END)
        self.emiss.delete('0',END)
        self.esurvival.delete('0',END)
        ############################################################   
        self.eharemsize.delete('0',END)          ########### Block 3
        self.erelationshipprob.delete('0',END)
        self.efavouritesprob.delete('0',END)
        self.espermvitality.delete('0',END)
        self.elact.deledelete ('0',END)
        self.espermlifetime.delete('0.0',END)
        #############################################################
        self.eovosync.delete('0',END)            ############ Block 4
        self.erelationshipdur.delete('0',END)
        self.efavouritesnum.delete('0',END)
        self.ecopaday.delete('0',END)
        self.ecoppreg.delete('0',END)
        

    def get_entries(self):     
        ##############################################################
        self.iterations=int(self.eiterations.get()) ########### Block1
        self.children=float(self.echildren.get())
        self.reproductive_span=float(self.ereproductive_span.get())  
        ##############################################################
        self.tabu=int(self.etabu.get())             ########### Block2
        self.detection_probability=int(self.edetection.get())
        self.fertile=int(self.efertile.get())
        self.survival=int(self.esurvival.get())              
        ##############################################################
        self.haremsize=float(self.eharemsize.get()) ########### Block3
        self.relationshipprob=float(self.erelationshipprob.get())
        self.favouritesprob=float(self.efavouritesprob.get())
        self.spermvitality=int(self.espermvitality.get())
        self.lact=int(self.elact.get())
        self.spermlifetime=float(self.espermlifetime.get()) 
        ##############################################################
        self.ovusync=float(self.eovosync.get())     ########### Block4  
        self.relationshipdur=int(self.erelationshipdur.get())      
        self.favouritesnum=int(self.efavouritesnum.get())
        self.copaday=int(self.ecopaday.get())
        self.coppreg=int(self.ecoppreg.get())
        
        self.Check_Rbc()   ############################################ Checks which model to use
    
   
   
    def Check_Plothist(self): ######################################## Plot radio buttons
        if (self.plothist==1):
            self.plothist=0
        else:
            self.plothist=1
 
    def Check_Plotmean(self):
        if (self.plotmean==1):
            self.plotmean=0
        else:
            self.plotmean=1
            
    def Check_Plotrange(self):
            if (self.plotrange==1):
                self.plotrange=0
            else:
                self.plotrange=1
                
    def Check_Plotpoolsize(self):
            if (self.plotpool==1):
                self.plotpool=0
            else:
                self.plotpool=1
    def Check_Rbc(self):
        self.modelselect=self.rbc.get()
     

    def Check_Rbplot(self):
        self.plotselection=self.rbplot.get()

    
########################################################################################################################################
########################################################################################## Simulation
########################################################################################################################################

########################################################################################################################################
########################################################################################## harem
########################################################################################################################################
        
        
    def moulay_harem(self):
        
        self.canvas.figure.clf()
        self.canvas.show()
        self.canvas_3.figure.clf()
        self.canvas_3.show()
        self.canvas_2.figure.clf()
        self.canvas_2.show()
        self.canvas_4.figure.clf()
        self.canvas_4.show()
        self.canvas_5.figure.clf()
        self.canvas_5.show()
        
        min=999999999999
        max=-99999999999
        
        fmin=999999999999
        fmax=-99999999999
        survive=0
        self.get_entries()
        
        self.dirname = tkFileDialog.askdirectory(parent=root,title='Please select a results directory')
    
        if self.dirname:
                   #print self.modelselect 
            fname=('h'+'_'+ str(self.modelselect) +'_' + self.type+'_'+str(self.tabu) + '_'+str(self.detection_probability) + '_'+str(self.fertile) + '_'+str(self.survival) + '_'+str(self.spermvitality) + '_'+str(self.copaday) +
            '_'+str(self.lact)+ '_'+str(self.iterations) + '_'+str(self.children)+ '_'+str(self.haremsize) +'_' + str(self.reproductive_span) + '_'+str(self.ovusync)+ '_'+str(self.relationshipprob)+
            '_'+str(self.relationshipdur)+'_'+str(self.favouritesprob) + '_'+str(self.favouritesnum)+ '_'+str(self.miss))
         
            lightfile=open(self.dirname + '/'+ fname+'.txt'	,'w')
            lightfile.write('type'+'\t'+'iter' +'\t'+'children'+'\t'+ 'mean' +'\t'+'min'+'\t'+ 'max'+'\t'+ 'fluct'+'\t'+ 'test'+'\t'+ 'nchild'+'\n')
            
            
            
            cops = np.zeros(self.iterations-1)      ####### holds plot data
            meancop=np.zeros(self.iterations-1)     ####### holds plot data
            maxcop=np.zeros(self.iterations-1)      ####### holds plot data
            mincop=np.zeros(self.iterations-1)      ####### holds plot data
            meancop=np.zeros(self.iterations-1)     ####### holds plot data
            meangirls=np.zeros(self.iterations-1)   ####### holds plot data
            pool=np.zeros(self.iterations-1)        ####### holds plot data
            meanfluct= np.zeros(self.iterations-1)
            minfluct= np.zeros(self.iterations-1)
            maxfluct= np.zeros(self.iterations-1)
    
            
            total_number_of_xxcops=0.0
            total_number_girls_tested=0.0
            total_number_of_children=0.0
            fluctuation_sum=0.0
            fluctuation_mean=0.0
            
            ############################################################################################### iterate
            ############################################################################################### iterate
            ############################################################################################### iterate   
            
            for i  in range (1,self.iterations,1): 
                children=0.0
                                                                     ##################### create harem - all zero
                harem=np.zeros((self.haremsize,8),float) ####### harem data             
                                                                                    # index = girl number
                                                                                    # 0= cycle day
                                                                                    # 1= pregnancy in days
                                                                                    # 2= selected
                                                                                    # 3= xxcoped
                                                                                    # 4=fertility     
                                                                                    # 5=favourite - max 7
                                                                                    # 6 =age in days
                                                                                    # 7=number of children
                
                ######################################################################################## initialize harem
                ######################################################################################## initialize harem
                ######################################################################################## initialize harem
               
                ovsync=0   
                if (self.ovusync > 0):
                    synced=int(self.haremsize/100 * self.ovusync)
               
                for x in range (0,len(harem),1):                                    ##################### initialze cycle days random and age in days between 15 and 30
                    harem[x,0]=random.randint(0,26)
                    harem[x,6]=(random.randint(15,25))*365 
                    if (x>0):
                        if (self.ovusync > 0):                                      ##################### intialize    synchronized ovulation
                            if (ovsync<synced):
                                harem[x,0]=harem[x-1,0]
                                ovsync=ovsync+1
    
                    harem[x,4]=random.randint(0,100)                                ##################### fertility ###################                 
               
               
                for f in range(0,self.favouritesnum):                               #####################  create favourites max 7 + 4 wives
                     favgirl=random.randint(0,len(harem)-1)
                     harem[favgirl,5]=1
    
                time=0                                                              ##################### simulation time is zero
                pregnant_lact=(9+self.lact)*30                                      ##################### pregnancy and lactation time is 18 months - can be made enterable
                fluctuation=0                                                       ##################### holds harem fluctuation
                
                ########################################################################################simulate a life cycle 
                ########################################################################################simulate a life cycle 
                ########################################################################################isimulate a life cycle
                
                
                self.relationship=0
                relationshipduration=0
                relationshiphowoften=0
                children_sum=0
                girls_tested=0
                girl=0
                
                
                
                while (time < (self.reproductive_span*365)):                                           
                #while (time < 500):   
                    time=time+1
                                                                                    ##################### update harem
                    
                    for b in range (0,len(harem),1):                                    
                     harem[b,0]=harem[b,0] + 1                                      ##################### increment cycle per one day
                     if (harem[b,0]>26):                                            ##################### reset cyle
                        harem[b,0]=0
                     harem[b,6]=harem[b,6] + 1                                      #################### increment age per one day
                     if (harem[b,6]>(30*365)):                                      #################### replace if too old
                        fluctuation=fluctuation+1                                   #################### increment fluctuation counter
                        # harem[b,0] = random.randint(0,26)                         #################### 0= cycle day - keep because of ovusync
                        harem[b,1] =0                                               #################### 1= pregnancy in days - reset
                        harem[b,2] =0                                               #################### 2= selected - reset
                        harem[b,3] =0                                               #################### 3= xxcoped - reset
                        harem[b,4] = random.randint(0,100)                          #################### 4= fertility  - reset   - zero 
                        ##harem[b,5] =0                                             #################### 5=favourite - max 7    - keep because otherwise number too high                   
                        harem[b,6] = (random.randint(15,25))*365                    #################### 6 =age in days
                        harem[b,7] =0                                               ##################### 7= number of children
                        #print ( harem[b,6])
                        
                     
                     if (harem[b,1] >0):
                        harem[b,1]=harem[b,1] + 1                                   ###################### inc pregnancy if present
                        if (harem[b,1]> pregnant_lact):                             ######################  if longer than pregnancy + lactation time reset pregnancy 
                            harem[b,1]=0
                    
                    ######################################################################################   copulate twice for one day
                    ######################################################################################   copulate twice for one day
                    ######################################################################################   copulate twice for one day
                    
                    
                    ncd=0                                                           ###################### copulation counter
                    
                    
                    for ncd in range (0,self.copaday,1):                  
                        #print ncd
                        girl_found=0                                         
                                         
                        if (time >1):
                            if (self.relationship > 0):
                             relationshiphowoften =relationshiphowoften+1           ##################### count days of relationship
                             if (relationshiphowoften < relationshipduration+1):    ##### must take care here  - dont search for a girl if relationship repeat if not tabu exists
                                
                                testtabu=self.tabu
                                
                                if (harem[girl,1]>0):                               ################### pregnant girl does not menstruate
                                    girl_cycle_day=26
                                    #print ("pregnancy resets cycle")
                                else:    
                                                                  
                                    girl_cycle_day=harem[girl,0]
                                   
                                
                                if (girl_cycle_day > testtabu):                     ###################### girl is not menstruating
                                    girl_found=1                                    ###################### we have a girl - no search
                                    #print ("relationship controller no tabu : ", girl, " ",relationshiphowoften, relationshipduration) ###################### until duration is reached
                                else:
                                    self.relationship=0                             ###################### reset relation ship
                                    girl_found=0
                                    relationshipduration=0
                                    relationshiphowoften=0
                                    #print ("relationship controller tabu reset")
                             
                             else:
                                    self.relationship=0                              ###################### reset relation ship
                                    girl_found=0
                                    relationshipduration=0
                                    relationshiphowoften=0
                                    #print ("relationship controller duration reset")
                                    
                        
                        ################################################################################### we have to look for a girl who fulfills the basic conditions - if no relationship
                        ################################################################################### we have to look for a girl who fulfills the basic conditions
                      
                        search_girl=0
                        while (girl_found==0) and search_girl < len (harem):            ####################### search for a girl                   
                                girls_tested=girls_tested+1
                                search_girl=search_girl+1
            
                                
                                girl=random.randint(0,len(harem)-1)                     ####################### take random girl to look at    
                                
                                #print 'random girl', i, girl, ' preg:', harem[girl,1], self.coppreg
                                if ( harem[girl,1]<=self.coppreg): ####################### she is not pregnant or pregnancy still invisible
                                    
                                    #print 'in selection', i, girl, harem[girl,1], self.coppreg
                                    harem[girl,2]= harem[girl,2]+1                          ######################## increment girl selection counter
                                    
                                    ############################################################################### process girl
                                    ############################################################################### process girl
                                    ############################################################################### process girl 
                                    
                                    midcycle=0
                                    if (harem[girl,0] in self.conception_window):           ####################### is the girl in the conception window -ovulation detection
                                        midcycle=1                                          ####################### propability that she is in fertile window  p=6/27 (0.222222)
                                   
                                   
                                    ovusieve=1                                              ####################### if ovulation sieve is 1 lets all through
                                    detect=0                                                ####################### if an ovulation found - retains non-ovulating
                                    if (self.detection_probability > 0) :                           
                                            detect=random.randint(0,100)                                                       
                                            if (midcycle==0):
                                                if (detect  <   self.detection_probability):####################### reject non ovulating
                                                    ovusieve=0
                                                    #print "no ovu"
                                    favsieve=1                                              ######################## favourites  is 1 sieve lets all through
                                    xdetect=0                                               ######################## if favourite  - retains non-favourites
                                    if (self.favouritesprob > 0) :                           
                                            xdetect=random.randint(0,100)                                                       
                                            if ( harem[girl,5]==0):
                                                if (xdetect  <   self.favouritesprob ):
                                                    favsieve=0
                                  
                                    if (harem[girl,0] > self.tabu):                         ######################## if she is not menstruating religous tabus 4 days                     
                                        if (favsieve==1):                                   ######################## if she is not rejected from the conditions above - favourite   
                                  
                                            if (ovusieve==1):                               ######################## if she is not rejected from the conditions above  - ovulating                                        
                                                girl_found=1                                ######################## we have a girl fulfilling the basic conditions
                                                harem[girl,3]=harem[girl,3]+1
                                        
                                ################################################################################# girl found copulate copulate copulate
                                ################################################################################# girl found copulate copulate copulate
                                ################################################################################# girl found copulate copulate copulate             
                            
                        
                        if (self.relationship==0):                                            ######################## may be he falls in love with her-start relationship set variables
                            if (self.relationshipprob>0):
                                relationship=random.randint(0,100)
                                if (relationship <  self.relationshipprob):
                                    relationshipduration=random.randint(0,self.relationshipdur)
                                    self.relationship=1                                        ####################### he likes her a lot                                                                                                                         
                        
                        
                        
                                                                                               #########################  check for fertility, before calculating the rest - general fertility 92 %
                                                    
                        if (  harem[girl,4] < self.fertile+1):                        
                                                  
    
                            if ( harem[girl,1]==0):                                            ########################## this is necessary because of relationships - he can copulate with a pregnant girl
                                                     
                                #print 'in copulation', i, girl, harem[girl,1], self.coppreg                        
                                prob=random.uniform(0,1)
                                concprob=0                                                     
                                if (self.modelselect==1):
                                    concprob=self.concprobW[int(harem[girl,0])]                ########################## WILCOX
                                if (self.modelselect==2):                              
                                    concprob=self.concprobR[int(harem[girl,0])]                ########################## JOECHLE
                                if (self.modelselect==3):                               
                                    concprob=self.concprobS[int(harem[girl,0])]                ########################## SMB
                                
                                    
                                    
                                #sperm_aged=float((time/365)*1.52 )                             #############   sperm aging  1.52 % per year !!!!!!!!!!!
                                sperm_aged=float((time/365)*self.spermlifetime )  
                                print sperm_aged
                                nconcprob= concprob - ((concprob/100) * sperm_aged)
                                print time, concprob, nconcprob
                                
                                if self.spermvitality!=100:    
                                    concprob=concprob*(0.4*sin(0.5*pi*(time-1/4))+0.7)         ############ sperm fluctuation over days
                                                                                              
                                            
                                if ( prob < concprob):
                                    xmiss=random.randint(0,100)
                                    if (xmiss < self.miss+1):
                                        xsurvive=random.randint(0,100)                         #########################85% children survival rate     
                                        if (xsurvive < self.survival+1):
                                            children=1
                                            children_sum=children_sum+1
                                            harem[girl,7]=harem[girl,7]+1                      ###########################  increment children
                                            harem[girl,1]=1                                    ###########################  the girl is pregnant
                                                                                               #################### if she has a child she is fertile
                                            harem[b,4] =0
                            else:
                                print 'copulation with pregnant', i, girl, harem[girl,1], self.coppreg  
                                
                
                                                                                              ############################  children  analysis
                total_number_of_children = total_number_of_children+children_sum              #counts over all iterations xxcops
                self.mean=total_number_of_children/i                                          #->>> dynamic real mean xxcops            
    
                meancop[i-1]=self.mean                                                        ############################ meancop is the number of children over all iterations    
                xxcops=children_sum
                cops[i-1]=xxcops 
                                                                                              ########################### girls analysis
                
                
                total_number_girls_tested=total_number_girls_tested+girls_tested               ########################### counts over all iterations girls
                meangirls[i-1]=(total_number_girls_tested/i )                                  #----->>>>> dynamic real mean girls tested
                                                                                               #  girls approached for number of  children
                
                fluctuation_sum=fluctuation_sum+fluctuation
                fluctuation_mean=float(fluctuation_sum/i)
                meanfluct[i-1]=fluctuation_mean
                
                                                                                              #############how many children per women ????????
                
                nchild=0.0
                for b in range (0,len(harem),1):                                    
                     nchild=harem[b,7] + nchild 
                
                nchild=nchild/len(harem)
    
                
                if (xxcops < min):
                    min=xxcops
                if (xxcops > max):
                    max=xxcops                
                maxcop[i-1]=max
                mincop[i-1]=min
                
                if (fluctuation < fmin):
                    fmin=fluctuation
                if (fluctuation > fmax):
                    fmax=fluctuation                
                maxfluct[i-1]=fmax
                minfluct[i-1]=fmin
    
                ########################################################end analysis
                
                
                if (self.plotmean==1):
                ################################################## mean graph
                    self.canvas.figure.clf() 
                    bx=self.f.add_subplot(1,1,1)            
                    bx.plot(meancop[0:i-1])
                    if (self.plotrange==1):
                        bx.plot(mincop[0:i-1])
                        bx.plot(maxcop[0:i-1])
                    bx.set_xlabel('ITERATIONS', fontsize=7, fontweight='bold')
                    bx.set_ylabel('CHILDREN', fontsize=7, fontweight='bold')
                    bx.set_title(r'AVERAGE CHILDREN', fontsize=7, fontweight='bold')
                    bx.grid(True)
                    fontsize = 7
                    for tick in bx.xaxis.get_major_ticks():
                        tick.label1.set_fontsize(fontsize)
                        tick.label1.set_fontweight('bold')
                    for tick in bx.yaxis.get_major_ticks():
                        tick.label1.set_fontsize(fontsize)
                        tick.label1.set_fontweight('bold')      
                    bx.plot()
                    self.canvas.show()
                ##################################################mean graph
                ################################################## fluct graph
                    self.canvas_4.figure.clf() 
                    dx=self.f_4.add_subplot(1,1,1)            
                    dx.plot(meanfluct[0:i-1])
                    if (self.plotrange==1):
                        dx.plot(minfluct[0:i-1])
                        dx.plot(maxfluct[0:i-1])
                    dx.set_xlabel('ITERATIONS', fontsize=7, fontweight='bold')
                    dx.set_ylabel('FLUCTUATION', fontsize=7, fontweight='bold')
                    dx.set_title(r'MEAN FLUCTUATION', fontsize=7, fontweight='bold')
                    dx.grid(True)
                    fontsize = 7
                    for tick in dx.xaxis.get_major_ticks():
                        tick.label1.set_fontsize(fontsize)
                        tick.label1.set_fontweight('bold')
                    for tick in dx.yaxis.get_major_ticks():
                        tick.label1.set_fontsize(fontsize)
                        tick.label1.set_fontweight('bold')      
                    dx.plot()
                    self.canvas_4.show()
                ##################################################fluct graph
               
               
               
               
                if (self.plotselection==3):
                ################################################## pool graph
                    self.canvas_3.figure.clf() 
                    cx=self.f_3.add_subplot(1,1,1)            
                    cx.plot(meangirls[0:i-1])
                    #cx.plot(cops[0:i-1])
                    cx.set_xlabel('ITERATIONS', fontsize=7, fontweight='bold')
                    cx.set_ylabel('WOMEN', fontsize=7, fontweight='bold')
                    cx.set_title(r'WOMEN TESTED', fontsize=7, fontweight='bold')
                    cx.grid(True)
                    fontsize = 7
                    for tick in cx.xaxis.get_major_ticks():
                        tick.label1.set_fontsize(fontsize)
                        tick.label1.set_fontweight('bold')
                    for tick in cx.yaxis.get_major_ticks():
                        tick.label1.set_fontsize(fontsize)
                        tick.label1.set_fontweight('bold')      
                    cx.plot()
                    self.canvas_3.show()
                ##################################################pool graph
            
                bestcase=0.0
                worstcase=0.0
                averagecas=0.0
                worstcase= max
                averagecase= self.mean
                bestcase= min
                wtest=meangirls[i-1]/(self.reproductive_span*365)
                print (i, "max: ", worstcase, ' mean: ',averagecase,' ', "min: ",bestcase, " ","flux: ",fluctuation_mean, 'tested:',wtest)
                lightfile.write(self.type+'\t'+str(i) +'\t'+str(xxcops)+'\t'+ str(averagecase) +'\t'+ str(worstcase)+'\t'+ str(bestcase)+'\t'+ str(fluctuation_mean)+'\t'+str(wtest)+'\t'+str(nchild)+'\n')            
    
            
            if (self.plotselection==3):
                ##################################################################################### plot histogram
                self.canvas_2.figure.clf() 
                ax=self.f_2.add_subplot(1,1,1)
                n, bins, patches = ax.hist(cops, 50, normed=1, facecolor= 'red', alpha= 0.75)
                ax.set_xlabel('NUMBER OF CHILDREN', fontsize=7, fontweight='bold')
                ax.set_ylabel('FREQUENCY', fontsize=7, fontweight='bold')
                ax.set_title(r'CHILDREN', fontsize=7, fontweight='bold')
                ax.grid(True)
                fontsize = 7
                for tick in ax.xaxis.get_major_ticks():
                    tick.label1.set_fontsize(fontsize)
                    tick.label1.set_fontweight('bold')
                for tick in ax.yaxis.get_major_ticks():
                    tick.label1.set_fontsize(fontsize)
                    tick.label1.set_fontweight('bold')          
                ax.plot()
                self.canvas_2.show()
                ##################################################################################### plot histogram end
            
            lightfile.close
    
        
    
########################################################################################################################################
########################################################################################## all
########################################################################################################################################    
    
    def moulay(self):
        
        self.canvas.figure.clf()
        self.canvas.show()
        self.canvas_3.figure.clf()
        self.canvas_3.show()
        self.canvas_2.figure.clf()
        self.canvas_2.show()
        
        
        min=99999999999
        max=-9999999999
        survive=0
        self.get_entries()
        
        self.dirname = tkFileDialog.askdirectory(parent=root,title='Please select a results directory')
    
        if self.dirname:
            ########create filename
            fname='s'+'_'+ str(self.modelselect)+'_'+ self.type+'_'+str(self.tabu) + '_'+str(self.detection_probability) + '_'+str(self.fertile) + '_'+str(self.survival) + '_'+str(self.iterations) + '_'+str(self.children) + '_'+str(self.haremsize) + '_' + str(self.reproductive_span) + '_'+str(self.miss)    
            lightfile=open(self.dirname+'/'+fname+'.txt'	,'w')
            lightfile.write('type'+'\t'+'iter' +'\t'+'xxcops'+'\t'+ 'mean' +'\t'+'min'+'\t'+ 'max'+'\t'+ 'pool'+'\n')
            
           
            
            cops = np.zeros(self.iterations-1)    ####### holds plot data
            meancop=np.zeros(self.iterations-1)   ####### holds plot data
            maxcop=np.zeros(self.iterations-1)    ####### holds plot data
            mincop=np.zeros(self.iterations-1)    ####### holds plot data
            meancop=np.zeros(self.iterations-1)   ####### holds plot data
            meangirls=np.zeros(self.iterations-1) ####### holds plot data
            pool=np.zeros(self.iterations-1)      ####### holds plot data
            
            total_number_of_xxcops=0.0
            total_number_girls_tested=0
            total_ovu=0
            total_lut=0
    
            for i  in range (1,self.iterations,1): 
                conception=0.0
                xxcops=0.0
                number_of_xxcops=0.0
                conception_sum=0.0
                girls_tested=0
                self.mean=0.0
              
                ovu_sum=0.0
                lut_sum=0.0
    
                while (conception_sum < self.children):                                                 
                    cycleday=random.randint(0,26)                                    ######################################################## select female randomly
                    
                    xxcoped=0                                                        #### zere because no copulation
                   
                    
                    
                    
                    girls_tested=girls_tested+1
    
                    midcycle=0
    
                    if (cycleday in self.conception_window):                        #################ovulation detection
                        midcycle=1                                                  #  propability that she is in fertile window  p=6/27 (0.222222)
                   
                   
                    sieve=1                                                         ########################## sieve lets all through
                    detect=0                                                        ########################## snot an ovulation found
                    if (self.detection_probability > 0) :                           
                            detect=random.randint(0,100)                                                       
                            if (midcycle==0):
                                if (detect  <   self.detection_probability):
                                    sieve=0
                
                    
                    
                    if (sieve==1):                                                   ############################################### sieve is on - process
                    
                        if (midcycle==0):
                            lut_sum=lut_sum+1
                        else:
                            ovu_sum=ovu_sum+1
                        
                        if (cycleday > self.tabu):                                   ######################################################### religous tabus 5 days
                           
                           
                                        
                            #else  :                                  
                            xxcops=xxcops+1
                            xxcoped=1
                                    
                            if (xxcoped==1):
                                fertile=random.randint(0,100)                         ######################################################## fertility 92 %
                                if (fertile < self.fertile+1):
                                    prob=random.uniform(0,1)
                                    concprob=0                                          
                                    if (self.modelselect==1):                         ######################################################## WILCOX WEINBERG
                                            concprob=self.concprobW[cycleday]
                                    if (self.modelselect==2):                         ######################################################## JOECHLE
                                            concprob=self.concprobR[cycleday]
                                    if (self.modelselect==3):                         ######################################################## SMB
                                            concprob=self.concprobS[cycleday]
                                    if ( prob < concprob):
                                        xmiss=random.randint(0,100)                   ######################################################## 85% chilren survival rate     
                                        if (xmiss < self.miss+1):                     ################################### misscariage rate
                                            xsurvive=random.randint(0,100)            ######################################################## 85% chilren survival rate     
                                            if (xsurvive < self.survival+1):
                                                conception=1
                                                conception_sum=conception_sum+1            
                
                                                                                      ######################################################## copulation analysis
                total_number_of_xxcops = total_number_of_xxcops+xxcops                #counts over all iterations xxcops
                self.mean=total_number_of_xxcops/i                                    #->>> dynamic real mean xxcops
                
                meancop[i-1]=self.mean/(self.reproductive_span*365)                   #calculates numbers of xxcops necessary per day for number of children
                
                
                ovu_lut=0.0
                ovu_lut=ovu_sum/lut_sum
    
                self.mean=total_number_of_xxcops/i   
            
                cops [i-1]=xxcops                                                     #number of xxcops for number of children
                
                                                                                      #######################################################girls analysis
                total_number_girls_tested=total_number_girls_tested+girls_tested          #counts over all iterations girls
                meangirls[i-1]=(total_number_girls_tested/i )/ (self.reproductive_span*365)                  #----->>>>> dynamic real mean girls tested per day
                
                pool[i-1]=girls_tested                                                 # girls approached for number of  children
                
                                                                                    #dynamic real mean girls tested
            
                if (xxcops < min):
                    min=xxcops
                if (xxcops > max):
                    max=xxcops
                    
                maxcop[i-1]=max/(self.reproductive_span*365)
                mincop[i-1]=min/(self.reproductive_span*365)
                ########################################################end analysis
    
                
                
                
                
                if (self.plotmean==1):
                ################################################## mean graph
                    self.canvas.figure.clf() 
                    bx=self.f.add_subplot(1,1,1)            
                    bx.plot(meancop[0:i-1])
                    if (self.plotrange==1):
                        bx.plot(mincop[0:i-1])
                        bx.plot(maxcop[0:i-1])
                    bx.set_xlabel('ITERATIONS', fontsize=7, fontweight='bold')
                    bx.set_ylabel('COPULATIONS', fontsize=7, fontweight='bold')
                    bx.set_title(r'AVERAGE COPULATIONS PER DAY', fontsize=7, fontweight='bold')
                    bx.grid(True)
                    fontsize = 7
                    for tick in bx.xaxis.get_major_ticks():
                        tick.label1.set_fontsize(fontsize)
                        tick.label1.set_fontweight('bold')
                    for tick in bx.yaxis.get_major_ticks():
                        tick.label1.set_fontsize(fontsize)
                        tick.label1.set_fontweight('bold')      
                    bx.plot()
                    self.canvas.show()
                ##################################################mean graph
                
                if (self.plotselection==3):
                ################################################## pool graph
                    self.canvas_3.figure.clf() 
                    cx=self.f_3.add_subplot(1,1,1)            
                    cx.plot(meangirls[0:i-1])
    
                    cx.set_xlabel('ITERATIONS', fontsize=7, fontweight='bold')
                    cx.set_ylabel('WOMEN', fontsize=7, fontweight='bold')
                    cx.set_title(r'WOMEN TESTED', fontsize=7, fontweight='bold')
                    cx.grid(True)
                    fontsize = 7
                    for tick in cx.xaxis.get_major_ticks():
                        tick.label1.set_fontsize(fontsize)
                        tick.label1.set_fontweight('bold')
                    for tick in cx.yaxis.get_major_ticks():
                        tick.label1.set_fontsize(fontsize)
                        tick.label1.set_fontweight('bold')      
                    cx.plot()
                    self.canvas_3.show()
                ##################################################pool graph
            
                bestcase=0.0
                worstcase=0.0
                averagecase=0.0
                worstcase= max/(self.reproductive_span*365)
                averagecase= self.mean/(self.reproductive_span*365)
                bestcase= min/(self.reproductive_span*365)
                tested=girls_tested/(self.reproductive_span*365)
                print (i, "max: ",worstcase, ' ',"mean: ", averagecase,' ',"min: ", bestcase, tested)
               
                lightfile.write(self.type+'\t'+str(i) +'\t'+str(xxcops)+'\t'+ str(averagecase) +'\t'+ str(worstcase)+'\t'+ str(bestcase)+'\t'+ str(tested)+'\n')
            
            
            
            if (self.plotselection==3):
                ##################################################################################### plot histogram
                self.canvas_2.figure.clf() 
                ax=self.f_2.add_subplot(1,1,1)
                n, bins, patches = ax.hist(cops, 50, normed=1, facecolor= 'red', alpha= 0.75)
                ax.set_xlabel('NUMBER OF COPULATIONS', fontsize=7, fontweight='bold')
                ax.set_ylabel('FREQUENCY', fontsize=7, fontweight='bold')
                ax.set_title(r'COPULATIONS', fontsize=7, fontweight='bold')
                ax.grid(True)
                fontsize = 7
                for tick in ax.xaxis.get_major_ticks():
                    tick.label1.set_fontsize(fontsize)
                    tick.label1.set_fontweight('bold')
                for tick in ax.yaxis.get_major_ticks():
                    tick.label1.set_fontsize(fontsize)
                    tick.label1.set_fontweight('bold')          
                ax.plot()
                self.canvas_2.show()
                ##################################################################################### plot histogram end
            
            lightfile.close

        
                                
    def Quit(self): 
        self.master.destroy()
        self.master.quit()
#############################################################################plot routines on 2
    
    def plot_on_2(self,title,xaxis,yaxis, the_array) : 
            self.canvas_2.figure.clf() 
            ax=self.f_2.add_subplot(1,1,1)
            n, bins, patches = ax.hist(the_array, 20, normed=1, facecolor= 'red', alpha= 0.75)
            ax.set_xlabel(xaxis, fontsize=7, fontweight='bold')
            ax.set_ylabel(yaxis, fontsize=7, fontweight='bold')
            ax.set_title(title, fontsize=7, fontweight='bold')
            ax.grid(True)
            fontsize = 7
            for tick in ax.xaxis.get_major_ticks():
                tick.label1.set_fontsize(fontsize)
                tick.label1.set_fontweight('bold')
            for tick in ax.yaxis.get_major_ticks():
                tick.label1.set_fontsize(fontsize)
                tick.label1.set_fontweight('bold')          
            ax.plot()
            self.canvas_2.show()
#############################################################################plot routines on 3
    def plot_on_3(self,title,xaxis,yaxis, the_array) :
                self.canvas_3.figure.clf() 
                cx=self.f_3.add_subplot(1,1,1)            
                n, bins, patches = cx.hist(the_array, 20, normed=1, facecolor= 'red', alpha= 0.75)
                cx.set_xlabel(xaxis, fontsize=7, fontweight='bold')
                cx.set_ylabel(yaxis, fontsize=7, fontweight='bold')
                cx.set_title(title, fontsize=7, fontweight='bold')
                cx.grid(True)
                fontsize = 7
                for tick in cx.xaxis.get_major_ticks():
                    tick.label1.set_fontsize(fontsize)
                    tick.label1.set_fontweight('bold')
                for tick in cx.yaxis.get_major_ticks():
                    tick.label1.set_fontsize(fontsize)
                    tick.label1.set_fontweight('bold')      
                cx.plot()
                self.canvas_3.show()
      
    def plot_on_4(self,title,xaxis,yaxis, the_array) :
                self.canvas_4.figure.clf() 
                cx=self.f_4.add_subplot(1,1,1)            
                n, bins, patches = cx.hist(the_array, 20, normed=1, facecolor= 'red', alpha= 0.75)
                cx.set_xlabel(xaxis, fontsize=7, fontweight='bold')
                cx.set_ylabel(yaxis, fontsize=7, fontweight='bold')
                cx.set_title(title, fontsize=7, fontweight='bold')
                cx.grid(True)
                fontsize = 7
                for tick in cx.xaxis.get_major_ticks():
                    tick.label1.set_fontsize(fontsize)
                    tick.label1.set_fontweight('bold')
                for tick in cx.yaxis.get_major_ticks():
                    tick.label1.set_fontsize(fontsize)
                    tick.label1.set_fontweight('bold')      
                cx.plot()
                self.canvas_4.show()           
            
    def plot_on_5(self,title,xaxis,yaxis, the_array) :
                self.canvas_5.figure.clf() 
                cx=self.f_5.add_subplot(1,1,1)            
                n, bins, patches = cx.hist(the_array, 27, normed=1, facecolor= 'red', alpha= 0.75)
                cx.set_xlabel(xaxis, fontsize=7, fontweight='bold')
                cx.set_ylabel(yaxis, fontsize=7, fontweight='bold')
                cx.set_title(title, fontsize=7, fontweight='bold')
                cx.grid(True)
                fontsize = 7
                for tick in cx.xaxis.get_major_ticks():
                    tick.label1.set_fontsize(fontsize)
                    tick.label1.set_fontweight('bold')
                for tick in cx.yaxis.get_major_ticks():
                    tick.label1.set_fontsize(fontsize)
                    tick.label1.set_fontweight('bold')      
                cx.plot()
                self.canvas_5.show()          
            
root=Tkinter.Tk()



app=App(root,window_title)
root.title('MOULAY SIMULATION')
root.mainloop()
