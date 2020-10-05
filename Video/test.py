from FrameExtractor import FrameExtractor

# vid = FrameExtractor("./awoo.mp4", "temp")
# vid.load()
# vid.extract()
# from FrameLSB import FrameLSB
# f = FrameLSB('0.png', "001110101000101010", 'hidden.png')
# f.hide()

# from FrameLSB import ConstructBitsArray, FrameLSB, FrameUnLSB, BitsToInt, BitsToString
# from VideoLSB import VideoLSB, VideoUnLSB
import utils
# from constants import Mode
import sys
import FileReader as fr
from vigenere import Vigenere

# extractor = FrameExtractor(
#     "awoo.mp4", "temp")
# extractor.load()
# extractor.extract()

raw_data = fr.ByteArrayToIntArray(fr.ReadFileAsByteArray("test_file.txt"))
vig = Vigenere()
vig.input_key("awoo")
vig.set_auto(False)
vig.set_full(False)
vig.set_extended(True)
encrypted = vig.encrypt(''.join([chr(i) for i in raw_data]))
encrypted = bytes(encrypted)
print("BYTE ARRAY : ", encrypted)

vig2 = Vigenere()
vig2.input_key("awoo")
vig2.set_auto(False)
vig2.set_full(False)
vig2.set_extended(True)
decrypted = vig.decrypt(''.join([chr(i) for i in encrypted]))
print(bytes(decrypted))
# vid = VideoLSB("awoo.mp4", raw_data,
#                "hidden-awoo.avi", [0, 0])
# vid.stego_data("test_file", "txt", [0, 1])
# vid.makeVideo("hidden.avi")

# hiddenVid = VideoUnLSB("awoo.mp4")
# framecount, mode_bit, filename, ext = hiddenVid.get_stego_metadata()
# raw_data = hiddenVid.unstego_data(framecount, mode_bit)
# result = utils.BitsToRawString(raw_data)
# fr.SaveFileFromByteArray(result, "uncover.png")

# bitfield = ConstructBitsArray("Aku suka dia banget", Mode.seq_rand)
# src = FrameLSB("0.png", bitfield, "hidden.png")
# src.hide_random(69420)

# dest = FrameUnLSB("hidden.png", "other.png")
# dest_data_len = BitsToInt(dest.unhide_metadata_rand(32, 69420))
# print("Data length: ", dest_data_len)
# output_rand = dest.unhide_data_random(dest_data_len, 34, 69420)
# print(BitsToString(output_rand))
# output_data = dest.unhide_data(dest_data_len, 32)
# print(BitsToString(output_data))
# vid = VideoLSB("awoo.mp4", "Aku suka kamu", "awoo_hidden.mp4", "11")
# bitfield = ConstructBitsArray("Aku suka kamu")
# vid.get_max_data()
# packets = vid.split_data()
# print(packets[0])
# print(bitfield)
