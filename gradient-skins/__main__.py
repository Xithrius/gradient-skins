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


def sample_gradient(hs: tuple[bool, bool, bool]):
    # return get_gradient_3d(64, 64, (8, 159, 143), (42, 72, 88), hs)
    return get_gradient_3d(64, 64, (128, 0, 128), (137, 207, 240), hs)


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


def main():
    array = sample_gradient((False, False, False))
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

    img.save('examples/cut_from_v.png', quality=100)


def generator():
    array = sample_gradient((True, True, True))
    Image.fromarray(np.uint8(array)).save('examples/gradient_h.png', quality=100)

    array = sample_gradient((False, False, False))
    Image.fromarray(np.uint8(array)).save('examples/gradient_v.png', quality=100)

    array = sample_gradient((True, True, False))
    Image.fromarray(np.uint8(array)).save('examples/gradient_hv.png', quality=100)


if __name__ == "__main__":
    # generator()
    main()
