import sys
file = "babesia-bovis/babesia_bovis_raw1"
sys.argv[1:] = ["--source="+file, "--output="+file+".prep", "threads=7", "blocks=30", "patterns=30"]


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
fileName = [x for x in sys.argv if x.startswith("--source=")][0][9:]
print("Reading from file: " + fileName)
with open(fileName, 'r') as f:
    for i, line in enumerate(f):
        if (i % 4 == 1):
            genomes.append(line)

# Convert each line from string to bits
## G = 00
## A = 01
## T = 10
## C = 11
## N = 100
print("Translating characters")
trans = str.maketrans({'G' : '00', 'A' : '01', 'T' : '10', 'C' : '11', 'N' : '100', '\n' : ''})
binary_genomes = [line.translate(trans) for line in genomes]
fileName = [x for x in sys.argv if x.startswith("--output=")][0][9:]
print("Writing output to: " + fileName)


if not any([s.startswith("threads=") for s in sys.argv]):
    with open(fileName, 'w+') as f:
        for genome in binary_genomes:
            f.write(str(int(genome,2)))
            f.write('\n')
    sys.exit()
        
hashes = []

h1 = int([x for x in sys.argv if x.startswith("threads=")][0][8:])
h2 = int([x for x in sys.argv if x.startswith("blocks=")][0][7:])
h3 = int([x for x in sys.argv if x.startswith("patterns=")][0][9:])
hashes = [[int(x, 2) % h1, int(x, 2) % h2, int(x, 2) % h3] for x in binary_genomes]

with open(fileName, 'w+') as f:
    f.write("threads: {}, blocks: {}, patterns: {} \n".format(h1, h2, h3))
    for hash_line in hashes:
        strl = ','.join(str(e) for e in hash_line)
        f.write(strl)
        f.write('\n')
    sys.exit()
            
