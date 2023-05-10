import subprocess
import math
import time
import random
from timeout_decorator import timeout


usableSVariable = [10, 12, 18, 20, 26,30,32,36,42,46,48,49,55,60,62,69,75,84,88,91,95,97,101,114,119,125,127,138,140,149,153,160,166,168,179,181,185,187,200,213,217,225,236,242,248,257,263,269,280,295,301,305,324,337,341,347,355,362,368,372,380,385,393,405,418,428,434,447,453,466,478,486,491,497,511,526,532,542,549,557,563,573,580,588,594,600,606,619,633,640,648,666,675,685,693,703,718,728,736,747,759,778,792,802,811,821,835,845,860,870,891,903,913,926,938,950,963,977,989,1002,1020,1032,1050,1074,1085,1099,1111,1136,1152,1169,1183,1205,1220,1236,1255,1269,1285,1306,1347,1361,1389,1404,1420,1436,1461,1477,1502,1522,1539,1561,1579,1600,1616,1649,1673,1698,1716,1734,1759,1777,1800,1824,1844,1863,1887,1906,1926,1954,1979,2005,2040,2070,2103,2125,2152,2195,2217,2247,2278,2315,2339,2367,2392,2416,2447,2473,2502,2528,2565,2601,2640,2668,2701,2737,2772,2802,2831,2875,2906,2938,2979,3015,3056,3101,3151,3186,3224,3265,3299,3344,3387,3423,3466,3502,3539,3579,3616,3658,3697,3751,3792,3840,3883,3924,3970,4015,4069,4112,4165,4207,4252,4318,4365,4418,4468,4513,4567,4626,4681,4731,4780,4838,4901,4954,5008,5063,5116,5172,5225,5279,5334,5391,5449,5506,5566,5637,5694,5763,5823,5896,5975,6039,6102,6169,6233,6296,6363,6427,6518,6589,6655,6730,6799,6878,6956,7033,7108,7185,7281,7360,7445,7520,7596,7675,7770,7855,7935,8030,8111,8194,8290,8377,8474,8559,8654,8744,8837,8928,9019,9111,9206,9303,9400,9497,9601,9708,9813,9916,10017,10120,10241,10351,10458,10567,10676,10787,10899,11015,11130,11245,11358,11475,11590,11711,11829,11956,12087,12208,12333,12460,12593,12726,12857,13002,13143,13284,13417,13558,13695,13833,13974,14115,14272, 14415, 14560, 14713, 14862, 15011, 15170, 15325, 15496, 15651, 15808, 15977, 16161, 16336, 16505, 16674, 16851, 17024, 17195, 17376, 17559, 17742, 17929, 18116, 18309, 18503, 18694, 18909, 19126, 19325, 19539, 19740, 19939, 20152, 20355, 20564, 20778, 20988, 21199, 21412, 21629, 21852, 22073, 22301, 22536, 22779, 23010, 23252, 23491, 23730, 23971, 24215, 24476, 24721, 24976, 25230, 25493, 25756, 26022, 26291, 26566, 26838, 27111, 27392, 27682, 27959, 28248, 28548, 28845, 29138, 29434, 29731, 30037, 30346, 30654, 30974, 31285, 31605, 31948, 32272, 32601, 32932, 33282, 33623, 33961, 34302, 34654, 35031, 35395, 35750, 36112, 36479, 36849, 37227, 37606, 37992, 38385, 38787, 39176, 39576, 39980, 40398, 40816, 41226, 41641, 42067, 42490, 42916, 43388, 43840, 44279, 44729, 45183, 45638, 46104, 46574, 47047, 47523, 48007, 48489, 48976, 49470, 49978, 50511, 51017, 51530, 52062, 52586, 53114, 53650, 54188, 54735, 55289, 55843, 56403]

def getSVariable(number):
    # get neareset number from usableSVariable
    return min(usableSVariable, key=lambda x:abs(x-number))

@timeout(4)
def run(command):
    try:
        call = subprocess.run(command, shell=True, capture_output=True)
        if (call.stderr):
            print(call.stderr)
        # print("@@ run: ", command)
        # print("@@ stdout result: ", call.stdout.decode("utf-8"))
        # time.sleep(0.5)
        return call
    except Exception as e:
        print("Method timed out.", command)


