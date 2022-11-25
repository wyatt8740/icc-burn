#! /usr/bin/env python3
import argparse
from argparse import RawTextHelpFormatter
from io import BytesIO # for BytesIO on embedded profiles
from PIL import Image, ImageCms

intent=ImageCms.Intent.SATURATION

parser=argparse.ArgumentParser(description='Burns ICC profiles into images.', formatter_class=RawTextHelpFormatter)
parser.add_argument('--icc_in', dest='icc_in', type=str, nargs=1, default=None,
                    help='ICC file to apply to the input. If none given, sRGB is\n\
automatically assumed unless there is an embedded profile.')
parser.add_argument('--intent', dest='intent', type=int, nargs=1, default=None,
                    help='Which rendering intent to use for correction. Options are:\n\
0 (Perceptual) (default)\n\
1 (Relative Colorimetric)\n\
2 (Saturation)\n\
3 (Absolute Colorimetric)')
parser.add_argument('icc_out', metavar='icc_out', type=str, nargs=1,
                    help='ICC file to apply to the output.')
parser.add_argument('input_file', metavar='infile', type=str, nargs=1,
                    help='The file that needs an ICC profile burned into it.')
parser.add_argument('output_file', metavar='outfile', type=str, nargs=1,
                    help='Where to place the picture with the burned-in profile.')
parser.add_argument('--reverse', dest='reverse', action='store_true', default=False, help='Try to reverse the applied correction instead (inverse).')

args=parser.parse_args()
reverse=args.reverse
icc_in=args.icc_in
if args.icc_in is not None:
    icc_in=args.icc_in[0]

icc_out=args.icc_out[0]
input_file=args.input_file[0]
output_file=args.output_file[0]

input_file=Image.open(input_file)
if input_file is None:
    print("E: Could not open input image.")
    exit(1)

# convert to RGB (convert() will just copy the image if it is already RGB).
if 'A' in input_file.mode:
    input_file=input_file.convert('RGBA')
else:
    input_file=input_file.convert('RGB')

# default to srgb
if icc_in is None:
    if input_file.info.get('icc_profile') is not None:
        icc_in=BytesIO(input_file.info.get('icc_profile')) # hope that binary thing counts
    else:
        icc_in=ImageCms.createProfile("sRGB", -1)

if args.intent is not None:
    intent=args.intent[0]

xform=None
if reverse:
    print("Reverse mode.")
    xform=ImageCms.buildTransform(icc_out, icc_in,
                              input_file.mode, input_file.mode,
                              intent, 0)
#                              ImageCms.Intent.PERCEPTUAL, 0)
else:
    xform=ImageCms.buildTransform(icc_in, icc_out,
                              input_file.mode, input_file.mode,
                              intent, 0)
#                              ImageCms.Intent.PERCEPTUAL, 0)


img2=ImageCms.applyTransform(input_file, xform, inPlace=False)
img2.save(output_file)
