from rembg import remove
from PIL import Image
import io

# Open input image
input_path = "./profile.jpg"
output_path = "./bg-profile.jpg"

with open(input_path, "rb") as f:
    input_image = f.read()

# Remove background
output_image = remove(input_image)

# Save the output
with open(output_path, "wb") as f:
    f.write(output_image)
