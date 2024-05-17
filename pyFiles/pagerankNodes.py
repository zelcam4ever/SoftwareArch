import os
import re
import networkx as nx
import matplotlib.pyplot as plt

def construct_dependency_graph(directory):
    G = nx.DiGraph()
    nodes = []
    for root, _, files in os.walk(directory):
        package_name = os.path.relpath(root, directory).replace(os.path.sep, '.')  # Get the relative path from the root directory

        # Skip the root directory itself
        if package_name == '.':
            continue

        # Skip files containing the word "test" in their paths
        if "test" in package_name:
            continue

        #DELETE
        excluded_keywords = ("diagrams", "binary", "words_stats", "logging", "crowd_translations", "word_scheduling", "cl","word_sta","config")
        if any(keyword in package_name for keyword in excluded_keywords):
            continue
        #DELETE


        # Get the root package name (i.e., before the first dot)
        root_packages = package_name.split('.')
        root_package_name = root_packages[0]+"."+root_packages[1] if len(root_packages) > 1 else root_packages[0]
        if "node" == root_package_name:
            continue

        if root_package_name in nodes:
            continue
        nodes.append(root_package_name)
        #print(root_package_name)
        G.add_node(root_package_name)

        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                file_path = os.path.join(root, file)
                dependencies = extract_dependencies(file_path)
                #print("\n"+file + ": ")
                #print(dependencies)
                for dependency in dependencies:
                    if irrelevant_package(dependency):
                        continue
                    dependency_name = dependency.replace(".py","").replace(os.path.sep, '.').replace("zeeguu.", '').replace("zeeguu", '')

                    root_dependencies = dependency_name.split('.')
                    root_dependency_name = root_dependencies[0]+"."+root_dependencies[1] if len(root_dependencies) > 1 else root_dependencies[0]
                    if len(root_dependency_name) < 1:
                        continue
                    print(root_package_name + " has " + root_dependency_name + "->" + str(len(root_dependency_name)))
                    G.add_edge(root_package_name, root_dependency_name)

    return G

def irrelevant_package(package_name):
    if "test" in package_name:
        return True
    if "__init__.py" in package_name:
        return True
    if "util" in package_name:
        return True
    if package_name == 'core':
        return True
    if package_name.startswith("zeeguu"):
        return False
    return True

def import_from_line(line):
    try:
        y = re.search("^from (\S+)", line)
        if not y:
            y = re.search("^import (\S+)", line)
        return y.group(1)
    except:
        return None

def extract_dependencies(file):
    all_imports = []

    lines = [line for line in open(file)]

    for line in lines:
        imp = import_from_line(line)

        if imp:
            all_imports.append(imp)

    return all_imports

def calculate_packagerank(dependency_graph, alpha=0.85, max_iter=100, tol=1e-6):
    # Calculate PageRank scores for files
    file_pagerank_scores = nx.pagerank(dependency_graph, alpha=alpha, max_iter=max_iter, tol=tol)

    # Aggregate file-level PageRank scores into package-level scores
    package_pagerank_scores = {}
    for node, score in file_pagerank_scores.items():

        packages_name = node.split('.') # Extract package name from the node
        package_name = packages_name[0]+"."+packages_name[1] if len(packages_name) > 1 else packages_name[0] # Extract package name from the node

        if package_name not in package_pagerank_scores:
            package_pagerank_scores[package_name] = 0
        package_pagerank_scores[package_name] += score

    print(package_pagerank_scores)
    return package_pagerank_scores


def visualize_dependency_graph(dependency_graph, package_pagerank_scores):
    pos = nx.kamada_kawai_layout(dependency_graph)  # Positions for all nodes

    # Adjust node sizes based on PageRank scores
    node_sizes = [package_pagerank_scores.get(node, 0) * 10000 for node in dependency_graph.nodes()]

    plt.figure(figsize=(24, 16))

    # Draw nodes
    nx.draw_networkx_nodes(dependency_graph, pos, node_size=node_sizes, node_color='skyblue')

    # Draw edges
    nx.draw_networkx_edges(dependency_graph, pos, width=1.0, alpha=0.5, edge_color='gray')

    # Draw labels
    nx.draw_networkx_labels(dependency_graph, pos, font_size=10, font_family='sans-serif')

    plt.title('PageRank Scores and Dependencies')
    plt.axis('off')
    plt.show()



if __name__ == "__main__":
    # Specify the root directory containing your Python files
    root_directory = "./zeeguu"

    # Construct the dependency graph
    dependency_graph = construct_dependency_graph(root_directory)

    # Calculate PackageRank scores
    package_pagerank_scores = calculate_packagerank(dependency_graph)

    # Visualize the dependency graph
    visualize_dependency_graph(dependency_graph, package_pagerank_scores)
