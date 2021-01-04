import os
import cairo
import pickle
import string
import numpy as np
import matplotlib.pyplot as plt
from enum import IntEnum
from matplotlib import font_manager
from svg.path import parse_path
from svg.path.path import Line, CubicBezier, Move, Close
from xml.dom import minidom
from io import BytesIO
from utils import draw_bezier

STYLE = {
    cairo.FONT_SLANT_NORMAL: {
        cairo.FONT_WEIGHT_NORMAL: "n",
        cairo.FONT_WEIGHT_BOLD: "b"
    },
    cairo.FONT_SLANT_ITALIC: {
        cairo.FONT_WEIGHT_NORMAL: "i",
        cairo.FONT_WEIGHT_BOLD: "ib"
    }
}


def draw_glyph(char, font_face, slant, weight):
    memory = BytesIO()
    with cairo.SVGSurface(memory, 60, 80) as surface:
        context = cairo.Context(surface)

        context.set_source_rgb(0, 0, 0)
        context.set_line_width(1)
        context.select_font_face(font_face, slant, weight)
        context.set_font_size(50)

        ret = context.text_extents(char)
        context.move_to(10, ret.height + 10)
        context.text_path(char)
        context.stroke()
    memory.seek(0)
    return memory


def main(args):

    for font_file in font_manager.findSystemFonts([os.path.expanduser(args.fontdir)]):
        font = font_manager.FontProperties()
        font.set_file(font_file)
        font_name = font.get_name()
        font_face = font_name.replace(' ', '_').lower()

        for slant in [cairo.FONT_SLANT_NORMAL, cairo.FONT_SLANT_ITALIC]:
            for weight in [cairo.FONT_WEIGHT_NORMAL, cairo.FONT_WEIGHT_BOLD]:
                style_str = STYLE[slant][weight]
                savepath = os.path.join(args.savedir, font_face, style_str)
                os.makedirs(savepath, exist_ok=True)

                for char in string.ascii_letters + string.digits:
                    memory = draw_glyph(char, font_name, slant, weight)
                    glyph_image_file = os.path.join(savepath, char + '.svg')
                    with open(glyph_image_file, 'wb') as f:
                        f.write(memory.getbuffer())


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--savedir', type=str, required=True, help='Directory for saving')
    parser.add_argument('--fontdir', type=str, required=False,
                        default='~/.fonts', help='The default system font directory (also need to be cached)')
    args = parser.parse_args()

    main(args)
