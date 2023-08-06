
use std::error;
use std::fmt;
use std::net::{AddrParseError, Ipv4Addr};
use std::num::ParseIntError;
use std::str::FromStr;


/// Enum agregating all errors raised while parsing CIDR or IP strings
#[derive(Debug)]
pub enum CidrStringParsingError {
    /// Raised when CIDR string does not have a slash
    MissingSlash{
        /// a CIDR string that was passed to parser
        cidr: String,
    },
    /// Raised when IP or IP part of CIDR string is not parsable to Ipv4Addr
    AddressParseError{
        /// a CIDR or IP string that was passed to parser
        cidr: String,
        /// a string that the library tried to parse as a Ipv4Addr
        ip_part: String,
        /// an error that was raised by internal library
        original_error: AddrParseError,
    },
    /// Raised when prefix length part of CIDR string is not parsable to integer
    PrefixLengthParseError{
        /// a CIDR string that was passed to parser
        cidr: String,
        /// a string that the library tried to parse as a prefix length int
        prefix_len_part: String,
        /// an error that was raised by internal library
        original_error: ParseIntError,
    },
    /// Raised when parsed prefix length is bigger than 32
    PrefixLengthTooBig{
        /// a CIDR string that was passed to parser
        cidr: String,
        /// parsed prefix length value
        prefix_len: u8,
    },
}

impl fmt::Display for CidrStringParsingError {
    /// Returns human readable string describing the error
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            CidrStringParsingError::MissingSlash{cidr} => {
                write!(f, "Provided CIDR '{}' does not contain a '/' character", cidr)
            }
            CidrStringParsingError::AddressParseError{cidr, ip_part, original_error} => {
                write!(
                    f,
                    "Cannot parse '{}' (the first part of '{}') into IPv4 Address. \
                    Underlying error: {}",
                    ip_part, cidr, original_error
                )
            }
            CidrStringParsingError::PrefixLengthParseError{cidr, prefix_len_part, original_error} => {
                write!(
                    f,
                    "Cannot parse '{}' (the second part of CIDR '{}') into prefix length. \
                    Underlying error: {}",
                    prefix_len_part, cidr, original_error
                )
            }
            CidrStringParsingError::PrefixLengthTooBig{cidr, prefix_len} => {
                write!(f,
                    "Provided CIDR '{}' is invalid. Parsed prefix length '{}' is too big. \
                    It has to be 0 <= prefix_len <= 32",
                    cidr, prefix_len
                )
            }
        }
    }
}

impl error::Error for CidrStringParsingError {
    /// If this error was caused by different one this method returns the original error
    fn source(&self) -> Option<&(dyn error::Error + 'static)> {
        match *self {
            CidrStringParsingError::AddressParseError{
                cidr: _, ip_part: _, original_error: ref e
            } => Some(e),

            CidrStringParsingError::PrefixLengthParseError{
                cidr: _, prefix_len_part: _, original_error: ref e
            } => Some(e),

            _ => None,
        }
    }
}


/// Parses given string into tuple of two integers: network address and prefix length
///
/// # Arguments
///
/// * `cidr` - a CIDR string to be parsed
///
/// # Examples
///
/// ```
/// use best_route_finder::ip_strings_parsers::cidr_string_to_integers;
///
/// let result: (u32, u8) = cidr_string_to_integers("192.168.1.0/24").unwrap();
/// assert_eq!((0xC0_A8_01_00_u32, 24_u8), result)
/// ```
pub fn cidr_string_to_integers(cidr: &str) -> Result<(u32, u8), CidrStringParsingError> {
    match cidr.rsplit_once("/") {
        None => {
            Err(CidrStringParsingError::MissingSlash{cidr: cidr.to_string()})
        }
        Some(tuple) => {
            let ip_address: Ipv4Addr = match Ipv4Addr::from_str(&tuple.0) {
                Ok(value) => value,
                Err(err) => return Err(
                    CidrStringParsingError::AddressParseError{
                        cidr: cidr.to_string(),
                        ip_part: tuple.0.to_string(),
                        original_error: err,
                    }
                ),
            };
            let ip_address_as_int: u32 = ip_address.into();
            let prefix_len: u8 = match tuple.1.parse() {
                Ok(value) => value,
                Err(err) => return Err(
                    CidrStringParsingError::PrefixLengthParseError{
                        cidr: cidr.to_string(),
                        prefix_len_part: tuple.1.to_string(),
                        original_error: err,
                    }
                ),
            };
            if prefix_len > 32 {
                return Err(CidrStringParsingError::PrefixLengthTooBig{cidr: cidr.to_string(), prefix_len: prefix_len})
            }
            Ok((ip_address_as_int, prefix_len))
        }
    }
}

