from backend.models import WarehouseCell, Warehouse

def get_simple_warehouse_layout():
    dimensions = (7, 14)
    grid = init_matrix(dimensions)

    # mark some cells as shelves
    for i in range(1, 5):
        grid[i][2] = WarehouseCell.Shelving
        grid[i][3] = WarehouseCell.Shelving
        grid[i][6] = WarehouseCell.Shelving
        grid[i][7] = WarehouseCell.Shelving
        grid[i][10] = WarehouseCell.Shelving
        grid[i][11] = WarehouseCell.Shelving

    warehouse = Warehouse(dimensions, grid)
    return warehouse

def get_large_warehouse_layout():
    dimensions = (28, 31)
    grid = init_matrix(dimensions)

    #s1, s2
    for i in range(2,6):
        grid[i][1] = WarehouseCell.Shelving

    grid[5][1] = WarehouseCell.Shelving
    grid[3][5] = WarehouseCell.Shelving
    grid[4][5] = WarehouseCell.Shelving
    grid[3][6] = WarehouseCell.Shelving
    grid[4][6] = WarehouseCell.Shelving

    #b1, b2, b3, b4, b5
    for i in range(6, 11):
        grid[i][1] = WarehouseCell.Shelving
    grid[7][3] = WarehouseCell.Shelving
    grid[7][4] = WarehouseCell.Shelving
    grid[7][6] = WarehouseCell.Shelving
    grid[9][3] = WarehouseCell.Shelving
    grid[9][4] = WarehouseCell.Shelving
    grid[9][6] = WarehouseCell.Shelving

    #p1, p2, ... p8
    for i in range(11, 22):
        grid[i][1] = WarehouseCell.Shelving

    for i in range(3, 5):
        grid[11][i] = WarehouseCell.Shelving
    
    for i in range(3, 5):
        grid[13][i] = WarehouseCell.Shelving
    
    grid[15][3] = WarehouseCell.Shelving
    grid[17][3] = WarehouseCell.Shelving
    grid[19][3] = WarehouseCell.Shelving

    grid[15][5] = WarehouseCell.Shelving
    grid[17][5] = WarehouseCell.Shelving
    grid[19][5] = WarehouseCell.Shelving

    #ff1, ff2
    for i in range(22, 28):
        grid[i][1] = WarehouseCell.Shelving
    
    for i in range(2, 5):
        grid[27][i] = WarehouseCell.Shelving
    
    grid[23][3] = WarehouseCell.Shelving
    grid[23][4] = WarehouseCell.Shelving

    #lower vertical shelf
    y = [9, 11, 13, 15, 17, 19, 21]

    for j in y:
        for i in range(15, 21):
            grid[i][j] = WarehouseCell.Shelving

    #middle vertical shelf
    y = [9, 11, 13, 15, 17, 19, 21]

    for j in y:
        for i in range(7, 13):
            grid[i][j] = WarehouseCell.Shelving

    #m1..m4, d1, d2
    y = [9, 11, 13, 15, 19, 21]

    for j in y:
        for i in range(3, 5):
            grid[i][j] = WarehouseCell.Shelving

    #r1..r4
    x = [3, 5, 7]

    for i in x:
        for j in range(24, 27):
            grid[i][j] = WarehouseCell.Shelving
    
    for i in range(2, 9):
        grid[i][29] = WarehouseCell.Shelving
    
    #c1..c7
    for i in range(9, 16):
        grid[i][29] = WarehouseCell.Shelving
    grid[10][24] = WarehouseCell.Shelving
    grid[10][26] = WarehouseCell.Shelving
    
    grid[12][24] = WarehouseCell.Shelving
    grid[12][26] = WarehouseCell.Shelving

    grid[14][24] = WarehouseCell.Shelving
    grid[14][26] = WarehouseCell.Shelving

    #a1..a4
    x = [17, 19, 21]

    for i in x:
        for j in range(24, 27):
            grid[i][j] = WarehouseCell.Shelving
    
    for i in range(16, 23):
        grid[i][29] = WarehouseCell.Shelving

    #counter
    grid[25][10] = WarehouseCell.Shelving
    grid[25][11] = WarehouseCell.Shelving

    grid[25][14] = WarehouseCell.Shelving
    grid[25][15] = WarehouseCell.Shelving

    grid[25][18] = WarehouseCell.Shelving
    grid[25][19] = WarehouseCell.Shelving

    grid[25][22] = WarehouseCell.Shelving
    grid[25][23] = WarehouseCell.Shelving
    
    warehouse = Warehouse(dimensions, grid)
    return warehouse

# Utility function to initialise a cells of a matrix as Navigable  
def init_matrix(size):
    matrix = []
    for i in range(size[0]):
        row = []
        for j in range(size[1]):
            row.append(WarehouseCell.Navigable)
        matrix.append(row)
    return matrix

