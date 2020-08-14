true = True
false = False

pins = [false, true, true, true, false, true, true, true, false, true, true, true, false, true, true, true, true, true, true, false, false, false, false, true, true, true, false, true, true, false, true, true, true, true, false, true, false, true, true, true]
output = []


for i in range(len(pins)-1):
    if pins[i]:
        output.append(i)
    else:
        continue

print(output)
