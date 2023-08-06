use colored::*;
use best_route_finder::{RoutingTableTree};

fn main() {
    let mut table = RoutingTableTree::new();
    println!("{}", "Errors when inserting by string".green().underline());
    match table.insert_by_string("0.0.0.1", "eth0") {
        Ok(_) => {},
        Err(error) => println!("{}", error),
    };
    match table.insert_by_string("0.0.0.1/a", "eth0") {
        Ok(_) => {},
        Err(error) => println!("{}", error),
    };
    match table.insert_by_string("0.0.0.0.1/16", "eth0") {
        Ok(_) => {},
        Err(error) => println!("{}", error)
    };
    match table.insert_by_string("0.0.0.1/35", "eth0") {
        Ok(_) => {},
        Err(error) => println!("{}", error)
    };
    println!("\n{}", "Errors when searching by string".green().underline());
    match table.search_by_string("0.0.0.0.1") {
        Ok(_) => {},
        Err(error) => println!("{}", error)
    };
}
