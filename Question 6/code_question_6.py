# =============================================================================
# Question 6 - Points inside/outside polygon
# =============================================================================
import sys
from shapely.geometry import Point, Polygon

org_stdout = sys.stdout

# =============================================================================
# Helper functions
# =============================================================================
# This function stores the coordinates from the given files as 
# coordinate-tuples into a list, and returns the list
# It takes in 1 parameter: name of file containing the coordinates (filename)

def obtain_coord_list (filename):

    with open(filename, 'r') as file:
        coord = file.read()
        coord = coord.split()
        
        n = len(coord)
        coord_ls = []
        
        for i in range (0, n, +2):
            x = int(coord[i])
            y = int(coord[i+1])
            coord_tp = tuple([x, y])
            coord_ls.append(coord_tp)

    return coord_ls

# =============================================================================
# Main function
# =============================================================================
# This function determines whether the test points lie inside or outside the
# given polygon, and outputs the corresponding test results
# It takes in 2 parameters, as indicated below:
# (1) name of file containing the coordinates of a polygon (poly_file)
# (2) name of file containing the coordinates of test points (points_file)
    
def points_in_polygon (poly_file, points_file):
    
    # obtain lists of polygon and point coordinate-tuples
    poly_ls = obtain_coord_list(poly_file)
    points_ls = obtain_coord_list(points_file)
    
    # create a polygon from the list of polygon coordinates
    # the Polygon constructor takes two positional parameters; the first is an
    # ordered sequence of (x, y[, z]) point tuples, which wil be implicitly
    # closed by copying the first tuple to the last index; the second is an 
    # optional unordered sequence of ring-like sequences specifying interior
    # boundaries or "holes" of the feature
    polygon = Polygon(poly_ls)
    
    for point in points_ls:
        # create Point objects from test point coordinates
        # the Point constructor takes positional coordinate values or
        # point tuple parameters
        point_obj = Point(point)
        
        # check if point_obj lies inside (incl. boundary) the polygon, and
        # output the result of the test with coordinates of the point
        # object.intersects(other) method returns True if the boundary or
        # interior of the object intersect in any way with those of the other
        if point_obj.intersects(polygon):
            print(point[0], point[1], "inside")
        else:
            print(point[0], point[1], "outside")
        
    return

# =============================================================================
# Test case: 10-sided polygon
# =============================================================================
# input files containing coordinates of polygon and points to be tested
poly_file = 'input_question_6_polygon'
points_file = 'input_question_6_points'

sys.stdout = open('output_question_6', 'w')

# check if the given points lie inside or outside the given polygon, and
# output the respective test result for the given points
points_in_polygon(poly_file, points_file)

sys.stdout.close()
sys.stdout = org_stdout
# =============================================================================
