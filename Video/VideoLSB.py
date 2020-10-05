import cv2
import math
from Video.FrameLSB import ConstructBitsArray, FrameLSB, FrameUnLSB
from Video.FrameExtractor import FrameExtractor
import Video.utils as utils
import os
import glob


class VideoLSB():
    def __init__(self, video_input, data_to_hide, video_output, mode):
        self.video_input = video_input
        self.data_to_hide = utils.RawStringToBits(data_to_hide)
        self.video_output = video_output
        self.mode = mode
        self.get_max_data()

    def get_max_data(self):
        vcap = cv2.VideoCapture(self.video_input)
        if vcap.isOpened():
            width = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frames = int(vcap.get(cv2.CAP_PROP_FRAME_COUNT))
            print(f"{width}x{height} {frames} frames.")
            total_data = math.floor((width * height * 3 * (frames - 1)) / 8)
            data_per_frame = math.floor((width * height * 3) / 8)
            print("Total data that can fit : {} bytes, {} bytes on each frames".format(
                total_data, data_per_frame))
            self._total_data_per_frame = data_per_frame
            self._total_data_max = total_data
            self._total_frames = frames
            self._width = width
            self._height = height

    def save_metadata(self, data_length_in_bits: int, mode: list, filename: str, ext: str):
        metadata = []
        metadata.extend(utils.IntToBits(data_length_in_bits))
        metadata.extend(mode)
        metadata.extend(utils.ConstructVideoMetadata(filename, ext))
        first_frame = FrameLSB("temp/0.png", metadata, "temp/0.png")
        first_frame.hide()
        print("Saved metadata to frame 0")

    def split_data(self):
        # total frames required
        total_required_frames = math.ceil(
            len(self.data_to_hide) / self._total_data_per_frame)
        # asumsi ascii non-null string
        packets = []
        for i in range(0, len(self.data_to_hide), self._total_data_per_frame):
            if i + self._total_data_per_frame > len(self.data_to_hide):
                print(self.data_to_hide[i:])
                packets.append(ConstructBitsArray(
                    self.data_to_hide[i:], [0, 0]))
            else:
                packets.append(ConstructBitsArray(
                    self.data_to_hide[i:i+self._total_data_per_frame], [0, 0]))
        return packets

    def stego_data(self, filename, ext,  mode: list,  seed=0):
        max_other_frames = self._total_data_per_frame - 34
        total_needed_frames = math.ceil(
            (len(self.data_to_hide) / max_other_frames))
        self.save_metadata(total_needed_frames, mode, filename, ext)
        # case only one frame
        frames = []
        for i in range(0, len(self.data_to_hide), max_other_frames):
            frames.append(self.data_to_hide[i:i+max_other_frames])
        if mode[0] == 1:
            # is random

            frame_seq = utils.GenerateIntegerSequenceFromSeed(
                (self._total_frames, 1), total_needed_frames, seed, 1)
            frame_idx = 1
            for frame in frame_seq:
                path = os.path.join(os.getcwd(), "temp",
                                    "{:d}.png".format(frame))
                target = os.path.join(os.getcwd(), "temp",
                                      "{:d}.png".format(frame))
                data_to_hide = []
                data_to_hide.extend(utils.IntToBits(len(frames[frame_idx-1])))
                data_to_hide.extend(mode)
                data_to_hide.extend(frames[frame_idx-1])
                print("Dataframe len:", len(data_to_hide))
                # print(utils.IntToBits(total_needed_frames))
                f = FrameLSB(path, data_to_hide, target)
                if mode[1] == 1:
                    f.hide_random(seed)
                else:
                    f.hide()
                frame_idx += 1
                print("Data hidden at frame ", frame)
        else:
            total_needed_frames = math.ceil(
                (len(self.data_to_hide) / max_other_frames))
            for frame in range(1, total_needed_frames+1):
                path = os.path.join(os.getcwd(), "temp",
                                    "{:d}.png".format(frame))
                target = os.path.join(os.getcwd(), "temp",
                                      "{:d}.png".format(frame))
                data_to_hide = []
                data_to_hide.extend(utils.IntToBits(len(frames[frame-1])))
                data_to_hide.extend(mode)
                data_to_hide.extend(frames[frame-1])
                f = FrameLSB(path, data_to_hide, target)
                if mode[1] == 1:
                    f.hide_random(seed)
                else:
                    f.hide()
                print("Data hidden at frame ", frame)

    def makeVideo(self, filename):
        print("Creating video")
        fourcc = cv2.VideoWriter_fourcc('R', 'G', 'B', 'A')
        out = cv2.VideoWriter(filename, fourcc, 30,
                              (self._width, self._height))

        for i in range(0, self._total_frames):
            img = cv2.imread('temp/{:d}.png'.format(i))
            out.write(img)

        out.release()
        print("Finished creating video")


