
from PIL import Image, ImageEnhance,ImageDraw,ImageFont
from pylab import *



def CombineViews(Im1, Im2, resample=Image.BICUBIC, resize_big_image=True):
    im1 = Image.open(Im1).convert("RGB")
    im2 = Image.open(Im2).convert("RGB")# convert B&W into RGB to be able to draw in color on the pictures
    if im1.height == im2.height:
        _im1 = im1
        _im2 = im2
    elif (((im1.height > im2.height) and resize_big_image) or
          ((im1.height < im2.height) and not resize_big_image)):
        _im1 = im1.resize((int(im1.width * im2.height / im1.height), im2.height), resample=resample)
        _im2 = im2
    else:
        _im1 = im1
        _im2 = im2.resize((int(im2.width * im1.height / im2.height), im1.height), resample=resample)
    dst = Image.new('RGB', (_im1.width + _im2.width, _im1.height))
    dst.paste(_im1, (0, 0))
    dst.paste(_im2, (_im1.width, 0))
    # save the view as a .jpg file
    from Main import output_images_directory_path
    dst.save(output_images_directory_path+"\\CombinedView.jpg")
