#! /usr/bin/env python3
import argparse
from io import BytesIO # for BytesIO on embedded profiles
from PIL import Image, ImageCms

# .cube LUT support
from pillow_lut import load_cube_file

parser=argparse.ArgumentParser(description='Burns ICC profiles into images.')
parser.add_argument('--icc_in', dest='icc_in', type=str, nargs=1, default=None,
                    help='ICC file to apply to the input. If none given, sRGB is automatically assumed (unless there is an embedded profile).')
parser.add_argument('cube_out', metavar='cube_out', type=str, nargs=1,
                    help='cube file to apply to the output.')
parser.add_argument('input_file', metavar='infile', type=str, nargs=1,
                    help='The file that needs an ICC profile burned into it.')
parser.add_argument('output_file', metavar='outfile', type=str, nargs=1,
                    help='Where to place the picture with the burned-in profile.')

args=parser.parse_args()
icc_in=args.icc_in
if args.icc_in is not None:
    icc_in=args.icc_in[0]

cube_out=args.cube_out[0]
cubelut=None
if cube_out is not None:
    cubelut=load_cube_file(cube_out)

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

srgb_default_profile=ImageCms.createProfile("sRGB", -1)
        
xform=ImageCms.buildTransform(icc_in, srgb_default_profile,
                              input_file.mode, input_file.mode,
                              ImageCms.INTENT_PERCEPTUAL, 0)

img2=ImageCms.applyTransform(input_file, xform, inPlace=False).filter(cubelut)
img2.save(output_file)