class VideoUnLSB():
    def __init__(self, path):
        self.video_input = path
        self.get_max_data()

    def get_max_data(self):
        vcap = cv2.VideoCapture(self.video_input)
        if vcap.isOpened():
            width = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            frames = int(vcap.get(cv2.CAP_PROP_FRAME_COUNT))
            print(f"{width}x{height} {frames} frames.")
            total_data = math.floor((width * height * 3 * frames) / 8)
            data_per_frame = math.floor((width * height * 3) / 8)
            print("Total data that can fit : {} bytes, {} bytes on each frames".format(
                total_data, data_per_frame))
            self._total_data_per_frame = data_per_frame
            self._total_data_max = total_data
            self._total_frames = frames

    def get_stego_metadata(self):
        extract = FrameExtractor(self.video_input, 'temp')
        extract.extract_single()
        path = os.path.join(os.getcwd(), "temp",
                            "0.png")
        first_frame = FrameUnLSB(path, "aaaa.png")
        metadata = first_frame.unhide_metadata(330)
        frame_count = int(utils.BitsToInt(metadata[:32]))
        mode_bit = metadata[32:34]
        filename = utils.BitsToString(metadata[34:34+(32*8)])
        ext = utils.BitsToString(metadata[34+(32*8):34+(37*8)])
        print(frame_count)
        print(mode_bit)
        print(filename)
        print(ext)
        # os.remove(path)
        return frame_count, mode_bit, filename, ext

    def unstego_data(self, frame_count, mode, seed=0):
        data = []
        max_other_frames = self._total_data_per_frame - 34
        total_needed_frames = frame_count
        if mode[0] == 1:
            # random frame seq
            frame_seq = utils.GenerateIntegerSequenceFromSeed(
                (self._total_frames, 1), total_needed_frames, seed, 1)
            frame_idx = 1
            for frame in frame_seq:
                print("Checking frame", frame)
                path = os.path.join(os.getcwd(), "temp",
                                    "{:d}.png".format(frame))
                target = os.path.join(os.getcwd(), "temp",
                                      "{:d}.png".format(frame))
                f = FrameUnLSB(path, target)
                if mode[1] == 1:
                    bits = f.unhide_data_random(34, seed)
                    data.extend(bits)
                else:
                    print("Sequential pixel")
                    bits = f.unhide_data(34)
                    data.extend(bits)
                frame_idx += 1
                print("Data uncovered at frame ", frame)
        else:
            frame_seq = range(1, total_needed_frames+1)
            frame_idx = 1
            for frame in frame_seq:
                print("Checking frame", frame)
                path = os.path.join(os.getcwd(), "temp",
                                    "{:d}.png".format(frame))
                target = os.path.join(os.getcwd(), "temp",
                                      "{:d}.png".format(frame))
                f = FrameUnLSB(path, target)
                if mode[1] == 1:
                    bits = f.unhide_data_random(34, seed)
                    data.extend(bits)
                else:
                    print("Sequential pixel")
                    bits = f.unhide_data(34)
                    data.extend(bits)
                frame_idx += 1
                print("Data uncovered at frame ", frame)
        return data
