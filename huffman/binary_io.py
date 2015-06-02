
def write_encoded_binary(code_length_map, binary_string, path_out):
    """
    Takes byte arrays of code lengths and string of binary symbols
    and writes them to path_out

    Args:
        code_length_map (dict) : byte array of code lengths
        binary_string (string) : String of characters '0's or '1's
    """
    binary_code_bytes = create_binary_code_bytes(code_length_map)
    binary_data = create_encoded_data_string(binary_string)

    file1 = open(path_out, 'wb+')
    file1.write(binary_code_bytes + binary_data)
    file1.close()

def read_encoded_binary(path_in):
    """
    Takes a path location and generates a code length map and encoded string

    Args:
        path_in (string): Path to encoded binary file

    Returns:
        code_length_map (dict) : byte array of code lengths
        binary_string (string) : String of characters '0's or '1's
    """
    encoded_file = open(path_in, 'rb')
    bytes_list = list(bytearray(encoded_file.read()))
    encoded_file.close()
    code_length_map = bytes_list[0:256]
    data_bytes = bytes_list[256:]
    code_length_map = get_code_lengths_from_bytes(code_length_map)
    binary_string = get_encoded_data_string(data_bytes)
    return code_length_map, binary_string


def write_string_to_file(path, string_out):
    """
    Args:
        path (string) : Path to write decoded file to
        string_out (string) : Decoded file data string
    """
    file_in = open(path, 'wb+')
    file_in.write(string_out)
    file_in.close()


def read_string_from_file(path):
    """
    Args:
        path (string) : Path to read decoded file from

    Returns:
        string_in (string) : Decoded file data string

    Note:
        O(n) - since reading file
    """
    file_in = open(path, 'rb')
    string_in = file_in.read()
    file_in.close()
    return string_in


def create_encoded_data_string(binary_string):
    """
    Creates Binary Array of Encoded String

    Args:
        binary_string (string) : String of characters, '0's or '1's

    Returns:
        byte_list (bytearray) : Array of encoded bytes

    Note:
        O(n) - Byte array length is of same order as input
    """
    byte_list = [int(binary_string[x:x + 8], 2) for x in range(0, len(binary_string), 8)]  # O(n)
    final_byte_length = len(binary_string) % 8
    if final_byte_length == 0:
        final_byte_length = 8
    byte_list = byte_list + [final_byte_length]
    byte_list = bytearray(byte_list)
    return byte_list

def get_encoded_data_string(data_bytes):
    """
    Generates and encoded string of binary characters from a bytearray of data_bytes

    Args:
        data_bytes (bytearray) : Array of encoded data bytes

    Returns:
        binary_string (string) : String of binary '0's and '1's

    Note:
        data_bytes[-1] is the length of the last byte ( data_bytes[-2] )
    """
    data_bytes_list = list(data_bytes)
    binary_character_list = ['{0:08b}'.format(x) for x in data_bytes_list[0:-2]]
    binary_string = "".join(binary_character_list)
    binary_string = binary_string + ('{0:0%sb}' % data_bytes_list[-1]).format(data_bytes_list[-2])
    return binary_string


def create_binary_code_bytes(code_length_map):
    """
    Generates binary code bytes from a code length map

    Args:
        code_length_map (dict) : Mapping of code symbol : code length

    Returns:
        code_bytes (bytearray) : Array of code bytes

    Note:
        O(1) - Since 256 symbols
    """
    code_bytes = bytearray()  # O(1)
    for char_index in range(0, 256):  # O(1)
        if chr(char_index) in code_length_map:  # O(1)
            code_bytes.append(code_length_map[chr(char_index)])  # O(1)
        else:
            code_bytes.append(0)  # O(1)
    return code_bytes

def get_code_lengths_from_bytes(code_bytes):
    """
    Generates a mapping of symbol to code length from bytes of code lengths

    Args:
        code_bytes (bytearray) : Array of bytes representing code lengths

    Returns:
        code_length_map (dict) : Mapping of Symbol to code length

    Note:
        O(1) - Dictionary size is 256
    """
    code_length_map = {}
    for q in range(0, len(code_bytes)):
        if code_bytes[q] != 0:
            code_length_map[chr(q)] = code_bytes[q]
    return code_length_map

