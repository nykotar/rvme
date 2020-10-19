import random

def gen_tid():
    tid = list()
    for _ in range(8):
        tid.append(str(random.randint(0, 9)))
    tid.insert(4, '-')
    return ''.join(tid)