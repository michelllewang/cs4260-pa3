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
    leaf1 = TreeNode(utility=0.3)
    leaf2 = TreeNode(utility=0.6)
    leaf3 = TreeNode(utility=0.8)
    split_node = TreeNode(feature="t1", threshold=7, left_child=leaf2, right_child=leaf3)
    root = TreeNode(feature="t0", threshold=5, left_child=leaf1, right_child=split_node)
    return root

def main():
    # Example input
    element = {"t0": 1, "t1": 2}
    regression_tree_root = build_simple_tree()

    # Predict utility for the given input
    predicted_utility = predict_utility(element, regression_tree_root)
    print(f"Predicted utility: {predicted_utility}")

if __name__ == "__main__":
    main()
