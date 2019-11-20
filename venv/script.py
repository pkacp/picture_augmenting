import os
import random
import string
from scipy import ndarray
import skimage as sk
from skimage import transform
from skimage import util
from skimage import filters
from skimage import io


def random_string(string_length=6):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(string_length))


def resize_to_params(image_array: ndarray, width=64, height=64):
    return sk.transform.resize(image_array, (width, height))


def random_rotation(image_array: ndarray):
    random_degree = random.uniform(-25, 25)
    return sk.transform.rotate(image_array, random_degree)


def random_blur(image_array: ndarray):
    random_value = random.uniform(0, 3)
    return sk.filters.gaussian(image_array, random_value)


def random_noise(image_array: ndarray):
    return sk.util.random_noise(image_array)


available_transformations = {
    'rotate': random_rotation,
    'noise': random_noise,
    'blur': random_blur
}

folder_path = 'images/30'
generated_folder_path = 'images/generated'
num_of_generated_files = 10

images = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

for image in images:
    for i in range(num_of_generated_files):
        # read image as an two dimensional array of pixels
        image_to_transform = resize_to_params(sk.io.imread(image))
        # random num of transformation to apply
        num_transformations_to_apply = random.randint(0, len(available_transformations))

        num_transformations = 0
        transformed_image = None
        while num_transformations <= num_transformations_to_apply:
            key = random.choice(list(available_transformations))
            transformed_image = available_transformations[key](image_to_transform)
            num_transformations += 1

        new_file_path = '%s/%s.jpg' % (generated_folder_path, random_string())

        io.imsave(new_file_path, transformed_image)
