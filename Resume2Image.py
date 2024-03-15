import os
from wand.image import Image as WandImage
from PIL import Image
import io



def convert_pdf_to_images(pdf_path):
    with WandImage(filename=pdf_path, resolution=300) as img:
        images = []
        for i, page in enumerate(img.sequence):
            with WandImage(page) as page_image:
                images.append(page_image.make_blob('jpeg'))
    return images

def merge_images_horizontally(images):
    pil_images = [Image.open(io.BytesIO(image_data)) for image_data in images]
    widths, heights = zip(*(image.size for image in pil_images))
    total_width = sum(widths)
    max_height = max(heights)
    merged_image = Image.new('RGB', (total_width, max_height))
    x_offset = 0
    for image in pil_images:
        merged_image.paste(image, (x_offset, 0))
        x_offset += image.width
    return merged_image

def main():
    input_folder = 'Resumes'
    output_folder = 'Output_Images'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.jpg')

            images = convert_pdf_to_images(input_path)
            merged_image = merge_images_horizontally(images)

            merged_image.save(output_path)
            print(f"PDF '{filename}' converted to image and saved to '{output_path}'")

if __name__ == "__main__":
    main()
