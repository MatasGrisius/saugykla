import subprocess
import math
import time
import random

def run(command):
    call = subprocess.run(command, shell=True, capture_output=True)
    if (call.stderr):
        print (call.stderr)
    # print("@@ run: ", command)
    # print("@@ stdout result: ", call.stdout.decode("utf-8"))
    time.sleep(0.5)
    return call

def splitFileIntoParts(fileName, size):
    run("split " + fileName + " -b " + str(size) + " --additional-suffix=.part -d")

def listFiles(name):
    return run('ls ' + name).stdout.decode("utf-8").splitlines()

splitFileIntoParts("IMG.jpg", 50000)

list = listFiles("*.part")
files_count = list.__len__()
# create array of numbers from 0 to files_count
numbers = [i for i in range(files_count)]
# shuffle the array
random.shuffle(numbers)

# log list
print(list)
# for each file, print the file name and the file size
for file in list:
    print(file, run("wc -c < " + file).stdout.decode("utf-8")[:-1])

for file in list:
    # rename the file to a new name using numbers array
    run("mv " + file + " " + str(numbers.pop()) + ".part")

# Merge all files in list 
run("cat *.part > IMG.restored.jpg")

run("rm *.part")

