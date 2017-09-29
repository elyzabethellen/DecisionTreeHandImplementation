# CS529-Fall2017

===== ===== ===== ===== </br>
CS 529 PROJECT 1: DECISION TREES </br>
Danny Byrd and Elizabeth E. Esterly (Team Neuromancer) </br>
Please read the following instructions to run our code. </br>

**IMPORTANT: Python 2.7.x is required. Some features may not work with Python 3.x. If you do not currently have Python 2.7.x on your system, you can install it here:* https://www.python.org/downloads/

<u>FILE LISTING</u><br>
<ul><li>pythontree.py - has all of the old stuff, but just the methods now, so everything we wrote for the tree</li>
    <li>data.py - has data helper methods, like the methods for loading a file, saving a file, and cross validation methods to divide data set into test / train </li>
    <li>experiments.py - has a preset list of experiments which are run as functions: 
        <ul>
        <li>INFO GAIN with all levels of CHI SQUARED CONFIDENCE </li>
        <li>GINI INDEX with all levels of CHI SQUARED CONFIDENCE </li>
        <li>KAGGLE - this one will load the dataset , make a tree with basic presets and create a submission file called sampleSubmission.csv </li>
        <li>KAGGLE Competition - this one does’t really have anything in it, but we could put our best experiment sample there or something </li><ul>
    <li>run.py runs the 4 experiment functions, you can turn on and off different parts </li>
    <li>featureBuilder.py - works on the imported data itself … there is a method called “preprocessData” (line: 133)  which has a list of transformations you can do on the data itself .. so like there are some commented out functions, each just modifies the data in place… so you can just turn them on or off (trees take a really long time with more of these, so we’d probably want to leave most of them off for the final turn in on the assignment)  and it gets called as data is imported, and as kaggle submissions are imported as well….so its a single point to change features for train / test 
    <li>launch.py - called from a shell script, this guy “runs” run.py … but first it checks python version is correct</li> 
    <li>launcher.sh - updated to run a python script, instead of an R script </li></ul>

===== ===== ===== ===== 
