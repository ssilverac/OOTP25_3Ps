OOTP25 Player Performance Predictor (3Ps)

This project is being developed as a way to incorporate a variety of different python libraries
and design concepts to further develop my skills at programming. By the end not only do i hope to have a decent little program to tinker with, but most importantly,i hope to be able to write better, more efficient, and clean code.

The Idea:
The main goal of this project is to be able to implement a method to help me predict and target specific players who will improve my teams performance in OOTP25. By using Pandas and numpy to manipulate and engineer data, matplotlib and seaborn to visualize data, and *hopefully* a basic Neural Network to feed processed data to and hopefully make a decision on which player or players to acquire.

Background
 If youre not familiar with Out of the Park Baseball 25, it is a highly detailed and immersive baseball management simulation video game. In OOTP25, players take on the role of a team manager and general manager, guiding a baseball team through seasons with the goal of achieving success. The game features a comprehensive simulation of real-world baseball, including player stats, team dynamics, and league structures.

Why OOTP25?
1) Lots of data can be generated from this game
    * every player, every team, every game generates a ton of data. There are over 14,000 players from the major leagues down to the rookie leagues, each with a litany of statistics.
2) Neural networks require lots of data, so this fits nicely with that requirement.
3) since its a simulation game, its quick and easy to test out predictions, and generate more new data
4) I find baseball is fun!

Current Progress:
Project is still in its infancy. so far I have a working fileParser class.
    - This class takes raw data from OOTP25 and cleans and extracts relevant sections, creates a dataframe and saves it as a csv for later analysis.

Current focus:
Develop a Player, Team, and Season class, to house all the relevant data for each, and write functions to select, clean, and engineer relevant data.

Future Objectives:
Create an algorithm to automate the creation of relevant stats
Create a Neural Network from scratch (i.e without the use of external libraries)

Bare in mind, I am a beginer at programming. I have been using ChatGPT to as a sort of tutor and resource for learning. Any feedback, recommendations, suggestions etc would be appreciated.