How to run the app!

1. "Run" the code
2. Within your Terminal, type 
   streamlit run app.py
   This should launch in your web browser if streamlit is installed
3. Obtain college basketball stats online for your team
4. Input these stats into the app
5. Check your team's chances for March Madness!

How it works!

1. After reviewing datasets of past March Madness tournaments, I've set the code to use a teams stats to calculate a Power Score from 0 to 1.

2. Designating probabilities based on historical advancement per seed served as a baseline as well.

3. Probabilities are then slightly increased or decreased from these baselines based on how strong the team's Power Score is relative to the average.

4. The result should offer a realistic estimate of a team's chances based on the success past teams with similar stats have recorded.