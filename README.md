# icc-burn

This permanently **(and irreversibly)** bakes an ICC profile's color
corrections into an image. Nice for brute forcing color management onto
wallpapers, in software without color management, and so forth. Just don't
use the images on any other screens, ever, or try to view them in any properly
color managed programs. :)

Using images that have had ICC corrections baked in with color managed software
will get the same corrections applied a second time and therefore look wrong.
The only real use-case for this is viewing images in non-managed software
(setting desktop wallpapers is a great example of where this is harmless,
except that your screenshots will look wrong on other screens).

Written as a proof of concept for possibly adding color management to MComix.
Doesn't seem like it'll be that hard after all!

## Dependencies

* Python 3
* Pillow (Don't use PIL; it's been dead for a decade).

## Notes

The ICC files here are ones I made for my own personal use. They are included
for testing purposes, but if you want to try them on your screens you can go
ahead. I just won't promise any good results :)

The Dell U2412M one will have minimal visible changes on an sRGB monitor,
since my U2412M is very close to covering 100% of sRGB.

The ThinkPad X201 Tablet profile, on the other hand, will drastically boost
some colours; its screen covers about 51% of sRGB, if I recall correctly,
and therefore if you just want to see that it works you should probably
try that profile for pretty obvious results.

Right now, the program is hardcoded to always use a 'perceptual' rendering
intent. Since this is just a proof-of-concept, I don't mind, but adding
support for the other intents should be pretty trivial if you look at the
Pillow `ImageCms` documentation.

The first test image is from Wikimedia Commons, and has an embedded Adobe
RGB profile. It is used to test behavior when dealing with wide gamut images,
as well as to verify that embedded profiles can be used.

The other image is a wallpaper I use, which is based on a screenshot that I
essentially redrew in GIMP to clean up chroma subsampling artifacts. This image
represents a typical sRGB input profile picture with easy-to-see color changes
(large, flat surfaces).
