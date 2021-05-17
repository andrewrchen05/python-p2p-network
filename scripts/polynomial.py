# O(n^5) algorithm

def polynomial(n):
    for i in range(1, n):
        for j in range(1, n):
            for k in range(1, n):
                for l in range(1, n):
                    for m in range(1, n):
                        print("Iteration: " + str(i) + str(j) + str(k) + str(l) + str(m))

num = 10
polynomial(num)