def encode(s, w, r, fileName, tempFileName):
    return run("/opt/libRaptorQ/build/bin/RaptorQ encode -s " + str(s) + " -w " + str(w) + " -r " + str(r) + " " + fileName + " " + tempFileName)


def decode(s, w, b, tempFileName, fileName):
    return run("/opt/libRaptorQ/build/bin/RaptorQ decode -s " + str(s) + " -w " + str(w) + " -b " + str(b) + " " + tempFileName + " " + fileName)


def getFileSize(fileName):
    return int(run("wc -c < " + fileName).stdout.decode("utf-8")[:-1])


def getFileHash(fileName):
    return run("openssl dgst -sha256 " + fileName).stdout.decode("utf-8").split(' ')[1][:-1]


def checkParameters(sVariable, wVariable, repairVariable, fileName, tempFileName):
    originalHash = getFileHash(fileName)
    originalFileSize = getFileSize(fileName)
    encodeResult = encode(sVariable, wVariable, repairVariable, fileName, tempFileName)
    if (encodeResult and encodeResult.returncode == 1):
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
        else:
            return True
    return False


def fixedEncode(s, w, r, fileName, tempFileName):
    b = getFileSize(fileName)
    initialHash = getFileHash(fileName)
    endHash = None
    while (initialHash != endHash):
        if (endHash != None):
            print("fixedEncode is looping")

        start = time.time()
        encodeResult = encode(s, w, r, fileName, "fixedEncodeTemp")
        end = time.time()
        print("užkoduoti užtruko: ", end - start)

        start = time.time()
        encrypt("fixedEncodeTemp", "fixedEncodeTemp.cypher", "p455w0rd")
        end = time.time()
        print("užšifruoti užtruko: ", end - start)

        start = time.time()
        decrypt("fixedEncodeTemp.cypher", "uncyphered", "p455w0rd")
        end = time.time()

        if (encodeResult.returncode == 1):
            continue
        if (getFileSize("fixedEncodeTemp") < int(b)):
            continue
        start = time.time()
        decodeResult = decode(s, w, b, "fixedEncodeTemp", "fixedEncodeTemp2")
        end = time.time()
        print("dekoduoti užtruko: ", end - start)

        if (decodeResult.returncode == 1):
            continue
        endHash = getFileHash("fixedEncodeTemp2")
    run("mv fixedEncodeTemp " + tempFileName)
    run("rm fixedCodeTemp2")

def findParameters(fileName, startSVariable = usableSVariable[0]):
    tempFileName = "temp"
    usableSVariables = list(filter(lambda x: x >= startSVariable, usableSVariable))
    for sVariable in usableSVariables:
        wVariable = 1
        if getFileSize(fileName) > 200000:
            wVariable = 1000
        while (wVariable < 50000):
            wVariable = math.ceil(max(wVariable * 1, wVariable + 1))
            print(sVariable, wVariable, 1)
            if checkParameters(sVariable, wVariable, 1, fileName, tempFileName):
                return sVariable, wVariable
                # else:
                # print("Files are equal, but it is unclear how to divide ", str(sVariable), " ", str(wVariable), int(repairVariable), getFileSize(tempFileName))
            # else:
                # print("Files are different")


def splitFileIntoParts(fileName, size):
    run("split " + fileName + " -b " + str(size) +
        " --additional-suffix=.part -a 8")


def mergeFileFromParts(fileName, newFileName):
    run("cat *" + fileName + ".part > " + newFileName)
    run("rm *" + fileName + ".part")


def encrypt(fileName, outputFileName, password):
    run("openssl enc -aes-256-cbc -k " + password +
        " -in " + fileName + " -out " + outputFileName)


def decrypt(fileName, outputFileName, password):
    run("openssl enc -d -aes-256-cbc -k " + password +
        " -in " + fileName + " -out " + outputFileName)


def generate_digit_strings(num_of_strings):
    digit_strings = []
    for i in range(num_of_strings):
        digit_string = str(i).zfill(6)
        digit_strings.append(digit_string)
    return digit_strings

# for i in range(1, 5):
#    for x in range(1, 50):
#        sVariable, wVariable = findParameters("passwords.txt", x)
#        print("result: ", sVariable, wVariable, x)


def listFiles(name):
    return run("ls -1 " + name).stdout.decode("utf-8").splitlines()


secret = "secretCode5555"


