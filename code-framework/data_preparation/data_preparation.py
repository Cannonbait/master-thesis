import sys
# sys.argv[1:] = ["--source=fastq.fq", "--output=output.prep", "-h1=7", "-h2=13", "-h3=17"]


if (len(sys.argv) < 2
    or any([s == "--help" for s in sys.argv])
    or any([s == "-h" for s in sys.argv])):
    print("Example usage: ")
    print("--source=fastq.fq --output=output.prep -h1=7 -h2=97 -h3=31")


if not any([s.startswith("--source=") for s in sys.argv]):
    print("Specify source file using --source=")
    sys.exit()

if not any([s.startswith("--output=") for s in sys.argv]):
    print("Specify output file using --output=")
    sys.exit()

# Read file and extract relevant lines
genomes = []
with open('fastq.fq', 'r') as f:
    for i, line in enumerate(f):
        if (i % 4 == 1):
            genomes.append(line)

# Convert each line from string to bits
## G = 00
## A = 01
## T = 10
## C = 11
trans = str.maketrans({'G' : '00', 'A' : '01', 'T' : '10', 'C' : '11', '\n' : ''})
binary_genomes = [line.translate(trans) for line in genomes]
fileName = [x for x in sys.argv if x.startswith("--output=")][0][9:]
print(fileName)

if not any([s.startswith("-h1=") for s in sys.argv]):
    with open(fileName, 'w+') as f:
        for genome in binary_genomes:
            f.write(genome)
            f.write('\n')
    sys.exit()
        
hashes = []

h1 = int([x for x in sys.argv if x.startswith("-h1=")][0][4:])
h2 = int([x for x in sys.argv if x.startswith("-h2=")][0][4:])
h3 = int([x for x in sys.argv if x.startswith("-h3=")][0][4:])


hashes = [[int(x, 2) % h1, int(x, 2) % h2, int(x, 2) % h3] for x in binary_genomes]

with open(fileName, 'w+') as f:
    for hash_line in hashes:
        strl = ','.join(str(e) for e in hash_line)
        f.write(strl)
        f.write('\n')
    sys.exit()
            
