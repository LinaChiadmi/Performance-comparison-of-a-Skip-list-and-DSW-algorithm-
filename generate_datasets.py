import random
import os

# Function to generate dataset
def generate_dataset(size, filename):
    with open(filename, 'w') as file:
        for _ in range(size):
            file.write(f"{random.randint(1, 10000)}\n")

# Function to create a folder if it doesn't exist
def create_dataset_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Main function
def main():
    dataset_sizes = [100, 200, 500, 1000, 2000, 4000,8000]  # Define different dataset sizes
    dataset_folder = 'datasets'  # Folder to store datasets
    create_dataset_folder(dataset_folder)

    for size in dataset_sizes:
        filename = f"{dataset_folder}/dataset_{size}.txt"
        generate_dataset(size, filename)
        print(f"Generated dataset of size {size} at {filename}")

# Run the script
if __name__ == "__main__":
    main()
