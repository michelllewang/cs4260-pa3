import csv


class TreeNode:
    """
    A class representing a tree node.

    Attributes:
        feature (string): Theme used as splitting criteria.
        threshold (float): Value for deciding whether to go down left or right child.
        left_child (TreeNode): Points to left child node.
        right_child (TreeNode): Points to right child node.
        utility (float): Utility value.
    """
    def __init__(self, feature=None, threshold=None, left_child=None, right_child=None, utility=None):
        self.feature = feature
        self.threshold = threshold
        self.left_child = left_child
        self.right_child = right_child
        self.utility = utility

    def is_leaf(self):
        return self.utility is not None


def predict_utility(element, node):
    """
    Predicts the utility of an element.

    Args:
        element (dict): A dictionary representing presence/absence of themes.
        node (TreeNode): Node being analyzed.

    Returns:
        Utility value.
    """
    if node.is_leaf():
        return node.utility
    feature_value = element[node.feature]
    if feature_value <= node.threshold:
        return predict_utility(element, node.left_child)
    else:
        return predict_utility(element, node.right_child)


def build_simple_tree():
    """
    Builds an edge regression tree based on the presence of food, music, and nature.

    Returns:
        Root of regression tree.
    """
    leaf1 = TreeNode(utility=0)
    leaf2 = TreeNode(utility=0.02)
    leaf3 = TreeNode(utility=0.04)
    leaf4 = TreeNode(utility=0.06)
    leaf5 = TreeNode(utility=0.08)
    leaf6 = TreeNode(utility=0.1)

    # Nodes at level 2
    split_node_t1_0 = TreeNode(feature="nature", threshold=0.5, left_child=leaf1, right_child=leaf2)
    split_node_t1_1 = TreeNode(feature="nature", threshold=0.5, left_child=leaf3, right_child=leaf4)

    # Root and level 1 nodes
    split_node_t0_0 = TreeNode(feature="music", threshold=0.5, left_child=split_node_t1_0, right_child=split_node_t1_1)
    split_node_t0_1 = TreeNode(feature="music", threshold=0.5, left_child=leaf5, right_child=leaf6)

    root = TreeNode(feature="food", threshold=0.5, left_child=split_node_t0_0, right_child=split_node_t0_1)

    return root

  
def build_simple_tree2():
    """
    Builds an edge regression tree based on the presence of animals, sports, and cinema.

    Returns:
        Root of regression tree.
    """
    leaf1 = TreeNode(utility=0)
    leaf2 = TreeNode(utility=0.0142)
    leaf3 = TreeNode(utility=0.0284)
    leaf4 = TreeNode(utility=0.0426)
    leaf5 = TreeNode(utility=0.0568)
    leaf6 = TreeNode(utility=0.0710)
    leaf7 = TreeNode(utility=0.0852)
    leaf8 = TreeNode(utility=0.1)

    # Nodes at level 2
    split_node_t1_0 = TreeNode(feature="cinema", threshold=0.5, left_child=leaf1, right_child=leaf2)
    split_node_t1_1 = TreeNode(feature="cinema", threshold=0.5, left_child=leaf3, right_child=leaf4)
    split_node_t1_2 = TreeNode(feature="cinema", threshold=0.5, left_child=leaf5, right_child=leaf6)
    split_node_t1_3 = TreeNode(feature="cinema", threshold=0.5, left_child=leaf7, right_child=leaf8)

    # Root and level 1 nodes
    split_node_t0_0 = TreeNode(feature="sports", threshold=0.5, left_child=split_node_t1_0, right_child=split_node_t1_1)
    split_node_t0_1 = TreeNode(feature="sports", threshold=0.5, left_child=split_node_t1_2, right_child=split_node_t1_3)

    root = TreeNode(feature="animals", threshold=0.5, left_child=split_node_t0_0, right_child=split_node_t0_1)

    return root


def main():
    """
    Calculates utilities for each edge and adds them to CSV file.

    Return:
        None
    """

    # Load the decision tree model
    regression_tree_root = build_simple_tree()

    # Load locations from CSV file
    edges = []
    with open('EdgeThemes.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            edges.append(row)

    # Predict utility for each location and update CSV file
    with open('EdgeThemesUtil_1.csv', 'w', newline='') as output_file:
        fieldnames = ['edgeLabel', 'locationA', 'locationB', 'actualDistance', 'Theme1', 'Theme2', 'Theme3', 'Utility',
                      'Contributer', 'Notes']
        csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        csv_writer.writeheader()

        for edge in edges:
            element = {
                "food": float(edge['Theme1']),
                "music": float(edge['Theme2']),
                "nature": float(edge['Theme3'])
            }
            predicted_utility1 = predict_utility(element, regression_tree_root_1)
            edge['Utility'] = predicted_utility1
            csv_writer.writerow(edge)


if __name__ == "__main__":
    main()