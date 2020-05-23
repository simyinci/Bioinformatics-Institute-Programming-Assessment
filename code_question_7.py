# =============================================================================
# Question 7 - Coordinates-to-index & Index-to-coordinates
# =============================================================================
import sys

org_stdout = sys.stdout

# =============================================================================
# Helper functions
# =============================================================================
# This function calculates the number of coordinates (n) provided in the file,
# and saves the list of coordinates into a matrix; it returns both the number
# of coordinates (n) and matrix containing the coordinates (matrix)
# It takes in 1 parameter: name of file containing coordinates (filename);
# where the first line in the file contains the coordinate labels

def read_coordinates (filename):
    
    with open(filename, 'r') as file:
        coord_ls = file.readlines()
    
    n = len(coord_ls) - 1   # number of coordinates
    
    matrix = []
    
    for i in range (1, n+1):
        x = coord_ls[i].split()
        coord = [int(j) for j in x]
        matrix.append(coord)
        
    return n, matrix

# =============================================================================
# This function calculates the number of indexes (n) provided in the file,
# and saves the list of indexes into a list; it returns both the number of
# indexes (n) and list containing the indexes (index)
# It takes in 1 parameter: name of file containing index(es) (filename);
# where the first line in the file contains the label 'index'

def read_indexes (filename):
    
    with open(filename, 'r') as file:
        indexes = file.read()
        indexes = indexes.split()
        indexes.pop(0)   # remove the first element which contains a label
    
    index = [int(i) for i in indexes]
    
    n = len(index)   # number of indexes
    
    return n, index

# =============================================================================
# Main functions
# =============================================================================
# This function converts coordinates in a d-dimensional grid into its index,
# and outputs the index; refer to equations_question_7.pdf for the formula
# It takes in 3 parameters, as indicated below:
# (1) grid dimension (d)
# (2) a list of grid sizes (L)
# (3) a list of coordinates in a d-dimensional grid (coord)

def coordinates_to_index_dD (d, L, coord):
    
    index = 0
    
    for i in range (d):
        
        mult = 1 
        
        for j in range (i):
            mult *= L[j]
        
        index += coord[i] * mult
    
    return index

# =============================================================================
# This function converts index in a d-dimensional grid into its coordinates,
# and outputs the coordinates in a list; refer to equations_question_7.pdf
# for the formulas
# It takes in 3 parameters, as indicated below:
# (1) grid dimension (d)
# (2) a list of grid sizes (L)
# (3) index in a d-dimensional grid (index)

def index_to_coordinates_dD (d, L, index):
    
    coord = []   # stores coordinates in reverse order (xd, x(d-1), ..., x1)
    
    # evaluate the last coordinate
    den1 = 1
    
    for i in range (d-1):
        den1 *= L[i] 
    
    x = index // den1
    coord.append(x)
    
    # evaluate the remaining coordinates
    num = index
    
    for i in range (1, d):
        
        den2 = 1
        
        for j in range (d-1-i):
            den2 *= L[j]
        
        num -= den1 * coord[i-1]
        x = num // den2
        coord.append(x)
        
        den1 = den2
        
    coord.reverse()   # to put coordinates in proper order (x1, x2, ..., xd)
    
    return coord

# =============================================================================
# Part 1: 2-dimension
# =============================================================================
d = 2          # grid dimension
L = [50, 57]   # grid sizes

# -----------------------------------------------------------------------------
# input file containing coordinates in a 2-dimensional grid
file_coord = 'input_coordinates_7_1.txt'

# calculate the number of coordinates (n) provided in the input file and 
# save the list of coordinates into a matrix (matrix)
n, matrix = read_coordinates(file_coord)

sys.stdout = open('output_index_7_1.txt', 'w')

# output index label
print("index")

# convert given coordinates to index and output the index
for i in range (n):
    index = matrix[i][0] + L[0] * matrix[i][1]
    print(index)

sys.stdout.close()

# -----------------------------------------------------------------------------
# input file containing indexes in a 2-dimensional grid
file_index = 'input_index_7_1.txt'

# calculate the number of indexes (n) provided in the input file and save
# the list of indexes into a list (index)
n, index = read_indexes(file_index)

sys.stdout = open('output_coordinates_7_1.txt', 'w')

# output coordinate labels
print("x1" + "\t" + "x2")

# convert given indexes to coordinates and output the coordinates
for i in range (n):
    x2 = index[i] // L[0]
    x1 = index[i] % L[0]
    print(str(x1) + "\t" + str(x2))

sys.stdout.close()

# =============================================================================
# Part 2: d-dimension
# =============================================================================
d = 6                    # grid dimension
L = [4, 8, 5, 9, 6, 7]   # grid sizes

# -----------------------------------------------------------------------------
# input file containing coordinates in a d-dimensional grid
file_coord = 'input_coordinates_7_2.txt'

# calculate the number of coordinates (n) provided in the input file and 
# save the list of coordinates into a matrix (matrix)
n, matrix = read_coordinates(file_coord)

sys.stdout = open('output_index_7_2.txt', 'w')

# output index label
print("index")

# convert given coordinates to index and output the index
for i in range (n):
    index = coordinates_to_index_dD(d, L, matrix[i])
    print(index)
    
sys.stdout.close()

# -----------------------------------------------------------------------------
# input file containing indexes in a d-dimensional grid
file_index = 'input_index_7_2.txt'

# calculate the number of indexes (n) provided in the input file and save
# the list of indexes into a list (index)
n, index = read_indexes(file_index)

sys.stdout = open('output_coordinates_7_2.txt', 'w')

# generate and output coordinate labels
labels = []

for i in range (1, d+1):
    labels.append("x" + str(i))

print("\t".join(labels))

# convert given indexes to coordinates and output the coordinates
for i in range (n):
    coord = index_to_coordinates_dD(d, L, index[i])
    print("\t".join(map(str, coord)))

sys.stdout.close()

# =============================================================================
sys.stdout = org_stdout
# =============================================================================