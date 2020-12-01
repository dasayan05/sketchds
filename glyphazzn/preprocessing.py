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


class SVG(IntEnum):
    MOVETO = 1
    LINETO = 2
    CUBICBEZIER = 3
    CLOSE = 4
    DONE = 0


def draw_glyph(char, font_face, slant, weight):
    memory = BytesIO()
    with cairo.SVGSurface(memory, 70, 80) as surface:
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


def parse_glyph(memory):
    with minidom.parse(memory) as doc:
        paths = doc.getElementsByTagName('path')
        if len(paths) == 0:
            return []
        assert len(paths) == 1, "There supposed to be only one path"
        path = parse_path(paths[0].getAttribute('d'))

        glyph = []
        for e in path:
            if isinstance(e, Move):
                point = e.end
                glyph.append([SVG.MOVETO.value, point.real, point.imag, 0., 0., 0., 0., 0., 0.])
            elif isinstance(e, Line):
                line_start = e.start
                line_end = e.end
                glyph.append([SVG.LINETO.value, line_start.real,
                              line_start.imag, line_end.real, line_end.imag, 0., 0., 0., 0.])
            elif isinstance(e, CubicBezier):
                bz_start = e.start
                bz_control1 = e.control1
                bz_control2 = e.control2
                bz_end = e.end
                glyph.append([SVG.CUBICBEZIER.value, bz_start.real, bz_start.imag, bz_control1.real, bz_control1.imag,
                              bz_control2.real, bz_control2.imag, bz_end.real, bz_end.imag])
            elif isinstance(e, Close):
                glyph.append([SVG.CLOSE.value, 0., 0., 0., 0., 0., 0., 0., 0.])
            else:
                raise ValueError(f'Unknown path element "{e.__class__.__name__}"')

        glyph.append([SVG.DONE.value, 0., 0., 0., 0., 0., 0., 0., 0.])
        return glyph


def write_glyphs(glyph, axis):
    axis.cla()
    for instructions in glyph:
        cmd, *args = instructions
        if cmd == SVG.MOVETO:
            start = args[:2]
        elif cmd == SVG.LINETO:
            pts = np.array(args[:4]).reshape((2, 2))
            axis.plot(pts[:, 0], pts[:, 1], color='black')
            end = args[2:4]
        elif cmd == SVG.CUBICBEZIER:
            cpts = np.array(args[:]).reshape((4, 2))
            draw_bezier(cpts, curvePlotKwagrs=dict(color='black'), draw_axis=axis)
            end = args[-2:]
        elif cmd == SVG.CLOSE:
            pts = np.array([start, end])
            axis.plot(pts[:, 0], pts[:, 1], color='black')
        elif cmd == SVG.DONE:
            break
    axis.invert_yaxis()
    axis.axis('off')
    axis.set_aspect('equal')


def main(args):
    fig = plt.figure(figsize=(2.55, 2.55))
    ax = plt.gca()

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
                    glyph = parse_glyph(memory)

                    if len(glyph) > 0:
                        if args.raster:
                            # save the image
                            write_glyphs(glyph, ax)
                            glyph_image_file = os.path.join(savepath, char + '.png')
                            plt.savefig(glyph_image_file, bbox_inches='tight')

                        # save binary file
                        glyph_bin_file = os.path.join(savepath, char + '.npy')
                        with open(glyph_bin_file, 'wb') as f:
                            np.save(f, np.array(glyph))
                    else:
                        print(
                            f'Some problem with font {font_name}, style {style_str}, glyph {char}')


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--savedir', type=str, required=True, help='Directory for saving')
    parser.add_argument('--fontdir', type=str, required=False,
                        default='~/.fonts', help='The default system font directory (also need to be cached)')
    parser.add_argument('--raster', action='store_true',
                        help='additionally produce rasterized versions')
    args = parser.parse_args()

    main(args)
