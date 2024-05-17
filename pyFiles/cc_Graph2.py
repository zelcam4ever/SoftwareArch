import os
from radon.complexity import cc_visit
import matplotlib.pyplot as plt

def calculate_complexity(directory):
    # Initialize a dictionary to store package complexity results
    package_complexity_results = {}

    # Walk through all directories and files in the root directory
    for root, _, files in os.walk(directory):
        package_name = os.path.relpath(root, directory)  # Get the relative path from the root directory

        # Skip the root directory itself
        if package_name == '.':
            continue

        # Skip files containing the word "test" in their paths
        if "test" in package_name:
            continue

        # Get the package name
        package_name = package_name.replace(os.path.sep, '.')

        # Calculate the Cyclomatic Complexity for files within the package
        package_complexity = 0
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                    complexity_results = cc_visit(content)
                    for result in complexity_results:
                        package_complexity += result.complexity

        # Group packages with the same root
        root_packages = package_name.split('.')
        root_package = root_packages[0]+"."+root_packages[1] if len(root_packages) > 1 else root_packages[0]
        if root_package not in package_complexity_results:
            package_complexity_results[root_package] = 0
        package_complexity_results[root_package] += package_complexity

    return package_complexity_results

def plot_results(results):
    root_packages = list(results.keys())
    complexities = list(results.values())

    plt.figure(figsize=(10, 6))
    plt.bar(root_packages, complexities, color='skyblue')
    plt.xlabel('Root Package')
    plt.ylabel('Total Cyclomatic Complexity')
    plt.title('Total Cyclomatic Complexity per Root Package')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Specify the root directory containing your Python files
    root_directory = "./zeeguu"

    # Calculate complexity
    package_results = calculate_complexity(root_directory)

    # Plot results
    plot_results(package_results)
