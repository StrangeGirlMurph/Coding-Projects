import os


dir = os.listdir(os.curdir)
i = 1
for d in dir:
    os.rename(d, "%02i" % i)
    i += 1
