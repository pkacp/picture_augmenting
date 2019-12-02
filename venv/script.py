import os
import random
import string
from scipy import ndarray
import skimage as sk
from skimage import transform
from skimage import util
from skimage import filters
from skimage import io
import wx

folder_path = ""
generated_folder_path = "generated"
desired_folder_size = 5
make_bw = False
desired_image_width = 32
desired_image_height = 32
available_transformations = {}


def generate_image_name(number):
    return str(number).zfill(6)


def resize_to_params(image_array: ndarray, width=desired_image_width, height=desired_image_height):
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


def whole_function(event):
    print(folder_path)
    # print(widthTxt.GetLineText(0))
    width = int(widthTxt.GetLineText(0))
    heigth = int(heightTxt.GetLineText(0))
    desired_folder_size = int(filesNumberTxt.GetLineText(0))
    subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir()]
    image_number = 1
    for dir in subfolders:
        current_folder_path = dir
        current_folder_name = os.path.basename(dir)
        images_in_dir = [os.path.join(current_folder_path, f) for f in os.listdir(current_folder_path) if
                         os.path.isfile(os.path.join(current_folder_path, f))]
        f = open("dataset.csv", "w+")

        single_image_transformations_number = round(desired_folder_size / len(images_in_dir))

        for image in images_in_dir:
            for i in range(single_image_transformations_number):
                image_to_transform = resize_to_params(sk.io.imread(image), width, heigth)
                if make_bw == True:
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


def on_color_change(e):
    choice = colorRadioBox.GetStringSelection()
    global make_bw
    if choice == color_list[0]:
        make_bw = False
    if choice == color_list[1]:
        make_bw = True


def on_blur_change(e):
    global available_transformations
    val = blurChBox.GetValue()
    if val == True:
        available_transformations['blur'] = random_blur
    else:
        available_transformations.pop('blur')


def on_rotation_change(e):
    global available_transformations
    val = rotationChBox.GetValue()
    if val == True:
        available_transformations['rotate'] = random_rotation
    else:
        available_transformations.pop('rotate')


def on_noise_change(e):
    global available_transformations
    val = noiseChBox.GetValue()
    if val == True:
        available_transformations['noise'] = random_noise
    else:
        if "noise" in available_transformations:
            available_transformations.pop('noise')


app = wx.App()
frame = wx.Frame(parent=None, title='Picture augmenting')
frame.SetSize(0, 0, 640, 480)


def open_dir_dialog(event):
    open_dialog = wx.DirDialog(frame, "Choose main folder", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
    open_dialog.ShowModal()
    print(open_dialog.GetPath())
    folderLabel.SetLabel(open_dialog.GetPath())
    global folder_path
    folder_path = open_dialog.GetPath()
    open_dialog.Destroy()


panel = wx.Panel(frame, wx.ID_ANY)

buttonToGetMainFolder = wx.Button(panel, wx.ID_ANY, 'Select folder with images', (10, 10))
buttonToGetMainFolder.Bind(wx.EVT_BUTTON, open_dir_dialog)
folderLabel = wx.StaticText(panel, label="", pos=(200, 15))

color_list = ['RGB', 'Grayscale']

colorRadioBox = wx.RadioBox(panel, label='Choose color palette', pos=(10, 50), choices=color_list, majorDimension=1,
                            style=wx.RA_SPECIFY_ROWS)
colorRadioBox.Bind(wx.EVT_RADIOBOX, on_color_change)

blurChBox = wx.CheckBox(panel, id=21, label="Blur", pos=(10, 100), name="blurChBox")
blurChBox.Bind(wx.EVT_CHECKBOX, on_blur_change)

rotationChBox = wx.CheckBox(panel, id=22, label="Rotation", pos=(10, 120), name="rotationChBox")
rotationChBox.Bind(wx.EVT_CHECKBOX, on_rotation_change)

noiseChBox = wx.CheckBox(panel, id=23, label="Noise", pos=(10, 140), name="noiseChBox")
noiseChBox.Bind(wx.EVT_CHECKBOX, on_noise_change)

wx.StaticText(panel, label="Output width:", pos=(10, 170))
widthTxt = wx.TextCtrl(panel, value=str(desired_image_width), pos=(120, 160))

wx.StaticText(panel, label="Output height:", pos=(10, 200))
heightTxt = wx.TextCtrl(panel, value=str(desired_image_height), pos=(120, 190))

wx.StaticText(panel, label="Desired number of files for each category:", pos=(10, 240))
filesNumberTxt = wx.TextCtrl(panel, value=str(desired_folder_size), pos=(300, 230))

buttonToExecute = wx.Button(panel, wx.ID_ANY, 'Execute', (10, 400))
buttonToExecute.Bind(wx.EVT_BUTTON, whole_function)

frame.Centre()
frame.Show()
app.MainLoop()
