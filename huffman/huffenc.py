import binary_io
import operator
"""
Main Huffman Encoding Module:

Main functions are encode and decode

"""

def generate_frequency_table(string_in):
    """
    Generates a frequency table of the bytes from an input string

    Args:
        string_in (String) : String to generate frequency of

    Returns:
        freq (dict) : Frequency mapping of bytes in string_in

    Note:
        O(n) - Iterating over entire string

    """
    freq = {}
    for byte in string_in:
        if byte not in freq:
            freq[byte] = 0
        else:
            freq[byte] += 1
    return freq


def get_minimum_frequency_pair(freq_table):
    """
    Get two min values from dictionary, O(1) since len(freq_table)<=256

    Args:
        freq_table (dict) : Mapping from symbol to frequency

    Returns:
        minimum_frequency_pair (tuple) : Pair of symbols with minimum frequency

    Note:
        O(1) - Bounded by 256 bytes
    
    """
    symbols = freq_table.keys()
    symbols.sort(key=freq_table.__getitem__)
    minimum_frequency_pair = (symbols[1], symbols[0])
    return minimum_frequency_pair


def increment_table(freq_table):
    """
    Move from table 's_n' to 's_n+1'

    Args:
        freq_table (dict) : Mapping from symbol to frequency

    Returns:
        freq_table (dict) : Augmented frequency table

    Note:
        O(1) - Bounded by 256 bytes

    """
    min_pair = get_minimum_frequency_pair(freq_table)
    combined_probability = freq_table[min_pair[0]] + freq_table[min_pair[1]]
    del freq_table[min_pair[0]]  # Remove from dictionary
    del freq_table[min_pair[1]]  # Remove from dictionary
    freq_table[
        min_pair] = combined_probability  # Add combined tuple to dictionary, along with combined probability
    return freq_table


def generate_code_length_map(huffman_tree, tree_depth=0, code_length_map={}):
    """
    For each side of the huffman_tree, recursively generate the length of the huffman_tree to that point

    Args:
        huffman_tree (dict) : Nested list of lists of symbols
        tree_depth (int) : Depth in Huffman Tree (defaults to 0)
        code_length_map (dict) : Intermediate from symbol to code length (defaults to {} )

    Returns:
        code_length_map (dict) : Mapping from symbol to code length

    Note:
        O(1) - Huffman_tree depth is bounded at 255

    """
    for x in [1, 0]:
        if huffman_tree[not x].__class__ is not tuple:
            code_length_map[huffman_tree[not x]] = tree_depth + 1
        else:
            generate_code_length_map(huffman_tree[not x], tree_depth + 1, code_length_map)
    return code_length_map


def generate_symbol_mapping(code_length_map, reverse=False):
    """
    Generates Canonical Huffman Code from code lengths

    Args:
        code_length_map (dict) : Mapping from symbol to code length
        reverse (bool) : Determines whether mapping is from symbol to codeword or inverse

    Returns:
        canonical_code (dict) : Mapping from symbol to codeword or inverse

    Note:
        O(1) - Code size is bounded by 256 Bytes

    """
    code_length_map = code_length_map.items()  # Convert dictionary to list of tuples
    code_length_map.sort(key=operator.itemgetter(1, 0))  # Sort by length, then alphabetically
    bit = code_length_map[0][1]  # Number of bits of current code
    code = 0  # Code to map
    if not reverse:
        canon = [(code_length_map[0][0], ('{0:0%sb}' % bit).format(code))]  # First element is assigned zeros
    else:
        canon = [(('{0:0%sb}' % bit).format(code), code_length_map[0][0])]  # Reversed if inverse mapping
    for q in code_length_map[1:]:
        new_bit = q[1]  # New bit length is the first length
        code += 1  # increment x
        code = code << (new_bit - bit)
        if not reverse:
            new_element = (q[0], ('{0:0%sb}' % new_bit).format(code))
        else:
            new_element = (('{0:0%sb}' % new_bit).format(code), q[0])
        canon.append(new_element)
        bit = new_bit
    canonical_code = dict(canon)
    return canonical_code


