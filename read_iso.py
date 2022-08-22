
from utils import sector_size, decode, explanation

# ----------------------------------
iso_file_path = '2022_0821_A.iso'
skipped_sectors = 0
block_size = sector_size
recognized_sector = {
    0x10: 'primary_volume_descriptor',
    0x11: 'boot_record',
}
# ----------------------------------
# iso_file_path = 'D:\\2_Software\\2_Software_Install\\20191221_Ubuntu_81_04_3\\ubuntu-18.04.3-desktop-amd64.iso'
# skipped_sectors = 0
# # skipped_sectors = 0xf3100
# block_size = sector_size
# recognized_sector = {
#     0x10: 'primary_volume_descriptor',
#     0x11: 'boot_record',
#     0xf314a: 'load',  # according to boot catalog, load RBA @ 0xf314a
# }
# ----------------------------------

f = open(iso_file_path, 'rb')
f.seek(skipped_sectors * sector_size)  # if the ISO file is too large, you may want to skip former sectors and read latter ones.
iso_file = bytearray(f.read())
f.close()

# print(bytearray([0x12, 0x34]) == bytearray([0x14, 0x34]))

sectors_cnt = len(iso_file) // sector_size
print('\nTotally {}=0x{:03x} sectors (not including skipped sectors), each has {}=0x{:03x} bytes.'.format(sectors_cnt, sectors_cnt, sector_size, sector_size))
for sector_id in range(skipped_sectors, skipped_sectors + sectors_cnt):
    sector_content = iso_file[(sector_id-skipped_sectors)*sector_size : (sector_id-skipped_sectors+1)*sector_size]

    if sector_id not in recognized_sector:
        continue

    if sector_content == bytearray([0x00] * sector_size):
        print('\nsector 0x{:03x}: \033[0;37m(all zeros)\033[0m'.format(sector_id))
        continue

    if sector_id in recognized_sector:
        print('\nsector 0x{:03x}: recognized as \033[1;31m{}\033[0m'.format(sector_id, recognized_sector[sector_id]))
        to_continue = True

        if recognized_sector[sector_id] == 'primary_volume_descriptor':
            print(explanation(0, 1, sector_content, 'type code (0x01 for primary volume descriptor)', 'int8'))
            print(explanation(1, 5, sector_content, 'standard identifier (always \'CD001\')', 'strA'))
            print(explanation(6, 1, sector_content, 'version (always 0x01)', 'int8'))
            print(explanation(7, 1, sector_content, 'unused (always 0x00)', 'int8'))

            print(explanation(8, 32, sector_content, 'system identifier', 'strA'))
            print(explanation(40, 32, sector_content, 'volume identifier', 'strD'))
            print(explanation(72, 8, sector_content, 'unused (all zeroes)', 'int_LSB'))

            print(explanation(80, 8, sector_content, 'volume space size', 'int_LSB_MSB'))
            print(explanation(88, 32, sector_content, 'unused (all zeroes)', 'int_LSB'))

            print(explanation(120, 4, sector_content, 'volume set size', 'int_LSB_MSB'))
            print(explanation(124, 4, sector_content, 'volume sequence number', 'int_LSB_MSB'))
            print(explanation(128, 4, sector_content, 'logical block size', 'int_LSB_MSB'))

            print()
            print(explanation(132, 8, sector_content, 'path table size', 'int_LSB_MSB'))
            print(explanation(140, 4, sector_content, 'LBA of L-path-table', 'int_LSB', double_formats=True))
            print(explanation(144, 4, sector_content, 'LBA of op-L-path-table', 'int_LSB', double_formats=True))
            print(explanation(148, 4, sector_content, 'LBA of M-path-table', 'int_MSB', double_formats=True))
            print(explanation(152, 4, sector_content, 'LBA of op-M-path-table', 'int_MSB', double_formats=True))

            LBA_of_L_path_table = decode(sector_content[140:140+4], 'int_LSB')
            sector_of_L_path_table = LBA_of_L_path_table * block_size // sector_size
            print('\t\033[1;31mWill recognize sector 0x{:03x} as {}\033[0m'.format(sector_of_L_path_table, 'L_path_table'))
            recognized_sector[sector_of_L_path_table] = 'L_path_table'

            LBA_of_R_path_table = decode(sector_content[148:148+4], 'int_MSB')
            sector_of_R_path_table = LBA_of_R_path_table * block_size // sector_size
            print('\t\033[1;31mWill recognize sector 0x{:03x} as {}\033[0m'.format(sector_of_R_path_table, 'R_path_table'))
            recognized_sector[sector_of_R_path_table] = 'R_path_table'

            print(explanation(156, 34, sector_content, 'root directory entry', 'directory_entry'))

            LBA_of_root_dir = decode(sector_content[158:158+8], 'int_LSB_MSB')
            sector_of_root_dir = LBA_of_root_dir * block_size // sector_size
            print('\t\033[1;31mWill recognize sector 0x{:03x} as {}\033[0m'.format(sector_of_root_dir, 'root dir /'))
            recognized_sector[sector_of_root_dir] = 'dir /'

            print()
            print(explanation(190, 128, sector_content, 'volume set identifier   ', 'strD'))
            print(explanation(318, 128, sector_content, 'publisher identifier    ', 'strA'))
            print(explanation(446, 128, sector_content, 'data preparer identifier', 'strA'))
            print(explanation(574, 128, sector_content, 'application identifier  ', 'strA'))
            print(explanation(702, 37, sector_content, 'copyright file identifier    ', 'strD'))
            print(explanation(739, 37, sector_content, 'abstract file identifier     ', 'strD'))
            print(explanation(776, 37, sector_content, 'bibliographic file identifier', 'strD'))
            print(explanation(813, 17, sector_content, '...', 'dec-datetime'))
            print(explanation(830, 17, sector_content, '...', 'dec-datetime'))
            print(explanation(847, 17, sector_content, '...', 'dec-datetime'))
            print(explanation(864, 17, sector_content, '...', 'dec-datetime'))

            print(explanation(881, 1, sector_content, 'file structure version (always 0x01)', 'int8'))
            print(explanation(882, 1, sector_content, 'unused (always 0x00)', 'int8'))

            print(explanation(883, 512, sector_content, '...', '...'))
            print(explanation(1395, 653, sector_content, 'reserved', '...'))

        elif recognized_sector[sector_id] == 'boot_record':
            print(explanation(0, 1, sector_content, 'type code (0x00 for boot record)', 'int8'))
            print(explanation(1, 5, sector_content, 'standard identifier (always \'CD001\')', 'strA'))
            print(explanation(6, 1, sector_content, 'version (always 0x01)', 'int8'))
            print(explanation(7, 32, sector_content, 'boot system identifier', 'strA'))
            print(explanation(39, 32, sector_content, 'boot identifier', 'strA'))
            print(explanation(71, 4, sector_content, 'LBA of boot catalog if using El Torito', 'int_LSB', double_formats=True))
            print(explanation(75, 1973, sector_content, 'boot system use', '...'))

            LBA_of_boot_catalog = decode(sector_content[71:71+4], 'int_LSB')
            sector_of_boot_catalog = LBA_of_boot_catalog * block_size // sector_size
            print('\t\033[1;31mWill recognize sector 0x{:03x} as {}\033[0m'.format(sector_of_boot_catalog, 'boot_catalog'))
            recognized_sector[sector_of_boot_catalog] = 'boot_catalog'

        elif recognized_sector[sector_id] == 'boot_catalog':
            print('\tValidation entry:')
            print(explanation(0, 1, sector_content, 'header ID (always 0x01)', 'int8'))
            print(explanation(1, 1, sector_content, 'platform', '...', values_description={
                # bytearray([0x00]): '80x86',
                # bytearray([0x01]): 'Power PC',
                # bytearray([0x02]): 'Mac',
            }))
            print(explanation(2, 2, sector_content, 'reserved (all zeroes)', 'int_LSB'))
            print(explanation(4, 24, sector_content, 'manufacturer/developer of CD-ROM', 'strA'))
            print(explanation(28, 2, sector_content, 'checksum', 'int_LSB', double_formats=True))
            print(explanation(30, 1, sector_content, 'key byte (always 0x55)', 'int8', double_formats=True))
            print(explanation(31, 1, sector_content, 'key byte (always 0xAA)', 'int8', double_formats=True))

            print()
            print('\tDefault Entry:')
            print(explanation(32, 1, sector_content, 'boot indicator', '...', values_description={
                # bytearray([0x88]): 'bootable',
                # bytearray([0x00]): 'not bootable',
            }))
            print(explanation(33, 1, sector_content, 'boot media type', '...', values_description={
                # bytearray([0x00]): 'no emulation',
                # bytearray([0x01]): '1.2 meg diskette',
                # bytearray([0x02]): '1.44 meg diskette',
                # bytearray([0x03]): '2.88 meg diskette',
                # bytearray([0x04]): 'hard disk (drive 80)',
            }))
            print(explanation(34, 2, sector_content, 'load segment (zero represents 0x7C0)', 'int_LSB'))
            print(explanation(36, 1, sector_content, 'system type', 'int8'))
            print(explanation(37, 1, sector_content, 'unused (always 0x00)', 'int8'))
            print(explanation(38, 2, sector_content, 'sector count', 'int_LSB'))
            print(explanation(40, 4, sector_content, 'load RBA (start address of virtual disk)', 'int_LSB', double_formats=True))
            print(explanation(44, 20, sector_content, 'unused (all zeroes)', 'int_LSB'))

            LBA_of_load = decode(sector_content[40:40+4], 'int_LSB')
            sector_of_load = LBA_of_load * block_size // sector_size
            print('\t\033[1;31mWill recognize sector 0x{:03x} as {}\033[0m'.format(sector_of_load, 'load'))
            recognized_sector[sector_of_load] = 'load'

        elif recognized_sector[sector_id] == 'L_path_table':
            pos = 0
            while sector_content[pos] != 0x00:
                dir_name_len = decode([sector_content[pos]], 'int8')
                dir_record_len = 1 + 1 + 4 + 2 + (dir_name_len + 1)//2*2
                print(explanation(pos, dir_record_len, sector_content, 'dir record', '...'))
                print('\t'+explanation(pos, 1, sector_content, 'dir name length', 'int8'))
                print('\t'+explanation(pos+1, 1, sector_content, 'extended attribute record length', 'int8'))
                print('\t'+explanation(pos+2, 4, sector_content, 'LBA', 'int_LSB', double_formats=True))
                print('\t'+explanation(pos+6, 2, sector_content, 'parent dir number', 'int_LSB'))
                print('\t'+explanation(pos+8, dir_name_len, sector_content, 'dir name', 'strD'))
                if dir_name_len % 2 == 1:
                    print('\t'+explanation(pos+8+dir_name_len, 1, sector_content, 'zero padding for odd-length dir name', 'int8'))

                dir_name = decode(sector_content[pos+8:pos+8+dir_name_len], 'strD')
                LBA_of_dir = decode(sector_content[pos+2:pos+2+4], 'int_LSB')
                sector_of_dir = LBA_of_dir * block_size // sector_size
                print('\t\t\033[1;31mWill recognize sector 0x{:03x} as {}\033[0m'.format(sector_of_dir, 'dir {}'.format(dir_name)))
                recognized_sector[sector_of_dir] = 'dir {}'.format(dir_name)

                pos += dir_record_len

        elif recognized_sector[sector_id] == 'load':
            to_continue = False
            # print('\tBootstrap Code Area: (reader not implemented yet)')

        elif recognized_sector[sector_id] == '':
            pass

        if to_continue: continue

    # binary search to determine the length of trailing zeros bytes.
    L, R = 1, sector_size  # result (the trailing zeros length) falls in [L,R]
    while L < R:
        mid = (L+R+1) // 2
        if sector_content[-mid:] == bytearray([0x00] * mid):
            L = mid
        else:
            R = mid - 1
    length_of_trailing_zeros_bytes = L  # never equals sector_size (because "all zeros" case has continued)
    print('\nsector 0x{:03x}: unrecognized. trailing bytes [0x{:03x} : 0x{:03x}] are zeros.'.format(sector_id, sector_size-length_of_trailing_zeros_bytes, sector_size-1))

    # 16 bytes per line
    for line_id in range(0, (sector_size - length_of_trailing_zeros_bytes) // 16 + 1):
        print('\tbytes 0x{:02x}_ [{:04d} , {:04d}] : '.format(line_id, line_id*16, line_id*16+15), end='')
        line_content = sector_content[line_id*16 : (line_id+1)*16]

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
                if byte_content >=0x20:
                    print('\033[0;34m{}\033[0m'.format(chr(byte_content)), end='')
                elif byte_content == 0x00:
                    print('\033[0;37m?\033[0m', end='')
                else:
                    print('\033[0;31m?\033[0m', end='')
            print(']', end='')

            print()

        # print('  {}'.format(str(line_content)))

# for i in range(0, 256):
#     print(i, chr(i))

