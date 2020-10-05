def ReadFileAsByteArray(filepath):
    with open(filepath, "rb") as f:
        return f.read()


def SaveFileFromByteArray(arr, filepath):
    with open(filepath, "wb") as f:
        f.write(arr)


def ByteArrayToIntArray(byte_arr):
    res = []
    for e in byte_arr:
        res.append(int(e))
    return res


def IntArrayToByteArray(int_arr):
    res = b''
    length = len(int_arr)
    # for i in range(length):
    #     print(bytes(int_arr[i]))
    print(length)
    return res