def work(file):
    # print(file, run("wc -c < " + file).stdout.decode("utf-8")[:-1])
    encrypt(file, file + ".enc", secret)
    encryptedSize = getFileSize(file + ".enc")
    sVariable, wVariable = findParameters(file + ".enc", 100)
    # sVariable, wVariable = 114, 27276
    # print("chosen variables", sVariable, wVariable)
    fixedEncode(sVariable, wVariable, 100, file +
                ".enc", file + ".enc.tobesplit")
    splitFileIntoParts(file + ".enc.tobesplit", sVariable)
    mergeFileFromParts(file + ".enc.tobesplit", file + ".enc.merged")
    decode(sVariable, wVariable, encryptedSize,
           file + "enc.tobesplit", file + ".res")
    decrypt(file + ".res", file + ".res.dec", secret)
    print("restored: ", getFileSize(file + ".res.dec"),
          " ", getFileHash(file + ".res.dec"))


def workMain(originalFileName):
    originalHash = getFileHash(originalFileName)
    print("original: ", originalFileName, " ", getFileSize(
        originalFileName), " ", originalHash, " ")
    for i in range(1, 500):
        splitFileIntoParts(originalFileName, 5000)
        list = listFiles("*.part")
        for file in list:
            work(file)

# work("IMG.jpg")


def simpleWork(filename):
    good_i = 0
    originalHash = getFileHash(filename)
    print("original: ", filename, " ", getFileSize(
        filename), " ", originalHash, " ")
    for (x, r_variable) in enumerate(range(1, 60)):
        # sVariable, wVariable = findParameters(filename, r_variable)
        sVariable, wVariable = 97, 9
        print("chosen variables", sVariable, wVariable, r_variable)
        calculated_block_length = sVariable * wVariable + r_variable
        print("calculated_block_length", calculated_block_length)
        
        fixedEncode(sVariable, wVariable, r_variable,  filename, filename + ".enc")
        
        print("encoded: ", filename, " ", getFileSize(filename + ".enc"),
              " ", getFileHash(filename + ".enc"), " ")
        decode(sVariable, wVariable, getFileSize(filename),
               filename + ".enc", filename + ".res")
        print("restored: ", getFileSize(filename + ".res"),
              " ", getFileHash(filename + ".res"))

        i = 5525
        fileSizeBeforeSplit = getFileSize(filename + ".enc")
        fileHashBeforeSplit = getFileHash(filename + ".enc")
        a = splitFileIntoParts(filename + ".enc", i)
        list = listFiles("*.part")
        list.sort()
        files_count = list.__len__()

        if not files_count > 0:
            print(i, "nepavyko splitinti")
            continue
        # create array of numbers from 0 to files_count
        numbers = generate_digit_strings(list.__len__())
        # shuffle the array
        random.shuffle(numbers)

        # for each file, print the file name and the file size
        for file in list:
            run("mv " + file + " " + str(numbers.pop(0)) + ".part")

        # Merge all files in list
        run("cat *.part > " + filename + ".enc.merged")
        fileSizeAfterSplit = getFileSize(filename + ".enc.merged")
        fileHashAfterSplit = getFileHash(filename + ".enc.merged")

        run("rm *.part")
        decode(sVariable, wVariable, getFileSize(filename),
               filename + ".enc.merged", filename + ".res.from-merged")

        restoredHash = getFileHash(filename + ".res.from-merged")
        if (restoredHash == originalHash):
            print("GOOD: ", i, "sVariable", sVariable, "wVariable:", wVariable, "r_variable", r_variable, "orig size:", getFileSize(filename), "rest size:", getFileSize(
                filename + ".res.from-merged"), "hash equals:", getFileHash(filename) == getFileHash(filename + ".res.from-merged"), "skirtumas nuo praeito:", i - good_i)
            good_i = i

simpleWork("files/IMG.jpg")


# def manoWork(fileName):
#     fileSize = getFileSize(fileName)
#     r = 50
#     s, w = findParameters(fileName)
#     tempFileName = "fixedEncodeTemp"

#     # fixedEncode(sVariable, wVariable, r_variable, fileName, fileName + ".enc")
#     encodeResult = encode(s, w, r, fileName, "files/" +tempFileName)
#     decodeResult = decode(s, w, fileSize, "files/" + tempFileName, "retrieved_" + fileName)
#     if (decodeResult.returncode == 1):
#         print('test')
#     print('done')
# # 5
# # *
# # 23
# # *
# # 2467

# manoWork("files/IMG.jpg")
