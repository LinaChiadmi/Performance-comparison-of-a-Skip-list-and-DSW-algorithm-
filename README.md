# Performance-comparison-of-a-Skip-list-and-DSW-algorithm-
In this project we implement a skiplist and dsw algorithm then we perform experiments to compare their performance in time and memory usage over incremental dataset sizes.
## Project overview:
This project includes:
- Implementations of a Skip List and DSW Algorithm for tree balancing.
- Visualization of both algorithms' steps in the terminal and as image outputs.
- an experiment to compare the time and memory complexity of the two algorithms using four operations: insert, search, delete, and range-search. (done on datasets of incremental sizes)
## Installation instructions:
To run this project, clone the repository then create a virtual environment as follows  
'python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate'  
After that, install the required dependencies 'pip install -r requirements.txt' (Note: This project was tested using Ubuntu, so the requirements.txt file was generated in that environment.)
## Usage:
You can now run skiplist.py to visualize how it works on a given example , it will display the different steps of the process in the terminal (Fig 2 in the project) and also output an image of the skiplist (fig1).(Note: The output image is directly stored in the current directory as skiplist.png without being displayed.)  
You can also run dsw.py which will generate images of the different steps of dsw on a given example . (images are stored in the current directory)  
Now that you understand how these two algorithms work, let's move on to the experiment.  
The datasets are already provided in this repository in the folder datasets . They were initially generated with generate_datasets.py file and are datasets of sizes: 100, 200, 500, 1000, 2000, 4000, and 8000 elements.  
You can now run experiment.py. This will output comparison graphs between dsw and skiplist for each of the four operations(insert,search,delete,range search) , 2 for each operation, 1 in term of time and one in term of memory usage. results will be stored in results folder (as you can see in the repo).If the results folder doesn't exist, it will be automatically created.
