import os
import random
import string
from scipy import ndarray
import skimage as sk
from skimage import transform
from skimage import util
from skimage import filters
from skimage import io


def generate_image_name(number):
    return str(number).zfill(10)


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


def make_img_grayscale(image_array: ndarray):
    return sk.color.rgb2gray(image_array)


available_transformations = {
    'rotate': random_rotation,
    'noise': random_noise,
    'blur': random_blur
}

folder_path = 'images/'
generated_folder_path = 'images/generated'
desired_folder_size = 5

subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir() ]

for dir in subfolders:
    current_folder_path = dir
    current_folder_name = os.path.basename(dir)
    images_in_dir = [os.path.join(current_folder_path, f) for f in os.listdir(current_folder_path) if os.path.isfile(os.path.join(current_folder_path, f))]
    f = open("dataset.csv", "w+")

    single_image_transformations_number = round(desired_folder_size/len(images_in_dir))

    image_number = 1
    for image in images_in_dir:
        for i in range(single_image_transformations_number):
            image_to_transform = resize_to_params(sk.io.imread(image))
            image_to_transform = make_img_grayscale(image_to_transform)
            num_transformations_to_apply = random.randint(0, len(available_transformations))

            num_transformations = 0
            transformed_image = None
            while num_transformations <= num_transformations_to_apply:
                key = random.choice(list(available_transformations))
                transformed_image = available_transformations[key](image_to_transform)
                num_transformations += 1

            generated_name = generate_image_name(image_number)
            image_number += 1
            new_file_path = '%s/%s.jpg' % (generated_folder_path, generated_name)
            f.write("%s, %s\n" % (generated_name, current_folder_name))

            io.imsave(new_file_path, transformed_image)

    f.close()
