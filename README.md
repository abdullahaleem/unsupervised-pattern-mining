# ms-prefixspan
Prefx Span with different minimum item support aka MS-PS.

Prefix span is an algorithm used for sequential pattern mining. Traditionally, prefix span used a single minimum item support for all item. The problem with this approach is if the MIS is set to a low value there are alot of irrelevent patterns, and if set too high you miss out on rare items. In MS-PS there different MIS for each item and a parameter called Support Difference Constraint(max difference between support of 2 items).

This project was for the course Data mining and Text mining at Univeristy of Illinois at Chicago.

Group Members:- Abdullah Aleem and Hamidreza Almasai 

Note: Written with python 2

data_xxx.txt contains the sequences.
parameters_xxx.txt contains the parameters
result_xxx.txt is the file the results are written to.
msprefixspan.py runs the main algorithm.


There are 2 datasets of 100 and 1000 sequences for testing.
For new datasets and parameters, changed the name of inputs in  ___MAIN____ (Starting line 490)



Credits:-
Bing Liu, my data mining and text mining professor at UIC. This algorithm is adapted from his book, Web Data Mining.

