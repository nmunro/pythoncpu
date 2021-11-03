def string_to_hex(s):
    return [hex(a) for a in [ord(c) for c in s]]
