use crate::ip_strings_parsers::{
    cidr_string_to_integers,
    ip_string_to_integer,
    CidrStringParsingError,
};
use crate::routing_table_tree_node::RoutingTableTreeNode;

static BIT_MASKS: [u32; 32] = [
    1 << 31, 1 << 30,
    1 << 29, 1 << 28, 1 << 27, 1 << 26, 1 << 25, 1 << 24, 1 << 23, 1 << 22, 1 << 21, 1 << 20,
    1 << 19, 1 << 18, 1 << 17, 1 << 16, 1 << 15, 1 << 14, 1 << 13, 1 << 12, 1 << 11, 1 << 10,
    1 << 9, 1 << 8, 1 << 7, 1 << 6, 1 << 5, 1 << 4, 1 << 3, 1 << 2, 1 << 1, 1,
];

/// Stores a routing table in form of a tree
#[derive(Debug)]
pub struct RoutingTableTree {
    /// Root node of the tree
    root: Box<RoutingTableTreeNode>,
}

impl RoutingTableTree {
    /// Creates a new, empty tree
    pub fn new() -> Self {
        RoutingTableTree { root: Box::new(RoutingTableTreeNode::new()) }
    }

    /// Inserts given route to the routing table.
    ///
    /// # Arguments
    ///
    /// * `network_address` - integer representation of network address; it can contain non-zero host bits, which will be ignored while adding to the tree
    /// * `prefix_length` - route prefix length
    /// * `iface_name` - the name of the next-hop interface associated with the route
    ///
    /// # Examples
    ///
    /// ```
    /// use best_route_finder::RoutingTableTree;
    ///
    /// let mut tree: RoutingTableTree = RoutingTableTree::new();
    /// tree.insert(& 0xC0_A8_01_00_u32, & 24_u8, "eth0");
    /// ```
    pub fn insert(&mut self, network_address: &u32, prefix_length: &u8, iface_name: &str) {
        let mut current_node = &mut self.root;
        for index in 0..*prefix_length as usize {
            current_node = current_node.get_or_create_sub_tree(&(network_address & BIT_MASKS[index]));
        }
        current_node.interface = Some(iface_name.to_string());
    }

    /// Returns next-hop interface for the given IP address based on stored routing table.
    ///
    /// # Arguments
    ///
    /// * `ip_address` - integer representation of ip address to search the next-hop interface for
    ///
    /// # Examples
    ///
    /// ```
    /// use best_route_finder::RoutingTableTree;
    ///
    /// let mut tree: RoutingTableTree = RoutingTableTree::new();
    /// tree.insert(& 0xC0_A8_01_00_u32, & 24_u8, "eth0");
    /// let found_next_hop = tree.search(& 0xC0_A8_01_45_u32);
    /// assert_eq!(Some("eth0".to_string()), found_next_hop);
    /// let not_found_next_hop = tree.search(& 0x01_01_01_01_u32);
    /// assert_eq!(None, not_found_next_hop);
    /// ```
    pub fn search(&self, ip_address: &u32) -> Option<String> {
        let mut current_node = Some(&self.root);
        let mut returned_iface = &self.root.interface;
        for index in 0..32 as usize {
            current_node = current_node.unwrap().get_sub_tree(&(ip_address & BIT_MASKS[index]));
            match current_node {
                None => {break}
                Some(node) => {
                    if node.interface.is_some() {
                        returned_iface = &node.interface;
                    }
                }
            }
        }
        returned_iface.clone()
    }

    /// Inserts given route to the routing table.
    ///
    /// # Arguments
    ///
    /// * `cidr` - CIDR string; the network address can have non-zero host bits, which will be ignored while adding to the tree
    /// * `iface_name` - the name of the next-hop interface associated with the route
    ///
    /// # Examples
    ///
    /// ```
    /// use best_route_finder::RoutingTableTree;
    ///
    /// let mut tree: RoutingTableTree = RoutingTableTree::new();
    /// match tree.insert_by_string("192.168.1.0", "eth0") {
    ///     Ok(_) => {println!("Added successfully");}
    ///     Err(err) => {println!("Error while adding {}", err)}
    /// }
    /// ```
    pub fn insert_by_string(&mut self, cidr: &str, iface_name: &str) -> Result<(), CidrStringParsingError> {
        let (network_address, prefix_length) = cidr_string_to_integers(cidr)?;
        self.insert(&network_address, &prefix_length, iface_name);
        Ok(())
    }

