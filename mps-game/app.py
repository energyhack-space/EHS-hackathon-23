
from PyQt5.QtWidgets import QLineEdit, QScrollArea, QSizePolicy, QGridLayout, QApplication, QWidget, QLabel, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QDesktopWidget, QSpinBox, QFrame, QPushButton, QMessageBox, QHeaderView, QProgressDialog, QProgressBar
from PyQt5.QtGui import QPixmap, QIcon, QMovie, QFont
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QApplication

import sys
import datetime


import pulp as pl
import random 
import numpy as np
import pandas as pd

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QApplication

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


def MPSGameSimulation(no_ess, no_gen):

    model_timer_start = datetime.datetime.now()

    
    """optimization problem"""
    power = pl.LpProblem("power", pl.LpMaximize)
    
    
    
    """sets"""
    
    T = 48
    
    
    bar = pd.read_excel('i_10i_sce2.xlsx')
    B = len(bar)
    
    ess = pd.read_excel('ess.xlsx')
    
    if no_ess > 0:
        ess = pd.concat([ess] * no_ess, ignore_index=True)
    else:
        ess = pd.DataFrame()
    
    S = len(ess)
    
    gen = pd.read_excel('gen.xlsx')
        
    if no_gen > 0:
        gen = pd.concat([gen] * no_gen, ignore_index=True)
    else:
        gen = pd.DataFrame()
        
        
    G = len(gen)
    
    M = S + G
    
    line = pd.read_excel('l_10i.xlsx')
    L = len(line)
    
    
    
    
    """parameters"""
    
        
        
    x_i = bar["x_i"] # Priority of load at bus i.
    Nmps_i = bar["N_mps"] # Available MPS connection points of bus i.
    
        
    Pdemand_t_i = pd.read_excel('demand_10i.xlsx')
    
    Ttravels_i_j = pd.read_excel('Ttravels.xlsx') # bus to bus travel time matrix
    Ttravelg_i_j = pd.read_excel('Ttravelg.xlsx')  # bus to bus travel time matrix
    
    station = [1 if deger > 0 else 0 for deger in Nmps_i] # 1 if MPS station is present, 0 otherwise
    station[0] = M
    
    
    teta_g = pd.DataFrame(np.ones((48, 10))) # busbars inaccessible due to road damage
    
    failed_roads = random.sample(range(1, 10), 2) # list of damaged road IDs
    
    teta_s = pd.DataFrame(np.ones((48, 10))) # busbars inaccessible due to road damage
    
    failed_periods_r = [[22, 28], [22, 33]] # road fail periods
    
    for num in range(len(failed_roads)):
        
        if num == 0:
            if failed_roads[num] == 1:
                teta_s.iloc[failed_periods_r[0][0]:failed_periods_r[0][1], 4:10] = 0
            elif failed_roads[num] == 2:
                teta_s.iloc[failed_periods_r[0][0]:failed_periods_r[0][1], 1:4] = 0
            elif failed_roads[num] == 3:
                teta_s.iloc[failed_periods_r[0][0]:failed_periods_r[0][1], 2:4] = 0
            elif failed_roads[num] == 4:
                teta_s.iloc[failed_periods_r[0][0]:failed_periods_r[0][1], 3] = 0
            elif failed_roads[num] == 5:
                teta_s.iloc[failed_periods_r[0][0]:failed_periods_r[0][1], 5:10] = 0
            elif failed_roads[num] == 6:
                teta_s.iloc[failed_periods_r[0][0]:failed_periods_r[0][1], 6:10] = 0
            elif failed_roads[num] == 7:
                teta_s.iloc[failed_periods_r[0][0]:failed_periods_r[0][1], 7:8] = 0
            elif failed_roads[num] == 8:
                teta_s.iloc[failed_periods_r[0][0]:failed_periods_r[0][1], 8] = 0
            elif failed_roads[num] == 9:
                teta_s.iloc[failed_periods_r[0][0]:failed_periods_r[0][1], 9] = 0
    
    
        else:
            
            if failed_roads[num] == 1:
                teta_s.iloc[failed_periods_r[1][0]:failed_periods_r[1][1], 4:10] = 0
            elif failed_roads[num] == 2:
                teta_s.iloc[failed_periods_r[1][0]:failed_periods_r[1][1], 1:4] = 0
            elif failed_roads[num] == 3:
                teta_s.iloc[failed_periods_r[1][0]:failed_periods_r[1][1], 2:4] = 0
            elif failed_roads[num] == 4:
                teta_s.iloc[failed_periods_r[1][0]:failed_periods_r[1][1], 3] = 0
            elif failed_roads[num] == 5:
                teta_s.iloc[failed_periods_r[1][0]:failed_periods_r[1][1], 5:10] = 0
            elif failed_roads[num] == 6:
                teta_s.iloc[failed_periods_r[1][0]:failed_periods_r[1][1], 6:10] = 0
            elif failed_roads[num] == 7:
                teta_s.iloc[failed_periods_r[1][0]:failed_periods_r[1][1], 7:8] = 0
            elif failed_roads[num] == 8:
                teta_s.iloc[failed_periods_r[1][0]:failed_periods_r[1][1], 8] = 0
            elif failed_roads[num] == 9:
                teta_s.iloc[failed_periods_r[1][0]:failed_periods_r[1][1], 9] = 0
    
    
    failed_periods = [[22,27], [22,32], [22,38]] # line fail periods
    failed_lines = random.sample(range(1, 9), 3) # list of damaged road IDs
    failed_lines = sorted(failed_lines)
    
    # fail matrix
    # binary value for damage of lines, 1 is available line 0 is damaged line
    d = pd.DataFrame(np.ones((T, L)))
    
    for f in range(len(failed_periods)):
        rows_to_change =  list(range(failed_periods[f][0],failed_periods[f][1]))
        d.iloc[rows_to_change, failed_lines[f]] = 0
        
    
    """variables"""
    
    Pd_i_t = {(i,t): pl.LpVariable(cat=pl.LpContinuous, name="Pd_i_t_{}_{}".format(i,t)) for i in range(B) for t in range(T)} # Total restored power demand at bus 𝑖 during period 𝑡 [kW]
    
    Pch_s_i_t = {(s,i,t): pl.LpVariable(cat=pl.LpContinuous, name="Pch_s_i_t_{}_{}_{}".format(s,i,t)) for s in range(S) for i in range(B) for t in range(T)} # Charging power of MESS 𝑒 during period 𝑡 [kW].
    Pdch_s_i_t = {(s,i,t): pl.LpVariable(cat=pl.LpContinuous, name="Pdch_s_i_t_{}_{}_{}".format(s,i,t)) for s in range(S) for i in range(B) for t in range(T)} # Discharging power of MESS 𝑒 during period 𝑡 [kW]
    P_g_i_t = {(g,i,t): pl.LpVariable(cat=pl.LpContinuous, name="P_g_i_t_{}_{}_{}".format(g,i,t)) for g in range(G) for i in range(B) for t in range(T)}  # Output power of MEG 𝑔 during period 𝑡 [kW].
    
    mu_s_i_t = {(s,i,t): pl.LpVariable(cat=pl.LpBinary, name="mu_s_i_t_{}_{}_{}".format(s,i,t)) for s in range(S) for i in range(B) for t in range(T)} # Binary variable; 1 if MPS 𝑚 is connected to bus 𝑖, else 0.
    mu_g_i_t = {(g,i,t): pl.LpVariable(cat=pl.LpBinary, name="mu_g_i_t_{}_{}_{}".format(g,i,t)) for g in range(G) for i in range(B) for t in range(T)} # Binary variable; 1 if MPS 𝑚 is connected to bus 𝑖, else 0.
    
    SOC_s_t = {(s,t): pl.LpVariable(cat=pl.LpContinuous, name="SOC_s_t_{}_{}".format(s,t)) for s in range(S) for t in range(T)} # State of energy of MESS 𝑒 at period 𝑡 [kWh].
    
    u_s_i_t = {(s,i,t): pl.LpVariable(cat=pl.LpBinary, name="u_s_i_t_{}_{}_{}".format(s,i,t)) for s in range(S) for i in range(B) for t in range(T)} # Binary variable; 1 if MESS 𝑒 is charging, else 0.
    
    Pf_i_t = {(i,t): pl.LpVariable(cat=pl.LpContinuous, name="Pf_i_t_{}_{}".format(i,t)) for i in range(B) for t in range(T)} # Total active power provided by substation at bus 𝑖 during period 𝑡 [kW].
    Pfload_i_t = {(i,t): pl.LpVariable(cat=pl.LpContinuous, name="Pfload_i_t_{}_{}".format(i,t)) for i in range(B) for t in range(T)} # Active power provided by substation at bus 𝑖 to meet demand during period 𝑡 [kW].
    
    f_h_t = {(l,t): pl.LpVariable(cat=pl.LpContinuous, name="f_h_t_{}_{}".format(l,t)) for l in range(L) for t in range(T)} # Active power flow of branch 𝑙 during period t [kW]
    
    Pmps_i_t = {(i,t): pl.LpVariable(cat=pl.LpContinuous, name="Pmps_i_t_{}_{}".format(i,t)) for i in range(B) for t in range(T)} # Total power output of MPS during period 𝑡 [kW].
    Pmpsload_i_t = {(i,t): pl.LpVariable(cat=pl.LpContinuous, name="Pmpsload_i_t_{}_{}".format(i,t)) for i in range(B) for t in range(T)} # MPS output power for supplying load demand during period 𝑡 [kW].
    
    # positive and negative components of f_h_t
    cf_plus = {(l,t): pl.LpVariable(cat=pl.LpContinuous, name="cf_plus_{}_{}".format(l,t)) for l in range(L) for t in range(T)}
    cf_minus = {(l,t): pl.LpVariable(cat=pl.LpContinuous, name="cf_minus_{}_{}".format(l,t)) for l in range(L) for t in range(T)}
    
    # absolute value of f_h_t
    absf = {(l,t): pl.LpVariable(cat=pl.LpContinuous, name="absf_{}_{}".format(l,t)) for l in range(L) for t in range(T)}
    
    """objective func"""
    power += pl.lpSum([x_i[i]*Pd_i_t[i,t] for i in range(B) for t in range(T)])  + 0.0001*pl.lpSum([mu_s_i_t[s,i,t] for s in range(S) for i in range(B) for t in range(T)]) + 0.0001*pl.lpSum([mu_g_i_t[g,i,t] for g in range(G) for i in range(B) for t in range(T)])
    
    
    """constraints"""
    
    #mps connection
    for t in range(T):
        if t < 22:
            for s in range(S):
                power += mu_s_i_t[s,0,t] >= 1
            for g in range(G):
                power += mu_g_i_t[g,0,t] >= 1
                
        for s in range(S):
            power += pl.lpSum([mu_s_i_t[s,i,t] for i in range(B)]) <= 1
        for g in range(G):
            power += pl.lpSum([mu_g_i_t[g,i,t] for i in range(B)]) <= 1
    
        """dent"""
        for i in range(B):
            for s in range(S):
                power += mu_s_i_t[s,i,t] <= teta_s.iloc[t,i]
            for g in range(G):
                power += mu_g_i_t[g,i,t] <= teta_g.iloc[t,i]
        """dent"""
            
        for i in range(B):
            if station[i] == 1:
                mus = pl.lpSum([mu_s_i_t[s,i,t] for s in range(S)])
                mug = pl.lpSum([mu_g_i_t[g,i,t] for g in range(G)])
                mum = mus + mug
            
                power += mum <= Nmps_i[i]
    
    
    #turn node i
                
    dmgPend = 0
    
    for l in range(L):
        for t in range(T):
            if t+1 < T:
                if d.iloc[t,l] - d.iloc[t+1,l] < 0:
                    dmgPend = t
                    tao = Ttravelg_i_j.iloc[l+1,0]
                    arri = dmgPend + tao
                   
                    
                        
            
    for t in range(T):            
        if t > arri+1:
            for s in range(S):
                power += mu_s_i_t[s,0,t] >= 1
            for g in range(G):
                power += mu_g_i_t[g,0,t] >= 1 
                
                
    
    #mps rooting
                
    
    for t in range(T):
        for g in range(G):
            for j in range(B):
                for i in range(B):
                    
                    if j!=i and t+Ttravelg_i_j.iloc[i,j] < T :
                        for tao in range(Ttravelg_i_j.iloc[i,j]):
                            power += mu_g_i_t[g,i,t+tao+1] + mu_g_i_t[g,j,t] <= 1
    
                        
        for s in range(S):
            for j in range(B):
                for i in range(B):
                    if j!=i and t+Ttravels_i_j.iloc[i,j] < T :
                        for tao in range(Ttravels_i_j.iloc[i,j]):
                            power += mu_s_i_t[s,i,t+tao+1] + mu_s_i_t[s,j,t] <= 1
    
                            
    #mps power scheduling
    for t in range(T):
        for s in range(S):
            if t <= 23:
                power += SOC_s_t[s,t] == ess.iloc[s,6]
            else:
                power += SOC_s_t[s,t] == SOC_s_t[s,t-1] + pl.lpSum([(Pch_s_i_t[s,i,t-1]*ess.iloc[s,3])*0.50 for i in range(B) if station[i]==1]) - pl.lpSum([(Pdch_s_i_t[s,i,t-1]*(1/ess.iloc[s,3]))*0.50 for i in range(B) if station[i]==1])
                
            power += SOC_s_t[s,t] >= ess.iloc[s,5]
            power += SOC_s_t[s,t] <= ess.iloc[s,6]    
                
                
    for t in range(T):
        for i in range(B):
            if station[i] == 1:
                for s in range(S):
                    
    
                    power += Pch_s_i_t[s,i,t] >= 0
                    power += Pch_s_i_t[s,i,t] <= mu_s_i_t[s,i,t]*ess.iloc[s,4]
                    power += Pdch_s_i_t[s,i,t] >= 0
                    power += Pdch_s_i_t[s,i,t] <= mu_s_i_t[s,i,t]*ess.iloc[s,4]
                    power += Pch_s_i_t[s,i,t] <= ess.iloc[s,4]*u_s_i_t[s,i,t]
                    power += Pdch_s_i_t[s,i,t] <= ess.iloc[s,4]*(1-u_s_i_t[s,i,t])
                    
                    power += u_s_i_t[s,i,t] <= mu_s_i_t[s,i,t]
                    
                    
                    #baradan ayrılan araç ne şarj olabilir ne deşarj olabilir? mu ile yukarıdaki denklemleri çarpmak gerekebilir
                for g in range(G):
                    power += P_g_i_t[g,i,t] >= 0   
                    power += P_g_i_t[g,i,t] <= mu_g_i_t[g,i,t]*gen.iloc[g,3]
                                       
    #power balance
    
    for t in range(T):
        for i in range(B):
            # power += Pfload_i_t[i,t] + Pmpsload_i_t[i,t] +  pl.lpSum([d.iloc[t,l]*f_h_t[l,t]*alfa.iloc[t,l] for l in range(L) if line.iloc[l,2] == i+1]) - pl.lpSum([d.iloc[t,l]*f_h_t[l,t]*alfa.iloc[t,l] for l in range(L) if line.iloc[l,1] == i+1]) == Pd_i_t[i,t] 
            power += Pfload_i_t[i,t] + Pmpsload_i_t[i,t] +  pl.lpSum([f_h_t[l,t] for l in range(L) if line.iloc[l,2] == i+1]) - pl.lpSum([f_h_t[l,t] for l in range(L) if line.iloc[l,1] == i+1]) == Pd_i_t[i,t] 
            
            power += Pd_i_t[i,t] >= 0
            power += Pd_i_t[i,t] <= Pdemand_t_i.iloc[t,i]
            
            if station[i] == 1:
                power += Pmpsload_i_t[i,t] == pl.lpSum([Pdch_s_i_t[s,i,t] for s in range(S)]) - pl.lpSum([Pch_s_i_t[s,i,t] for s in range(S)]) + pl.lpSum([P_g_i_t[g,i,t] for g in range(G)])
                power += Pmps_i_t[i,t] == Pmpsload_i_t[i,t]
                
            else:
                power += Pmpsload_i_t[i,t] == 0
                power += Pmps_i_t[i,t] == 0
            
    for t in range(T):
        for l in range(L):
            
            power += f_h_t[l,t]  >= -line.iloc[l,3]      
            power += f_h_t[l,t]   <=  line.iloc[l,3]
    
    for t in range(T):
        for i in range(B):
            if bar.iloc[i,1] == 1:
                power += 0 <= Pf_i_t[i,t]
                power += 0 <= Pfload_i_t[i,t]
    
                power += Pf_i_t[i,t] <= bar.iloc[i,2] 
                
                power += Pf_i_t[i,t] == Pfload_i_t[i,t] 
                    
            elif bar.iloc[i,1] == 0:
                
                power += Pf_i_t[i,t] == 0
                power += Pfload_i_t[i,t] == 0
    
    
    
    for l in range(L):
        for t in range(T):
            # we restrict the flow on the lines with the disable binary value d
            # Calculate the constraints for all l and t
            power += f_h_t[l,t] <= line.iloc[l,3]*d.iloc[t,l]
            power += f_h_t[l,t]  >=  -line.iloc[l,3]*d.iloc[t,l]
            # absolute value, positive and negative components of the power flow
            power += f_h_t[l,t] == cf_plus[l,t] - cf_minus[l,t]
            power += absf[l,t] == cf_plus[l,t] + cf_minus[l,t]
    
    
           
    
    
    
    power.solve(pl.GLPK_CMD() )
    
    print("Status:", pl.LpStatus[power.status])   
    
    """print"""
    
    
    
    Pd = pd.DataFrame()
    mugg = pd.DataFrame()
    muss = pd.DataFrame()
    
    for i in range(B):
        for t in range(T):
            Pd.loc[t,i] = Pd_i_t[i,t].varValue
            
            if G>0:
                mugg.loc[t,i] = mu_g_i_t[0,i,t].varValue
            if S>0:
                muss.loc[t,i] = mu_s_i_t[0,i,t].varValue
    
    Pload = Pd
    Pload_real = Pdemand_t_i.copy()
    Pload_real.columns = range(Pload_real.shape[1])
    
    # Tüm hücrelerin toplamını alın
    total_score = Pd.to_numpy().sum()
    
    max_score = Pdemand_t_i.to_numpy().sum()
    
    player_score = total_score/max_score*100

    model_timer_end = datetime.datetime.now()

    model_timer = model_timer_end - model_timer_start
    

    return player_score, Pload, Pload_real, model_timer
  

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Sabitler
        self.ROW_COUNT = 1
        self.COL_COUNT = 2
        screen_rect = QDesktopWidget().screenGeometry()


        self.GAME_TITLE = "Mobil Güç Sistemleri Oyunu"

        self.setWindowTitle(self.GAME_TITLE)
        self.setWindowIcon(QIcon("ehs-logo-1-mini-2.png"))
        self.setStyleSheet("background-color: white;")

        
        layout = QHBoxLayout()
        
                
       
       
       # LEFT Layout
        frame = QFrame()
        frame.setStyleSheet("background-color: white;")
        
        frame_layout = QVBoxLayout()
        frame_layout.setAlignment(Qt.AlignCenter)



        # resmi
        self.image = QLabel(self)
        pixmap = QPixmap('10-bus.png').scaledToWidth(int(screen_rect.width()/2) - 90)
        self.image.setPixmap(pixmap)
        frame_layout.addWidget(self.image)
        frame.setLayout(frame_layout)
        
        # Buton
        button = QPushButton("Optimizasyonu Başlat!")
        button.setStyleSheet("background-color: turquoise; border-radius: 10px; height: 40px; color: white; font-weight: bold;")
        button.clicked.connect(self.perform_optimization)
        frame_layout.addWidget(button)
        frame.setLayout(frame_layout)

        # Arka plan başlığı
        self.title_label = QLabel(self)
        self.title_label.setText(self.GAME_TITLE)
        self.title_label.setStyleSheet("font-weight: bold; font-size:44px; font-family: Open Sans; color: turquoise;")
        self.title_label.setFixedWidth(int(screen_rect.width()/2) - 90)
        frame_layout.addWidget(self.title_label)
        frame.setLayout(frame_layout)        
        
        self.title_label = QLabel(self)
        self.title_label.setText("<p>Oyun yönergeleri aşağıdaki gibidir:</p>"
                                "<ol>"
                                "<li>Sağ taraftaki tablodan tır tipi depolama ve off-road jeneratör sayılarını seçiniz</li>"
                                "<li>Optimizasyonu başlat butonuna basınız</li>"
                                "<li>Optimizasyonun çözüm süresi bilgisayarınız ile ilgilidir</li>"
                                "</ol>")
        self.title_label.setStyleSheet("font-size: 15px; font-family: Open Sans; color: #173a90;")
        self.title_label.setFixedWidth(int(screen_rect.width()/2) - 90)
        frame_layout.addWidget(self.title_label)
        frame.setLayout(frame_layout)


        # RIGHT Layout
        frame_r = QFrame()
        frame_r.setStyleSheet("background-color: white;")
        frame_layout_r = QVBoxLayout()
        frame_layout_r.setAlignment(Qt.AlignCenter)
        
        
        # Arka plan resmi
        self.image = QLabel(self)
        pixmap = QPixmap('mps-3.png').scaledToWidth(int(screen_rect.width()/2) - 90)
        self.image.setPixmap(pixmap)

        frame_layout_r.addWidget(self.image, alignment=Qt.AlignCenter)
        frame_r.setLayout(frame_layout_r) 

        # Table Start
        self.table = QTableWidget(self)
        self.table.setColumnCount( self.COL_COUNT)
        self.table.setRowCount( self.ROW_COUNT)

        for i in range(0,  self.ROW_COUNT):
            for j in range(0, self.COL_COUNT):
                spinbox = QSpinBox(self)
                spinbox.setRange(0, 20)
                spinbox.setSingleStep(1)
                self.table.setCellWidget(i, j, spinbox)

        # Sütun isimleri
        labels = ["# Mobile Energy Storage", "# Mobile Generator System"]
        self.table.setHorizontalHeaderLabels(labels)

        # Sütun genişliği
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # Sütun genişlikleri
        table_width = self.table.width()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setDefaultSectionSize(int(table_width / self.table.columnCount())) 

        # Set the table height to fit the page
        table_height = int(screen_rect.height() / 12)
        self.table.setMaximumHeight(table_height)
        self.table.setFixedWidth(int(screen_rect.width()/2) - 90)

        frame_layout_r.addWidget(self.table, alignment=Qt.AlignCenter)
        frame_r.setLayout(frame_layout_r)  
        
        
        layout.addWidget(frame, Qt.AlignCenter)
        layout.addWidget(frame_r, Qt.AlignCenter)

        # layout.addWidget(frame)
        # layout.addWidget(frame_r)



        self.setLayout(layout)

        # Pencere boyutunu ayarla
        self.resize(screen_rect.width() -150, screen_rect.height()-150)


    
    def perform_optimization(self):
        print("Optimizasyon Başladı!!")
        BESSTruckCount = self.table.cellWidget(0, 0).value()
        GenTruckCount = self.table.cellWidget(0, 1).value()

        # print(f'BESS Tir: {BESSTruckCount}')
        # print(f'Jenerator Tir: {GenTruckCount}')

         # Show the "Processing" message box
        progress = QMessageBox(self)
        progress.setWindowTitle("Güç Sistemi Optimizasyonu")
        progress.setWindowModality(Qt.WindowModal)
        progress.setWindowFlags(progress.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        progress.setText("İşlem sürüyor, lütfen bekleyin... Bilgisayar hızınıza göre ~10 dk civarı sürebilir.")
        progress.show()
        progress.button(QMessageBox.Ok).setDisabled(True)

        QApplication.processEvents()  # Update the GUI to show the message box

        player_score, Pload, Pload_real, model_timer = MPSGameSimulation(BESSTruckCount,GenTruckCount)

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




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())