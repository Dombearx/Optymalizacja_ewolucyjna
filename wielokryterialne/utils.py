def makelogFile(lines, outputName):
    file = open(outputName, "w")
    for line in lines:
        for value in line:
            file.write(str(value) + "\t")
        file.write("\n")
    file.close()


def saveParetoFront(front):
    outputName = "front.gen"
    file = open(outputName, "w")
    for individual in front:
        file.write(individual[0])
        file.write("\n")

    file.close()


class result:

    def __init__(self, islandsLog, hallOfFamers, time):
        self.islandsLog = islandsLog
        self.hallOfFamers = hallOfFamers
        self.time = time

    def getIslandsLog(self):
        return self.islandsLog

    def getHallOfFamers(self):
        return self.hallOfFamers

    def getTime(self):
        return self.time
