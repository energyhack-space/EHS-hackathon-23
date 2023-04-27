<div align="center" id="top"> 
  <img src="./.github/app.gif" alt="Battery Placement and Sizing Game" />

  &#xa0;

  
</div>

<h1 align="center">&#128267; Battery Placement and Sizing Game &#128267;</h1>


<!-- Status -->

<!-- <h4 align="center"> 
	🚧  Batarya Yerleştirme ve Boyutlandırma Oyunu 🚀 Under construction...  🚧
</h4> 

<hr> -->


<br>

## :dart: About ##

This is a Python script that defines a simulation of a power grid's resiliency. It is a simulation that determines how resilient a power grid is when faced with failure scenarios. The script uses the CVXPY optimization library to find a solution to the power flow and resiliency problem.

The script defines a function called BESResiliencySimulation that takes four arguments. The first argument is failed_lines, which is a list of the lines that have failed. The second argument is P_i, which is a list of the power capacity of each bus. The third argument is E_i, which is a list of the energy capacity of the battery at each bus. The fourth argument is failed_periods, which is a list of tuples that indicate the periods of time during which a line is failed.

The function solves the power flow problem and determines how much load is fed to each bus. It also determines the amount of energy stored in the battery at each bus, whether the battery is charging or discharging, and the binary values that determine if the critical loads are being fed. Finally, the function calculates the player score, which is a metric that measures how well the power grid is performing in the given scenario.

The script also defines two classes: GraphDialog and Window. GraphDialog creates a dialog box for displaying the graphs of the results of the simulation, while Window creates the main window for the user interface.

## :sparkles: Excel Inputs ##

:heavy_check_mark: <strong>h:</strong> There is electrical load information about 33 busbars. It also contains information on which bus is the feeder and the feeder's feeding capacity.\
:heavy_check_mark: <strong>l:</strong> This input shows between which two bars the lines are located and includes the power flow capacities in the lines.\
:heavy_check_mark: <strong>powercurves:</strong> It shows the electricity consumption of load types for 1 day (15 minutes - 96 periods).

## :rocket: Packages ##

The following important packages were used in this project:

- [PyQt5](https://pypi.org/project/PyQt5/)
- [CVXPY](https://www.cvxpy.org/)


## :white_check_mark: Requirements ##

Before starting :checkered_flag:, you need to have <a href="https://code.visualstudio.com/download" target="_blank">VScode(Visual Studio Code)</a> installed.

## :checkered_flag: Starting ##

```bash
# Dowload the bess-game folder as a zip file and add it to your workspace in VScode
$ https://github.com/energyhack-space/EHS-hackathon-23/archive/refs/heads/main.zip

# create a virutal enviroment (venv)
$ py -3 -m venv venv

#activate the venv
$ venv\Scripts\activate 

# Install dependencies
$ pip install -r requirements.txt

# Run the project
$ app.py
```

## :memo: License ##

Made with :heart: by <a href="https://github.com/energyhack-space" target="_blank">energyhack-space</a>

&#xa0;

<a href="#top">Back to top</a>