    /// Returns next-hop interface for the given IP address based on stored routing table.
    ///
    /// # Arguments
    ///
    /// * `ip_address` - ip address to search the next-hop interface for
    ///
    /// # Examples
    ///
    /// ```
    /// use best_route_finder::RoutingTableTree;
    ///
    /// let mut tree: RoutingTableTree = RoutingTableTree::new();
    /// tree.insert_by_string("192.168.1.0/24", "eth0").unwrap();
    /// let found_next_hop = tree.search_by_string("192.168.1.145").unwrap();
    /// assert_eq!(Some("eth0".to_string()), found_next_hop);
    /// let not_found_next_hop = tree.search_by_string("1.1.1.1").unwrap();
    /// assert_eq!(None, not_found_next_hop);
    /// ```
    pub fn search_by_string(&self, ip_address: &str) -> Result<Option<String>, CidrStringParsingError> {
        let ip_address: u32 = ip_string_to_integer(ip_address)?;
        Ok(self.search(&ip_address))
    }
}


#[cfg(test)]
mod tests {
    use rstest::{fixture, rstest};
    use crate::routing_table_tree::{RoutingTableTree};

    macro_rules! assert_interface {
        (empty, $node:expr) => {{ assert!($node.interface.is_none()); }};
        ($iface_name:expr, $node:expr) => {{ assert_eq!($node.interface.as_ref().unwrap(), $iface_name); }};
    }

    macro_rules! assert_subtrees {
        (both, $node:expr) => {{
            assert!($node.left.is_some());
            assert!($node.right.is_some());
        }};
        (empty, $node:expr) => {{
            assert!($node.left.is_none());
            assert!($node.right.is_none());
        }};
        (only_left, $node:expr) => {{
            assert!($node.left.is_some());
            assert!($node.right.is_none());
        }};
        (only_right, $node:expr) => {{
            assert!($node.left.is_none());
            assert!($node.right.is_some());
        }};
    }

    /// Returns a three with structure below
    ///
    ///          <None>
    ///
    #[fixture]
    fn empty_tree() -> RoutingTableTree {
        RoutingTableTree::new()
    }

    /// Returns a three with structure below
    ///
    ///          default_iface
    ///
    #[fixture]
    fn empty_with_default() -> RoutingTableTree {
        let mut tree = RoutingTableTree::new();
        tree.insert(& 0, & 0, "default_iface");
        tree
    }

    /// Returns a three with structure below
    ///
    ///          <None>
    ///          /    \
    ///       left    right
    ///
    #[fixture]
    fn one_level_tree() -> RoutingTableTree {
        let mut tree = RoutingTableTree::new();
        tree.insert(& 0, & 1, "left");
        tree.insert(& 0x80_00_00_00, & 1, "right");
        tree
    }

    /// Returns a three with structure below
    ///
    ///          default_iface
    ///          /
    ///       left
    ///
    #[fixture]
    fn just_left_sub_tree() -> RoutingTableTree {
        let mut tree = RoutingTableTree::new();
        tree.insert(& 0, & 0, "default_iface");
        tree.insert(& 0, & 1, "left");
        tree
    }

    /// Returns a three with structure below
    ///
    ///          default_iface
    ///          /           \
    ///         /             \
    ///    <None>             right
    ///         \             /
    ///        deep_left     <None>
    ///                           \
    ///                           deep_right
    ///
    #[fixture]
    fn search_tree() -> RoutingTableTree {
        let mut tree = RoutingTableTree::new();
        tree.insert(& 0, & 0, "default_iface");
        tree.insert(& 0x80_00_00_00, & 1, "right");
        tree.insert(& 0xA0_00_00_00, & 3, "deep_right");
        tree.insert(& 0x40_00_00_00, & 2, "deep_left");
        tree
    }

    /// Returns a three with structure below
    ///
    ///                                          default
    ///                                       /           \
    ///                                      /             \
    ///                                     X               1
    ///                                    / \             / \
    /// <down below there is one /32 route>   01          X   <down below there is one /32 route>
    ///                                                    \
    ///                                                     101
    ///
    #[fixture]
    fn complex_tree() -> RoutingTableTree {
        let mut tree = RoutingTableTree::new();
        tree.insert(& 0x00_00_00_00, & 0, "default");
        tree.insert(& 0x80_00_00_00, & 1, "1");
        tree.insert(& 0x40_00_00_00, & 2, "01");
        tree.insert(& 0xA0_00_00_00, & 3, "101");
        tree.insert(& 0xC0_A8_01_45, & 32, "11000000101010000000000101000101");
        tree.insert(& 0x0A_A8_01_45, & 32, "00001010101010000000000101000101");
        tree
    }

