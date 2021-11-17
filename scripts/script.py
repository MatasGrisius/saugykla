import subprocess
import math
import time

def run(command):
    call = subprocess.run(command, shell=True, capture_output=True)
    #if (call.stderr):
        #print (call.stderr)
    #print("@@ run: ", command)
    #print("@@ stdout result: ", call.stdout.decode("utf-8"))
    #time.sleep(0.5)
    return call

def encode(s,w,r,fileName,tempFileName):
    return run("/opt/libRaptorQ/build/bin/RaptorQ encode -s " + str(s) + " -w " + str(w) + " -r " + str(r) + " " + fileName + " " + tempFileName)

def decode(s,w,b,tempFileName, fileName):
    return run("/opt/libRaptorQ/build/bin/RaptorQ decode -s " + str(s) + " -w " + str(w) + " -b " + str(b) + " " + tempFileName + " " + fileName)

def getFileSize(fileName):
    return int(run("wc -c < " + fileName).stdout.decode("utf-8")[:-1])

def getFileHash(fileName):
    return run("openssl dgst -sha256 " + fileName).stdout.decode("utf-8").split(' ')[1][:-1]

def checkParameters(sVariable, wVariable, repairVariable, fileName, tempFileName):
    originalHash = getFileHash(fileName)
    originalFileSize = getFileSize(fileName)
    encodeResult = encode(sVariable, wVariable, repairVariable, fileName, tempFileName)
    if (encodeResult.returncode == 1):
        return False
    decodeResult = decode(sVariable, wVariable, originalFileSize, tempFileName, "retrieved_" + fileName)
    if (decodeResult.returncode == 1):
        return False
    if (getFileSize(tempFileName) < int(originalFileSize)):
        return False
    retrievedHash = getFileHash("retrieved_" + fileName)

    if (originalHash == retrievedHash):
        if ((getFileSize(tempFileName) / (wVariable * 2 + 16)) % 1 == 0):
            return True
    return False

def fixedEncode(s,w,r,fileName,tempFileName):
    b = getFileSize(fileName)
    initialHash = getFileHash(fileName)
    endHash = None
    while (initialHash != endHash):
        if (endHash != None):
            print("fixedEncode is looping")
        encodeResult = encode(s,w,r,fileName, "fixedEncodeTemp")
        if (encodeResult.returncode == 1):
            continue
        if (getFileSize("fixedEncodeTemp") < int(b)):
            continue
        decodeResult = decode(s,w,b,"fixedEncodeTemp", "fixedEncodeTemp2")
        if (decodeResult.returncode == 1):
            continue
        endHash = getFileHash("fixedEncodeTemp2")
    run("mv fixedEncodeTemp " + tempFileName)
    run("rm fixedCodeTemp2")

def findParameters(fileName, repairVariable):
    tempFileName = "temp"
    for sVariable in range(97, 3000):
        wVariable = 1
        while (wVariable < 50000):
            wVariable = math.ceil(max(wVariable * 1.1, wVariable + 1))
            #print(sVariable, wVariable, repairVariable)
            if checkParameters(sVariable, wVariable, repairVariable, fileName, tempFileName):
                return sVariable, wVariable
                #else:
                    #print("Files are equal, but it is unclear how to divide ", str(sVariable), " ", str(wVariable), int(repairVariable), getFileSize(tempFileName))
            #else:
                #print("Files are different")

def splitFileIntoParts(fileName, size):
    run("split " + fileName + " -b " + str(size) + " --additional-suffix=.part -d")

def mergeFileFromParts(fileName):
    run("cat *.part > " + fileName)
    run("rm *.part")

def encrypt(fileName, outputFileName, password):
    run("openssl enc -aes-256-cbc -k " + password + " -in " + fileName + " -out " + outputFileName)

def decrypt(fileName, outputFileName, password):
    run("openssl enc -d -aes-256-cbc -k " + password + " -in " + fileName + " -out " + outputFileName)

#for i in range(1, 5):
#    for x in range(1, 50):
#        sVariable, wVariable = findParameters("passwords.txt", x)
#        print("result: ", sVariable, wVariable, x)

originalFileName = "passwords.txt"
originalHash = getFileHash(originalFileName)
print("original: ", originalFileName, " ", getFileSize(originalFileName), " ", originalHash, " ")
secret = "secretCode5555"
for i in range(1, 500):
    encrypt(originalFileName, originalFileName + ".enc", secret)
    encryptedSize = getFileSize(originalFileName + ".enc")
    #sVariable, wVariable = findParameters(originalFileName + ".enc", 100)
    sVariable, wVariable = 114, 27276
    #print("chosen variables", sVariable, wVariable)
    fixedEncode(sVariable, wVariable, 100, originalFileName + ".enc", "temp2")
    decode(sVariable, wVariable, encryptedSize, "temp2", originalFileName + ".enc" + ".res")
    decrypt(originalFileName + ".enc" + ".res", originalFileName + ".enc" + ".res" + ".dec", secret)
    print("restored: ", getFileSize(originalFileName + ".enc" + ".res" + ".dec"), " ", getFileHash(originalFileName + ".enc" + ".res" + ".dec"))