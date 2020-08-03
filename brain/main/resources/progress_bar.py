"""
Author: Team Alpha Squad
Date  : Sat Aug 01 2020
Desc  : This Progress bar can be added in a python code to make console more interactive
Functions :
    printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r")
    inputs:
        iteration : current iteration number
        total     : total number of iterations
        prefix    : text before progressbar
        suffix    : text after progressbar
        decial    : result upto decimals
        length    : length of progressbar
        fill      : character to fill in progressbar
"""

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