    /// Tests creating new tree
    #[rstest]
    fn new_tree_has_empty_root(empty_tree: RoutingTableTree) {
        assert_interface!(empty, empty_tree.root);
        assert_subtrees!(empty, empty_tree.root);
    }

    /// Tests adding a default route
    #[rstest]
    fn insert_default_route_into_empty(mut empty_tree: RoutingTableTree) {
        empty_tree.insert(& 0, & 0, "default");
        assert_interface!("default", empty_tree.root);
        assert_subtrees!(empty, empty_tree.root);
    }

    /// Tests that non-empty host bits are ignored
    #[rstest]
    fn insert_with_non_empty_host_bits(mut empty_tree: RoutingTableTree) {
        empty_tree.insert(& 0xFF_FF_FF_FF, & 1, "right");
        assert_interface!(empty, empty_tree.root);
        assert_subtrees!(only_right, empty_tree.root);
        let root_right = empty_tree.root.right.unwrap();
        assert_interface!("right", root_right);
        assert_subtrees!(empty, root_right);
    }

    /// Tests adding a route with first bit 0 and prefix len 1
    #[rstest]
    fn insert_left_of_root_into_empty(mut empty_tree: RoutingTableTree) {
        empty_tree.insert(& 0, & 1, "left");
        assert_interface!(empty, empty_tree.root);
        assert_subtrees!(only_left, empty_tree.root);
        let root_left = empty_tree.root.left.unwrap();
        assert_interface!("left", root_left);
        assert_subtrees!(empty, root_left);
    }

    /// Tests adding a route with first bit 1 and prefix len 1
    #[rstest]
    fn insert_right_of_root_into_empty(mut empty_tree: RoutingTableTree) {
        empty_tree.insert(& 0x80_00_00_00, & 1, "right");
        assert_interface!(empty, empty_tree.root);
        assert_subtrees!(only_right, empty_tree.root);
        let root_right = empty_tree.root.right.unwrap();
        assert_interface!("right", root_right);
        assert_subtrees!(empty, root_right);
    }

    /// Tests adding route with longer prefix length to empty tree
    /// Added route has first bits 010 and prefix length 3
    ///
    ///          <None>
    ///          /
    ///     <None>
    ///          \
    ///          <None>
    ///          /
    ///       deep
    ///
    #[rstest]
    fn insert_deeper_level_into_empty(mut empty_tree: RoutingTableTree) {
        empty_tree.insert(& 0x40_00_00_00, & 3, "deep");
        assert_interface!(empty, empty_tree.root);
        assert_subtrees!(only_left, empty_tree.root);
        let node_0 = empty_tree.root.left.unwrap();
        assert_interface!(empty, node_0);
        assert_subtrees!(only_right, node_0);
        let node_01 = node_0.right.unwrap();
        assert_interface!(empty, node_01);
        assert_subtrees!(only_left, node_01);
        let node_010 = node_01.left.unwrap();
        assert_interface!("deep", node_010);
        assert_subtrees!(empty, node_010);
    }

    /// Tests that adding a route second time overwrites the interface name
    #[rstest]
    fn overwrite_interface_name(empty_tree: RoutingTableTree) {
        let mut tree = empty_tree;
        tree.insert(& 0x80_00_00_00, & 1, "first_value");
        assert_interface!(empty, tree.root);
        assert_subtrees!(only_right, tree.root);
        let node_1 = tree.root.right.as_ref().unwrap();
        assert_interface!("first_value", node_1);
        assert_subtrees!(empty, node_1);
        tree.insert(& 0x80_00_00_00, & 1, "second_value");
        let node_1 = tree.root.right.as_ref().unwrap();
        assert_interface!("second_value", node_1);
        assert_subtrees!(empty, node_1);
    }

    /// Tests that adding a default route to non empty tree does not remove sub trees
    #[rstest]
    fn append_default_route_does_not_clear_the_tree(one_level_tree: RoutingTableTree) {
        let mut tree = one_level_tree;
        tree.insert(& 0, & 0, "default");
        assert_interface!("default", tree.root);
        assert_subtrees!(both, tree.root);
        let node_0 = tree.root.left.unwrap();
        assert_interface!("left", node_0);
        assert_subtrees!(empty, node_0);
        let node_1 = tree.root.right.unwrap();
        assert_interface!("right", node_1);
        assert_subtrees!(empty, node_1);
    }

