# =============================================================================
# Question 5 - Colouring
# =============================================================================
import sys
import numpy as np

org_stdout = sys.stdout

# =============================================================================
# Helper functions
# =============================================================================
# This function sorts the colour beads in descending quantity, and returns
# the sorted list of bead colours with its respective quantity
# It takes in 2 parameters, as indicated below:
# (1) list of bead colours (col)
# (2) list of bead quantity wrt col (beads)

def sort_beads (col, beads):
    
    n = len(col)   # number of different bead colours
    
    beads_sort = beads.copy()       # make a shallow copy of 'beads'
    beads_sort.sort(reverse=True)   # sort the shallow copy in descending order
    
    col_sort = []
    
    # fill col_sort with the corresponding bead colors for the sorted copy 
    i = 0
    while (i < n):
        # this expression takes into consideration that there could be
        # similar quantity for the different coloured beads
        indices = [j for j, x in enumerate(beads) if x == beads_sort[i]]
        
        for index in indices:
            col_sort.append(col[index])
        
        i += len(indices)   # skip checking similar values
        
    return col_sort, beads_sort
    
# =============================================================================
# This function fills a grid space, and updates the parameters to an alternate
# grid space; it returns both the updated grid and updated parameters
# It takes in 10 parameters, as indicated below:
# (1) square grid to be filled (grid)
# (2) dimension of square grid (L)
# (3) list of bead colours (col); should be sorted in descending quantity
# (4) list of bead quantity wrt col (beads)
# (5) number of beads left to fill in the grid (t_bead)
# (6) number of grids already filled with col[k] (bead)
# (7) index of grid row to fill (i)
# (8) index of grid coloumn to fill (j)
# (9) index of bead colour to fill (k)
# (10) boolean variable indicating the ref point for alternate filling (first)
#      - True: ref point = grid[0][0]
#      - False: ref point = grid[0][1]

def fill_alt (grid, L, col, beads, t_bead, bead, i, j, k, first):
    
    grid[i][j] = col[k]
    
    bead += 1
    t_bead -= 1
    j += 2   # update index to an alternate grid space
    
    if (j >= L):
        i += 1   # update index to the next row
        
        if (i >= L):
            i = 0           # restart index to the first row
            first = False   # change ref point as alternate grid spaces 
                            # wrt grid[0][0] are completely filled
        
        # update column index wrt to reference point and row index
        if first:
            if (i%2 == 0):
                j = 0
            else:
                j = 1
                
        else:
            if (i%2 == 0):
                j = 1
            else:
                j = 0
            
    if (bead == beads[k]):
        k += 1     # update colour index to the next color in given list
        bead = 0   # restart bead counter
    
    return grid, t_bead, bead, i, j, k, first

# =============================================================================
# This function fills a grid space that will incur penalty, and it returns
# both the updated grid and updated parameters
# It takes in 8 parameters, as indicated below:
# (1) square grid to be filled (grid)
# (2) list of bead colours (col); should be sorted in descending quantity
# (3) number of beads that will incur penalty (p_bead)
# (4) number of beads left to fill in the grid (t_bead)
# (5) number of grids already filled with col[k] (bead)
# (6) index of grid row to fill (i)
# (7) index of grid coloumn to fill (j)
# (8) index of bead colour to fill (k)

def fill_penalty (grid, col, p_bead, t_bead, bead, i, j, k):
    
    grid[i][j] = col[k]
    
    p_bead -= 1
    bead += 1
    t_bead -= 1
    
    return grid, p_bead, bead, t_bead

# =============================================================================
# This function skips a grid space, and returns the updated parameters
# It takes in 3 parameters, as indicated below:
# (1) dimension of square grid (L)
# (2) index of grid row to skip (i)
# (3) index of grid coloumn to skip (j)

def skip (L, i, j):
    
    j += 2   # update index to an alternate grid space
    
    if (j >= L):
        i += 1   # update index to the next row
        
        # update colum index wrt to row index
        if (i%2 == 0):
            j = 1
        else:
            j = 0
    
    return i, j

# =============================================================================
# This function fills the given square grid with the given coloured beads,
# and returns the filled grid; it is catered for a grid with even dimension
# and when penalty cannot be avoided by alternating placements (i.e. the 
# coloured bead with the largest quantity exceeds half the grid size); 
# penalty incurred from putting 2 beads of the same colur as neighbours
# (4 neighbour connections) is hence minimized.
# It takes in 4 parameters, as indicated below:
# (1) an empty square grid to be filled (grid)
# (2) dimension of square grid (L)
# (3) list of bead colours (col); should be sorted in descending quantity
# (4) list of bead quantity wrt col (beads)
# (5) number of beads to fill in the grid (t_bead)
# (6) number of beads that will incur penalty (p_bead)

