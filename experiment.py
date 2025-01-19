import time
import tracemalloc
import matplotlib.pyplot as plt
from skiplist import SkipList
from dsw import BinaryTree
import os

# Function to load dataset
def load_dataset(filename):
    with open(filename, 'r') as file:
        return [int(line.strip()) for line in file.readlines()]

# Function to measure time for an operation
def measure_time(func, *args):
    start_time = time.perf_counter()
    result = func(*args)
    end_time = time.perf_counter()
    return end_time - start_time

# Function to measure memory usage for an operation
def measure_memory(func, *args):
    tracemalloc.start()
    func(*args)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak - current  # Return peak memory usage during the operation


# Running the insert experiment
def run_insert_experiment(dataset_sizes):
    insert_times_skiplist = []
    insert_times_dsw = []
    memory_usage_insert_skiplist = []
    memory_usage_insert_dsw = []

    
    for size in dataset_sizes:
        # Load the dataset
        dataset = load_dataset(f"datasets/dataset_{size}.txt")
        
        # Measure the time for Skip List insertion
        skiplist = SkipList(max_level=4, p=0.5)
        insert_time_skiplist = measure_time(lambda: [skiplist.insert(value) for value in dataset])
        insert_memory_skiplist = measure_memory(lambda: [skiplist.insert(value) for value in dataset])
        insert_times_skiplist.append(insert_time_skiplist)
        memory_usage_insert_skiplist.append(insert_memory_skiplist)

        # Measure the time for DSW tree insertion
        tree = BinaryTree()
        insert_time_dsw = measure_time(lambda: [tree.insert(value) for value in dataset])
        insert_memory_dsw = measure_memory(lambda: [tree.insert(value) for value in dataset])
        insert_times_dsw.append(insert_time_dsw)
        memory_usage_insert_dsw.append(insert_memory_dsw)
    return insert_times_skiplist, insert_times_dsw, memory_usage_insert_skiplist, memory_usage_insert_dsw

# Running the search experiment
def run_search_experiment(dataset_sizes):
    search_times_skiplist = []
    search_times_dsw = []
    memory_usage_search_skiplist = []
    memory_usage_search_dsw = []

    for size in dataset_sizes:
        # Load the dataset
        dataset = load_dataset(f"datasets/dataset_{size}.txt")
        
        # Measure the time and memory for Skip List search
        skiplist = SkipList(max_level=4, p=0.5)
        for value in dataset:
            skiplist.insert(value)  # Insert the elements first
        search_time_skiplist = measure_time(skiplist.search, dataset[-1])  # Searching for the last element
        search_memory_skiplist = measure_memory(lambda: skiplist.search(dataset[-1]))
        search_times_skiplist.append(search_time_skiplist)
        memory_usage_search_skiplist.append(search_memory_skiplist)

        # Measure the time and memory for DSW tree search
        tree = BinaryTree()
        for value in dataset:
            tree.insert(value)
        search_time_dsw = measure_time(tree.search, dataset[-1])
        search_memory_dsw = measure_memory(lambda: tree.search(dataset[-1]))
        search_times_dsw.append(search_time_dsw)
        memory_usage_search_dsw.append(search_memory_dsw)

    return search_times_skiplist, search_times_dsw, memory_usage_search_skiplist, memory_usage_search_dsw

# Running the delete experiment
def run_delete_experiment(dataset_sizes):
    delete_times_skiplist = []
    delete_times_dsw = []
    memory_usage_delete_skiplist = []
    memory_usage_delete_dsw = []

    for size in dataset_sizes:
        # Load the dataset
        dataset = load_dataset(f"datasets/dataset_{size}.txt")
        
        # Measure the time and memory for Skip List delete
        skiplist = SkipList(max_level=4, p=0.5)
        for value in dataset:
            skiplist.insert(value)
        delete_time_skiplist = measure_time(skiplist.delete, dataset[-1])  # Delete the last element
        delete_memory_skiplist = measure_memory(lambda: skiplist.delete(dataset[-1]))
        delete_times_skiplist.append(delete_time_skiplist)
        memory_usage_delete_skiplist.append(delete_memory_skiplist)

        # Measure the time and memory for DSW tree delete
        tree = BinaryTree()
        for value in dataset:
            tree.insert(value)
        delete_time_dsw = measure_time(tree.delete, dataset[-1])
        delete_memory_dsw = measure_memory(lambda: tree.delete(dataset[-1]))
        delete_times_dsw.append(delete_time_dsw)
        memory_usage_delete_dsw.append(delete_memory_dsw)

    return delete_times_skiplist, delete_times_dsw, memory_usage_delete_skiplist, memory_usage_delete_dsw

