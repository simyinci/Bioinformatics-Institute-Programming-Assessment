# =============================================================================
# Question 4 - Connected components
# =============================================================================
import sys

org_stdout = sys.stdout

# =============================================================================
# Helper functions
# =============================================================================
# This function stores the given image into a nested list (matrix), and
# returns the nested list with parameters indicating its size
# It takes in 1 parameter: name of file containing the binary image (filename)

def image_to_matrix (filename):
    
    matrix = []
    
    with open(filename, 'r') as file:
        image = file.readlines()
    
    for line in image:
        line = line.split()
        row = [int(i) for i in line]
        matrix.append(row)
    
    m = len(matrix)   # number of rows
    n = len(row)      # number of columns
    
    return matrix, m, n

# =============================================================================
# This function applies zero padding to a matrix (stored as a nested list),
# and returns the padded matrix
# It takes in 3 parameters, as indicated below:
# (1) a matrix stored as a nested list (matrix)
# (2) number of rows in the matrix (m)
# (3) number of columns in the matrix (n)

def apply_zero_padding (matrix, m, n):
    
    matrix.insert(0, [0] * n)   # zero pad the top border
    matrix.append([0] * n)      # zero pad the bottom border
    
    for i in range (len(matrix)):
        matrix[i].insert(0, 0)   # zero pad the left border
        matrix[i].append(0)      # zero pad the right border
    
    return matrix

# =============================================================================
# This function removes zero padding from a matrix (stored as a nested list),
# and returns the matrix
# It takes in 1 parameter: a matrix stored as a nested list (matrix)

def remove_zero_padding (matrix):
    
    matrix.pop(0)    # remove the top border
    matrix.pop(-1)   # remove the bottom border
    for row in matrix:
        row.pop(0)    # remove the left border
        row.pop(-1)   # remove the right border
    
    return matrix

# =============================================================================
# This function group and sort all "connected" labels into the same list, and
# returns a nested list containing the distinct groups of "connected" labels
# It takes in 1 parameter: a list of equivalent labels (equiv_lb)

def group_connected_labels (equiv_lb):    
    
    equiv_lb.sort()   # sort the list in ascending order
    
    # create a list that stores distinct groups of "connected" labels
    # assign the smallest pair of equivalent labels as the first group
    equiv_lb_gp = [equiv_lb[0]]
    
    for i in range (1, len(equiv_lb)):
        
        # create boolean variable to track if a pair of equivalent labels
        # belong to any groups in equiv_lb_gp
        extend = False
        
        if (equiv_lb[i] != equiv_lb[i-1]):   # only check unique pairs
            
            for j in range (len(equiv_lb_gp)):
                
                for k in range (len(equiv_lb_gp[j])):
                    
                    if ((equiv_lb[i][0] == equiv_lb_gp[j][k]) or 
                        (equiv_lb[i][1] == equiv_lb_gp[j][k])):
                        # group "connected" labels
                        equiv_lb_gp[j].extend(equiv_lb[i])
                        # keep unique labels and sort in ascending order
                        equiv_lb_gp[j] = sorted(set(equiv_lb_gp[j]))
                        extend = True
                        break
            
            if extend == False:
                # assign the pair of equivalent labels as a new group
                equiv_lb_gp.append(equiv_lb[i])
                
    return equiv_lb_gp

# =============================================================================
# This function evaluates and returns both the expected number of distinct
# clusters and list of unused labels, after grouping of "connected" labels
# It takes in 2 parameters, as indicated below:
# (1) a list of equivalent labels (equiv_lb)
# (2) number of clusters prior to grouping of "connected" labels (num_clus)

