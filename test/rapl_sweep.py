import os
from parse import *
from time import *
from pprint import *


def test(benchmark, minW, maxW, step):
    output=[]
    for i in range(minW, maxW, step):
        # set rapl
        output.append({'date': time(), 'rapl': {}, 'perf': run_perf_return_dict(benchmark)})
    return output

def run_perf_return_dict(benchmark):
    output = os.popen('perf stat {} 2>&1 1>/dev/null'.format(benchmark)).read()
    output = output.split('\n') #split on \n ['val key # val key'.]
    output = map(lambda x: x.split('#'), output) #split on # : ['value key # value key',] -> [['value key', 'value key'],]
    output = [filter(lambda x: x is not '', el) for el in output] #remove empty elements
    output = filter(lambda x : x != [], output)
    output = list(output[1:]) #remove header
    output = [map(lambda x: x.split(' '), el) for el in output] # split on ' '
    output = [[[i for i in el if i is not ''] for el in line] for line in output]#filter '' away but keep line structure
    output = [[el for el in line if len(el)>0] for line in output]
    output = filter(lambda x: len(x)>0, output)
    output = [[[values[0], ' '.join(values[1:])] for values in l] for l in output]
    o={}
    old_n = 0
    for n, line in enumerate(output, start=0):
        if len(line) > 1:
            old_n = n
            o[line[0][1]] = {'value': line[0][0], line[1][1]: line[1][0]}
        elif len(line) is 1:
            o[output[old_n][0][1]][line[0][1]] = line[0][0]
    return o


if __name__ == "__main__":
    pprint(run_perf_return_dict('ls'))

