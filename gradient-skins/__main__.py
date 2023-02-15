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
    return get_gradient_3d(64, 64, (8, 159, 143), (42, 72, 88), hs)


def generator():
    array = sample_gradient((True, True, True))
    Image.fromarray(np.uint8(array)).save('examples/gradient_h.png', quality=100)

    array = sample_gradient((False, False, False))
    Image.fromarray(np.uint8(array)).save('examples/gradient_v.png', quality=100)

    array = sample_gradient((True, True, False))
    Image.fromarray(np.uint8(array)).save('examples/gradient_hv.png', quality=100)


if __name__ == "__main__":
    generator()
