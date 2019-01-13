# **Finding Lane Lines on the Road**

## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file. But feel free to use some other method and submit a pdf if you prefer.

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"
[image2]: ./examples/rho9_96.png "rho = 9"
[image3]: ./examples/rho1_8.png "rho = 1"
[image4]: ./examples/edge.png "edges"
[image5]: ./examples/masked_edge.png "masked edges"
[image6]: ./examples/rho3_theta1000_28.png "masked edges"
[image7]: ./examples/nightWhiteDottedMissed.jpg "not work for night"
[image8]: ./examples/avgLeftRightLine.jpg "only two lines"
---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 5 steps.
1. Convert the image into grayscale.

  ![grayscale][image1]
2. Blur the grayscale image with kernel size of 9
3. Use Canny method with the threshold of low = 50 and high = 150 to detect edges in the blur image.

   ![edges][image4]
4. By looking at the image, I decided the vertices of the region of interest, and apply the mask using this region.

   ![masked edges][image5]
5. Find Hough lines using the Hough function on the masked image.
  While adjusting the parameter, I found several tips. If I have rho = 1, the Hough function will miss the dotted while line.

  ![rho = 1][image3]

  If I have rho too big (like 9), he number of Hough lines will be too many and have a lot of small variations. See image.

  ![rho = 9][image2]

  With a bit of experiment, I found rho = 3 is the optimal. With theta being smaller, the lines are more concentrated.

  ![rho =3 and theta = pi/1000][image6]

6. Filter the lines and find the left and right line and only draw them. This results only two solid lines, and the result photo is much cleaner.
  ![two lines][image8]


### 2. Identify potential shortcomings with your current pipeline

In the first version of the pipeline, I am using the following vertices. This is too arbitrary that it does not even fit an image with different resolution.
```
vertices = np.array([[(60, image.shape[0]),(450, 320), (510, 320), (900, image.shape[0])]], dtype=np.int32)
```    
![missed the right line][image7]

This does not sounds like too much of a problem because in real use case, the parameters are calibrated to each of the specific car model. I can assume the view from the same car will be fixed.

Still, my current approach have several drawbacks:
1. it will not adapt to case where there is a turn or car is going up hill or down hill. All these cases will fail the fix region approach.
2. Non-lane lines. Any lines which appears in the region of interest will be detected. The current algorithm cannot distinguish between the valid lines and the other lines. For example, in the challenge.mp4, there are many lines appears in the region of interest that messed things up.  

### 3. Suggest possible improvements to your pipeline

Build adaptive region detection.
1. detect all lines that appears in the lower half of the image. This is to make sure we capture all possible lane lines.
2. Because the nature of the lane lines will intercept at roughly the same point, we can find the point which is intercept at roughly the center of the view. It will pick only lines intercepts near the center of the image.
3. After that, we pick the two lines closes to the center vertical line.
