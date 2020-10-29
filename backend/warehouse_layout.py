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
    pass


# Utility function to initialise a cells of a matrix as Navigable  
def init_matrix(size):
    matrix = []
    for i in range(size[0]):
        row = []
        for j in range(size[1]):
            row.append(WarehouseCell.Navigable)
        matrix.append(row)
    return matrix

get_simple_warehouse_layout()