from collections import defaultdict

dict_1 = defaultdict()
dict_1["a"] = 1


dict_2 = defaultdict()
dict_2["a"] = 1


dict_2["b"] = 2

c = [k for k in dict_2.keys() if k not in dict_1]

print(c)