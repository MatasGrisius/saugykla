import subprocess

print("Initialization")

def run(command):
    call = subprocess.run(command, shell=True, capture_output=True)
    if (call.stderr):
        print (call.stderr)
    result = call.stdout.decode("utf-8")
    print("@@ run: ", command)
    print("@@ result: ", result)
    return result

result = run("echo test; echo `pwd`")

print(result)

size = run("wc -c < /opt/libRaptorQ/build/bin/RaptorQ")[:-1]
print("size: ", size)
size = "1000000"
print("encode: ", run("/opt/libRaptorQ/build/bin/RaptorQ encode -s 32 -w 300 -r 20 /opt/libRaptorQ/build/bin/RaptorQ /opt/libRaptorQ/build/bin/temp"))
print("decode: ", run("/opt/libRaptorQ/build/bin/RaptorQ decode -s 32 -w 300 -b " + size + " /opt/libRaptorQ/build/bin/temp /opt/libRaptorQ/build/bin/decoded"))

