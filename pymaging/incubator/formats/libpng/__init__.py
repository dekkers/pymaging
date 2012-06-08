# -*- coding: utf-8 -*-
# Copyright (c) 2012 Jeroen Dekkers
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted, provided that the
# above copyright notice and this permission notice appear in all
# copies.

import array
from ctypes import CDLL, CFUNCTYPE, POINTER, byref, c_ubyte, c_void_p, c_size_t, py_object, cast, create_string_buffer

from pymaging.formats import Format
from pymaging.image import Image
from pymaging.colors import RGBA, RGB

READFUNC = CFUNCTYPE(None, c_void_p, POINTER(c_ubyte), c_size_t)

libpng = CDLL("libpng15.so.15")
libpng.png_create_read_struct.restype = c_void_p
libpng.png_create_info_struct.restype = c_void_p
libpng.png_set_read_fn.argtypes = [c_void_p, py_object, READFUNC]
libpng.png_get_io_ptr.res_type = c_void_p


def png_read_func(png_ptr, data, length):
    p = libpng.png_get_io_ptr(png_ptr)
    fileobj = cast(p, py_object).value
    contents = fileobj.read(length)
    for i in range(length):
        try:
            # Python 3
            data[i] = contents[i]
        except TypeError:
            # Python 2
            data[i] = ord(contents[i])

read_func = READFUNC(png_read_func)


def decode(fileobj):
    header = fileobj.read(8)
    if libpng.png_sig_cmp(header, 0, 8):
        fileobj.seek(0)
        return None

    # FIXME: We should provide error functions, python just crashes on errors
    # now.
    png_ptr = libpng.png_create_read_struct(b"1.5.10", None, None, None)
    if not png_ptr:
        return None

    info_ptr = libpng.png_create_info_struct(png_ptr)
    if not info_ptr:
        libpng.png_destroy_read_struct(byref(png_ptr), None, None)
        return None

    libpng.png_set_read_fn(png_ptr, fileobj, read_func)
    fileobj.seek(0)
    color_type = libpng.png_get_color_type(png_ptr, info_ptr)
    libpng.png_read_info(png_ptr, info_ptr)
    libpng.png_set_expand(png_ptr)
    libpng.png_set_interlace_handling(png_ptr)
    libpng.png_read_update_info(png_ptr, info_ptr)

    color_type = libpng.png_get_color_type(png_ptr, info_ptr)
    width = libpng.png_get_image_width(png_ptr, info_ptr)
    height = libpng.png_get_image_height(png_ptr, info_ptr)
    rowbytes = libpng.png_get_rowbytes(png_ptr, info_ptr)
    row_pointers = (POINTER(c_ubyte) * height)()
    buf = []
    for i in range(height):
        buf.append(create_string_buffer(rowbytes))
        row_pointers[i] = cast(byref(buf[i]), POINTER(c_ubyte))
    libpng.png_read_image(png_ptr, row_pointers)

    pixels = []
    for i in range(height):
        pixels.append(array.array('B', buf[i].raw))

    if color_type == 2:
        mode = RGB
    elif color_type == 6:
        mode = RGBA
    else:
        raise NotImplementedError("Support for color type %d not implemented yet" % color_type)

    return Image(width, height, pixels, mode, palette=None)


def encode(image, fileobj):
    return None

LIBPNG = Format(decode, encode, ['png'])
