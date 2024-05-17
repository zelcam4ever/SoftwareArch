import os
from radon.complexity import cc_visit
import matplotlib.pyplot as plt

def calculate_complexity(directory):
    # Initialize a dictionary to store file complexity results
    file_complexity_results = {}

    # Walk through all directories and files in the root directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                # Skip files containing the word "test" in their paths
                if "test" in root:
                    continue

                file_path = os.path.join(root, file)
                file_complexity = 0

                # Calculate the Cyclomatic Complexity for the file
                with open(file_path, 'r') as f:
                    content = f.read()
                    complexity_results = cc_visit(content)

                    # Aggregate complexity of all functions/methods in the file
                    for result in complexity_results:
                        file_complexity += result.complexity

                file_complexity_results[file_path] = file_complexity

    return file_complexity_results

def write_results(results, output_file):
    with open(output_file, 'w') as f:
        for file_path, complexity in results.items():
            f.write(f"File: {file_path}\n")
            f.write(f"  Unified Cyclomatic Complexity: {complexity}\n\n")

def plot_results(results):
    file_paths = list(results.keys())
    complexities = list(results.values())

    plt.figure(figsize=(10, 6))
    plt.barh(file_paths, complexities, color='skyblue')
    plt.xlabel('Unified Cyclomatic Complexity')
    plt.ylabel('File Path')
    plt.title('Cyclomatic Complexity of Python Files')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Specify the root directory containing your Python files
    root_directory = "./zeeguu"

    # Calculate complexity
    results = calculate_complexity(root_directory)

    # Plot results
    plot_results(results)
