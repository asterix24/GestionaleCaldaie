block = []
block_copy = False
write_mark = False
out = open('out.rtf', 'wr')
with open('lettera.rtf', 'r') as f:
    for line in f:
        if '>>START<<' in line:
            #inizio la copia del blocco.
            block_copy = True
            print "Start"
        if '>>END<<' in line:
            #inizio la copia del blocco.
            block_copy = False
            write_mark = True
            line = 'XXX'

        if block_copy and not write_mark:
            block.append(line)
        else:
            out.write(line)

out.flush()
out.close()

out_txt = ""
for i in range(3):
    for j in block:
        out_txt += j

out = open('out2.rtf', 'w')
with open('out.rtf', 'r') as f:
    pos = 0
    while True:
        line = f.readline()

        if not line:
            break

        if 'XXX' in line:
            print line
            line = line.replace('XXX', out_txt)
            print pos, line

        out.write(line)

out.close()
