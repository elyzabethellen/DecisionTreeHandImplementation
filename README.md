# CS529-Fall2017

===== ===== ===== ===== </br>
CS 529 PROJECT 1: DECISION TREES </br>
Danny Byrd and Elizabeth E. Esterly (Team Neuromancer) </br>
Please read the following instructions to run our code. </br>

**IMPORTANT: Python 2.7.x is required. Some features may not work with Python 3.x. If you do not currently have Python 2.7.x on your system, you can install it here:* https://www.python.org/downloads/

<u>FILE LISTING</u><br>
<ul><li>pythontree.py - has all of the old stuff, but just the methods now, so everything we wrote for the tree
    <li>data.py - has data helper methods, like the methods for loading a file, saving a file, and cross validation methods to divide data set into test / train 
    <li>experiments.py - has a preset list of experiments which are run as functions (this is where you can write your own etc… data is ready to go by the time it gets here! ) … there are 4 functions that run: 
        INFO GAIN with all levels of CHI SQUARED CONFIDENCE 
        GINI INDEX with all levels of CHI SQUARED CONFIDENCE
        KAGGLE - this one will load the dataset , make a tree with basic presets and create a submission file called sampleSubmission.csv 
        KAGGLE Competition - this one does’t really have anything in it , but we could put our best experiment sample there or something 

    <li>run.py…. runs these 4 functions , so like if you open that file, you can turn off different parts (good if you just want to play, so like turn off 1-3 and then run the kaggle competition function where we can dump all our ambitions and dreams 
    
    <li>featureBuilder.py - got organized into functions , it doesn’t even read a file anymore!! now it just works on the imported data itself … there is a method called “preprocessData” (line: 133)  which has a list of transformations you can do on the data itself .. so like there are some commented out functions, each just modifies the data in place… so you can just turn them on or off (trees take a really long time with more of these, so we’d probably want to leave most of them off for the final turn in on the assignment)  and it gets called as data is imported, and as kaggle submissions are imported as well….so its a single point to change features for train / test 

    <li>launch.py - called from a shell script, this guy “runs” run.py … but first it checks python version is correct 
    <li>launcher.sh - updated to run a python script, instead of an R script …</ul>


this will build an output CSV file will the following additional features from the main data: 

it will label the DNA,and Class respectively and then add:

first, last characters, (first/last) 

a Y/N flag which covers if the given string is 25 % made of a particular character (there are four one for each AGTC, labeled as 25pA,25pT, etc...) ) 

then several sequences of 2 letters, these are output from the markov model which covers the probability a given transition occurs given a starting state 
so for ex the AT value means what is the probability of going from A to T, given you are in A . 
There is column for each possible transition. They were quantitative values so I binned them into 0,1,2,3,4 (the numbers correspond to ranges of P(.25, .50, .75 up to 1), with 0 being never happened at all)

Then there are a set of columns for every possible set of 4 letters (AGTC) ... with a (T/F) if they occur in a given string. 

annd just in case all of these features end up being useless...the last set of columns are each character from the DNA itself, they are just numbered.


===== ===== ===== ===== 
