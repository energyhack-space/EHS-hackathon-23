# -*- coding: utf-8 -*-
"""
Created on Tue May 16 15:11:22 2023

@author: SemanurSancar
"""






import sys
import sys
from PyQt5.QtWidgets import QLineEdit, QScrollArea, QSizePolicy, QGridLayout, QApplication, QWidget, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QDesktopWidget, QSpinBox, QFrame, QPushButton, QMessageBox, QHeaderView, QProgressDialog, QProgressBar
from PyQt5.QtGui import QPixmap, QIcon, QMovie, QFont
from PyQt5.QtCore import Qt, QThread
import pandas as pd

import numpy as np

import cvxpy as cp

import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QApplication
import random



class GraphDialog(QDialog):
    def __init__(self, Pload, Pload_real):
        super().__init__()
        self.setWindowTitle("Baraların Yük Grafikleri")
        self.setWindowIcon(QIcon("ehs-logo-1-mini-2.png"))

        # Create a figure for each column of the DataFrame
        figs = []
        for col in Pload.columns:
            fig, ax = plt.subplots(figsize=(5, 6))
            ax.plot(Pload_real[col], label='Pload_real', color="pink")
            ax.plot(Pload[col], label='Pload', color="black", linestyle="--")
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Power (kW)')
            ax.set_title("Bus {}".format(col+1))
            ax.legend()
            figs.append(fig)

        # Create a scroll area for the graphs
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        self.graph_widget = QWidget(scroll_area)
        self.graph_widget.setMinimumSize(1000, 3000)
        scroll_area.setWidget(self.graph_widget)

        # Create a grid layout for the graphs
        layout = QGridLayout(self.graph_widget)
        for i, fig in enumerate(figs):
            canvas = FigureCanvas(fig)
            layout.addWidget(canvas, i//2, i%2)

        # Add the scroll area to the layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # Maximize the window
        self.showMaximized()

        # Apply tight layout to the figures
        for fig in figs:
            fig.tight_layout()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Batarya Yerleştirme ve Boyutlandırma Oyunu")
        self.setWindowIcon(QIcon("ehs-logo-1-mini-2.png"))
        self.setStyleSheet("background-color: white;")

        # Arka plan resmi
        self.background = QLabel(self)
        pixmap = QPixmap('33bus.jpg').scaledToWidth(1000)
        self.background.setPixmap(pixmap)




        # Tablo
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setRowCount(33)

        for i in range(0, 33):
            for j in range(0, 2):
                spinbox = QSpinBox(self)
                spinbox.setRange(0, 1000)
                if j == 0:
                    spinbox.setSingleStep(5)  # set singleStep to 5 for the first column
                else:
                    spinbox.setSingleStep(5)  # set singleStep to 10 for the second column
                self.table.setCellWidget(i, j, spinbox)


        # Sütun isimleri
        labels = ["BESS Power Capacity (MW)", "BESS Energy Capacity (MWh)"]
        self.table.setHorizontalHeaderLabels(labels)

        # Sütun genişliği
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # Sütun genişlikleri
        table_width = self.table.width()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setDefaultSectionSize(table_width / self.table.columnCount())

        # Set the table height to fit the page
        table_height = 1000
        self.table.setMaximumHeight(table_height)
        
        for i in range(0, 33):
            self.table.setRowHeight(i, 29)

        
        
        # Layout
        layout = QHBoxLayout()
        frame = QFrame()
        frame.setStyleSheet("background-color: white;")
        layout.addWidget(frame)
        frame_layout = QVBoxLayout()
        frame_layout.addWidget(self.background)
        frame_layout.setAlignment(Qt.AlignCenter)

        # Devre dışı kalacak hatlar input
        self.failed_lns = QLineEdit(self)
        self.failed_lns.setPlaceholderText("Devre dışı kalacak hatları liste şeklinde giriniz. Örnek: 5,12,24,29,30")
        self.failed_lns.setStyleSheet("background-color: white; border: 1px solid black; padding: 5px;")
        frame_layout.addWidget(self.failed_lns)
        frame.setLayout(frame_layout)
        
        # Buton
        button = QPushButton("Optimizasyonu Başlat!")
        button.setStyleSheet("background-color: turquoise; border-radius: 10px; height: 40px; color: white; font-weight: bold;")
        button.clicked.connect(self.perform_optimization)
        frame_layout.addWidget(button)
        frame.setLayout(frame_layout)

        # Arka plan başlığı
        self.title_label = QLabel(self)
        self.title_label.setText("Batarya Yerleştirme ve Boyutlandırma Oyunu")
        self.title_label.setStyleSheet("font-weight: bold; font-size:44px; font-family: Open Sans; color: turquoise;")
        self.title_label.setFixedWidth(1000)
        frame_layout.addWidget(self.title_label)
        frame.setLayout(frame_layout)        
        
        self.title_label = QLabel(self)
        self.title_label.setText("<p>Oyun yönergeleri aşağıdaki gibidir:</p>"
                                  "<ol>"
                                  "<li>Sağ taraftaki tablodan her bir bara için bataryanın güç ve enerji kapasiteleri seçilmelidir</li>"
                                  "<li>Eğer barada batarya olmadığı düşünülüyorsa 0 değeri kalmalı</li>"
                                  "<li>Ardından bara resminin altında olan bölüme devre dışı kalacak hat numaralarını virgül ile sıralı giriniz</li>"
                                  "<li>Optimizasyonu başlat butonuna basınız</li>"
                                  "<li>Optimizasyonun çözüm süresi bilgisayarınız ile ilgilidir</li>"
                                  "</ol>")
        self.title_label.setStyleSheet("font-size: 15px; font-family: Open Sans; color: #173a90;")
        self.title_label.setFixedWidth(1000)
        frame_layout.addWidget(self.title_label)
        frame.setLayout(frame_layout)


        
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Pencere boyutunu ayarla
        screen_rect = QDesktopWidget().screenGeometry()
        self.resize(screen_rect.width() - 100, screen_rect.height() - 100)


    
    def perform_optimization(self):
        input_tb = pd.DataFrame()
        
        for i in range(0, 33):
            for j in range(0, 2):
                input_tb.loc[i,j] = self.table.cellWidget(i, j).value()
        
        # print(self.failed_lns.text())
        # print(type(self.failed_lns.text()))
        value_list = self.failed_lns.text()
        failed_lines = [int(number)-1 for number in value_list.split(",")]
        # failed_lines = random.sample(range(1, 33), 20)
        # Suppose this is your list of unique random numbers
        unique_random_numbers = random.sample(range(1, 33), 5)
        # Subtract 1 from each element in the list
        failed_lines = [number - 1 for number in unique_random_numbers]
        P_i = input_tb[0]
        E_i = input_tb[1]
        failed_periods = [[2,8], [72,89]]
        # failed_periods = [[2,4], [8,9]]
        
        # Show the "Processing" message box
        progress = QMessageBox(self)
        progress.setWindowTitle("Güç Sistemi Optimizasyonu")
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowFlags(progress.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        progress.setText("İşlem sürüyor, lütfen bekleyin... Bilgisayar hızınıza göre ~10 dk civarı sürebilir.")
        progress.show()
        progress.button(QMessageBox.Ok).setDisabled(True)
        
        QApplication.processEvents()  # Update the GUI to show the message box
        
        player_score, Pload, Pload_real, model_timer = BESResiliencySimulation(failed_lines, P_i, E_i, failed_periods)

        # Close the "Processing" message box
        progress.close()

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Oyuncu Puanı")
        msg_box.setText("Optimizasyon tamamlandı!\n Sonuç: %{}\n Model Süresi: {}".format(player_score, model_timer))
        msg_box.exec_()
        msg_box.accept()

        # Create the line chart and show it in a dialog
        graph_dialog = GraphDialog(Pload, Pload_real)
        graph_dialog.exec_()


        

def BESResiliencySimulation(failed_lines, P_i, E_i, failed_periods):
    
    model_timer_start = datetime.datetime.now()
    
    
    """sets"""
    # sets aid in organizing and classifying objects in the model, making the model more understandable and easier to manage.
    time = 96
    # time = 30
    
    # info of lines
    line = pd.read_excel('l.xlsx')
    #number of lines
    nol = len(line)
    
    #info of buses
    h = pd.read_excel('h.xlsx')
    # number of buses
    nob = len(h)
    
    "parameters"
    # represent the inputs of the model and provide dynamicity to the model, enabling it to reach a solution.
    
    # periodical consumption of load types
    loads = pd.read_excel('powercurves.xlsx') #MW
    
    # determine the failed periods that are failed
    rows_to_change = []
    
    for i in range(len(failed_periods)):
        rows_to_change = rows_to_change + list(range(failed_periods[i][0],failed_periods[i][1])) 
    

    # fail matrix
    d = pd.DataFrame(np.ones((time, nol)))
    
    # set the failed lines to 0
    for i in range(len(failed_lines)):
        d.iloc[rows_to_change, failed_lines[i]] = 0
    
    
    
    delta_T = 0.25 #  15 min:0.25 | 30 min:0.5 | 60 min:1
    
    # discharge efficiency of battery
    Eff_dch = 0.875
    # charge efficiency of battery
    Eff_ch = 0.9
    # dept of discharge
    DoD = 0.2
    
    """variables"""
    # unknown values that we aim to find
    
    # Active power flow of branch l during period t
    f_h_t = cp.Variable((nol,time), nonneg=False )
    # absolute value of f_h_t
    absf = cp.Variable((nol,time), nonneg=True )
    # Total losses on the lines at time t
    THL_t = cp.Variable((time), nonneg=True )
    # Total active power provided by substation at bus i during period t
    P_f_i_t = cp.Variable((nob,time), nonneg=True )
    # load fed on bus i at time t
    P_load_i_t = cp.Variable((nob,time), nonneg=True )
    # Actual load on bus i at time t
    P_load_i_t_real = cp.Variable((nob,time), nonneg=True )
    
    # Binary values that make the feeding decision of critical loads
    u1_i_t = cp.Variable((nob,time), boolean=True )
    u2_i_t = cp.Variable((nob,time), boolean=True )
    u3_i_t = cp.Variable((nob,time), boolean=True )
    u4_i_t = cp.Variable((nob,time), boolean=True )
    
    # positive and negative components of f_h_t
    cf_plus = cp.Variable((nol,time), nonneg=True )
    cf_minus = cp.Variable((nol,time), nonneg=True )
    
    # Discharge power of the battery at time t at bus i
    BESS_dch_i_t = cp.Variable((nob,time), nonneg=True )
    # Charge power of the battery at time t at bus i
    BESS_ch_i_t = cp.Variable((nob,time), nonneg=True )
    # State-of-energy of the battery at time t at bus i
    SOE_i_t = cp.Variable((nob,time), nonneg=True )
    # Binary value that decides the charge-discharge status of the batteries
    v_i_t = cp.Variable((nob,time), boolean=True )
    
    """obj func"""
    # objective function that we are trying to minimize or maximize
    # We maximize the fed loads on the buses
    # We maximize SOE to allow battery to charge between two events
    # We minimize total losses
    obj = cp.Maximize(sum([ 2000*u1_i_t[i,t] + 1000*u2_i_t[i,t] + 500*u3_i_t[i,t]+ 250*u4_i_t[i,t]  for i in range(nob) for t in range(time)]) + 0.00000001 * sum([SOE_i_t[i,t] for i in range(nob) for t in range(time)]) - 0.000000000001 * sum([THL_t[t] for t in range(time)]))
    
    """constraints"""
    # The constraints in the problem may be constraints such as budget and duration.
    
    # creating a constraint list
    conslist = []
    
    # powerflow & line losses
    
    # power flow capacity of lines
    conslist.append(f_h_t >= -100)
    conslist.append(f_h_t <= 100 )    
    
    # we assumed total distribution losses as 2%.
    # Create a coefficient vector for matrix multiplication
    coeff_vector = np.full(nol, 0.02)
    
    # multiplying the power flow in the line by 2% we find the losses
    # Perform matrix multiplication
    conslist.append(THL_t == np.matmul(coeff_vector, absf))


    # feeder eq.s

    # physical constraint of main feeder (cannot be less than 0)
    conslist.append(0 <= P_f_i_t)
    
    # If it is the main feeder, it can power the grid as much as the feeder capacity.
    for t in range(time):
        conslist.append(P_f_i_t[:,t] <= h.iloc[:,6] * h.iloc[:,5])
                    
    
    # Convert the h DataFrame to a NumPy array for faster calculations
    h_array = h.to_numpy()
    
    # Create a 2D array with the shape of u1_i_t by repeating the h_array[:, 0] along the time axis
    h_array_2d1 = np.tile(h_array[:, 0], (time, 1)).T
    h_array_2d2 = np.tile(h_array[:, 1], (time, 1)).T
    h_array_2d3 = np.tile(h_array[:, 2], (time, 1)).T
    h_array_2d4 = np.tile(h_array[:, 3], (time, 1)).T
    
    # a load can only be fed if it is in the bus
    # Compare u1_i_t with the h_array_2d array
    conslist.append(u1_i_t <= h_array_2d1)
    conslist.append(u2_i_t <= h_array_2d2)
    conslist.append(u3_i_t <= h_array_2d3)
    conslist.append(u4_i_t <= h_array_2d4)
    
    # Convert E_i to a NumPy array
    E_i_array = np.array(E_i)
    
    # Multiply E_i_array by DoD
    DoD_E_i = DoD * E_i_array
    
    # Create a 2D array with the shape of SOE_i_t by repeating the DoD_E_i array along the time axis
    DoD_E_i_2d = np.tile(DoD_E_i, (time, 1)).T
    
    # instant state-of-energy cannot fall below the dept-of-discharge rate
    # Compare DoD_E_i_2d with the SOE_i_t array
    conslist.append(DoD_E_i_2d <= SOE_i_t)
    
    # Create a 2D array with the shape of SOE_i_t by repeating the E_i_array along the time axis
    E_i_2d = np.tile(E_i_array, (time, 1)).T
    
    # instant state-of-energy cannot exceed the battery energy capacity in the bus
    # Compare SOE_i_t with the E_i_2d array
    conslist.append(SOE_i_t <= E_i_2d)
    
    # The battery can only be charged as much as its empty energy capacity.
    # Calculate the constraint for all i and t
    conslist.append( BESS_ch_i_t * Eff_ch * delta_T <= E_i_2d - SOE_i_t)
    
    # The battery can only be discharged as much as the energy in it.
    # Calculate the constraint for all i and t
    conslist.append( BESS_dch_i_t * delta_T <= SOE_i_t)
    
    # charge-discharge physical constraints
    conslist.append( 0    <= BESS_ch_i_t)
    conslist.append( 0    <=  BESS_dch_i_t)
    
    # Initial value is entered for state-of-energy
    # Compare SOE_i_t for t=0 with E_i_array
    conslist.append( SOE_i_t[:, 0] == E_i_array)
    
    
    # Convert line and d DataFrames to NumPy arrays
    line_array = line.to_numpy()
    d_array = d.to_numpy()
    
    # we restrict the flow on the lines with the disable binary value d
    # Calculate the constraints for all l and t
    conslist.append( f_h_t <= line_array[:, 3].reshape(-1, 1) * d_array.T)
    conslist.append( f_h_t >= -line_array[:, 3].reshape(-1, 1) * d_array.T)
    
    # absolute value, positive and negative components of the power flow
    conslist.append( f_h_t == cf_plus - cf_minus)
    conslist.append( absf == cf_plus + cf_minus)

    #power balance
    for t in range(time):
        for i in range(nob):
            # Power balance at time t in each bus
            conslist.append(P_f_i_t[i,t]  + sum([f_h_t[l,t] for l in range(nol) if line.iloc[l,2] == i+1]) - sum([f_h_t[l,t] for l in range(nol) if line.iloc[l,1] == i+1]) + BESS_dch_i_t[i,t]*Eff_dch == P_load_i_t[i,t] + BESS_ch_i_t[i,t])
            # load fed in each bus at time t
            conslist.append(P_load_i_t[i,t] == u1_i_t[i,t]*loads.iloc[t,0]*h.iloc[i,0] + u2_i_t[i,t]*loads.iloc[t,1]*h.iloc[i,1] + u3_i_t[i,t]*loads.iloc[t,2]*h.iloc[i,2]  + u4_i_t[i,t]*loads.iloc[t,3]*h.iloc[i,3])
            # real load on each bus at time t
            conslist.append(P_load_i_t_real[i,t] == loads.iloc[t,0]*h.iloc[i,0] + loads.iloc[t,1]*h.iloc[i,1] + loads.iloc[t,2]*h.iloc[i,2]  + loads.iloc[t,3]*h.iloc[i,3])

            
            # physical cons. of discharging & charging
            conslist.append( BESS_ch_i_t[i,t] <= P_i[i]*v_i_t[i,t])
            conslist.append( BESS_dch_i_t[i,t] <= P_i[i]*(1-v_i_t[i,t]))        

                
            if t > 0:
                # periodical charge/discharge equation
                conslist.append( SOE_i_t[i,t] == SOE_i_t[i,t-1] + BESS_ch_i_t[i,t]*Eff_ch*delta_T - BESS_dch_i_t[i,t]*delta_T)
                
            
            
    """solving"""
    # In this section, commands are given to solve the problem.
    
    # Optimization problem is generated with objective function and constraint list.
    prob = cp.Problem(obj, conslist)
    
    # The open source code GLPK_MI solver is used, which can solve the Mixed-Integer Linear Programming (MILP) problem.
    prob.solve(solver=cp.GLPK_MI)
    
    
    print(prob.status)
    print(prob.value)
    
    
    
    
    """ printing response"""
    # print the resulting variable values in code
    
    u4 = pd.DataFrame()
    u1 = pd.DataFrame()
    u2 = pd.DataFrame()
    u3 = pd.DataFrame()
    
    Pload = pd.DataFrame()
    Pload_real = pd.DataFrame()
    
    
    
    for i in range(nob):
        for t in range(time):
            Pload.loc[t,i] = P_load_i_t[i,t].value
            Pload_real.loc[t,i] = P_load_i_t_real[i,t].value
            u4.loc[t,i] = u4_i_t[i,t].value
            u1.loc[t,i] = u1_i_t[i,t].value
            u2.loc[t,i] = u2_i_t[i,t].value
            u3.loc[t,i] = u3_i_t[i,t].value
            
    
    critical_points = [100, 75,50, 25]            
    
    total_u1 = sum(u1.sum(axis=1))          
    total_u2 = sum(u2.sum(axis=1))
    total_u3 = sum(u3.sum(axis=1))
    total_u4 = sum(u4.sum(axis=1))
    
    total_score = total_u1*critical_points[0] + total_u2*critical_points[1] + total_u3*critical_points[2] + total_u4*critical_points[3]
    
    max_u1 = sum(h["base"])*time
    max_u2 = sum(h["hos"])*time
    max_u3 = sum(h["tv"])*time
    max_u4 = sum(h["non"])*time
    
    max_score =  max_u1*critical_points[0] + max_u2*critical_points[1] + max_u3*critical_points[2] + max_u4*critical_points[3]
    
    player_score = round(total_score/max_score*100,2)

    model_timer_end = datetime.datetime.now()

    model_timer = model_timer_end - model_timer_start
    
    return player_score, Pload, Pload_real, model_timer




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
    
    






