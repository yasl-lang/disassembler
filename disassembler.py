import sys
if len(sys.argv) == 1:
    print("Please supply a file name")
    sys.exit()
elif len(sys.argv) > 2:
    print("Too many arguments supplied")
    sys.exit()

RED = '\x1B[31m'
GRN = '\x1B[32m'
MAG = '\x1B[35m'
YEL = '\x1B[33m'
END = '\x1B[0m'

bc = {
        0x00: " nop",
        0x01: "   n",
        0x02: "   i",
        0x03: " im1",
        0x04: "  i0",
        0x05: "  i1",
        0x06: "  i2",
        0x07: "  i3",
        0x08: "  i4",
        0x09: "  i5",
        0x0A: "   d",
        0x0B: "  d0",
        0x0C: "  d1",
        0x0D: "  d2",
        0x0E: "dnan",
        0x0F: "dinf",
        0x10: "  bf",
        0x11: "  bt",
        0x12: "   f",
        0x20: " bor",
        0x21: "bxor",
        0x22: "band",
        0x23: "bnot",
        0x24: " bsl",
        0x25: " bsr",
        0x30: "ifor",
        0x32: "efor",
        0x33: "ini1",
        0x35: "ini2",
        0x50: " end",
        0x58: " dup",
        0x5B: "swap",
        0x5F: " pop",
        0x60: " add",
        0x61: " sub",
        0x62: " mul",
        0x63: " exp",
        0x64: "fdiv",
        0x65: "idiv",
        0x66: " mod",
        0x67: " neg",
        0x68: " pos",
        0x69: " not",
        0x6A: " len",
        0x6B: "cnct",
        0x72: "  gt",
        0x73: "  ge",
        0x74: "  eq",
        0x76: "  id",
        0x80: " set",
        0x81: " get",
        0x91: "  br",
        0x93: " brf",
        0x95: " brt",
        0x97: " brn",
        0x9F: "goto",
        0xBB: " str",
        0xBC: "tabl",
        0xBD: "list",
        0xF0: "halt",
        0xF4: "gstr",
        0xF5: "lstr",
        0xF6: " gld",
        0xF7: " lld",
        0xF8: " ret",
        0xF9: " cll",
        0xFA: "rcll",
        0xFF: "puts",
}
arg = {
        0x02: 8,
        0x0A: 8,
        0x12: 8,
        0x91: 8,
        0x93: 8,
        0x95: 8,
        0x97: 8,
        0x9F: 8,
        0xBB: 8,
        0xF4: 1,
        0xF5: 1,
        0xF6: 1,
        0xF7: 1,
        0xF9: 1,
        0xFA: 1,
}
cp = []

bytes_read = open(sys.argv[1], "rb").read()
header_bytes = []
main_bytes = []

def print_byte(i, b, color=RED):
    b = hex(b).lstrip('0x')
    while len(b) < 2:
        b = '0' + b
    b = color + '  ' + b + END
    if i % 16 == 15:
        return b + '\n'
    else:
        return b + ' '

def print_char(i, b, color=GRN):
    b = "'" + chr(b) + "'"
    while len(b) < 4:
        b = ' ' + b
    b = color + b + END
    if i % 16 == 15:
        return b + '\n'
    else:
        return b + ' '

def process_byte(i, b):
    if b in bc:
        b = YEL + bc[b] + END
        if i % 16 == 15:
            return b + '\n'
            print(b)
        else:
            return b + ' '
    else:
        print("error")
        print(hex(b))
        sys.exit()
    
header_len = int.from_bytes(bytes_read[:8], byteorder=sys.byteorder, signed=True)

       
main_bytes = []
fns = []
strs = []
i = header_len
while i < len(bytes_read):
    if bytes_read[i] == 0x12:
        fns.append(int.from_bytes(bytes_read[i+1:i+9], byteorder=sys.byteorder,signed=True))
    if bytes_read[i] == 0xBB:
        strs.append(int.from_bytes(bytes_read[i+1:i+9], byteorder=sys.byteorder,signed=True))
    main_bytes.append(process_byte(i - header_len, bytes_read[i]))
    for j in range(arg.get(bytes_read[i], 0)):
        i += 1
        main_bytes.append(print_byte(i - header_len, bytes_read[i]))
    i += 1

header_bytes = []
for i in range(16):
    header_bytes.append(print_byte(i, bytes_read[i], color=MAG))

i = 16
while i < header_len:
    if i in strs:
        str_len = int.from_bytes(bytes_read[i:i+8], byteorder=sys.byteorder,signed=True)
        for j in range(8):
            header_bytes.append(print_byte(i, bytes_read[i], color=GRN))
            i += 1
        for j in range(str_len):
            header_bytes.append(print_char(i, bytes_read[i]))
            i += 1
    elif i in fns:
        print(hex(i))
        header_bytes.append(print_byte(i, bytes_read[i], color=RED))
        i += 1
    else:
        header_bytes.append(print_byte(i, bytes_read[i], color=RED))
        i += 1

print("header")
print(''.join(header_bytes))
print("entry point")
print(''.join(main_bytes))
print('end of bytecode')
