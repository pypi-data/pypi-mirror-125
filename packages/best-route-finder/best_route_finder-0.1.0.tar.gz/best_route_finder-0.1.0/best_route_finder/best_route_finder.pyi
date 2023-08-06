from dataclasses import dataclass
from ipaddress import IPv4Network
from typing import Optional


@dataclass
class __RoutingTableEntry:
    """
    Interface for a class representing single routing table entry

    User shall provide own implementation of this interface
    """
    subnet: IPv4Network  #: a subnet part of an entry
    interface: str  #: next-hop interface name associated with the subnet


class IPv4RoutingTableTree:
    """
    A class representing routing table and providing search functions
    """
    def __init__(self) -> None: ...

    @staticmethod
    def from_mapping(entries: list[__RoutingTableEntry]) -> 'IPv4RoutingTableTree':
        """
        Creates a IPv4RoutingTableTree as fills it with data

        :param entries: list of routing table entries that will be added to the created tree
        :return: a IPv4RoutingTableTree instance filled with entries
        """

    def insert(network_address: int, prefix_length: int, interface: str) -> None:
        """
        Inserts given route to the routing table

        :param network_address: integer representation of network address;
            it can contain non-zero host bits, which will be ignored while adding to the tree
        :param prefix_length: route prefix length
        :param iface_name: the name of the next-hop interface associated with the route
        """

    def search(ip_address: int) -> Optional[str]:
        """
        Returns next-hop interface for the given IP address based on stored routing table

        :param ip_address: integer representation of ip address to search the next-hop interface for
        :return: next-hop interface found for given ip address or None if no route matched
        """

    def insert_by_string(cidr: str, interface: str) -> None:
        """
        Inserts given route to the routing table

        :param cidr: CIDR string;  the network address can contain non-zero host bits,
            which will be ignored while adding to the tree
        :param iface_name: the name of the next-hop interface associated with the route
        """

    def search_by_string(ip_address: str) -> Optional[str]:
        """
        Returns next-hop interface for the given IP address based on stored routing table

        :param ip_address: ip address to search the next-hop interface for
        :return: next-hop interface found for given ip address or None if no route matched
        """