/// Parses given string into integer representation of given IP address
///
/// # Arguments
///
/// * `ip_address_string` - an IP string to be parsed
///
/// # Examples
///
/// ```
/// use best_route_finder::ip_strings_parsers::ip_string_to_integer;
///
/// let result: u32 = ip_string_to_integer("192.168.1.16").unwrap();
/// assert_eq!(0xC0_A8_01_10_u32, result)
/// ```
pub fn ip_string_to_integer(ip_address_string: &str) -> Result<u32, CidrStringParsingError> {
    match Ipv4Addr::from_str(ip_address_string) {
        Ok(ip_address) => Ok(ip_address.into()),
        Err(err) => return Err(
            CidrStringParsingError::AddressParseError{
                cidr: ip_address_string.to_string(),
                ip_part: ip_address_string.to_string(),
                original_error: err,
            }
        ),
    }
}

#[cfg(test)]
mod tests {
    use rstest::rstest;
    use crate::ip_strings_parsers::{cidr_string_to_integers, CidrStringParsingError, ip_string_to_integer};

    #[test]
    fn cidr_parsing_from_string_ref() {
        assert_eq!(cidr_string_to_integers(&String::from("0.0.0.4/15")).unwrap(), (4_u32, 15_u8));
    }

    #[test]
    fn cidr_parsing_from_str() {
        assert_eq!(cidr_string_to_integers("0.0.0.4/15").unwrap(), (4_u32, 15_u8));
    }

    #[rstest]
    #[case("0.0.0.0/0", (0, 0))]
    #[case("0.0.0.1/0", (1, 0))]
    #[case("0.0.0.234/0", (234, 0))]
    #[case("0.0.1.0/0", (256, 0))]
    #[case("0.1.0.0/0", (65_536, 0))]
    #[case("1.0.0.0/0", (16_777_216, 0))]
    fn cidr_parsing_ok(#[case] cidr: &str, #[case] expected: (u32, u8)) {
        match cidr_string_to_integers(cidr) {
            Ok(result) => {
                assert_eq!(result, expected);
            }
            Err(err) => {
                panic!("Case {}. {}", cidr, err)
            }
        }
    }

    #[rstest]
    #[case("0.0.0.0/33")]
    fn cidr_parsing_too_big_prefix(#[case] cidr: &str) {
        match cidr_string_to_integers(cidr) {
            Err(CidrStringParsingError::PrefixLengthTooBig{cidr: _, prefix_len: _}) => (),
            Err(err) => panic!(
                "Case {}. The function returned an error, but not PrefixLengthTooBig error but: {}",
                cidr, err
            ),
            Ok(result) => panic!(
                "Case {}. The function did not return an error, but succeeded with result: {:?}",
                cidr, result
            ),
        }
    }

    #[rstest]
    #[case("0.0.0.0/-1")]
    #[case("0.0.0.0/")]
    #[case("0.0.0.0/abc")]
    #[case("0.0.0.0/true")]
    fn cidr_parsing_not_parsable_prefix(#[case] cidr: &str) {
        match cidr_string_to_integers(cidr) {
            Err(CidrStringParsingError::PrefixLengthParseError{
                cidr: _, prefix_len_part: _, original_error: _
            }) => (),
            Err(err) => panic!(
                "Case {}. The function returned an error, but not PrefixLengthParseError error but: {}",
                cidr, err
            ),
            Ok(result) => panic!(
                "Case {}. The function did not return an error, but succeeded with result: {:?}",
                cidr, result
            ),
        }
    }