def get_default_path(path_in, encoding):
    """
    Automatically generates output path if not specified

    Args:
        path_in (string) : path to input file
        encoding (bool) :  encoding or decoding

    Returns:
        path_out (string) : auto-generated path to output

    Note:
        O(1) by inspection

    """
    if encoding:
        path_out = path_in.split(".")[0] + "_encoded" + ".hc"
    else:
        path_out = path_in.split(".")[0] + "_decoded" + ".txt"
    return path_out


def encode_string(string_in, code_map):
    """
    Maps input string to output using the generated code map

    Args:
        string_in (string) : String of input bytes
        code_map (dict) : Huffman map

    Returns:
        string_out (string) : Encoded String

    Note:
        O(n) - Must iterate over the entire input.

    """
    string_out = ""
    for q in string_in:
        string_out += code_map[q]
    return string_out


def generate_code_lengths(huffman_tree):
    """
    Generates a mapping of symbol to code length.

    Args:
        huffman_tree (dict) : Nested list of lists of symbols

    Returns:
        code_length_map (dict) : Mapping from symbol to code length

    Note:
        O(1) - Huffman_tree size is bounded
    Note:
        Code length is equivalent to tree depth

    """
    if len(huffman_tree) > 1:
        code_length_map = generate_code_length_map(huffman_tree)
    else:
        if len(huffman_tree) == 1:
            code_length_map = {huffman_tree[0]: 1}
        else:
            code_length_map = {}
    return code_length_map


def encode_file(path_in, path_out):
    """
    Encode file path_in into new file path_out

    Args:
        path_in (String) : Path of file to encode_file
        path_out (String): Path of encoded file to create

    Note:
        O(n) - Composition of called functions
    """
    print "*" * 10
    print "Huffman encoding: " + path_in
    try:
        plaintext = binary_io.read_string_from_file(path_in)  # O(n)
    except IOError:
        print "File %s could not be found for encoding. \n" % path_in
        raise SystemExit
    freq_table = generate_frequency_table(plaintext)  # O(n)
    for q in range(1, len(freq_table) - 1):  # O(1) since len(s)-1<=255
        freq_table = increment_table(freq_table)  # O(1)
    huffman_tree = freq_table.keys()  # O(1)
    code_length_map = generate_code_lengths(huffman_tree)  # O(1)
    if len(code_length_map) > 0:
        code_map = generate_symbol_mapping(code_length_map)  # O(1)
    else:
        code_map = {}
    string_out = encode_string(plaintext, code_map)  # O(n)
    print "Outputting to:" + path_out
    print "*" * 10
    binary_io.write_encoded_binary(code_length_map, string_out, path_out)  # O(n)


def decode_file(path_in, path_out):
    """
    Decode file path_in into new file path_out

    Args:
        path_in (String) : Path of file to encode_file
        path_out (String): Path of encoded file to create

    Note:
        O(n) - Composition of called functions
    """
    print "*" * 10
    print "Huffman decoding: " + path_in
    try:
        code_length_map, encoded_string = binary_io.read_encoded_binary(path_in)  # O(n)
    except Exception as e:
        print "File %s could not be found for decoding. \n"
        print str(e)
        code_length_map = {}
        encoded_string = ""
    if len(code_length_map) > 0:
        code_length_map = generate_symbol_mapping(code_length_map, True)  # O(1)
    else:
        code_length_map = {}
    decoded_string = ""
    partial_code = ""
    for char in encoded_string:  # O(n)
        partial_code += char
        if partial_code in code_length_map:
            decoded_string += code_length_map[partial_code]
            partial_code = ""

    print "Outputting to:" + path_out
    print "*" * 10
    binary_io.write_string_to_file(path_out, decoded_string)  # O(n)
