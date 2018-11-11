# ms-prefixspan
Prefx Span with different minimum item support aka MS-PS.

Prefix span is algorithm used for sequential pattern mining. Traditionally, prefix span used a single minimum item support for all item. The problem with this approach is if the MIS is set to a low value there is alot of irrelevent patterns, and if set too high you miss out on important pattern. In MS-PS there different MIS for each item and a parameter called Support Difference Constraint(max difference between support of 2 items).

This project was for the course Data mining and Text mining at Univeristy of Illinois at Chicago.

Group Members:- Abdullah Aleem and Hamidreza Almasai 

data_xxx.txt contains the sequences.
parameters_xxx.txt contains the parameters
result_xxx.txt is the file the results are written to.
msprefixspan.py runs the main algorithm.


There are 2 datasets of 100 and 1000 sequences for testing.
For new datasets and parameters, changed the name of inputs in  ___MAIN____ (Starting line 490)





The algorithm, taken from the book written by my professor, Bing Liu:

1. Find every item i whose actual support in the sequence database S is at
least MIS(i). i is called a frequent item.
2. Sort all the discovered frequent items in ascending order according to
their MIS values. Let i1, …, iu be the frequent items in the sorted order.
3. For each item ik in the above sorted order:
  (i) identify all the data sequences in S that contain ik and at the same
  time remove every item j in each sequence that does not satisfy
  |sup(j) – sup(ik)| ≤ SDC. The resulting set of sequences is denoted by Sk.
  Note that we are not using ik as the prefix to project the database S.
  (ii) call the function r-PrefixSpan(ik, Sk, count(MIS(ik))) (restricted PrefixSpan),
  which finds all sequential patterns that contain ik, i.e., no
  pattern that does not contain ik should be generated. r-PrefixSpan()
  uses count(MIS(ik)) (the minimum support count in terms of the
  number of sequences) as the only minimum support for mining in Sk.
  The sequence count is easier to use than the MIS value in percentage,
  but they are equivalent. Once the complete set of such patterns
  is found from Sk, All occurrences of ik are removed from S.

r-PrefixSpan() is almost the same as PrefixSpan with one important difference.
During each recursive call, either the prefix or every sequence in the
projected database must contain ik because, as we stated above, this function
finds only those frequent sequences that contain ik. Another minor difference
is that the support difference constraint needs to be checked during
each projection as sup(ik) may not be the lowest in the pattern.


