firstfile = "a b \n c d "
secondfile = "a b \n d c \n c d"

def script_combine(f1, f2):
    firstfile_lines = f1.split('\n')
    secondfile_lines = f2.split('\n')

    combined = []
    l1 = 0
    l2 = 0
    while True:
        if l1 > len(firstfile_lines)-1:
            break
        if l2 > len(secondfile_lines)-1:
            break
        if firstfile_lines[l1] == secondfile_lines[l2]:
            combined.append(firstfile_lines[l1])
        if secondfile_lines[l2] != firstfile_lines[l1]:
            combined.append(firstfile_lines[l1])
            combined.append(secondfile_lines[l2])
        l1 += 1
        l2 += 1
    return "\n".join(combined)