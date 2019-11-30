passwords1_path = r"data/passwords/passwords1.txt"
passwords2_path = r"data/passwords/passwords2.txt"
# 60000 and 10000

# print("Reading passwords2")
# i = 0
# fin = open(passwords2_path, 'r')
# fout = open('data/passwords/p2_test.txt', 'w')

# for i in range(10000):
#     fout.write(fin.readline())

# fin.close()
# fout.close()

with open('data/passwords/p1_test.txt', 'r') as f:
    pass1 = f.read().splitlines()

with open('data/passwords/p2_test.txt', 'r') as f:
    pass2 = f.read().splitlines()

counter = 0
for p in pass2:
    if p in pass1:
        counter += 1

print(counter)  # 14
    