# Running the range search experiment
def run_range_search_experiment(dataset_sizes):
    range_search_times_skiplist = []
    range_search_times_dsw = []
    memory_usage_range_search_skiplist = []
    memory_usage_range_search_dsw = []

    for size in dataset_sizes:
        # Load the dataset
        dataset = load_dataset(f"datasets/dataset_{size}.txt")
        
        # Measure the time and memory for Skip List range search
        skiplist = SkipList(max_level=4, p=0.5)
        for value in dataset:
            skiplist.insert(value)
        range_search_time_skiplist = measure_time(skiplist.range_search, min(dataset), max(dataset))  # Range search
        range_search_memory_skiplist = measure_memory(lambda: skiplist.range_search(min(dataset), max(dataset)))
        range_search_times_skiplist.append(range_search_time_skiplist)
        memory_usage_range_search_skiplist.append(range_search_memory_skiplist)

        # Measure the time and memory for DSW tree range search
        tree = BinaryTree()
        for value in dataset:
            tree.insert(value)
        range_search_time_dsw = measure_time(tree.range_search, min(dataset), max(dataset))  # Range search
        range_search_memory_dsw = measure_memory(lambda: tree.range_search(min(dataset), max(dataset)))
        range_search_times_dsw.append(range_search_time_dsw)
        memory_usage_range_search_dsw.append(range_search_memory_dsw)

    return range_search_times_skiplist, range_search_times_dsw, memory_usage_range_search_skiplist, memory_usage_range_search_dsw

# Plotting the results
def plot_results(dataset_sizes, 
                 insert_times_skiplist, insert_times_dsw, 
                 search_times_skiplist, search_times_dsw, 
                 delete_times_skiplist, delete_times_dsw, 
                 range_search_times_skiplist, range_search_times_dsw,
                 memory_usage_insert_skiplist, memory_usage_insert_dsw,
                 memory_usage_search_skiplist, memory_usage_search_dsw,
                 memory_usage_delete_skiplist, memory_usage_delete_dsw,
                 memory_usage_range_search_skiplist, memory_usage_range_search_dsw):
                     
    if not os.path.exists('results'):
	    os.makedirs('results')                
    # Insert Operation Time Comparison
    plt.figure(figsize=(10, 6))
    plt.plot(dataset_sizes, insert_times_skiplist, label="SkipList Insert Time", color='blue')
    plt.plot(dataset_sizes, insert_times_dsw, label="DSW Tree Insert Time", color='red')
    plt.xlabel('Dataset Size')
    plt.ylabel('Time (seconds)')
    plt.title('Insert Operation Time Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/insert_times.png')
    plt.show()

    # Insert Operation Memory Usage Comparison
    plt.figure(figsize=(10, 6))
    plt.plot(dataset_sizes, memory_usage_insert_skiplist, label="SkipList Memory Usage (Insert)", color='blue')
    plt.plot(dataset_sizes, memory_usage_insert_dsw, label="DSW Tree Memory Usage (Insert)", color='red')
    plt.xlabel('Dataset Size')
    plt.ylabel('Memory Usage (bytes)')
    plt.title('Insert Operation Memory Usage Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/insert_memory_usage.png')
    plt.show()

    # Search Operation Time Comparison
    plt.figure(figsize=(10, 6))
    plt.plot(dataset_sizes, search_times_skiplist, label="SkipList Search Time", color='green')
    plt.plot(dataset_sizes, search_times_dsw, label="DSW Tree Search Time", color='orange')
    plt.xlabel('Dataset Size')
    plt.ylabel('Time (seconds)')
    plt.title('Search Operation Time Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/search_times.png')
    plt.show()

    # Search Operation Memory Usage Comparison
    plt.figure(figsize=(10, 6))
    plt.plot(dataset_sizes, memory_usage_search_skiplist, label="SkipList Memory Usage (Search)", color='green')
    plt.plot(dataset_sizes, memory_usage_search_dsw, label="DSW Tree Memory Usage (Search)", color='orange')
    plt.xlabel('Dataset Size')
    plt.ylabel('Memory Usage (bytes)')
    plt.title('Search Operation Memory Usage Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/search_memory_usage.png')
    plt.show()

    # Delete Operation Time Comparison
    plt.figure(figsize=(10, 6))
    plt.plot(dataset_sizes, delete_times_skiplist, label="SkipList Delete Time", color='purple')
    plt.plot(dataset_sizes, delete_times_dsw, label="DSW Tree Delete Time", color='cyan')
    plt.xlabel('Dataset Size')
    plt.ylabel('Time (seconds)')
    plt.title('Delete Operation Time Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/delete_times.png')
    plt.show()

    # Delete Operation Memory Usage Comparison
    plt.figure(figsize=(10, 6))
    plt.plot(dataset_sizes, memory_usage_delete_skiplist, label="SkipList Memory Usage (Delete)", color='purple')
    plt.plot(dataset_sizes, memory_usage_delete_dsw, label="DSW Tree Memory Usage (Delete)", color='cyan')
    plt.xlabel('Dataset Size')
    plt.ylabel('Memory Usage (bytes)')
    plt.title('Delete Operation Memory Usage Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/delete_memory_usage.png')
    plt.show()

    # Range Search Operation Time Comparison
    plt.figure(figsize=(10, 6))
    plt.plot(dataset_sizes, range_search_times_skiplist, label="SkipList Range Search Time", color='brown')
    plt.plot(dataset_sizes, range_search_times_dsw, label="DSW Tree Range Search Time", color='pink')
    plt.xlabel('Dataset Size')
    plt.ylabel('Time (seconds)')
    plt.title('Range Search Operation Time Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/range_search_times.png')
    plt.show()

    # Range Search Operation Memory Usage Comparison
    plt.figure(figsize=(10, 6))
    plt.plot(dataset_sizes, memory_usage_range_search_skiplist, label="SkipList Memory Usage (Range Search)", color='brown')
    plt.plot(dataset_sizes, memory_usage_range_search_dsw, label="DSW Tree Memory Usage (Range Search)", color='pink')
    plt.xlabel('Dataset Size')
    plt.ylabel('Memory Usage (bytes)')
    plt.title('Range Search Operation Memory Usage Comparison')
    plt.legend()
    plt.grid(True)
    plt.savefig('results/range_search_memory_usage.png')
    plt.show()


