def count_type(filename):
    f = open(filename, 'rb')

    num_N = 0
    num_I = 0
    num_B = 0
    num_E = 0
    num_P = 0
    num_other = 0
    for line in f:
        line = line.decode('gbk', 'ignore')
        line_split = line.split(' ')
        if line_split[2] == 'N':
            num_N += 1
        elif line_split[2] == 'I':
            num_I += 1
        elif line_split[2] == 'B':
            num_B += 1
        elif line_split[2] == 'E':
            num_E += 1
        elif line_split[2] == 'P':
            num_P += 1
        else:
            print(line)
            num_other += 1

    print("Number of N: ", num_N)
    print("Number of I: ", num_I)
    print("Number of B: ", num_B)
    print("Number of E: ", num_E)
    print("Number of P: ", num_P)
    print("Number of Other: ", num_other)

count_type('IE_data/train.txt')