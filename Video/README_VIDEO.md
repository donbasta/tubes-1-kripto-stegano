# Stego-AVI

## TODO LIST

- Pake LSB (Yokatta...)
- Input : file AVI, file pesan, kunci-stego
- Encrypted/Decrypted sebelum disisipkan
- Frame: Sequential / Random.
  -- Foreach Frame : Sisipkan secara sekuensial/acak
- Ekstraksi : Determine mode without additional info (Selipkan di awal)
- Video player (oh god)
- Show resulting video size + PSNR mean value

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

# DATA STRUCTURE

Data were structured as shown below for the first frame:

1. 32 bit : Length of actual data in this frame
2. 2 bit : Storing mode
3. 296 bit : Video Metadata : 32 byte null-padded string for title unless full 32 bit string.
   5 byte null-padded string for extension
4. Data
   This makes the first frame have 330 bits of metadata
   For next frames, video metadata field is omitted, so the total metadata is 34 bits

# Flow

1. Input video file. Specify the mode, with seed number, and target video file name
2. Split into frames. make it PNG
3. Calculate maximum data for each frame.
4. Split payload so each payloads + metadata fits the maximum data.
5.
