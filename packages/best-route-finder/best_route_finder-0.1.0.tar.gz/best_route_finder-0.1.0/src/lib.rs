use pyo3::prelude::*;
use pyo3::exceptions;
use pyo3::types::{PyList};
use best_route_finder::{RoutingTableTree as _RoutingTableTree};


macro_rules! extract_attribute {
    ($py_any:ident, $return_type:ty, $($attrs:expr),*) => {{
        let mut attr_value: &PyAny = $py_any;
        $(
            attr_value = match attr_value.getattr($attrs){
                Ok(value) => value,
                Err(err) => return Err(err),
            };
        )+
        match attr_value.extract::<$return_type>() {
            Ok(value) => value,
            Err(err) => return Err(err),
        }
    }}
}

#[pyclass]
struct IPv4RoutingTableTree {
    _routing_table: _RoutingTableTree,
}

#[pymethods]
impl IPv4RoutingTableTree {
    #[new]
    fn new() -> Self {
        IPv4RoutingTableTree { _routing_table: _RoutingTableTree::new() }
    }
    #[staticmethod]
    fn from_mapping(entries: &PyList) -> PyResult<Self> {
        let mut tree = IPv4RoutingTableTree { _routing_table: _RoutingTableTree::new() };
        for entry in entries {
            tree._routing_table.insert(
                &extract_attribute!(entry, u32, "subnet", "network_address", "_ip"),
                &extract_attribute!(entry, u8, "subnet", "prefixlen"),
                extract_attribute!(entry, &str, "interface"),
            );
        }
        Ok(tree)
    }
    fn insert(mut self_: PyRefMut<Self>, network_address: u32, prefix_length: u8, interface: &str) {
        self_._routing_table.insert(&network_address, &prefix_length, interface);
    }
    fn search(self_: PyRefMut<Self>, ip_address: u32) -> Option<String> {
        self_._routing_table.search(&ip_address)
    }
    fn insert_by_string(mut self_: PyRefMut<Self>, cidr: &str, interface: &str) -> PyResult<()> {
        match self_._routing_table.insert_by_string(cidr, interface) {
            Ok(value) => Ok(value),
            Err(err) => Err(PyErr::new::<exceptions::PyValueError, _>(err.to_string())),
        }
    }
    fn search_by_string(self_: PyRef<Self>, ip_address: &str) -> PyResult<Option<String>>  {
        match self_._routing_table.search_by_string(ip_address) {
            Ok(value) => Ok(value),
            Err(err) => Err(PyErr::new::<exceptions::PyValueError, _>(err.to_string())),
        }
    }
}


#[pymodule]
fn best_route_finder(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<IPv4RoutingTableTree>()?;
    Ok(())
}
