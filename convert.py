#!/usr/bin/env python3
from PIL import Image
import struct
import argparse

presets = {
    'ip286': (236, 82),
    'ip284': (132, 64),
    't28': (236, 82),
    't80': (132, 64),
    't10t': (132, 64),
    't12': (132, 64),
    't26': (132, 64),
    't22': (132, 64),
}

parser = argparse.ArgumentParser(description="Convert images to .dob files for Tiptel and Yealink phones")
parser.add_argument('-r', '--reverse', action='store_true', default=False, help="Convert .dob back to .png")
parser.add_argument('-p', '--preset', action='store', default=None, help="Output format preset", choices=presets.keys())
parser.add_argument('input', type=argparse.FileType('rb'), help="Input filename")
parser.add_argument('output', type=argparse.FileType('wb'), help="Output filename")
args = parser.parse_args()


def dob_to_png(args):
    dob = args.input.read()
    size = struct.unpack('BB', dob[0:2])
    print("Image size: {}x{}".format(size[0], size[1]))

    canvas = Image.new('RGB', size, (255, 255, 255))

    nibbles = []

    for byte in struct.iter_unpack('B', dob[2:]):
        nibble1 = byte[0] >> 4
        nibble2 = byte[0] & 0x0F
        nibbles.append(nibble2)
        nibbles.append(nibble1)

    for x in range(0, size[0]):
        for y in range(0, size[1]):
            address = x + y*size[0]
            value = 255 - (int)(nibbles[address] / 16.0 * 256.0)
            canvas.putpixel((x, y), (value, value, value))
    canvas.save(args.output, format="PNG")


def img_to_dob(args):
    canvas = Image.open(args.input)
    if args.preset is not None:
        preset = presets[args.preset]
        canvas.thumbnail(preset, Image.LANCZOS)
    canvas = canvas.convert(mode="L")
    canvas.show()
    args.output.write(struct.pack("BB", canvas.size[0], canvas.size[1]))
    pixels = []

    for y in range(0, canvas.size[1]):
        for x in range(0, canvas.size[0]):
            pixel = 15-(int)(canvas.getpixel((x, y)) / 256.0 * 16.0)
            pixels.append(pixel)

    outputbytes = []
    for i in range(0, len(pixels), 2):
        byte = pixels[i+1] * 16 + pixels[i]
        outputbytes.append(byte)
    args.output.write(bytes(outputbytes))
    args.output.close()


if args.reverse:
    dob_to_png(args)
else:
    img_to_dob(args)