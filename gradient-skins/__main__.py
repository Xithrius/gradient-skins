import argparse

import numpy as np
from PIL import Image


# https://github.com/nkmk/python-snippets/blob/master/notebook/numpy_generate_gradient_image.py
def get_gradient_2d(start: int, stop: int, width: int, height: int, is_horizontal: bool):
    if is_horizontal:
        return np.tile(np.linspace(start, stop, width), (height, 1))
    else:
        return np.tile(np.linspace(start, stop, height), (width, 1)).T


def get_gradient_3d(
    width: int,
    height: int,
    start_list: tuple[int, int, int],
    stop_list: tuple[int, int, int],
    is_horizontal_list: tuple[bool, bool, bool]
):
    result = np.zeros((height, width, len(start_list)))

    for i, (start, stop, is_horizontal) in enumerate(zip(start_list, stop_list, is_horizontal_list)):
        result[:, :, i] = get_gradient_2d(start, stop, width, height, is_horizontal)

    return result


removing = [
    (0, 8, 0, 8),
    (0, 8, 24, 64),
    (8, 16, 32, 64),
    (16, 20, 0, 4),
    (16, 20, 12, 20),
    (16, 20, 36, 44),
    (16, 20, 52, 64),
    (32, 64, 0, 16),
    (32, 48, 16, 64),
    (48, 64, 48, 64),
    (48, 52, 44, 48),
    (48, 52, 28, 36),
    (48, 52, 16, 20),
    (20, 32, 56, 64)
]


def generator(path: str, direction: str, start_color: tuple, end_color: tuple):
    gradient_direction = (False, False, False)
    if direction == 'h':
        gradient_direction = (True, True, True)
    elif direction == 'hv':
        gradient_direction = (True, True, False)

    array = get_gradient_3d(64, 64, start_color, end_color, gradient_direction)
    img = Image.fromarray(np.uint8(array)).convert('RGBA')
    img_arr = np.array(img)

    img_arr[48:64, 16:32] = np.copy(img_arr[28:44, 16:32])
    img_arr[16:32, 0:16] = np.copy(img_arr[28:44, 16:32])

    for (y1, y2, x1, x2) in removing:
        img_arr[y1:y2, x1:x2] = (0, 0, 0, 0)

    img_arr[48:64, 32:48] = img_arr[16:32, 40:56]

    # right arm at img_arr[16:32, 40:56]
    # left arm at img_arr[48:64, 32:48]
    # left leg at img_arr[48:64, 16:32]
    # right leg at img_arr[16:32, 0:16]

    img = Image.fromarray(img_arr)

    img.save(path, quality=100)


# https://stackoverflow.com/a/9979169
def rgb_tuple(s: str) -> tuple:
    try:
        r, g, b = map(int, s.split(','))

        return r, g, b
    except Exception:
        raise argparse.ArgumentTypeError("RGB value tuple must be formatted as r,g,b")


# (8, 159, 143), (42, 72, 88)
# (128, 0, 128), (137, 207, 240)
# example: pdm run gen ./test.png "8,159,143" "42,72,88"
def main():
    parser = argparse.ArgumentParser(description="Generate a gradient skin.")

    parser.add_argument("image_path", type=str, nargs="?", help="Where you want to save the skin to.")

    parser.add_argument('start_color', type=rgb_tuple, nargs="?", help="The RGB value to start with.")

    parser.add_argument('end_color', type=rgb_tuple, nargs="?", help="The RGB value to end with.")

    parser.add_argument("--direction", type=str, nargs="?", choices=["h", "v", "hv"], default="v")

    args = parser.parse_args()

    if args.direction != "v":
        raise ValueError("Only 'h' direction is supported at this time.")

    generator(args.image_path, args.direction, args.start_color, args.end_color)


if __name__ == "__main__":
    main()
