use best_route_finder::{RoutingTableTree};

fn main() {
    let mut table = RoutingTableTree::new();
    println!("Adding 192.168.3.0/24 to go via eth192");
    table.insert_by_string("192.168.3.0/24", "eth192").unwrap();
    println!("Adding 10.0.0.0/8 to go via eth10");
    table.insert_by_string("10.0.0.0/8", "eth10").unwrap();
    println!("");
    println!("192.168.3.123 goes through {}", table.search_by_string("192.168.3.123").unwrap().unwrap());
    println!("10.13.14.18 goes through {}", table.search_by_string("10.13.14.18").unwrap().unwrap());
    println!("1.1.1.1 goes through {:?}", table.search_by_string("1.1.1.1").unwrap());
}
