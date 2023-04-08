from pypdf import PdfReader
import sys
from PIL import Image
import os

IMAGE_QUALITY = 90
RESIZE_CONSTANT = 0.4

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input PDF file> <output directory> <optional: rotation angle e.g, -90, 90>")
        exit(1)

    input_file_name = sys.argv[1]
    output_directory_name = sys.argv[2]

    rotation_angle = None
    if len(sys.argv) == 4:
        rotation_angle = int(sys.argv[3])

    try: 
        os.mkdir(output_directory_name)
    except OSError as error: 
        print(error)

    try: 
        os.mkdir(os.path.join(output_directory_name, "tmp"))
    except OSError as error: 
        print(error)

    print("Directory '% s' created" % output_directory_name)


    # Extract images from PDF
    reader = PdfReader(input_file_name)

    compressed_images = []

    for i,page in enumerate(reader.pages):
        #page = [0]
        count = 0

        for image_file_object in page.images:
            file_name = f"page_{i}_image_{count}_{image_file_object.name}"
            file_path = os.path.join(output_directory_name, file_name)

            # Write uncompressed images to files
            with open(file_path, "wb") as fp:
                fp.write(image_file_object.data)
                count += 1

            # Open uncoipressed files and compress them
            img_picture = Image.open(file_path).convert("RGB")

            # Rotate image if needed
            if rotation_angle:
                img_picture = img_picture.rotate(rotation_angle, Image.NEAREST, expand = 1)

            # Resize picture
            x,y = img_picture.size
            img_picture = img_picture.resize((int(x * RESIZE_CONSTANT),int(y * RESIZE_CONSTANT)), Image.ANTIALIAS)

            # Lower the quality
            compressed_file_name = os.path.join(os.path.join(output_directory_name, "tmp"), file_name)
            img_picture.save(compressed_file_name, "JPEG", optimize=True, quality=IMAGE_QUALITY)

            compressed_images.append(Image.open(compressed_file_name).convert("RGB"))

    #img_picture = Image.open(all_image_list[0]) #.convert("RGB")
    compressed_images[0].save(r'my_images.pdf', save_all=True, append_images=compressed_images[1:])