# Main function to run the experiment
def main():
    dataset_sizes = [100, 200, 500, 1000, 2000, 4000, 8000]

    # Run the insert experiment with memory tracking
    insert_times_skiplist, insert_times_dsw, memory_usage_insert_skiplist, memory_usage_insert_dsw = run_insert_experiment(dataset_sizes)
    
    # Run the search experiment with memory tracking
    search_times_skiplist, search_times_dsw, memory_usage_search_skiplist, memory_usage_search_dsw = run_search_experiment(dataset_sizes)

    # Run the delete experiment with memory tracking
    delete_times_skiplist, delete_times_dsw, memory_usage_delete_skiplist, memory_usage_delete_dsw = run_delete_experiment(dataset_sizes)

    # Run the range search experiment with memory tracking
    range_search_times_skiplist, range_search_times_dsw, memory_usage_range_search_skiplist, memory_usage_range_search_dsw = run_range_search_experiment(dataset_sizes)

    # Print the results to the console
    print("Dataset Sizes:", dataset_sizes)
    print("SkipList Insert Times:", insert_times_skiplist)
    print("DSW Tree Insert Times:", insert_times_dsw)
    print("SkipList Search Times:", search_times_skiplist)
    print("DSW Tree Search Times:", search_times_dsw)
    print("SkipList Delete Times:", delete_times_skiplist)
    print("DSW Tree Delete Times:", delete_times_dsw)
    print("SkipList Range Search Times:", range_search_times_skiplist)
    print("DSW Tree Range Search Times:", range_search_times_dsw)
    print("SkipList Memory Usage (Insert):", memory_usage_insert_skiplist)
    print("DSW Tree Memory Usage (Insert):", memory_usage_insert_dsw)
    print("SkipList Memory Usage (Search):", memory_usage_search_skiplist)
    print("DSW Tree Memory Usage (Search):", memory_usage_search_dsw)
    print("SkipList Memory Usage (Delete):", memory_usage_delete_skiplist)
    print("DSW Tree Memory Usage (Delete):", memory_usage_delete_dsw)
    print("SkipList Memory Usage (Range Search):", memory_usage_range_search_skiplist)
    print("DSW Tree Memory Usage (Range Search):", memory_usage_range_search_dsw)

    # Plot and save the results
    plot_results(
        dataset_sizes, 
        insert_times_skiplist, insert_times_dsw, 
        search_times_skiplist, search_times_dsw, 
        delete_times_skiplist, delete_times_dsw, 
        range_search_times_skiplist, range_search_times_dsw,
        memory_usage_insert_skiplist, memory_usage_insert_dsw,
        memory_usage_search_skiplist, memory_usage_search_dsw,
        memory_usage_delete_skiplist, memory_usage_delete_dsw,
        memory_usage_range_search_skiplist, memory_usage_range_search_dsw
    )

# Run the experiment
if __name__ == "__main__":
    main()
