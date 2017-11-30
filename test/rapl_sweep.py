import os
import json
from parse import *
from time import *


N=4
M=4
O=4
benchmark='ls'

def test(benchmark,minW,maxW,step):
    output=[]
    for i in range(minW, maxW, step):
        # set rapl

        output.append({'date': time(), 'rapl': {}, 'perf': run_perf_return_dict(benchmark)})
    with open('data_{}_{}W_{}W_{}.json'.format(benchmark,minW,maxW,time()),'w+') as file:
        json.dump(output, file)




def run_perf_return_dict(benchmark):
    output = os.popen('perf stat {} 2>&1 1>/dev/null'.format(benchmark)).read()
    print output
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
    for n, line in enumerate(output, start=0):
        if len(output) > n+1:
            if len(line) > 1 and len(output[n+1]) > 1:
                o[line[0][1]] = {'value': line[0][0], line[1][1]: line[1][0]}
            elif len(output[n+1]) is 1:
                o[line[0][1]] = {'value': line[0][0], line[1][1]: line[1][0], line[0][1]: output[0][0]}
        else:
            o[line[0][1]] = {'value': line[0][0]}
    print o
    return o


if __name__ == "__main__":
    run_perf_return_dict(benchmark)





