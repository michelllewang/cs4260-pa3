import csv


class TreeNode:
    def __init__(self, feature=None, threshold=None, left_child=None, right_child=None, utility=None):
        self.feature = feature
        self.threshold = threshold
        self.left_child = left_child
        self.right_child = right_child
        self.utility = utility

    def is_leaf(self):
        return self.utility is not None


def predict_utility(element, node):
    if node.is_leaf():
        return node.utility
    feature_value = element[node.feature]
    if feature_value <= node.threshold:
        return predict_utility(element, node.left_child)
    else:
        return predict_utility(element, node.right_child)


# Construct the simple regression tree
def build_simple_tree():
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


def main():
    # Load the decision tree model
    regression_tree_root = build_simple_tree()

    # Load locations from CSV file
    edges = []
    with open('EdgeThemes.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            edges.append(row)

    # Predict utility for each location and update CSV file
    with open('EdgeThemesUtil.csv', 'w', newline='') as output_file:
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
            predicted_utility = predict_utility(element, regression_tree_root)
            edge['Utility'] = predicted_utility
            csv_writer.writerow(edge)


if __name__ == "__main__":
    main()