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



### 2. Identify potential shortcomings with your current pipeline

In the first version of the pipeline, I am using the following vertices. This is too arbitrary that it does not even fit an image with different resolution.
```
vertices = np.array([[(60, image.shape[0]),(450, 320), (510, 320), (900, image.shape[0])]], dtype=np.int32)
```    

After testing with dash cam image from my own car, I decided to improve it.


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to ...

Another potential improvement could be to ...
