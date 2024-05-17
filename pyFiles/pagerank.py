import os
import networkx as nx
import matplotlib.pyplot as plt

def construct_dependency_graph(directory):
    G = nx.DiGraph()

    for root, _, files in os.walk(directory):
        package_name = os.path.relpath(root, directory).replace(os.path.sep, '.')
        if "test" in package_name:  # Skip packages with "test" in their name
            continue
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                G.add_node(os.path.join(package_name, file))

    for root, _, files in os.walk(directory):
        package_name = os.path.relpath(root, directory).replace(os.path.sep, '.')
        if "test" in package_name:  # Skip packages with "test" in their name
            continue
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                file_path = os.path.join(root, file)
                dependencies = extract_dependencies(file_path)
                for dependency in dependencies:
                    if dependency.endswith('.py') and dependency != '__init__.py':
                        G.add_edge(os.path.join(package_name, file), os.path.join(package_name, dependency))

    return G


def extract_dependencies(file_path):
    # Implement a function to extract dependencies from a Python file
    # This can be done using static analysis or parsing import statements
    # For simplicity, assume each file depends on other files in the same directory
    with open(file_path, 'r') as f:
        content = f.read()
        # Extract import statements or other dependencies
        # For simplicity, we'll assume each file depends on other files in the same directory
        dependencies = [dependency for dependency in os.listdir(os.path.dirname(file_path)) if dependency.endswith('.py')]
    return dependencies

def calculate_packagerank(graph, alpha=0.85, max_iter=100, tol=1e-6):
    # Calculate PageRank scores for files
    file_pagerank_scores = nx.pagerank(graph, alpha=alpha, max_iter=max_iter, tol=tol)

    # Aggregate file-level PageRank scores into package-level scores
    package_pagerank_scores = {}
    for node, score in file_pagerank_scores.items():
        package_name = node.split(os.path.sep)[0]
        if package_name not in package_pagerank_scores:
            package_pagerank_scores[package_name] = 0
        package_pagerank_scores[package_name] += score

    return package_pagerank_scores

def visualize_results(package_pagerank_scores):
    packages = list(package_pagerank_scores.keys())
    scores = list(package_pagerank_scores.values())

    plt.figure(figsize=(10, 6))
    plt.barh(packages, scores, color='skyblue')
    plt.xlabel('PackageRank Score')
    plt.ylabel('Package')
    plt.title('PackageRank Scores for Each Package')
    plt.gca().invert_yaxis()  # Invert y-axis to have the highest score at the top
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Specify the root directory containing your Python files
    root_directory = "./zeeguu"

    # Construct the dependency graph
    dependency_graph = construct_dependency_graph(root_directory)

    # Calculate PackageRank scores
    package_pagerank_scores = calculate_packagerank(dependency_graph)

    # Visualize the PackageRank scores
    visualize_results(package_pagerank_scores)
