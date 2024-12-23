import threading
import random


f = open("proofs.txt",'a')
f_lock = threading.Lock()
print("what do you what the array length to be?")
iLength = int(input())

def calcChecksum(data):
    sum = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + (data[i+1] if i+1 < len(data) else 0)
        sum += word
        while sum > 0xFFFF:
            sum = (sum & 0xFFFF) + (sum >> 16)
    return ~sum & 0xFFFF

def randomize_bytes(length):
    return bytearray(random.randint(0,255) for _ in range(length))

def checkForEqualChecksum():
    totalRunsByThread = 0
    totalFoundByThread = 0
    jpre = randomize_bytes(iLength)
    j = calcChecksum(jpre)
    while True:
        totalRunsByThread+=1
        kpre = randomize_bytes(iLength)
        k = calcChecksum(kpre)
        if (j==k):
            totalFoundByThread+=1
            print(jpre," - ", j, "\n", kpre, " - ", k, "\n", "totalRunsByThread:", totalRunsByThread, "    totalFoundByThread:", totalFoundByThread)
            with f_lock:
                f.write(f'array1- {jpre} \narray2- {kpre} \nboth are equal to: {j} \n total runs by this thread: {totalRunsByThread}    the amount of proof we found with this thread: {totalFoundByThread} \n\n\n\n') 
 
# setup threads
threads = []

# Create and start threads
for _ in range(20):
    thread = threading.Thread(target=checkForEqualChecksum)
    thread.start()
    threads.append(thread)

# Wait for threads to finish
for thread in threads:
    thread.join()

print("something wrong we got an infinite loop how are you here mate")