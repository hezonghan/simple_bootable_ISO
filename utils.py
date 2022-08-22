

sector_size = 2048  # number of "bytes" per "sector"

constants = {
    'iso9660_volume_descriptor_type': {
        'boot_record': 0x00,
        'primary_volume_descriptor': 0x01,
        'supplementary_volume_descriptor': 0x02,
        'volume_partition_descriptor': 0x03,
        'volume_descriptor_set_terminator': 0xff,
    },
    'iso9660_volume_descriptor_identifier': b'CD001',
    'iso9660_volume_descriptor_version': 0x01,

    'iso9660_boot_record_boot_system_identifier': {
        'el_torito': b'EL TORITO SPECIFICATION' + bytearray([0x00] * 9),
    },

    'iso9660_primary_volume_descriptor_file_structure_version': 0x01,

    'el_torito_boot_record_boot_identifier': bytearray([0x00] * 32),

    'el_torito_validation_entry_header_ID': 0x01,
    'el_torito_validation_entry_platform_ID': {
        '80x86': 0x00,
        'Power_PC': 0x01,
        'Mac': 0x02,
    },
    'el_torito_validation_entry_key_bytes': bytearray([0x55, 0xAA]),

    'el_torito_default_entry_boot_indicator': {
        'bootable': 0x88,
        'not_bootable': 0x00,
    },
    'el_torito_default_entry_boot_media_type': {
        'no emulation': 0x00,
        '1.2 meg diskette': 0x01,
        '1.44 meg diskette': 0x02,
        '2.88 meg diskette': 0x03,
        'hard disk (drive 80)': 0x04,
    }
}

# ==============================================================
# number -> binary


def get_group(bits, v):  # split the value {v} into bytes, so the resulting binary has length {bits}.
    if bits % 8 != 0:
        raise Exception('bits={} is not multiple of 8'.format(bits))
    group = []
    for group_id in range(0, bits // 8):
        group.append(v % 256)
        v //= 256
    return group


def int_LSB_MSB(bits, v):  # Little-endian followed by big-endian encoded unsigned 32-bit integer.
    group = get_group(bits, v)
    return bytearray(group + group[::-1])


def int_LSB(bits, v):
    group = get_group(bits, v)
    return bytearray(group)


# ==============================================================
# binary -> number


def decode(arr, data_type, values_description=None, double_formats=False):
    if data_type == 'key_value':
        return values_description[arr]

    if data_type == 'strA' or data_type == 'strD':
        # return bytes(arr)
        ans = ''
        for b in arr:
            ans += chr(b)
        return '"'+ans+'"'

    if data_type == 'int8':
        return int(arr[0])

    if data_type == 'directory_entry':
        return '(not_supported_yet)'  # TODO

    if data_type == 'dec-datetime':
        return '(not_supported_yet)'  # TODO

    if data_type == '...':
        return '...'

    if data_type == 'int_LSB':
        arr = arr[::-1]
    elif data_type == 'int_LSB_MSB':
        arr = arr[len(arr)//2:]
    v = 0
    for b in arr:
        v *= 256
        v += b
    if double_formats:
        return '{:03d} = 0x{:03x}'.format(v, v)
    else:
        return v


def display(arr):
    for b in arr:
        print('{} '.format(b))


def bytes_str(arr):
    ans = ''
    for b in arr:
        ans += '  0x{:02x}'.format(b)
    return ans


def explanation(offset, length, source, field_name, data_type, values_description=None, double_formats=False):
    if length == 1:
        return '\tbyte 0x{:03x} or {:03d} : \033[0;37m{} = {}  \033[1;34m0x{:02x}\033[0m'.format(
            offset, offset,
            field_name, decode([source[offset]], data_type, values_description, double_formats),
            source[offset],
        )
    else:
        return '\tbytes [0x{:03x}:0x{:03x}] or [{:03d}:{:03d}] : \033[0;37m{} = {}\033[1;34m{}\033[0m'.format(
            offset, offset+length-1, offset, offset+length-1,
            field_name, decode(source[offset:offset+length], data_type, values_description, double_formats),
            bytes_str(source[offset:offset+length]),
        )


# ==============================================================


def dec_datetime(year, month, day, hour, minute, second, hundredths_of_second, time_zone_hour=+8):
    zone_offset = (time_zone_hour + 12) * 4
    return bytes('{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(year, month, day, hour, minute, second, hundredths_of_second), encoding='ascii') + bytearray([zone_offset])
