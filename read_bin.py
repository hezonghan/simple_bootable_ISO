

# 16 bytes per line
def print_line(line_id, line_content):
    print('\tbytes 0x{:02x}_ [{:04d} , {:04d}] : '.format(line_id, line_id * 16, line_id * 16 + 15), end='')
    if line_content == bytearray([0x00] * 16):
        print('\033[0;37m(all zeros)\033[0m')
    else:
        for byte_content in line_content:
            if byte_content == 0x00:
                color = '37'
            elif byte_content == 0x20:
                color = '32'
            else:
                color = '34'
            print('\033[0;{}m0x{:02x}\033[0m  '.format(color, byte_content), end='')

        print('[', end='')
        for byte_content in line_content:
            if byte_content >= 0x20:
                print('\033[0;34m{}\033[0m'.format(chr(byte_content)), end='')
            elif byte_content == 0x00:
                print('\033[0;37m?\033[0m', end='')
            else:
                print('\033[0;31m?\033[0m', end='')
        print(']', end='')

        print()


if __name__ == '__main__':
    bin_filepath = 'E:\\9_按时间\\2022_06\\2022_0819_01_vm_os\\my_asm_2022_0822\\A.bin'
    f = open(bin_filepath, 'rb')
    bin_content = f.read()
    f.close()

    for line_id in range(0, len(bin_content) // 16):
        line_content = bin_content[line_id * 16: (line_id + 1) * 16]
        print_line(line_id, line_content)

    # last line with not enough bytes:
    if len(bin_content) % 16 != 0:
        line_content = bin_content[len(bin_content) // 16 * 16 :]
        print_line(0, line_content)