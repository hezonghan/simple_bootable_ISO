
# iso9660 + EL Torito

from utils import sector_size, constants, int_LSB_MSB, int_LSB, display, dec_datetime


block_size = sector_size
block_address_of_el_torito_boot_catalog = 0x20
block_address_of_boot_image, sectors_cnt_of_boot_image = 0x30, 0x05
sector_address_of_partition_1, sectors_cnt_of_partition_1 = 0x40, 0x05

iso_file = bytearray(0x50 * sector_size)  # 256 * 2KB = 512KB


# ==============================================================
# VOLUME DESCRIPTORS


# _____________________________
# the primary volume descriptor
pos = 0x10 * sector_size
iso_file[pos+0] = constants['iso9660_volume_descriptor_type']['primary_volume_descriptor']
iso_file[pos+1 : pos+1+5] = constants['iso9660_volume_descriptor_identifier']
iso_file[pos+6] = constants['iso9660_volume_descriptor_version']
iso_file[pos+7] = 0x00

iso_file[pos+8 : pos+8+32] = b'<<<<====HZH-BOOTABLE--V1====>>>>'  # the name of the system that can act upon sectors 0x00-0x0f of the volume
iso_file[pos+40 : pos+40+32] = b'=======THE-PRIMARY-VOLUME======='
# iso_file[pos+72 : pos+72+8] = # all zeros

iso_file[pos+190 : pos+190+128] = (b'_' * 54) + b'THE_FIRST_VOLUME_SET' + (b'_' * 54)
iso_file[pos+318 : pos+318+128] = bytearray([0x20] * 128)
iso_file[pos+446 : pos+446+128] = bytearray([0x20] * 128)
iso_file[pos+574 : pos+574+128] = bytearray([0x20] * 128)
iso_file[pos+702 : pos+702+37] = bytearray([0x20] * 37)
iso_file[pos+739 : pos+739+37] = bytearray([0x20] * 37)
iso_file[pos+776 : pos+776+37] = bytearray([0x20] * 37)

# iso_file[pos+80 : pos+80+8] = int_LSB_MSB(32, )  # TODO  volume space size: number of logical blocks
# iso_file[pos+88 : pos+88+32] = # all zeros
iso_file[pos+120 : pos+120+4] = int_LSB_MSB(16, 1)  # TODO  volume set size: number of "disks"
iso_file[pos+124 : pos+124+4] = int_LSB_MSB(16, 0)  # TODO  the number of this disk in the volume set
iso_file[pos+128 : pos+128+4] = int_LSB_MSB(16, block_size)  # TODO  number of "bytes" per "logical block"

# iso_file[pos+132 : pos+132+8] = int_LSB_MSB(32, )  # TODO  the size (in bytes) of the path table
# iso_file[pos+140 : pos+140+4] = int_LSB(32, )  # TODO  the LBA of the L-path table.
# iso_file[pos+144 : pos+144+4] = int_LSB(32, )  # TODO  the LBA of the optional L-path table.
# iso_file[pos+148 : pos+148+4] = int_LSB(32, )  # TODO  the LBA of the M-path table.
# iso_file[pos+152 : pos+152+4] = int_LSB(32, )  # TODO  the LBA of the optional M-path table.

# iso_file[pos+156 : pos+156+34] = # root directory identifier is zero (of 34 bytes).

iso_file[pos+813 : pos+813+17] = dec_datetime(2022, 8, 20, 15, 50, 0, 0)
iso_file[pos+830 : pos+830+17] = dec_datetime(2022, 8, 20, 15, 53, 0, 0)
iso_file[pos+847 : pos+847+17] = dec_datetime(2023, 8, 20, 15, 53, 0, 0)
iso_file[pos+864 : pos+864+17] = dec_datetime(2024, 8, 20, 15, 53, 0, 0)

iso_file[pos+881] = constants['iso9660_primary_volume_descriptor_file_structure_version']
iso_file[pos+882] = 0x00


# _____________________________
# the boot record
pos = 0x11 * sector_size
iso_file[pos+0] = constants['iso9660_volume_descriptor_type']['boot_record']
iso_file[pos+1 : pos+1+5] = constants['iso9660_volume_descriptor_identifier']
iso_file[pos+6] = constants['iso9660_volume_descriptor_version']
iso_file[pos+7 : pos+7+32] = constants['iso9660_boot_record_boot_system_identifier']['el_torito']  # TODO
iso_file[pos+39 : pos+39+32] = constants['el_torito_boot_record_boot_identifier']
iso_file[pos+71 : pos+71+4] = int_LSB(32, block_address_of_el_torito_boot_catalog)  # TODO  # FIXME  is int32_LSB ??


