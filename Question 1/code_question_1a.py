# =============================================================================
# Question 1 - Operations for the right sum
# (attempt to output all possible operations for a desired sum)
# =============================================================================
import sys

org_stdout = sys.stdout
sys.stdout = open('output_question_1a', 'w')

# =============================================================================
# Main functions
# =============================================================================
# This function outputs the operations needed to get the desired sum, and
# returns the list storing the operations
# It takes in 3 parameters, as indicated below:
# (1) number of rows in given matrix (m)
# (2) number of columns in given matrix (n)
# (3) the desired sum (d_s)

def operation (m, n, d_s):
    
    op_ls = []   # to store the operations needed to get the desired sum
    
    # calculate minimum sum that can be achieved from the given matrix;
    # achieved by moving right along the first row, till the last column,
    # then move down the last column, till the last row
    min_sum = 1 * n
    
    for i in range (2, m+1):
        min_sum += i
    
    # calculate maximum sum that can be achieved from the given matrix;
    # achieved by moving down the first column, till the last row,
    # then move right along the last row, till the last column 
    max_sum = m * n
    
    for i in range (1, m):
        max_sum += i
    
    # check if desired sum (d_s) is within the achievable range for the
    # given matrix, before proceeding to output the operations
    if (d_s < min_sum):
        print(d_s, "No possible operations! Desired sum is smaller than "
              + "the minimum sum that can be achieved. Minimum sum from a "
              + str(m) + " x " + str(n) + " matrix is " + str(min_sum) + ".")
        
    elif (d_s > max_sum):
        print(d_s, "No possible operations! Desired sum is larger than "
              + "the maximum sum that can be achieved. Maximum sum from a "
              + str(m) + " x " + str(n) + " matrix is " + str(max_sum) + ".")
        
    else:
        # evaluate d_s to determine the required operations
        # the equipped logic will result in one of the following patterns
        # for the operations, where number of right (R) and down (D) varies:  
        # (A) if (d_s == min_sum): R --> D
        # (B) if (d_s == max_sum): D --> R
        # (C) if (d_s == min_sum + i*(m-1)) and (i >= 1): R --> D --> R
        # (D) else: R --> D --> R* --> D --> R , or
        #           D --> R* --> D --> R , where R* is always 1
        
        # Step 1: Identify the main column to move down
        # - moving right and down the last column gives the min_sum
        # - moving right, down the second last column, then right, 
        #   gives a sum that is (m-1) greater than min_sum
        # - the 'for' loop below hence helps to identify the value i,
        #   and the main column to move down, where i indicates
        #   the distance of the main column from the last column
        
        sum_1 = min_sum
        
        for i in range (n-1):
            sum_1 += (m-1)
            diff = d_s - sum_1
            
            if (diff <= 0):
                break
        
        # Step 2: List the required operations in op_ls ('R' or 'D' only)
        # - based on the main column identified in step 1
        # - op_ls is complete if d_s falls into Category A/B/C
        # - sum_2 is the sum achieved with the operations in op_ls
        
        for j in range ((n-i)-1):
            op_ls.append('R')
            
        for j in range (m-1):
            op_ls.append('D')
            
        ops = (m-1) + (n-1)   # number of operations required
        length = len(op_ls)   # number of operations already filled
        
        for j in range (length, ops):
            op_ls.append('R')
        
        sum_2 = min_sum + i * (m-1)
        
        # Step 3: Make further modifications to op_ls to achieve d_s
        # - this step is only required for d_s that falls in Category D,
        # - i.e. sum_2 is still smaller than d_s
        
        diff = d_s - sum_2
        
        if (diff > 0):
            op_ls[(n-i)-2] = 'D'
            op_ls[(n-i)-2+diff] = 'R'
        
        # Step 4: Output the required operations
        print(d_s, "".join(op_ls))
    
    return op_ls

# =============================================================================
# This function outputs the other possible operations to get the desired sum
# It takes in 2 parameters, as indicated below:
# (1) list containing the base operations to get the desired sum (op_ls)
# (2) the desired sum (d_s)

def permutations (op_ls, d_s):
    
    num = len(op_ls)
    change = True
    
    # check if a pair of 'RD' and 'DR' are present in op_ls
    # if present, swap 'RD' into 'DR' and 'DR' into 'RD' to get a different
    # set of operations; this effectively keeps the sum unchanged, as the 
    # respective swaps simultaneously increases and decreases the sum by 1
    
    while change:
        
        change = False
        first = False
        
        for i in range (num-1):
            if (op_ls[i] == 'R') and (op_ls[i+1] == 'D'):
                first = True
                for j in range (i+2, num-1):
                    if (op_ls[j] == 'D') and (op_ls[j+1] == 'R'):
                        op_ls[i] = 'D'
                        op_ls[i+1] = 'R'
                        op_ls[j] = 'R'
                        op_ls[j+1] = 'D'
                        print(d_s, ''.join(op_ls))
                        change = True
                        break
                    
            if change or first:
                break
            
    return

# =============================================================================
# Basic test: 4 x 4 matrix
# =============================================================================
m = 4                   # number of rows in matrix
n = 4                   # number of columns in matrix
sum_ls = [13, 16, 19]   # list containing the desired sums
size = len(sum_ls)      # number of desired sums to evaluate

# output the operations for each desired sum
for i in range (size):
    op_ls = operation(m, n, sum_ls[i])
    permutations(op_ls, sum_ls[i])
    
print()   # to output a blank line

# =============================================================================
# (a) 9 x 9 matrix
# =============================================================================
m = 9                        # number of rows in given matrix
n = 9                        # number of columns in given matrix
sum_ls = [65, 72, 90, 110]   # list containing the desired sums
size = len(sum_ls)           # number of desired sums to evaluate

# output the operations for each desired sum
for i in range (size):
    op_ls = operation(m, n, sum_ls[i])
    permutations(op_ls, sum_ls[i])
    
print()   # to output a blank line

# =============================================================================
# (b) 90,000 x 100,000 matrix
# =============================================================================
m = 90000                            # number of rows in matrix
n = 100000                           # number of columns in matrix
sum_ls = [87127231192, 5994891682]   # list containing the desired sums
size = len(sum_ls)                   # number of desired sums to evaluate

# output the operations for each desired sum
for i in range (size):
    op_ls = operation(m, n, sum_ls[i])
    # permutations(op_ls, sum_ls[i])
    # the 'permutations' function is not feasible for large matrices, as the 
    # approach equipped checks through almost every value, multiple times,
    # till all possible operations are being output; too time-consuming

# =============================================================================
sys.stdout.close()
sys.stdout = org_stdout
# =============================================================================