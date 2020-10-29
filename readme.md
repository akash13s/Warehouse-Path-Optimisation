# Warehouse Path Optimisation

### About 
This application calculates the path a bot should take in order to minimise the distance travelled by it while fetching items from various sections of a warehouse. 

### Approach to solve the problem 

The DP-bitmasking approach takes exponential time complexity, that is, it performs poorly if number of items to be picked is greater than 17.  

Using Christofides Algorithm, we always get a path whose cost is within 1.5 times the cost of the most suitable path, and the number of items that can now be picked is approximately 400. 


### How to start the application

1. `git clone https://github.com/akash13s/Warehouse-Path-Optimisation.git`
2. `cd WarehousePathOptimisation`
3. `pip install requirements.txt`
3. `run app.py`


### Postman collection list

https://www.getpostman.com/collections/2437a7e4e86cd53c4f42