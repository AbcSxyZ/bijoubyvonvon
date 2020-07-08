import os
import re
import io
from PIL import Image

def not_found_404(response):
    response("404 Not Found", [('Content-Type','text/html')])
    return [b"<h1>Page not found</h1>"]

def retrieve_filename_info(image_uri):
    size = None

    # Check if a size is specified.
    # Use 'filename.s-1234' format to specify a max width
    if re.match(".*.s-[0-9]{1,4}$", image_uri):
        image_uri = image_uri.split(".")
        size = int(image_uri[-1][2:])
        image_uri = ".".join(image_uri[:-1])
    if image_uri[0] == "/":
        image_uri = image_uri[1:]
    image_name = os.path.join(os.getcwd(), image_uri)
    return image_name, size

def return_image(response, image_uri):
    #Retrieve the absolute path of the requested URI
    image_name, size = retrieve_filename_info(image_uri)

    #Error for inexsiting file
    if not os.path.isfile(image_name):
        return not_found_404(response)

    #Return image on success
    extension = image_name.split(".")[-1]
    response('200 OK', [('Content-Type', 'image/{}'.format(extension))])
    with Image.open(image_name) as jewel_img:
        if size:
            jewel_img.thumbnail((size, size))
        output = io.BytesIO()
        if extension.lower() == "jpg":
            extension = "jpeg"
        jewel_img.save(output, format=extension)
    return [output.getvalue()]

def application(env, response):
    URI = env["REQUEST_URI"]
    return return_image(response, URI)
