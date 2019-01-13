import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import math

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.

    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    `vertices` should be a numpy array of integer points.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)

    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    #filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def calculateXFromY(m, b, y, shape):
    x = (y - b)/m
    if x < 0:
        x = 0
        y = b
    if x > shape[1]:
        x = shape[1]
        y = shape[1]*m + b
    return [int(x), int(y)]

def detect_left_right_lines(lines, shape):
    leftLines = []
    rightLines = []
    for line in lines:
        for x1,y1,x2,y2 in line:
            if (x1 != x2):
                tan = (y2-y1)/(x2-x1);
                if (tan < -0.577 and tan > -3.73): # left line
                    leftLines.append(line)
                elif tan > 0.577 and tan < 3.73:
                    rightLines.append(line)

    result = []
    if len(leftLines) > 0:
        b = []
        m = []
        maxX = 0;
        for line in leftLines:
            for x1,y1,x2,y2 in line:
                if (x1 > maxX):
                    maxX = x1
                if (x2 > maxX):
                    maxX = x2
                p = np.polyfit([x1, x2], [y1, y2], 1)
                b.append(p[1])
                m.append(p[0])
        avgB = sum(b)/float(len(b))
        avgM = sum(m)/float(len(m))
        point = calculateXFromY(avgM, avgB, shape[0], shape)
        result.append([[point[0], point[1], maxX, int(avgM*maxX+avgB)]])

    if len(rightLines) > 0:
        b = []
        m = []
        minX = 100000;
        for line in rightLines:
            for x1,y1,x2,y2 in line:
                if (x1 < minX):
                    minX = x1
                if (x2 < minX):
                    minX = x2
                p = np.polyfit([x1, x2], [y1, y2], 1)
                b.append(p[1])
                m.append(p[0])
        avgB = sum(b)/float(len(b))
        avgM = sum(m)/float(len(m))
        point = calculateXFromY(avgM, avgB, shape[0], shape)
        result.append([[minX, int(avgM*minX+avgB), point[0], point[1]]])

    # print("x1=", x1, " x2=", x2, " y1=", y1, " y2=", y2)
    return result

def draw_lines(img, lines, color=[255, 0, 0], thickness=6):
    """
    NOTE: this is the function you might want to use as a starting point once you want to
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).

    Think about things like separating line segments by their
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of
    the lines and extrapolate to the top and bottom of the lane.

    This function draws `lines` with `color` and `thickness`.
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.

    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    left_right_lines = detect_left_right_lines(lines, img.shape)
    # print(left_right_lines)
    draw_lines(line_img, left_right_lines)
    return line_img

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.

    `initial_img` should be the image before any processing.

    The result image is computed as follows:

    initial_img * α + img * β + γ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, γ)

def process_image(image):
    # NOTE: The output you return should be a color image (3 channel) for processing video below
    # TODO: put your pipeline here,
    # you should return the final output (image where lines are drawn on lanes)
    gray_image = grayscale(image)
    #plt.imshow(gray_image)
    smooth_image = gaussian_blur(gray_image, 5)
    #plt.imshow(smooth_image)
    edge_image = canny(smooth_image, 50, 150)
    #plt.imshow(edge_image)
    mask_image = np.zeros_like(edge_image)
    ignore_mask_color = 255
    # plt.imshow(mask_image)
    vertices = np.array([[(0, image.shape[0]),(0, image.shape[0]*3/4), (image.shape[1] / 3, image.shape[0] /2), (image.shape[1]*2/3, image.shape[0]/2), (image.shape[1], image.shape[0] *3/4), (image.shape[1], image.shape[0])]], dtype=np.int32)
    masked_edges_image = region_of_interest(edge_image, vertices)
    # plt.imshow(masked_edges_image)
    hough_image = hough_lines(masked_edges_image, 2, np.pi/360, 50, image.shape[0]/20, image.shape[0]/4)
    #plt.imshow(hough_image)
    result = weighted_img(hough_image, image)
    return result