    /// Tests adding a deep subtree to existing subtree.
    /// Added route has first bits 101 and prefix length 3
    ///
    ///          <None>
    ///          /    \
    ///       left    right
    ///               /
    ///          <None>
    ///               \
    ///              deep_right
    ///
    #[rstest]
    fn append_under_existing_node(one_level_tree: RoutingTableTree) {
        let mut tree = one_level_tree;
        tree.insert(& 0xA0_00_00_00, & 3, "deep_right");
        assert_interface!(empty, tree.root);
        assert_subtrees!(both, tree.root);
        let node_0 = tree.root.left.unwrap();
        assert_interface!("left", node_0);
        assert_subtrees!(empty, node_0);
        let node_1 = tree.root.right.unwrap();
        assert_interface!("right", node_1);
        assert_subtrees!(only_left, node_1);
        let node_10 = node_1.left.unwrap();
        assert_interface!(empty, node_10);
        assert_subtrees!(only_right, node_10);
        let node_101 = node_10.right.unwrap();
        assert_interface!("deep_right", node_101);
        assert_subtrees!(empty, node_101);
    }

    /// Tests adding new deep subtree
    /// Added route has first bits 101 and prefix length 3
    ///
    ///          default_iface
    ///          /           \
    ///       left           <None>
    ///                      /
    ///                 <None>
    ///                      \
    ///                     deep_right
    ///
    #[rstest]
    fn append_new_subtree(just_left_sub_tree: RoutingTableTree) {
        let mut tree = just_left_sub_tree;
        tree.insert(& 0xA0_00_00_00, & 3, "deep_right");
        assert_interface!("default_iface", tree.root);
        assert_subtrees!(both, tree.root);
        let node_0 = tree.root.left.unwrap();
        assert_interface!("left", node_0);
        assert_subtrees!(empty, node_0);
        let node_1 = tree.root.right.unwrap();
        assert_interface!(empty, node_1);
        assert_subtrees!(only_left, node_1);
        let node_10 = node_1.left.unwrap();
        assert_interface!(empty, node_10);
        assert_subtrees!(only_right, node_10);
        let node_101 = node_10.right.unwrap();
        assert_interface!("deep_right", node_101);
        assert_subtrees!(empty, node_101);
    }

    /// Tests adding a route with prefix length 32
    #[rstest]
    fn append_32_bits_route(empty_tree: RoutingTableTree) {
        let mut tree = empty_tree;
        tree.insert(& 0x00_00_00_00, & 32, "deep_left");
        let mut node = tree.root;
        // The height of the tree is highest prefix length + 1 (for the root)
        // In this test the height will be 33
        // This loop is not asserting on the leaf (asserted after the loop), so we need a check 32 nodes
        for _ in 0..32 {
            assert_interface!(empty, node);
            assert_subtrees!(only_left, node);
            node = node.left.unwrap();
        }
        assert_interface!("deep_left", node);
        assert_subtrees!(empty, node);
    }

    /// Tests adding a default route
    #[rstest]
    fn insert_by_string_default_route_into_empty(mut empty_tree: RoutingTableTree) {
        empty_tree.insert_by_string("0.0.0.0/0", "default").unwrap();
        assert_interface!("default", empty_tree.root);
        assert_subtrees!(empty, empty_tree.root);
    }

    /// Tests adding by string a route with first bit 0 and prefix len 1
    #[rstest]
    fn insert_by_string_left_of_root_into_empty(mut empty_tree: RoutingTableTree) {
        empty_tree.insert_by_string("0.0.0.0/1", "left").unwrap();
        assert_interface!(empty, empty_tree.root);
        assert_subtrees!(only_left, empty_tree.root);
        let root_left = empty_tree.root.left.unwrap();
        assert_interface!("left", root_left);
        assert_subtrees!(empty, root_left);
    }

    /// Tests adding by string a route with first bit 1 and prefix len 1
    #[rstest]
    fn insert_by_string_right_of_root_into_empty(mut empty_tree: RoutingTableTree) {
        empty_tree.insert_by_string("128.0.0.0/1", "right").unwrap();
        assert_interface!(empty, empty_tree.root);
        assert_subtrees!(only_right, empty_tree.root);
        let root_right = empty_tree.root.right.unwrap();
        assert_interface!("right", root_right);
        assert_subtrees!(empty, root_right);
    }

    /// Tests searching in empty tree
    #[rstest]
    fn search_in_empty_tree(empty_tree: RoutingTableTree) {
        let found_iface = empty_tree.search(& 0xC0_A8_01_45);
        assert!(found_iface.is_none())
    }

    /// Tests searching in tree with just default route
    #[rstest]
    fn search_in_default_route_tree(empty_with_default: RoutingTableTree) {
        let found_iface = empty_with_default.search(& 0xC0_A8_01_45);
        assert_eq!(found_iface.unwrap(), "default_iface");
    }

