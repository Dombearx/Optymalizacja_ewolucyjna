from subprocess import Popen, PIPE
import sys
import errno
import re
import os
import json
import pprint as pp
import pathlib

framsFolderPath = str(pathlib.Path().absolute()) + "\\..\\Framsticks50rc14"
frams = framsFolderPath + "\\frams.exe"


def parseIndividual(text):
    text = text.decode("utf-8")
    lines = text.split("\n")
    genotype = lines[2:]
    return genotype[0].strip()


def getSimpleGenotype():
    args = frams + " -Q -s -icliutils.ini \"getsimplest 1\" -q"
    process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return parseIndividual(stdout)


def framsMutate(individual):
    genotype = individual[0]
    args = frams + " -Q -s -icliutils.ini rnd mut -q"
    process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate(bytes(genotype, encoding="utf-8"))
    individual[0] = parseIndividual(stdout)


def framsEvaluate(individual):
    genotype = individual[0]
    fileName = saveIndividualToFile(genotype)

    path_to_file = "..\\\\..\\\\framsticks\\\\"
    path = path_to_file + fileName
    args = frams + " -Q -s -icliutils.ini \"expdef standard-eval\" \"eval eval-allcriteria.sim " + path + "\" -q"
    process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    with open(framsFolderPath + "\\data\\scripts_output\\genos_eval.json") as f:
        data = json.load(f)
    dictionary = data[0]
    results_temp = dictionary["evaluations"]
    results = results_temp[""]
    return(results["velocity"], results["vertpos"])


def framsCrossover(individual1, individual2):
    genotype1 = individual1[0]
    genotype2 = individual2[0]

    fileName1, fileName2 = saveParentsToFiles(genotype1, genotype2)

    path_to_file = "..\\\\..\\\\framsticks\\\\"
    path1 = path_to_file + fileName1
    path2 = path_to_file + fileName2

    args = frams + " -Q -s -icliutils.ini rnd \"crossover " + \
        path1 + " " + path2 + "\" -q"
    process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    individual1[0] = parseIndividual(stdout)

    process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    individual2[0] = parseIndividual(stdout)

    return individual1, individual2


def saveIndividualToFile(genotype):
    outputName = "toEvaluate.gen"
    file = open(outputName, "w")
    file.write("org:")
    file.write("\n")
    file.write("genotype:~")
    file.write("\n")
    file.write(genotype + "~")
    file.close()
    return outputName


def saveParentsToFiles(genotype1, genotype2):
    outputName1 = "parent1.gen"
    outputName2 = "parent2.gen"
    file = open(outputName1, "w")
    file.write(genotype1)
    file.close()

    file = open(outputName2, "w")
    file.write(genotype2)
    file.close()
    return outputName1, outputName2
