# StegoAWOO

Steganography on AVI With Object-Oriented Python

## Data Structure

In order to store information about the length of data to be read from the image,
several information needs to be stored.

Those are :

- UInt_64 that will need to reserve the first 64 bit. This size is choosen as
  it could cater image file with the size of 2,4GPx squared, which is already too damn big.
  It also only take the first 64 bit of the frame, which about the first 30 pixels. Assumptions were made
  that the video is at least 100x100 pixel wide. That's the software limitation
- Reading Mode : 11 | 12 | 21 | 22
- Random seed in UInt_32. A pretty big value. Nothing should go wrong.

# Data Structure

Data were structured as shown below for the first frame:

1. 32 bit : Length of actual data in this frame
2. 2 bit : Storing mode
3. 296 bit : Video Metadata : 32 byte null-padded string for title unless full 32 bit string.
   5 byte null-padded string for extension
4. Data
   This makes the first frame have 330 bits of metadata
   For next frames, video metadata field is omitted, so the total metadata is 34 bits

# Usage

Before starting, make sure to install all the library requirements which can be seen on
requirements.txt of the root folder.
Make sure

- Python3 is installed
- pip3 is installed

You can go with :

> pip3 install -r requirements.txt

or if on windows

> pip install -r requirements.txt

## Storing

1. Choose mode to "Store"
2. Select your desired storing mode.
3. Put in key if you picked storing mode that has random in it.
   This will be used to calculate the seed. Defaults to 0 for empty field.
4. If you're using encryption, then it's mandatory to put keys.
5. Select the input file. Must be video.
6. Select the file to store. Can be any file. Will display error later if file is too big.
7. Set the destination file and extension. Make sure to put ".avi" as extension. This is a must.
8. Press "Process" button.
9. If nothing goes wrong, output video will be made.
10. Click on "Calculate PSNR" to show the PSNR value from both video.
11. You can check the output video by clicking "Open Output" button

## Retrieval

1. Choose mode to "Retrieve"
2. If you're using encryption, then it's mandatory to put keys.
3. Select the input file. Must be video.
4. Set the destination file and extension. Can be any file and any extension.
5. To check the metadata, click "Get Metadata" button to show stored metadata.
6. If the metadata shown seems legit, then there is data stored. If not, then you should stop here.
7. Click "Process" button to extract the data.
8. If nothing goes wrong, output file will be made.
9. You can check the output file by clicking "Open Output" button

# About

StegAWOO is made by Arung Agamani Budi Putera - 13518005, as a task assignment fulfilment for IF4020 Cryptography course.
