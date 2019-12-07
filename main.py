from ImageProcessing import *
import FBPhotoAPIHandler
from filesaver import *
from main import *


program = FBPhotoAPIHandler.FBPhotoAPIHandler()
program.populate_to_visit()
program.populate_album_data()
program.populate_all_image_sources()
program.createimagedict()
downloadfiles()


im = Image.open("./Photos/111.jpg")
#Edit which photo here. TODO: Make file select.
orig_w, orig_h = im.size
factor = 1.5
new_im = im.resize((int(orig_w * factor), int(orig_h * factor)), Image.LANCZOS)
pixel_matrix = make_pixel_matrix(new_im)
target_image_width, target_image_height = new_im.size
size = 15
output_img = Image.new('RGB', (target_image_width, target_image_height), (255,255,255,0))
crop_and_resize("./Photos/", size)
sub_photos = prepare_sub_photos("./Photos/Subphotos/", size)
mean_rgbs = mean_rgbs_subimage(sub_photos)
for x in range(0, target_image_width, size):
    for y in range(0, target_image_height, size):
        s = get_sub_square(pixel_matrix, (y, x), size)
        target_rgb = calc_average_RGB(s)
        source_img_name = pythagoras_nearest_rgb(target_rgb, mean_rgbs)
        source_img = sub_photos[source_img_name]
        output_img.paste(source_img, (x, y))
output_img.show()
