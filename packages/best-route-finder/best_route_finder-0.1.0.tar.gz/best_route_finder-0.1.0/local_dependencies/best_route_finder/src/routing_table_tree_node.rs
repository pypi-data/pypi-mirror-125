/// Represents a node in a routing table tree
#[derive(Debug)]
pub struct RoutingTableTreeNode {
    /// next-hop interface for a route that ends in this node
    pub interface: Option<String>,
    /// node that is a root of left subtree (next bit of network address is 0)
    pub left: Option<Box<RoutingTableTreeNode>>,
    /// node that is a root of right subtree (next bit of network address is 1)
    pub right: Option<Box<RoutingTableTreeNode>>,
}

impl RoutingTableTreeNode {
    /// Creates new empty node having no interface and no subtrees
    pub fn new() -> Self {
        RoutingTableTreeNode {
            interface: None,
            left: None,
            right: None,
        }
    }

    /// Returns a reference to a subtree choosen based on given index.
    /// It returns left subtree for 0 and right for any other value
    pub fn get_sub_tree(&self, index: &u32) -> Option<&Box<RoutingTableTreeNode>> {
        let subtree = match index {
            0 => &self.left,
            _ => &self.right,
        };
        subtree.as_ref()
    }

    /// Returns a mutable reference to a subtree choosen based on given index.
    /// It returns left subtree for 0 and right for any other value.
    /// If the subtree does not exist its root (empty node) is created
    pub fn get_or_create_sub_tree(&mut self, index: &u32) -> &mut Box<RoutingTableTreeNode> {
        let subtree = match index {
            0 => &mut self.left,
            _ => &mut self.right,
        };
        if let None = subtree {
            *subtree = Some(Box::new(RoutingTableTreeNode::new()));
        }
        subtree.as_mut().unwrap()
    }
}


#[cfg(test)]
mod tests {
    use rstest::rstest;
    use crate::routing_table_tree_node::{RoutingTableTreeNode};

    fn create_node_with_interface(interface: &str) -> Option<Box<RoutingTableTreeNode>> {
        let mut node = Box::new(RoutingTableTreeNode::new());
        node.interface = Some(String::from(interface));
        Some(node)
    }

    #[test]
    fn new_node_is_empty() {
        let node = RoutingTableTreeNode::new();
        assert!(node.interface.is_none());
        assert!(node.left.is_none());
        assert!(node.right.is_none());
    }

    #[test]
    fn get_existing_subtree() {
        let mut node = RoutingTableTreeNode::new();
        node.left = create_node_with_interface("left");
        node.right = create_node_with_interface("right");
        assert_eq!(node.get_sub_tree(& 0).unwrap().interface, Some(String::from("left")));
        assert_eq!(node.get_sub_tree(& 1).unwrap().interface, Some(String::from("right")));
    }

    #[test]
    fn get_non_existing_left_subtree() {
        let mut node = RoutingTableTreeNode::new();
        node.right = create_node_with_interface("right");
        assert!(node.get_sub_tree(& 0).is_none());
        assert_eq!(node.get_sub_tree(& 1).unwrap().interface, Some(String::from("right")));
    }

    #[test]
    fn get_non_existing_right_subtree() {
        let mut node = RoutingTableTreeNode::new();
        node.left = create_node_with_interface("left");
        assert_eq!(node.get_sub_tree(& 0).unwrap().interface, Some(String::from("left")));
        assert!(node.get_sub_tree(& 1).is_none());
    }

    #[rstest]
    #[case(1)]
    #[case(100)]
    #[case(1024)]
    #[case(4294967295)]
    fn get_right_subtree_on_any_non_zero(#[case] right_index: u32) {
        let mut node = RoutingTableTreeNode::new();
        node.left = create_node_with_interface("left");
        node.right = create_node_with_interface("right");
        assert_eq!(node.get_sub_tree(& 0).unwrap().interface, Some(String::from("left")));
        assert_eq!(node.get_sub_tree(& right_index).unwrap().interface, Some(String::from("right")));
    }

    #[test]
    fn get_or_create_existing_subtree() {
        let mut node = RoutingTableTreeNode::new();
        node.left = create_node_with_interface("left");
        node.right = create_node_with_interface("right");
        assert_eq!(node.get_or_create_sub_tree(& 0).interface, Some(String::from("left")));
        assert_eq!(node.get_or_create_sub_tree(& 1).interface, Some(String::from("right")));
    }

    #[test]
    fn get_or_create_non_existing_left_subtree() {
        let mut node = RoutingTableTreeNode::new();
        assert!(node.get_or_create_sub_tree(& 0).interface.is_none());
        assert!(node.left.is_some());
        assert!(node.right.is_none());
    }

    #[rstest]
    #[case(1)]
    #[case(100)]
    #[case(1024)]
    #[case(4294967295)]
    fn get_or_create_non_existing_right_subtree(#[case] right_index: u32) {
        let mut node = RoutingTableTreeNode::new();
        assert!(node.get_or_create_sub_tree(& right_index).interface.is_none());
        assert!(node.left.is_none());
        assert!(node.right.is_some());
    }

    #[rstest]
    #[case(1)]
    #[case(100)]
    #[case(1024)]
    #[case(4294967295)]
    fn get_or_create_right_subtree_on_any_non_zero(#[case] right_index: u32) {
        let mut node = RoutingTableTreeNode::new();
        node.left = create_node_with_interface("left");
        node.right = create_node_with_interface("right");
        assert_eq!(node.get_or_create_sub_tree(& 0).interface, Some(String::from("left")));
        assert_eq!(node.get_or_create_sub_tree(& right_index).interface, Some(String::from("right")));
    }
}
