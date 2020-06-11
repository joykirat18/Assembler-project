opcode_table = {'CLA': "0000", 'LAC': "0001", "SAC": "0010", "ADD": "0011", "SUB": "0100", "BRZ": "0101", "BRN": "0110",
                "BRP": "0111", "INP": "1000", "DSP": "1001", "MUL": "1010", "DIV": "1011", "STP": "1100"}
symbol_table = {}
variable_table = {}
variables = []
opcodes = []
literal_table = {}
value_table = {}
end=[]
errors = []
start=[]

lc = 0
input_file = open("input.txt", "r")
intermediate_file = open("intermediate.txt", "w+")

for line in input_file:
    line = line.strip()
    line = line.split(" ")
    # if line[0]=="#" or line[0][0]=="#":
    #     continue
    for i in range(0, len(line)):
        if line[i] == "#" or line[i][0] == "#":  # removing comments
            line = line[:i]
            break
    print(line)
    if line[0] == "DS":
        if len(line) == 3:
            value_table[line[1]] = line[2]
        elif len(line) == 2:
            value_table[line[1][0]] = line[1][-1]
    if line[0] == "START":
        if len(line) == 2:
            a = line[1]
        else:
            a = 0
        lc = int(a) - 12
    else:
        lc += 12
        if len(bin(lc)[2:]) < 8:
            line.append("0" * (8 - len(bin(lc)[2:])) + bin(lc)[2:])  # converting location counter to binary
        else:
            line.append(bin(lc)[2:])

    intermediate_file.write(" ".join(line) + "\n")

input_file.close()
intermediate_file.close()
intermediate_file = open("intermediate.txt", "r")
for line in intermediate_file:
    line = line.strip()
    line = line.split(" ")
    if line[0] == "START":
        start.append(line[0])
        continue
    if line[0] == "END":
        end.append(line[0])
        break
    if line[0] == "INP":
        variables.append(line[1])
        variable_table[line[1]] = line[2]
    for i in range(0, len(line) - 1):
        if line[i] in variable_table or line[i] in symbol_table or line[i] in literal_table:
            continue
        elif line[i] in opcode_table:
            opcodes.append(line[i])
        elif line[0] not in opcode_table and line[1] in opcode_table:
            symbol_table[line[0]] = line[-1]
        elif line[i] not in variables and line[i] not in symbol_table:
            literal_table[line[i]] = line[-1]
        elif line[i] not in variables and line[i] not in symbol_table and line[i] not in opcode_table:
            errors.append(line[i]+" has not been defined")
    if(len(line)==2):
        if line[0]!="CLA" and line[0]!="STP":
            errors.append(line[0]+ " operand not specified")
    if len(line) == 3:
        if line[0] in opcode_table and (line[1] not in variable_table and line[1] not in literal_table and line[1] not in symbol_table):
            errors.append(line[1]+ " no operand specified ")
        if line[0] in symbol_table and (line[1] in opcode_table):
            errors.append("no operand specified")
    elif len(line) == 4:
        if line[0] in opcode_table:
            errors.append("more operands given than required")
        elif line[1] in opcode_table and (line[2] not in variable_table and line[2] not in literal_table and line[2] not in symbol_table):
            errors.append(line[2]+" operand specified ")
    elif len(line)>4:
        errors.append("too many operand specified")

print("symbol table")
print(symbol_table)
print("opcode table")
print(opcode_table)
print("variables")
print(variables)
print("opcodes")
print(opcodes)
print("variable_table")
print(variable_table)
print("literal table")
print(literal_table)


# PASS 1 ENDED
for i in  literal_table:
    try:
        type(int(i))
    except:
        errors.append(i+" is not defined")
if len(end) == 0:
    errors.append("no end statement")
if len(start) == 0:
    errors.append("no start statement")
if "STP" not in opcodes:
    errors.append("STP is missing")
print("errors")
print(errors)
print("")
intermediate_file.close()
if len(errors)!=0:
    exit()
intermediate_file = open("intermediate.txt", "r")
output_file = open("output.txt", "w+")
for line in intermediate_file:
    line = line.strip()
    line = line.split(" ")
    line = line[:-1]
    # print(line)
    # if line[0] == "CLA":
        # line.append("00000000")
    if line[0] == "START":
        continue
    if line[0] == "END":
        continue
    elif line[0] in symbol_table:
        line = line[1:]
    else:

        for i in range(0, len(line)):
            if line[i] in symbol_table:
                line[i] = symbol_table[line[i]]
            if line[i] in opcode_table:
                line[i] = opcode_table[line[i]]
            if line[i] in variable_table:
                line[i] = variable_table[line[i]]
            if line[i] in literal_table:
                line[i] = literal_table[line[i]]
        output_file.write(" ".join(line) + "\n")
        print(line)
        # print("LAH" not in symbol_table)

intermediate_file.close()
print(output_file.read())
output_file.close()
