
# from Audio import Audio
# # ar = [0,1,0,1,0,1,0,1]

# # ar = 255
# # print(format(ar, "08b"))

# # print(type(format(ar, "08b")))

# # print(ar)

# # ar = int(format(ar, "08b")[:-1] + "1", 2)

# # from PIL import Image
# # import numpy as np

# # im = Image.open('./tes.jpg')

# # ar = np.array(im)


# # # print(ar)
# # print(ar[0][0][0])
# # # print(format(ar[0][0][0], "08b")[:-1])
# # ar[0][0][0] = int(format(ar[0][0][0], "08b")[:-1] + )
# # print(ar.shape)

# file1 = Audio('./wav/tes1.wav')
# file2 = Audio('./stegowav/out2.wav')

# print(file1.array[:10])
# print(file2.array[:10])

from oct2py import Oct2Py
oc = Oct2Py()


script = "function y = myScript(x)\n" \
         "    y = x-5" \
         "end"

with open("myScript.m","w+") as f:
    f.write(script)

oc.myScript(7)