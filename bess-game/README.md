<div align="center" id="top"> 
  <img src="./.github/app.gif" alt="20230426 Hackathon Bess Game Github" />

  &#xa0;

  <!-- <a href="https://20230426hackathonbessgamegithub.netlify.app">Demo</a> -->
</div>

<h1 align="center">20230426 Hackathon Bess Game Github</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/{{YOUR_GITHUB_USERNAME}}/20230426-hackathon-bess-game-github?color=56BEB8">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/{{YOUR_GITHUB_USERNAME}}/20230426-hackathon-bess-game-github?color=56BEB8">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/{{YOUR_GITHUB_USERNAME}}/20230426-hackathon-bess-game-github?color=56BEB8">

  <img alt="License" src="https://img.shields.io/github/license/{{YOUR_GITHUB_USERNAME}}/20230426-hackathon-bess-game-github?color=56BEB8">

  <!-- <img alt="Github issues" src="https://img.shields.io/github/issues/{{YOUR_GITHUB_USERNAME}}/20230426-hackathon-bess-game-github?color=56BEB8" /> -->

  <!-- <img alt="Github forks" src="https://img.shields.io/github/forks/{{YOUR_GITHUB_USERNAME}}/20230426-hackathon-bess-game-github?color=56BEB8" /> -->

  <!-- <img alt="Github stars" src="https://img.shields.io/github/stars/{{YOUR_GITHUB_USERNAME}}/20230426-hackathon-bess-game-github?color=56BEB8" /> -->
</p>

<!-- Status -->

<!-- <h4 align="center"> 
	🚧  20230426 Hackathon Bess Game Github 🚀 Under construction...  🚧
</h4> 

<hr> -->

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/{{YOUR_GITHUB_USERNAME}}" target="_blank">Author</a>
</p>

<br>

## :dart: About ##

This is a Python script that defines a simulation of a power grid's resiliency. It is a simulation that determines how resilient a power grid is when faced with failure scenarios. The script uses the CVXPY optimization library to find a solution to the power flow and resiliency problem.

The script defines a function called BESResiliencySimulation that takes four arguments. The first argument is failed_lines, which is a list of the lines that have failed. The second argument is P_i, which is a list of the power capacity of each bus. The third argument is E_i, which is a list of the energy capacity of the battery at each bus. The fourth argument is failed_periods, which is a list of tuples that indicate the periods of time during which a line is failed.

The function solves the power flow problem and determines how much load is fed to each bus. It also determines the amount of energy stored in the battery at each bus, whether the battery is charging or discharging, and the binary values that determine if the critical loads are being fed. Finally, the function calculates the player score, which is a metric that measures how well the power grid is performing in the given scenario.

The script also defines two classes: GraphDialog and Window. GraphDialog creates a dialog box for displaying the graphs of the results of the simulation, while Window creates the main window for the user interface.

## :sparkles: Features ##

:heavy_check_mark: Feature 1;\
:heavy_check_mark: Feature 2;\
:heavy_check_mark: Feature 3;

## :rocket: Technologies ##

The following tools were used in this project:

- [Expo](https://expo.io/)
- [Node.js](https://nodejs.org/en/)
- [React](https://pt-br.reactjs.org/)
- [React Native](https://reactnative.dev/)
- [TypeScript](https://www.typescriptlang.org/)

## :white_check_mark: Requirements ##

Before starting :checkered_flag:, you need to have [Git](https://git-scm.com) and [Node](https://nodejs.org/en/) installed.

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone https://github.com/{{YOUR_GITHUB_USERNAME}}/20230426-hackathon-bess-game-github

# Access
$ cd 20230426-hackathon-bess-game-github

# Install dependencies
$ yarn

# Run the project
$ yarn start

# The server will initialize in the <http://localhost:3000>
```

## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.


Made with :heart: by <a href="https://github.com/{{YOUR_GITHUB_USERNAME}}" target="_blank">{{YOUR_NAME}}</a>

&#xa0;

<a href="#top">Back to top</a>