def fill_grid_even (grid, L, col, beads, t_bead, p_bead):
    
    # useful parameters
    bead = 0         # to track the number of grids filled (per colour)
    i = 0            # to iterate through the grid rows
    j = 0            # to iterate through the grid columns
    k = 0            # to iterate through the bead colours
    first = True     # indicate ref point for alternate filling
    penalty = True   # indicate if minimal penalty (< 4) filling is complete
    
    while (t_bead > 0):
        
        if penalty:
            # assign p_bead to grid spaces that will minimize its penalty
            # p_bead will incur a minimum penalty of 2, followed by 3
            
            i, j = 0, L-1   # fill the top right corner (penalty: 2)
            grid, p_bead, bead, t_bead = fill_penalty(
                    grid, col, p_bead, t_bead, bead, i, j, k)
            
            i, j = L-1, 0   # fill the bottom left corner (penalty: 2)
            if (p_bead > 0):
                grid, p_bead, bead, t_bead = fill_penalty(
                        grid, col, p_bead, t_bead, bead, i, j, k)
            
            # fill alternating spots along the borders (penalty: 3)
            # (first row --> first column --> last column --> last row)
            i, j = 0, 1
            while (p_bead > 0) and (j <= L-2):
                grid, p_bead, bead, t_bead = fill_penalty(
                        grid, col, p_bead, t_bead, bead, i, j, k)
                j += 2   # update index to an alternate grid space

            i, j = 1, 0
            while (p_bead > 0) and (i <= L-2):
                grid, p_bead, bead, t_bead = fill_penalty(
                        grid, col, p_bead, t_bead, bead, i, j, k)
                i += 2   # update index to an alternate grid space 
            
            i, j = 2, L-1
            while (p_bead > 0) and (i <= L-2):
                grid, p_bead, bead, t_bead = fill_penalty(
                        grid, col, p_bead, t_bead, bead, i, j, k)
                i += 2   # update index to an alternate grid space
            
            i, j = L-1, 2
            while (p_bead > 0) and (j <= L-2):
                grid, p_bead, bead, t_bead = fill_penalty(
                        grid, col, p_bead, t_bead, bead, i, j, k)
                j += 2   # update index to an alternate grid space
                
            penalty = False   # minimal penalty spaces (< 4) are filled
            i, j = 0, 0       # initialization for filling of remaining beads
                    
        else:
            # this block of code is executed after penalty has been minimised;
            # total penalty of (4 * p_bead) will be incurred here
            
            # fill empty grid spaces only, with alternating placements
            if (grid[i][j] == col[0]):
                i, j = skip(L, i, j)
                
            else:
                grid, t_bead, bead, i, j, k, first = fill_alt(
                        grid, L, col, beads, t_bead, bead, i, j, k, first)

    return grid

# =============================================================================
# This function fills the given square grid with the given coloured beads,
# and returns the filled grid; it is catered for a grid with odd dimension
# and when penalty cannot be avoided by alternating placements (i.e. the 
# coloured bead with the largest quantity exceeds half the grid size + 1); 
# penalty incurred from putting 2 beads of the same colur as neighbours
# (4 neighbour connections) is hence minimized.
# It takes in 4 parameters, as indicated below:
# (1) an empty square grid to be filled (grid)
# (2) dimension of square grid (L)
# (3) list of bead colours (col); should be sorted in descending quantity
# (4) list of bead quantity wrt col (beads)
# (5) number of beads to fill in the grid (t_bead)
# (6) number of beads that will incur penalty (p_bead)

def fill_grid_odd (grid, L, col, beads, t_bead, p_bead):
    
    # useful parameters
    bead = 0         # to track the number of grids filled (per colour)
    i = 0            # to iterate through the grid rows
    j = 0            # to iterate through the grid columns
    k = 0            # to iterate through the bead colours
    first = True     # indicate ref point for alternate filling
    penalty = True   # indicate if minimal penalty (< 4) filling is complete
    
    while (t_bead > 0):
        
        if penalty:            
            # assign p_bead to grid spaces that will minimize its penalty
            # p_bead will incur a minimum penalty of 3
            
            # fill alternating spots along the borders (penalty: 3)
            # (first row --> first column --> last column --> last row)
            i, j = 0, 1
            while (p_bead > 0) and (j <= L-2):
                grid, p_bead, bead, t_bead = fill_penalty(
                        grid, col, p_bead, t_bead, bead, i, j, k)
                j += 2   # update index to an alternate grid space

            i, j = 1, 0
            while (p_bead > 0) and (i <= L-2):
                grid, p_bead, bead, t_bead = fill_penalty(
                        grid, col, p_bead, t_bead, bead, i, j, k)
                i += 2   # update index to an alternate grid space 
            
            i, j = 1, L-1
            while (p_bead > 0) and (i <= L-2):
                grid, p_bead, bead, t_bead = fill_penalty(
                        grid, col, p_bead, t_bead, bead, i, j, k)
                i += 2   # update index to an alternate grid space
            
            i, j = L-1, 1
            while (p_bead > 0) and (j <= L-2):
                grid, p_bead, bead, t_bead = fill_penalty(
                        grid, col, p_bead, t_bead, bead, i, j, k)
                j += 2   # update index to an alternate grid space
                
            penalty = False   # minimal penalty spaces (< 4) are filled
            i, j = 0, 0       # initialization for filling of remaining beads        
            
        else:
            # this block of code is executed after penalty has been minimised;
            # total penalty of (4 * p_bead) will be incurred here
            
            # fill empty grid spaces only, with alternating placements
            if (grid[i][j] == col[0]):
                i, j = skip(L, i, j)
                        
            else:
                grid, t_bead, bead, i, j, k, first = fill_alt(
                        grid, L, col, beads, t_bead, bead, i, j, k, first)
                
    return grid

