import argparse
from PyPDF2 import PdfReader
import sys
from PIL import Image
import os

IMAGE_QUALITY = 90
RESIZE_CONSTANT = 0.4

def compress_images_from_pdf(input_file_name, output_file_name, output_directory_name, rotation_angle=None):
    try: 
        os.mkdir(output_directory_name)
    except OSError as error: 
        print(error)

    try: 
        os.mkdir(os.path.join(output_directory_name, "tmp"))
    except OSError as error: 
        print(error)

    print(f"Directory '{output_directory_name}' created")

    # Extract images from PDF
    reader = PdfReader(input_file_name)

    compressed_images = []

    for i, page in enumerate(reader.pages):
        count = 0

        for image_file_object in page.images:
            file_name = f"page_{i}_image_{count}_{image_file_object.name}"
            file_path = os.path.join(output_directory_name, file_name)

            # Write uncompressed images to files
            with open(file_path, "wb") as fp:
                fp.write(image_file_object.data)
                count += 1

            # Open uncompressed files and compress them
            img_picture = Image.open(file_path).convert("RGB")

            # Rotate image if needed
            if rotation_angle:
                img_picture = img_picture.rotate(rotation_angle, Image.NEAREST, expand = 1)

            # Resize picture
            x, y = img_picture.size
            img_picture = img_picture.resize((int(x * RESIZE_CONSTANT), int(y * RESIZE_CONSTANT)), Image.ANTIALIAS)

            # Lower the quality
            compressed_file_name = os.path.join(os.path.join(output_directory_name, "tmp"), file_name)
            img_picture.save(compressed_file_name, "JPEG", optimize=True, quality=IMAGE_QUALITY)

            compressed_images.append(Image.open(compressed_file_name).convert("RGB"))

    # Save compressed images as a PDF
    compressed_images[0].save(output_file_name, save_all=True, append_images=compressed_images[1:])


if __name__ == "__main__":
    # Define command-line arguments using argparse
    parser = argparse.ArgumentParser(description="Compress images from a PDF file")
    parser.add_argument("input_file", type=str, help="Input PDF file")
    parser.add_argument("output_file", type=str, help="Output PDF file")
    parser.add_argument("output_dir", type=str, help="Output directory")
    parser.add_argument("-r", "--rotation_angle", type=int, default=None, help="Optional rotation angle (in degrees) for images")
    args = parser.parse_args()

    # Extract command-line arguments
    input_file_name = args.input_file
    output_file_name = args.output_file
    output_directory_name = args.output_dir
    rotation_angle = args.rotation_angle

    compress_images_from_pdf(input_file_name, output_file_name, output_directory_name, rotation_angle)