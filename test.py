

# # iso_file = [bytes(0x02)] * 10
# iso_file = bytearray(10)
# miao = iso_file[5:8]
# print(miao)
# miao[2] = 0x03
# print(miao)
# print(iso_file)
# iso_file[1:4] = bytearray([0x04 , 0x05 , 0x06])
# print(iso_file)
# iso_file[1:4] = b'kfc'
# print(iso_file)
#
# f = open('2022_0819_A.iso', 'wb')
# # for sector_addr in range(0, 16):
# #     for
# # f.write(bytes(0x00))
# # f.seek(16*2048)
# # bytes.
# # f.write(bytes(0x02))
# f.write(iso_file)
# f.close()

# from utils import int_LSB_MSB, display
# # display(int_LSB_MSB(32, 256+9))
# print(int_LSB_MSB(32, 256+9))

# print(b'A' * 20)

# print(bytes('ABC', encoding='ascii'))
from utils import dec_datetime
print(dec_datetime(2022, 8, 20, 15, 50, 00, 12, +8))
