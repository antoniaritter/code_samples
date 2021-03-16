# Feb 21 2020
# Antonia Ritter
# Line break algorithm 

# run: 
# python3 line_break_algorithm.py line_break_algorighm_test.txt 
# (a text file without line breaks) 

# Solution for a question for CS 252 (Algorithms) at Carleton College: 
# the badness of a paragraph is the sum of the squares of the 
# badnesses (white space at the end) of all lines by the paragraph, except 
# the last. Give a dynamic programming algorithm to find a minimum-badness 
# layout of a given paragraph. O(n^2).


import sys  #for reading file
import math
math.inf


# reads words from file
# fills list words of the individual words
# and leng of their lengths
# Hyphenates words longer than line width
def read(words, leng, L):
    file = open(sys.argv[1],"r")
    for word in file.readline().split():
        while (len(word) > L):
            word1 = word[:L-1]+"-"
            word2 = word[L-1:]
            words.append(word1)
            leng.append(len(word1))
            word = word2
        
        words.append(word)
        leng.append(len(word))
    n = len(words)


# bad is a list of n lists
# bad[i][j] = the badness^2 of
# a line from words i to j
# or = infinity if they don't fit or i>j 
# bad[0][0] = (L-length first word)^2
def fillBad(arr, leng, L):
    n = len(arr)

    for i in range(0, n):
        
        for j in range(0, n):
            
            if (i <= j):
                width = 0
                for k in range(i, j):
                    width = width + leng[k]+1
                width = width + leng[j]

                if ((L-width) >=0 ):
                    if (i==n-1):
                        arr[i][j]=0
                    else:
                        arr[i][j] = ((L - width)**2)
                else:
                    arr[i][j] = math.inf
   
            else: 
                arr[i][j] = math.inf
            
            #print(arr)


# cost[j] = cost of opt(j) 
# = cost of the opt layout of words 1 to j
# = min_k (cost[k] + bad[k][j-1])
# cost[1] is 1st word, etc

# breaks is a list where breaks[j] = i means
# words i to j is the last line of opt(j)
# i.e. breaks[2] = 0 -> words[0] through words[2]
def fillCost(cost, bad, breaks):
    n = len(cost)

    cost[0]=0

    for j in range(1, n):

        cost[j] = math.inf

        for k in range(0, j):

            if (bad[k][j-1] != math.inf and
                cost[k]+bad[k][j-1] < cost[j]
            ): 
                cost[j] = cost[k]+bad[k][j-1]
                breaks[j-1] = k
    #print("cost =", cost)
    #print("breaks =", breaks)



# backwards is a list of the indices of
# the words that end the lines of the 
# opt layout, but backwards
# built using breaks; if breaks[j]=i then 
# if a line ends with j, the line before 
# it ends with i-1

# this function builds backwards and then
# uses it to print the layout
def layout(words, breaks, L):

    backwards = []
    w = len(words)-1
    while w>=0:
        backwards.append(w)
        w = breaks[w]-1

    w = 0
    for i in range(len(backwards)-1, -1, -1):
        Line = ""
        while w<=backwards[i]:
            Line = Line + words[w] + " "
            w = w+1
        print(Line)



def main():
    try:
        L = int(input("Enter width of line: "))
    except ValueError:
        print("Error: Enter an integer \n")

    # a list of strings
    words = []  
    # a list of ints, the lengths of words in words
    leng = []   

    # fill words an leng from file
    read(words, leng, L)
 
    n = len(words)
    # bad is a list of n-1 lists of length n-1
    bad = [[None for i in range(n)] for i in range(n)]
    # cost is a list length n
    cost = [None for i in range(n+1)]
    # cost is a list length n
    breaks = [None for i in range(n+1)]

    # fill the bad list
    fillBad(bad, leng, L)

    # fill the cost list
    fillCost(cost, bad, breaks)

    #tests...
    #print("words =", words)
    #print("bad =", bad)
    #print("breaks =", breaks)

    # use the breaks list to arrange
    # and print the words 
    print("")
    layout(words, breaks, L)

main()
