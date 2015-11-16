import concurrent.futures
def sumTo(fr, to):
    sumVal = 0
    for i in (fr, to):
        sumVal += i
    print("Sum from ", fr, to, " is :: ", sumVal)
    return sumVal
batchSize = 100000
executor = concurrent.futures.ThreadPoolExecutor(max_workers=batchSize);
s = []
to = 0
for i in range(0, 10):
    fr = to
    to += batchSize
    print ("Submitting :: ", fr, to)
    s.append(executor.submit(sumTo, fr, to))

print (s)

for future in concurrent.futures.as_completed(s) :
    print (future.result())