# =============================================================================
# This function fills the given square grid with the given coloured beads,
# and returns the filled grid; it is catered for situations when penalty can   
# be avoided by alternating placements (i.e. each type of coloured bead is less 
# than half the grid size); penalty incurred from putting 2 beads of the same
# colour as neighbours (4 neighbour connections) is hence 0.
# It takes in 5 parameters, as indicated below:
# (1) an empty square grid to be filled (grid)
# (2) dimension of square grid (L)
# (3) list of bead colours (col); should be sorted in descending quantity
# (4) list of bead quantity wrt col (beads)
# (5) number of beads to fill in the grid (t_bead)

def fill_grid (grid, L, col, beads, t_bead):
    
    # useful parameters
    bead = 0         # to track the number of grids filled (per colour)
    i = 0            # to iterate through the grid rows
    j = 0            # to iterate through the grid columns
    k = 0            # to iterate through the bead colours
    first = True
    
    while (t_bead > 0):
        
        # fill the given square grid with alternating placements
        grid, t_bead, bead, i, j, k, first = fill_alt(
                    grid, L, col, beads, t_bead, bead, i, j, k, first)

    return grid

# =============================================================================
# Main function
# =============================================================================
# This function outputs the bead placement in a square grid, for the given 
# grid size and number of beads; penalty incurred from putting 2 beads of 
# the same colur as neighbours (4 neighbour connections) is minimized
# It takes in 3 parameters, as indicated below:
# (1) dimension of square grid (L)
# (2) list of bead colours (col)
# (3) list of bead quantity wrt col (beads)

def place_beads (L, col, beads):
    
    # create an empty square grid to be filled with given coloured beads
    grid = np.empty([L,L], dtype=str)
    
    # sort beads in descending quantity; this will facilitate grid filling
    col_sort, beads_sort = sort_beads(col, beads)
    
    # calculate the number of beads to fill
    t_bead = L * L
    
    # determine which 'fill_grid' function to call; detailed explanation 
    # provided in the description for the respective functions; grids are 
    # filled with beads of largest quantity till the least in all scenarios
    
    if (L%2 == 0) and (beads_sort[0] > t_bead//2):
        # calculate the number of beads that will incur penalty
        p_bead = beads_sort[0] - t_bead//2
        # fill the empty square grid
        grid = fill_grid_even(grid, L, col_sort, beads_sort, t_bead, p_bead)
    
    elif (beads_sort[0] > t_bead//2 + 1):
        # calculate the number of beads that will incur penalty
        p_bead = beads_sort[0] - (t_bead//2 + 1)
        # fill the empty square grid
        grid = fill_grid_odd(grid, L, col_sort, beads_sort, t_bead, p_bead)
        
    else:
        # fill the empty square grid
        grid = fill_grid(grid, L, col_sort, beads_sort, t_bead)
    
    # output the bead placement                        
    for i in range (L):
        print(" ".join(map(str, grid[i])))
        
    return

# =============================================================================
# Part 1: 5 x 5 square grid - 2 bead colours
# =============================================================================
sys.stdout = open('output_question_5_1', 'w')

L = 5              # dimension of square grid
col = ['R', 'B']   # list of bead colours
beads = [12, 13]   # list of bead quantity wrt col

# output the bead placement
place_beads(L, col, beads)

sys.stdout.close()

# =============================================================================
# Part 2: 64 x 64 square grid - 5 bead colours
# =============================================================================
sys.stdout = open('output_question_5_2', 'w')

L = 64                                # dimension of square grid
col = ['R', 'B', 'G', 'W', 'Y']       # list of bead colours
beads = [139, 1451, 977, 1072, 457]   # list of bead quantity wrt col

# output the bead placement
place_beads(L, col, beads)

sys.stdout.close()

# =============================================================================
sys.stdout = org_stdout
# =============================================================================