    #[rstest]
    #[case("0.0.0.0-33")]
    #[case("0.0.0.0.33")]
    #[case("0.0.0.0")]
    #[case("0.0.0.0\\0")]
    fn cidr_parsing_missing_slash(#[case] cidr: &str) {
        match cidr_string_to_integers(cidr) {
            Err(CidrStringParsingError::MissingSlash{cidr: _}) => (),
            Err(err) => panic!(
                "Case {}. The function returned an error, but not MissingSlash error but: {}",
                cidr, err
            ),
            Ok(result) => panic!(
                "Case {}. The function did not return an error, but succeeded with result: {:?}",
                cidr, result
            ),
        }
    }

    #[rstest]
    #[case("0.0.0/32")]
    #[case("0.0/32")]
    #[case("0/32")]
    #[case("0.0.0./32")]
    #[case("0.0./32")]
    #[case("0./32")]
    #[case("0.0.00/32")]
    #[case("0.0.0.01/32")]
    #[case("0.0.0.001/32")]
    #[case("0.0.01.0/32")]
    #[case("0.0.001.0/32")]
    #[case("0.01.0.0/32")]
    #[case("0.001.0.0/32")]
    #[case("01.0.0.0/32")]
    #[case("001.0.0.0/32")]
    #[case("256.0.0.0/32")]
    #[case("0.256.0.0/32")]
    #[case("0.0.256.0/32")]
    #[case("0.0.0.256/32")]
    fn cidr_parsing_address_parse_error(#[case] cidr: &str) {
        match cidr_string_to_integers(cidr) {
            Err(CidrStringParsingError::AddressParseError{cidr: _, ip_part: _, original_error: _}) => (),
            Err(err) => panic!(
                "Case {}. The function returned an error, but not AddressParseError error but: {}",
                cidr, err
            ),
            Ok(result) => panic!(
                "Case {}. The function did not return an error, but succeeded with result: {:?}",
                cidr, result
            ),
        }
    }

    #[test]
    fn ip_parsing_from_string_ref() {
        assert_eq!(ip_string_to_integer(&String::from("0.0.0.4")).unwrap(), 4_u32);
    }

    #[test]
    fn ip_parsing_from_str() {
        assert_eq!(ip_string_to_integer("0.0.0.4").unwrap(), 4_u32);
    }

    #[rstest]
    #[case("0.0.0.0", 0)]
    #[case("0.0.0.1", 1)]
    #[case("0.0.0.234", 234)]
    #[case("0.0.1.0", 256)]
    #[case("0.1.0.0", 65_536)]
    #[case("1.0.0.0", 16_777_216)]
    fn ip_parsing_ok(#[case] ip_address: &str, #[case] expected: u32) {
        match ip_string_to_integer(ip_address) {
            Ok(result) => {
                assert_eq!(
                    result, expected,
                    "Case {}. The address was parsed to '{}' instead of '{}'",
                    ip_address, result, expected
                );
            }
            Err(err) => {
                panic!("Case {}. {}", ip_address, err)
            }
        }
    }

    #[rstest]
    #[case("0.0.0")]
    #[case("0.0")]
    #[case("0")]
    #[case("0.0.0.")]
    #[case("0.0.")]
    #[case("0.")]
    #[case("0.0.00")]
    #[case("0.0.0.01")]
    #[case("0.0.0.001")]
    #[case("0.0.01.0")]
    #[case("0.0.001.0")]
    #[case("0.01.0.0")]
    #[case("0.001.0.0")]
    #[case("01.0.0.0")]
    #[case("001.0.0.0")]
    #[case("256.0.0.0")]
    #[case("0.256.0.0")]
    #[case("0.0.256.0")]
    #[case("0.0.0.256")]
    fn ip_parsing_address_parse_error(#[case] ip_address: &str) {
        match ip_string_to_integer(ip_address) {
            Err(CidrStringParsingError::AddressParseError{cidr: _, ip_part: _, original_error: _}) => (),
            Err(err) => panic!(
                "Case {}. The function returned an error, but not AddressParseError error but: {}",
                ip_address, err
            ),
            Ok(result) => panic!(
                "Case {}. The function did not return an error, but succeeded with result: {:?}",
                ip_address, result
            ),
        }
    }
}