def clusters_and_free_labels (equiv_lb, num_clus):
        
    # calculate the expected number of distinct clusters
    for i in range (len(equiv_lb)):
        for j in range (1, len(equiv_lb[i])):
            num_clus -= 1
    
    # create a list that stores unused labels
    free_lb = []
    
    # since smallest label in each group of "connected" labels will replace
    # the other labels, labels that are replaced will become unused
    for i in range (len(equiv_lb)):
        for j in range (1, len(equiv_lb[i])):
            if (equiv_lb[i][j] <= num_clus):
                free_lb.append(equiv_lb[i][j])
    
    return num_clus, free_lb
    
# =============================================================================
# This function replaces "connected" labels in the matrix with the smallest 
# label in the "connected" group, and update labels in matrix with unused
# labels, and returns the updated matrix
# It takes in 6 parameters, as indicated below:
# (1) a labeled matrix, stored as a nested list (matrix)
# (2) number of rows in the matrix (m)
# (3) number of columns in the matrix (n)
# (4) a list of equivalent labels (equiv_lb)
# (5) number of distinct clusters in matrix (num_clus)
# (6) a list of unused labels (free_lb)

def update_labels (matrix, m, n, equiv_lb, num_clus, free_lb):
    
    # create a list that stores labels to be replaced with unused labels
    lb_edit = []
    
    for i in range (m):

        for j in range (n):
            
            # create boolean variable to track if "connected" labels have
            # been replaced with the smallest label
            change = False
            
            for k in range (len(equiv_lb)):
                
                for l in range (1, len(equiv_lb[k])):
                    
                    if (matrix[i][j] == equiv_lb[k][l]):
                        matrix[i][j] = equiv_lb[k][0]
                        change = True
                        break
                    
                if change:
                    break
            
            # check for labels that exceed the number of distinct clusters
            # these labels will be replaced accordingly with unused labels
            if (matrix[i][j] > num_clus):
                lb_edit.append([matrix[i][j], i, j])
                lb_edit.sort()
    
    # replace identified labels in lb_edit with free labels
    # since lb_edit is sorted in ascending order, the smallest label will be
    # replaced accordingly with the smallest free label
    
    flag = 0   # to iterate through the list of unused labels
    old_label = lb_edit[0][0]
    
    for k in range (len(lb_edit)):
        
        if (lb_edit[k][0] != old_label):
            old_label = lb_edit[k][0]
            flag += 1
    
        i = lb_edit[k][1]
        j = lb_edit[k][2]
        matrix[i][j] = free_lb[flag]
    
    return matrix

# =============================================================================
# Main functions
# =============================================================================
# This function cluster components in the given binary image using
# 8-connectivity, and outputs the labeled image
# It takes in 1 parameter: name of file containing the binary image (filename)

def eight_connectivity_clusters (filename):
    
    # store the given image into a nested list (matrix) and obtain its size
    # m: number of rows
    # n: number of columns
    matrix, m, n = image_to_matrix(filename)
    
    # apply zero padding to matrix for easier computation
    matrix = apply_zero_padding(matrix, m, n)
    
    # perform 8-connectivity check and assign labels
    label = 0       # to be assigned to pixels with a value of 1
    equiv_lb = []   # to store all labels that are equivalent or "connected"
    
    for i in range (1, m+1):
        
        for j in range (1, n+1):
            
            if (matrix[i][j] == 1):   # only check pixels with a value of 1
                
                temp = []   # temporary list to store labels that "connected"
                
                # check labels of neighbours; only check preceding neighbours 
                # as they would have been checked and assigned labels
                if (matrix[i][j-1] != 0):
                    temp.append(matrix[i][j-1])
                if (matrix[i-1][j-1] != 0):
                    temp.append(matrix[i-1][j-1])
                if (matrix[i-1][j] != 0):
                    temp.append(matrix[i-1][j])            
                if (matrix[i-1][j+1] != 0):
                    temp.append(matrix[i-1][j+1])
                
                # keep unique labels of neighbours and sort in ascending order
                temp = sorted(set(temp))
                
                if (len(temp) == 0):
                    # assign new label if there are no non-zero neighbours
                    label += 1
                    matrix[i][j] = label
                    
                elif (len(temp) == 1):
                    # assign same label as neighbours if all have the same label
                    matrix[i][j] = temp[0]
                    
                else:
                    # assign smallest label if neighbours have differing labels
                    # and keep track of labels that are "connected"
                    matrix[i][j] = temp[0]
                    equiv_lb.append(temp)
                    
    # group "connected" labels together
    equiv_lb = group_connected_labels(equiv_lb)
    
    # calculate the number of distinct clusters and identify labels that will 
    # be unused due to grouping of "connected" labels   
    num_clus, free_lb = clusters_and_free_labels(equiv_lb, label)
    
    # remove zero padding from the matrix
    matrix = remove_zero_padding(matrix)
    
    # replace "connected" labels in the matrix with the smallest label in the
    # "connected" group and update labels to match number of distinct clusters
    matrix = update_labels(matrix, m, n, equiv_lb, num_clus, free_lb)
    
    # output the labeled image
    for i in range (m):
        print(" ".join(map(str, matrix[i])))

    return

