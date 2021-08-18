from PIL import Image

infile = '灰度图.png'
outfile = 'new-灰度图.png'
im = Image.open(infile)
(x, y) = im.size  # read image size
width = 128  # define standard width
height = 128  # calc height based on standard width
out = im.resize((width, height), Image.ANTIALIAS)  # resize image with high-quality
out.save(outfile)

print('original size: ', x, y)
print('adjust size: ', width, height)
