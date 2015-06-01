

def write_encoded_binary(keys, binary_string, path_out):
    keys = create_binary_code_bytes(keys)
    data = create_encoded_data_string(binary_string)
    file1 = open(path_out, 'wb+')
    file1.write(keys + data)
    file1.close()

def read_encoded_binary(path_in):
    file1 = open(path_in, 'rb')
    a = list(bytearray(file1.read()))
    file1.close()
    keys = a[0:256]
    data = a[256:]
    keys = get_code_from_bytes(keys)
    binary_string = get_encoded_data_string(data)
    return keys, binary_string


def write_string_to_file(path, string_out):
    file_in = open(path, 'wb+')
    file_in.write(string_out)
    file_in.close()

def read_string_from_file(path):
    file_in = open(path, 'rb')
    string_in = file_in.read()
    file_in.close()
    return string_in


def create_encoded_data_string(string_out):  # O(n) #Creates Binary Array of Encoded String
    d = [int(string_out[x:x + 8], 2)
         for x in range(0, len(string_out), 8)]  # O(n)
    y = len(string_out) % 8
    if y == 0:
        y += 8
    d = d + \
        [
            y]  # additional byte is length of last byte, cost is only byte/file #O(1)
    d = bytearray(d)  # O(n)
    return d

def get_encoded_data_string(a):
    b = list(a)
    c = ['{0:08b}'.format(x) for x in b[0:-2]]
    d = "".join(c)
    d = d + (
        '{0:0%sb}' %
        b[-1]).format(b[-2])  # b[-1] is the length of the last byte, b[-2]. b[-1] used as stringvar to preappend correct number of 0's
    return d


def create_binary_code_bytes(g0):  # O(1) #Creates Binary array of Binary tree
    code_bytes = bytearray()  # O(1)
    for char_index in range(0,256):  # O(1)
        if chr(char_index) in g0:  # O(1)
            code_bytes.append(g0[chr(char_index)])  # O(1)
        else:
            code_bytes.append(0)  # O(1)
    return code_bytes

def get_code_from_bytes(code_bytes):
    code = {}
    for q in range(0, len(code_bytes)):
        if code_bytes[q] != 0:
            code[chr(q)] = code_bytes[q]
    return code