# =============================================================================
# This function cluster components in the given binary image using
# 4-connectivity, and outputs the labeled image
# It takes in 1 parameter: name of file containing the binary image (filename)

def four_connectivity_clusters (filename):
    
    # store the given image into a nested list (matrix) and obtain its size
    # m: number of rows
    # n: number of columns
    matrix, m, n = image_to_matrix(filename)
    
    # apply zero padding to matrix for easier computation
    matrix = apply_zero_padding(matrix, m, n)
    
    # perform 4-connectivity check and assign labels
    label = 0       # to be assigned to pixels with a value of 1
    equiv_lb = []   # to store all labels that are equivalent or "connected"
    
    for i in range (1, m+1):
        
        for j in range (1, n+1):
            
            if (matrix[i][j] == 1):   # only check pixels with a value of 1
                
                temp = []   # temporary list to store labels that "connected"
                
                # check labels of neighbours; only check preceding neighbours 
                # as they would have been checked and assigned labels
                if (matrix[i][j-1] != 0):
                    temp.append(matrix[i][j-1])
                if (matrix[i-1][j] != 0):
                    temp.append(matrix[i-1][j])
                
                # keep unique labels of neighbours and sort in ascending order
                temp = sorted(set(temp))
                
                if (len(temp) == 0):
                    # assign new label if there are no non-zero neighbours
                    label += 1
                    matrix[i][j] = label
                    
                elif (len(temp) == 1):
                    # assign same label as neighbours if all have the same label
                    matrix[i][j] = temp[0]
                    
                else:
                    # assign smallest label if neighbours have differing labels
                    # and keep track of labels that are "connected"
                    matrix[i][j] = temp[0]
                    equiv_lb.append(temp)
                    
    # group "connected" labels together
    equiv_lb = group_connected_labels(equiv_lb)
    
    # calculate the number of distinct clusters and identify labels that will 
    # be unused due to grouping of "connected" labels   
    num_clus, free_lb = clusters_and_free_labels(equiv_lb, label)
    
    # remove zero padding from the matrix
    matrix = remove_zero_padding(matrix)
    
    # replace "connected" labels in the matrix with the smallest label in the
    # "connected" group and update labels to match number of distinct clusters
    matrix = update_labels(matrix, m, n, equiv_lb, num_clus, free_lb)
    
    # output the labeled image
    for i in range (m):
        print(" ".join(map(str, matrix[i])))

    return

# =============================================================================
# Test case: 10 x 20 binary image
# =============================================================================
# input file containing a binary image
binary_image = 'input_question_4'

sys.stdout = open('output_question_4', 'w')

# cluster components in a binary image using 8-connectivity, and 
# output the labeled image
eight_connectivity_clusters(binary_image)

# cluster components in a binary image using 4-connectivity, and 
# output the labeled image
#four_connectivity_clusters(binary_image)

sys.stdout.close()
sys.stdout = org_stdout
# =============================================================================