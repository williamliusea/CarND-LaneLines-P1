import processimage as pimg
import argparse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

parser = argparse.ArgumentParser(description='Process single image. \nLoad from test_images/ and output to test_images_output/.')
parser.add_argument('filename', type=str,
                   help='filename in test_images directory')
args = parser.parse_args()

#reading in an image
image = mpimg.imread('test_images/'+args.filename)
result = pimg.process_image(image)
#printing out some stats and plotting
print('This image is:', type(image), 'with dimensions:', image.shape)
# plt.imshow(result)  # if you wanted to show a single color channel image called 'gray', for example, call as plt.imshow(gray, cmap='gray')
mpimg.imsave('test_images_output/'+args.filename, result)
plt.imshow(result)
