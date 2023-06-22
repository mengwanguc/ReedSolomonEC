from PIL import Image

TARGET_BOUNDS = (1024, 1024)

IMAGE_PATH = "F/tp_SLEC/figure.eps"

# Load the EPS at 10 times whatever size Pillow thinks it should be
# (Experimentaton suggests that scale=1 means 72 DPI but that would
#  make 600 DPI scale=8⅓ and Pillow requires an integer)
pic = Image.open(IMAGE_PATH)
pic.load(scale=10)

# Ensure scaling can anti-alias by converting 1-bit or paletted images
if pic.mode in ('P', '1'):
    pic = pic.convert("RGB")

# Calculate the new size, preserving the aspect ratio
ratio = min(TARGET_BOUNDS[0] / pic.size[0],
            TARGET_BOUNDS[1] / pic.size[1])
new_size = (int(pic.size[0] * ratio), int(pic.size[1] * ratio))

# Resize to fit the target size
pic = pic.resize(new_size, Image.ANTIALIAS)

# Save to PNG
pic.save("image.png")

