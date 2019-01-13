# Import everything needed to edit/save/watch video clips
import processimage as pimg
from moviepy.editor import VideoFileClip
import argparse
import matplotlib.image as mpimg

parser = argparse.ArgumentParser(description='Process single video image. \nLoad from test_videos/ and output to test_videos_output/.')
parser.add_argument('filename', type=str,
                   help='filename in test_videos directory')
args = parser.parse_args()

##### white_output = 'test_videos_output/night-highway-clearlane-bridge-curve.mp4'
## To speed up the testing process you may want to try your pipeline on a shorter subclip of the video
## To do so add .subclip(start_second,end_second) to the end of the line below
## Where start_second and end_second are integer values representing the start and end of the subclip
## You may also uncomment the following line for a subclip of the first 5 seconds
clip1 = VideoFileClip('test_videos/'+args.filename)
# clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4")
white_clip = clip1.fl_image(pimg.process_image) #NOTE: this function expects color images!!
white_clip.write_videofile('test_videos_output/'+args.filename, audio=False)
