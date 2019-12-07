from PIL import Image
import math
import os

def make_pixel_matrix(image):
    """Takes an image and creates a 2D array of image pixels"""
    pixels = list(image.getdata())
    return [pixels[i:i+image.width] for i in range(0, len(pixels), image.width)]


def get_sub_square(pixel_matrix, left_upper, size):
    """Takes 2D array of pixels, left-upper corner tuple, and size of the square
    in pixels.
    Naming reflects PIL region definition of 4-tuple:
    left, upper, right, lower.
    0,0 is top left.
    Returns sub-section, square, of pixel matrix"""
    #sets right_lower tuple
    right_lower = (left_upper[0]+size, left_upper[1]+size)
    #prepare to iterate over rows in image
    rows = pixel_matrix[left_upper[0]:right_lower[0]]
    #initialize empty square to store new pixel_matrix
    square = []
    for row in rows:
        square.append(row[left_upper[1]:right_lower[1]])
    return square


def calc_average_RGB(pixel_matrix):
    """Calculates the average RGB values for a pixel matrix, returns RGB tuple,
    forces integer values in tuple.
    """
    #Set all pixel values to 0 and counter to 0.
    red = 0
    green = 0
    blue = 0
    pixel_count = 0
    #add pixels in matrix
    for row in pixel_matrix:
        for color in row:
            red += color[0]
            green += color[1]
            blue += color[2]
            pixel_count += 1
    #return mean of each pixel as tuple, forced integer
    return (int(red/pixel_count), int(green/pixel_count), int(blue/pixel_count))

def calculate_color_difference(rgb1, rgb2):
    #Taken from https://stackoverflow.com/questions/8863810/python-find-similar-colors-best-way/8863872
    """Calculates color difference"""
    rm = 0.5 * (rgb1[0] + rgb2[0])
    rd = ((2 + rm) * (rgb1[0] - rgb2[0])) ** 2
    gd = (4 * (rgb1[1] - rgb2[1])) ** 2
    bd = ((3 - rm) * (rgb1[2] - rgb2[2])) ** 2
    return math.sqrt(rd + gd + bd)

def pythagoras_nearest_rgb(target_rgb, source_images_mean_rgbs):
    """Finds the source image with the closest rgb value to
    the target section. Target_rgb is the average RGB value of the target
    section.
    source_images_mean_rgbs is a dictionary of source filenames and the
    mean RGB value of that file.
    Returns the filename of the closest matching source image
    """
    best_match_name = None
    best_match_color_difference = None
    for path, source_rgb in source_images_mean_rgbs.items():
        color_difference = calculate_color_difference(target_rgb, source_rgb)
        if best_match_color_difference is None or color_difference < best_match_color_difference:
            best_match_name = path
            best_match_color_difference = color_difference
    return best_match_name


def crop_from_center(image):
    """Takes in an image, returns cropped image as square, cropped from center"""
    width, height = image.size
    if width < height:
        left = 0
        upper = (height-width)//2
        right = width
        lower = height - (math.ceil((height-width)/2))
    else:
        left = (width - height)//2
        upper = 0
        right = width - (math.ceil((width - height)/2))
        lower = height
    box = (left, upper, right, lower)
    return image.crop(box)

def crop_and_resize(file_path, size):
    #Want to change this, but running into file quality issues when not saving;
    #need to separate creating path, handle that in a different function.
        sub_path = "/Subphotos/"
        if not os.path.exists(file_path + sub_path):
            os.mkdir(file_path + sub_path)
        for filename in os.listdir(file_path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                full_path = os.path.join(file_path, filename)
                image = Image.open(full_path)
                cropped_image = crop_from_center(image)
                cropped_image.thumbnail((size, size), Image.ANTIALIAS)
                destination = os.path.join(file_path,sub_path)
                quality_val = 95
                cropped_image.save(file_path + sub_path + "T_" + filename, quality=quality_val)

# def resize(file_path, size): #./Photos/
#     sub_path = "/Subphotos/"
#     if not os.path.exists(file_path + sub_path):
#         os.mkdir(file_path + sub_path)
#     for filename in os.listdir(file_path):
#         if filename.endswith(".jpg") or filename.endswith(".png"):
#             full_path = os.path.join(file_path, filename)
#             image = Image.open(full_path)
#             image.thumbnail((size, size), Image.ANTIALIAS)
#             destination = os.path.join(file_path,sub_path)
#             quality_val = 95
#             image.save(file_path + sub_path + "T_" + filename, quality=quality_val)



def prepare_sub_photos(file_path, size):
    """Loads files from given path and subdirectories which are JPEG
    or PNG format.
    Stores them in a dictionary: Keys = filepath, Values = PIL Image Object.
    Returns the dictionary."""
    images = {}
    for filename in os.listdir(file_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            full_path = os.path.join(file_path, filename)
            image = Image.open(full_path)
            images[filename] = image
    return images


def mean_rgbs_subimage(images):
    """Creates and returns a dictionary of sub-file mean RGBS to access while building
    mosaic. Key = filename; value = meanRGB."""
    meanrgb = {}
    for filename, image in images.items():
        pixel_matrix = make_pixel_matrix(image)
        meanrgb[filename] = calc_average_RGB(pixel_matrix)
    return meanrgb
