# Library for finding best route in the routing table

Implementation of trie-tree best route finding algorithm.

It is actually a bindings wrapper for the Rust library.

## Usage

See [.pyi stub file](https://github.com/KRunchPL/best-route-finder/blob/master/py-best-route-finder/best_route_finder/best_route_finder.pyi) (also included in the package) for detailed information.

The information from the stub file should be visible in your IDE hints as well as shown by "Go to Definition" IDE action.

### Example

```python
from ipaddress import IPv4Address

from best_route_finder import IPv4RoutingTableTree

table = IPv4RoutingTableTree()
table.insert(int(IPv4Address('192.168.1.0')), 24, 'ens192')
table.insert_by_string('10.0.0.0/8', 'ens10')

assert 'ens192' == table.search_by_string('192.168.1.123')
assert 'ens10' == table.search(int(IPv4Address('10.1.1.43')))
```

### Creating form the list

The `IPv4RoutingTableTree` also provides an option to create a routing table by passing a list of entries.

```python
class IPv4RoutingTableTree:
    (...)
    def from_mapping(entries: list[__RoutingTableEntry]) -> 'IPv4RoutingTableTree': ...
```

The entries have to implement interface compatible with:

```python
@dataclass
class __RoutingTableEntry:
    """
    Interface for a class representing single routing table entry

    User shall provide own implementation of this interface
    """
    subnet: IPv4Network  #: a subnet part of an entry
    interface: str  #: next-hop interface name associated with the subnet
```

In low-level terms they have to be objects that will have proper attributes set, so the following code will not raise an error:

```python
assert isinstance(entry.subnet.network_address._ip, int)
assert isinstance(entry.subnet.prefixlen, int)
assert isinstance(entry.interface, str)
```