    /// Tests searching in empty sub tree of root
    #[rstest]
    fn search_in_empty_subtree(just_left_sub_tree: RoutingTableTree) {
        let found_iface = just_left_sub_tree.search(& 0x80_A8_01_45);
        assert_eq!(found_iface.unwrap(), "default_iface");
    }

    /// Tests searching finds an interface from leaf node
    #[rstest]
    fn search_in_the_leaf(search_tree: RoutingTableTree) {
        let found_iface = search_tree.search(& 0xA0_A8_01_45);
        assert_eq!(found_iface.unwrap(), "deep_right");
    }

    /// Tests searching finds an interface when last visited node has no interface
    /// Searching for something that starts with 100
    #[rstest]
    fn search_returns_interface_not_from_leaf(search_tree: RoutingTableTree) {
        let found_iface = search_tree.search(& 0x80_A8_01_45);
        assert_eq!(found_iface.unwrap(), "right");
    }

    /// Tests searching finds an interface when last visited node has no interface
    /// Searching for something that starts with 00
    #[rstest]
    fn search_in_search_tree_returns_default_route(search_tree: RoutingTableTree) {
        let found_iface = search_tree.search(& 0x00_A8_01_45);
        assert_eq!(found_iface.unwrap(), "default_iface");
    }

    // Tests searching in a complex tree
    #[rstest]
    #[case(0x00_00_00_00, "default")]  // Coming back to default when proper /5 node did not exist
    #[case(0xFF_FF_FF_FF, "1")]  // Coming back to /1 node when proper /3 node did not exist
    #[case(0x7F_A8_01_45, "01")]  // Reading from /2 leaf
    #[case(0xBB_A8_01_45, "101")]  // Reading from /3 leaf
    #[case(0xC0_A8_01_45, "11000000101010000000000101000101")]  // Reading from /32 leaf
    #[case(0xC0_A8_01_44, "1")]  // Coming back to /1 node from non-existing sibling of /32
    #[case(0x0A_A8_01_45, "00001010101010000000000101000101")]  // Reading from /32 leaf
    #[case(0x0A_A8_01_44, "default")]  // Coming back to default node from non-existing sibling of /32
    fn search_complex(#[case] ip_address: u32, #[case] expected_interface: &str, complex_tree: RoutingTableTree) {
        let found_iface = complex_tree.search(& ip_address);
        assert_eq!(found_iface.unwrap(), expected_interface);
    }

    // Test of some possible production solution
    #[rstest]
    fn end_to_end() {
        let mut tree = RoutingTableTree::new();
        tree.insert_by_string("0.0.0.0/1", "eth0").unwrap();
        tree.insert_by_string("10.0.0.0/8", "eth10").unwrap();
        tree.insert_by_string("10.0.11.0/23", "eth10-11-23").unwrap();
        tree.insert_by_string("192.168.0.0/16", "eth192").unwrap();
        tree.insert_by_string("192.168.6.0/23", "eth192-6-23").unwrap();
        tree.insert_by_string("192.168.6.0/24", "eth192-6-24").unwrap();
        tree.insert_by_string("192.168.7.0/24", "eth192-7-24").unwrap();
        tree.insert_by_string("192.168.50.0/24", "eth192-50-24").unwrap();
        tree.insert_by_string("192.168.50.0/25", "eth192-50-25").unwrap();
        tree.insert_by_string("192.168.45.128/25", "eth192-45-25").unwrap();
        tree.insert_by_string("192.168.45.128/32", "eth192-45-32").unwrap();
        let test_data: [(&str, Option<String>); 13] = [
            ("11.0.0.1", Some("eth0".to_string())),
            ("10.0.0.1", Some("eth10".to_string())),
            ("10.0.10.1", Some("eth10-11-23".to_string())),
            ("10.0.9.1", Some("eth10".to_string())),
            ("192.168.3.1", Some("eth192".to_string())),
            ("192.168.6.12", Some("eth192-6-24".to_string())),
            ("192.168.7.12", Some("eth192-7-24".to_string())),
            ("192.168.50.1", Some("eth192-50-25".to_string())),
            ("192.168.50.255", Some("eth192-50-24".to_string())),
            ("192.168.45.128", Some("eth192-45-32".to_string())),
            ("192.168.45.129", Some("eth192-45-25".to_string())),
            ("192.168.45.127", Some("eth192".to_string())),
            ("172.15.67.1", None),
        ];
        for (address, expected) in test_data {
            assert_eq!(tree.search_by_string(address).unwrap(), expected, "Tested address: {}", address);
        }
    }
}