# _____________________________
# the volume descriptor set terminator
pos = 0x12 * sector_size
iso_file[pos+0] = constants['iso9660_volume_descriptor_type']['volume_descriptor_set_terminator']
iso_file[pos+1 : pos+1+5] = constants['iso9660_volume_descriptor_identifier']
iso_file[pos+6] = constants['iso9660_volume_descriptor_version']


# ==============================================================
# BOOT CATALOG


# _____________________________
# the boot catalog: validation entry
pos = block_address_of_el_torito_boot_catalog * block_size  # TODO
iso_file[pos+0] = constants['el_torito_validation_entry_header_ID']
iso_file[pos+1] = constants['el_torito_validation_entry_platform_ID']['80x86']
iso_file[pos+2 : pos+2+2] = bytearray([0x00, 0x00])
# iso_file[pos+4 : pos+4+24] = b''  # TODO
iso_file[pos+28 : pos+28+2] = bytearray([0xaa, 0x55])  # TODO  checksum (currently fixed "0xaa55", todo implement checksum calculation)
iso_file[pos+30 : pos+30+2] = constants['el_torito_validation_entry_key_bytes']

# Note: if not set the "checksum of validation entry of boot catalog of EL TORITO",
#   the VirtualBox 6.0.4 does not care, but
#   the VMware Workstation 16.1.0 skips the CD-ROM booting and goes directly to network booting (printing something like "Network boot from AMD ...").
# This is verified by experiment comparing two ISO with the only difference at these 2-byte checksum!


# _____________________________
# the boot catalog: default entry
pos = block_address_of_el_torito_boot_catalog * block_size + 0x20  # TODO
iso_file[pos+0] = constants['el_torito_default_entry_boot_indicator']['bootable']
iso_file[pos+1] = constants['el_torito_default_entry_boot_media_type']['no emulation']
# iso_file[pos+2 : pos+2+2] = bytearray([0x00, 0x00])  # load segment. zeros for traditional segment 0x07c0
# iso_file[pos+4] = # TODO  system type
iso_file[pos+5] = 0x00
iso_file[pos+6 : pos+6+2] = int_LSB(16, sectors_cnt_of_boot_image)  # TODO  number of virtual/emulated sectors the system will store at Load Segment during the initial boot procedure
iso_file[pos+8 : pos+8+4] = int_LSB(32, block_address_of_boot_image)  # TODO  Load RBA


# ==============================================================
# BOOTABLE DISK IMAGE


# _____________________________
# bootstrap code area
pos = block_address_of_boot_image * block_size

# iso_file[pos+0 : pos+4] = bytearray([0x11, 0x22, 0x33, 0x44])

# iso_file[pos+0 : pos+2] = bytearray([0x0d, 0x0a])
# iso_file[pos+2 : pos+2+11] = b'HELLO_WORLD'
# iso_file[pos+13] = 0x00


iso_file[pos+0 : pos+0+17] = bytearray([0xb8, 0x00, 0xb8] + [0x8e, 0xc0] + [0x26, 0xc6, 0x06, 0x00, 0x00, 0x48] + [0x26, 0xc6, 0x06, 0x01, 0x00, 0x07])
# Note: These are machine codes generated by NASM, from the following 4 lines of asm:
#   mov AX, 0xB800  ; 0xB800 is the base of text video memory
#   mov ES, AX
#   mov byte [ES:0x0000], 'H'
#   mov byte [ES:0x0001], 0x07  ; white font + black background

# _____________________________
# partition table entry 1
pos = block_address_of_boot_image * block_size + 446
iso_file[pos] = 0x80  # status
iso_file[pos+4] = 0x0C  # partition type, 0x0C = FAT32 (LBA)
iso_file[pos+8 : pos+8+4] = int_LSB(32, sector_address_of_partition_1)  # LBA of first absolute sector in the partition
iso_file[pos+12 : pos+12+4] = int_LSB(32, sectors_cnt_of_partition_1)  # number of sectors in the partition

# _____________________________
# boot signature
pos = block_address_of_boot_image * block_size
iso_file[pos+510] = 0x55
iso_file[pos+511] = 0xaa



f = open('2022_0821_A.iso', 'wb')
f.write(iso_file)
f.close()

# Finally, create new virtual machine in VMWare Workstation, and load this ".iso" file.
