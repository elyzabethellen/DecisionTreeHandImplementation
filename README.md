# CS529-Fall2017

===== ===== ===== ===== </br>
CS 529 PROJECT 1: DECISION TREES </br>
Danny Byrd and Elizabeth E. Esterly (Team Neuromancer) </br>
Please read the following instructions to run our code. </br>

**IMPORTANT: Python 2.7.x is required. Some features may not work with Python 3.x. If you do not currently have Python 2.7.x on your system, you can install it here:* https://www.python.org/downloads/

<u>FILE LISTING</u><br>
<ul><li>Feature Extractor </ul>

for training:

**python featureBuilder.py [starting CSV file] [output CSV file]**

OR 

for testing: 

**python featureBuilder.py [starting CSV file] [output CSV file] h** 

... the extra h at the end is just a flag which turns off "Class" column (for the real data which won't have this column :)

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
