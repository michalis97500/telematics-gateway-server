length = 4

lst = [1]

for i in range(length):
    temp = list(lst)
    for j in range(i):
        lst[j+1] = temp[j] +temp[j+1]
    lst.append(1)
    temp = lst
    print(lst)