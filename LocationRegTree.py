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
def build_simple_tree1():
    leaf1 = TreeNode(utility=0)
    leaf2 = TreeNode(utility=0.2)
    leaf3 = TreeNode(utility=0.4)
    leaf4 = TreeNode(utility=0.6)
    leaf5 = TreeNode(utility=0.8)
    leaf6 = TreeNode(utility=1)

    # Nodes at level 2
    split_node_t1_0 = TreeNode(feature="nature", threshold=0.5, left_child=leaf1, right_child=leaf2)
    split_node_t1_1 = TreeNode(feature="nature", threshold=0.5, left_child=leaf3, right_child=leaf4)

    # Root and level 1 nodes
    split_node_t0_0 = TreeNode(feature="music", threshold=0.5, left_child=split_node_t1_0, right_child=split_node_t1_1)
    split_node_t0_1 = TreeNode(feature="music", threshold=0.5, left_child=leaf5, right_child=leaf6)

    root = TreeNode(feature="food", threshold=0.5, left_child=split_node_t0_0, right_child=split_node_t0_1)

    return root

# Construct the simple regression tree
def build_simple_tree2():
    leaf1 = TreeNode(utility=0)
    leaf2 = TreeNode(utility=0.142)
    leaf3 = TreeNode(utility=0.284)
    leaf4 = TreeNode(utility=0.426)
    leaf5 = TreeNode(utility=0.568)
    leaf6 = TreeNode(utility=0.710)
    leaf7 = TreeNode(utility=0.852)
    leaf8 = TreeNode(utility=1)

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
    # Example1 input
    element = {"food": 0, "music": 1, "nature": 0}
    regression_tree_root1 = build_simple_tree1()

    # Predict utility 1 for the given input
    predicted_utility1 = predict_utility(element, regression_tree_root1)
    print(f"Predicted utility for the First Tree: {predicted_utility1}")

    #Example2 input
    element = {"animals": 1, "sports": 0, "cinema": 1}
    regression_tree_root2 = build_simple_tree2()
    
    # Predict utility 2 for the given input
    predicted_utility2 = predict_utility(element, regression_tree_root2)
    print(f"Predicted utility for the Second Tree: {predicted_utility2}")




if __name__ == "__main__":
    main()