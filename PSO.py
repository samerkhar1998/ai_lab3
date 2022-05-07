from algorithems import *
from settings import GA_MAXITER,NQUEENS
from random import choice
def create_results_file(name):
    file = open(fr"outputs\{name}", "r")
    f = open(fr"newoutput\{name}", "w+")
    for _ in range(50):f.write("-")

    lines = file.readlines()
    lines = [x.split(' ') for x in lines]
    spaceforfirst=20
    for index,line in enumerate(lines):
        if line[:2]=="GA" or line[:2]=="TS" or line[:2]=="SA" or line[:2]=="AC":
            f.write("|")
            f.write(str(line))
            for i in range(len(line)-spaceforfirst):
                f.write(" ")
            f.write("|")
        if line[1:3]=="fi":
            f.write("|")
            f.write(str(lines[index+1]))
            f.write("|")
        if line[:3] == "Ti":
            f.write("|")
            f.write(str(lines[index + 1]))
            f.write("|")
        if line[:3] == "ti":
            f.write("|")
            f.write(str(lines[index + 1]))
            f.write("|")
