import processimage as pimg
import argparse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

parser = argparse.ArgumentParser(description='Process single image. Or all image in test_images/. \nLoad from test_images/ and output to test_images_output/.')
parser.add_argument('filename', type=str, nargs='?', default='', 
                   help='filename in test_images directory')
args = parser.parse_args()
if args.filename == '':
    filenames = os.listdir("test_images/")
else:
    filenames = [args.filename]
for name in filenames:
    #reading in an image
    image = mpimg.imread('test_images/'+name)
    result = pimg.process_image(image)
    #printing out some stats and plotting
    print('This image is:', type(image), 'with dimensions:', image.shape)
    # plt.imshow(result)  # if you wanted to show a single color channel image called 'gray', for example, call as plt.imshow(gray, cmap='gray')
    mpimg.imsave('test_images_output/'+name, result)
