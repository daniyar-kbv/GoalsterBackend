def encode(string):
    bytes = string.encode('utf-8')
    return int.from_bytes(bytes, 'little')


def decode(number):
    bytes = number.to_bytes((number.bit_length() + 7) // 8, 'little')
    return bytes.decode('utf-8')
