import os

from PIL import Image, ImageDraw, ImageQt, ImageSequence
from PySide6 import QtGui
from pathlib import Path



def emojisplitter(input_file, horizontal_emojis=1, vertical_emojis=1, split_confirmation=False):
    # inputs
    input_image = Image.open(str(input_file))
    horizontal_emojis = int(horizontal_emojis)
    vertical_emojis = int(vertical_emojis)

    # gifsupport
    input_sequence = []
    for frame in ImageSequence.Iterator(input_image):
        input_sequence.append(frame.copy())

    # work on copy
    preview_sequence = input_sequence.copy()
    # add transparent space but preserve aspect ratio of input image
    nr_of_image_pixels = 256
    if (input_image.width / input_image.height) > (horizontal_emojis / vertical_emojis):
        size = (horizontal_emojis * nr_of_image_pixels, int(horizontal_emojis * input_image.height / input_image.width * nr_of_image_pixels))
    else:
        size = (int(vertical_emojis * input_image.width / input_image.height * nr_of_image_pixels), vertical_emojis * nr_of_image_pixels)

    # find the correct place to center the image on the underlying canvas
    upper_left_paste_coordinate = (int(horizontal_emojis * nr_of_image_pixels / 2 - size[0] / 2),
                                   int(vertical_emojis * nr_of_image_pixels / 2 - size[1] / 2))

    # gifsupport
    output_sequence = []
    for preview_frame in preview_sequence:
        # do actual resizing to fit a 256 x 256 pixel grid
        preview_frame = preview_frame.resize(size)

        # create output image with the correct canvas size
        output = Image.new("RGBA", (horizontal_emojis * nr_of_image_pixels, vertical_emojis * nr_of_image_pixels))
        # make all pixels transparent
        output.putalpha(0)
        # paste the resized image on the canvas
        output.paste(preview_frame, upper_left_paste_coordinate)
        output_sequence.append(output)
        # output.show()  # for testing
    if not split_confirmation:
        # show the grid lines where the emoji will cut
        # work on copy
        preview_sequence = output_sequence.copy()
        # gifsupport
        for preview_frame in preview_sequence:

            # draw vertical lines
            for i in range(horizontal_emojis + 1):
                ImageDraw.Draw(preview_frame).line((i / horizontal_emojis * preview_frame.width, 0,
                                                    i / horizontal_emojis * preview_frame.width, preview_frame.height),
                                                   width=5,
                                                   fill=(255, 255, 255, 128))
            # draw horizontal lines
            for j in range(vertical_emojis + 1):
                ImageDraw.Draw(preview_frame).line((0, j / vertical_emojis * preview_frame.height, preview_frame.width,
                                                    j / vertical_emojis * preview_frame.height), width=5,
                                                   fill=(255, 255, 255, 128))
            # draw inner vertical lines
            for i in range(horizontal_emojis + 1):
                ImageDraw.Draw(preview_frame).line((i / horizontal_emojis * preview_frame.width, 0,
                                                    i / horizontal_emojis * preview_frame.width, preview_frame.height),
                                                   width=3, fill=(0, 0, 0, 128))
            # draw inner horizontal lines
            for j in range(vertical_emojis + 1):
                ImageDraw.Draw(preview_frame).line((0, j / vertical_emojis * preview_frame.height, preview_frame.width,
                                                    j / vertical_emojis * preview_frame.height), width=3,
                                                   fill=(0, 0, 0, 128))
            # preview_split.show()  # Show preview_split for testing purposes

        return pil2pixmap(preview_frame)

    if split_confirmation:
        # splitting the filepath to add the coordinates into the filename
        filepath = Path(input_file)
        filename = filepath.stem
        file_extension = filepath.suffix

        # cutting the image
        for i in range(horizontal_emojis):
            for j in range(vertical_emojis):
                # gif support
                image_to_save = []
                for output_frame in output_sequence:
                    image_to_save.append(output_frame.crop(
                        (i / horizontal_emojis * output_frame.width,
                         j / vertical_emojis * output_frame.height,
                         (i + 1) / horizontal_emojis * output_frame.width,
                         (j + 1) / vertical_emojis * output_frame.height)))
                    # output_frame.show()  # for testing

                # saving with coordinates in the filename
                if len(image_to_save) > 1:  # TODO: test different fileformats tested:png gif jpg bmp
                    image_to_save[0].save(
                        os.path.join(filepath.parent, filename + str(i) + str(j) + ".gif"), save_all=True,
                        append_images=image_to_save[1:], format="GIF")
                else:
                    image_to_save[0].save(os.path.join(filepath.parent, filename + str(i) + str(j) + ".png")
                                          , format="PNG")


"""https://stackoverflow.com/questions/34697559/pil-image-to-qpixmap-conversion-issue"""


def pil2pixmap(im):
    if im.mode == "RGB":
        r, g, b = im.split()
        im = Image.merge("RGB", (b, g, r))
    elif im.mode == "RGBA":
        r, g, b, a = im.split()
        im = Image.merge("RGBA", (b, g, r, a))
    elif im.mode == "L":
        im = im.convert("RGBA")
    # Bild in RGBA konvertieren, falls nicht bereits passiert
    im2 = im.convert("RGBA")
    data = im2.tobytes("raw", "RGBA")
    qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
    pixmap = QtGui.QPixmap.fromImage(qim)
    return pixmap
