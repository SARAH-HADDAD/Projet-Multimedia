import cv2
import numpy as np
import math

# Compute the mean squared error (MSE) between two blocks of images
def MSE(block1, block2):
    # Calculate the sum of the squared differences between the pixel values of the two blocks
    # and divide it by the number of pixels to get the mean squared error
    return np.sum((block1.astype("float") - block2.astype("float")) ** 2) / float(block1.shape[0] * block1.shape[1])

# Search for the most similar block in the second image within a specified search box around the
# block being compared in the first image
def search(block1, search_box, search_img, block_width, block_height):
    # Initialize the minimum MSE to a large value
    mse = +math.inf
    # Calculate the maximum x and y coordinates that the right bottom corner of the block
    # being compared in the first image can have within the search box
    max_x = (search_box[1][0] - block_width) + 1
    max_y = (search_box[1][1] - block_height)+ 1
    # Initialize the coordinates of the most similar block in the second image to None
    block2_coordinates = None

    # Loop through all the blocks within the search box
    for y in range(search_box[0][1], max_y):
        for x in range(search_box[0][0], max_x):
                # Get the current block in the second image
                block2 = search_img[y:y+block_height, x:x+block_width]
                # Calculate the MSE between the current block in the second image and the block
                # being compared in the first image
                temp = MSE(block1, block2)
                # If the MSE is smaller than the current minimum MSE, update the minimum MSE and
                # the coordinates of the most similar block in the second image
                if temp < mse:
                    mse = temp
                    block2_coordinates = [(x, y), (x+block_width, y+block_height)]
    # Return the coordinates of the most similar block in the second image
    return block2_coordinates

# Define the search box around a block as a span around the block
# Define the search box around a block as a span around the block
def search_box(coordinates, width, height, span):
    # If the top left x coordinate of the block is within span pixels from the left edge of the image,
    # set the top left x coordinate of the search box to 0
    # Otherwise, if it is within span pixels from the right edge of the image, set it to the width minus span
    # Otherwise, set it to the top left x coordinate minus span
    if coordinates[0][0] < span:
        top_left_x = 0
    elif coordinates[0][0] > width - span:
        top_left_x = width - span
    else:
        top_left_x = coordinates[0][0] - span
        
    # If the top left y coordinate of the block is within span pixels from the top edge of the image,
    # set the top left y coordinate of the search box to 0
    # Otherwise, if it is within span pixels from the bottom edge of the image, set it to the height minus span
    # Otherwise, set it to the top left y coordinate minus span
    if coordinates[0][1] < span:
        top_left_y = 0
    elif coordinates[0][1] > height - span:
        top_left_y = height - span
    else:
        top_left_y = coordinates[0][1] - span
    
    # If the bottom right x coordinate of the block is within span pixels from the right edge of the image,
    # set the bottom right x coordinate of the search box to the width of the image
    # Otherwise, set it to the bottom right x coordinate plus span
    if coordinates[1][0] > width - span:
        bottom_right_x = width
    else:
        bottom_right_x = coordinates[1][0] + span
        
    # If the bottom right y coordinate of the block is within span pixels from the bottom edge of the image,
   
def draw_green_box(img,coordinates):
    if coordinates is not None:
        cv2.rectangle(img, 
        (coordinates[0][0], coordinates[0][1]), 
        (coordinates[1][0], coordinates[1][1]), 
        (0 , 255, 0), 2)

def draw_red_box(img,coordinates):
    if coordinates is not None:
        cv2.rectangle(img, 
        (coordinates[0][0], coordinates[0][1]), 
        (coordinates[1][0], coordinates[1][1]), 
        (0, 0, 255), 2)
def main():
    # Set the block size to 32x32 pixels
    block_width, block_height = 32, 32
    # Set the MSE threshold to 50
    seuil = 50
    # Set the span around the block to search in to 100 pixels
    span = 100

    # Read the first image
    image1 = "images/image072.png"
    img1 = cv2.imread(image1)

    # Read the second image
    image2 = "images/image092.png"
    img2 = cv2.imread(image2)

    # Convert the images to the XYZ color space
    img1_xyz = cv2.cvtColor(img1, cv2.COLOR_BGR2XYZ)
    img2_xyz = cv2.cvtColor(img2, cv2.COLOR_BGR2XYZ)

    # Extract the X channel from the images
    img1_x = img1_xyz[:,:,0]
    img2_x = img2_xyz[:,:,0]

    # Get the width and height of the images
    width = img1_x.shape[1]
    height = img1_x.shape[0]

    # Divide the first image into blocks of size block_width x block_height
    for y in range(0, height, block_height):
        for x in range(0, width, block_width):
            # Get the current block in the first image
            block1 = img1_x[y:y+block_height, x:x+block_width]
            # Define the search box around the block in the second image
            search_box_coords = search_box([(x, y), (x+block_width, y+block_height)], width, height, span)
            # Search for the most similar block within the search box in the second image
            block2_coords = search(block1, search_box_coords, img2_x, block_width, block_height)
            # Calculate the MSE between the two blocks
            mse = MSE(block1, img2_x[block2_coords[0][1]:block2_coords[1][1], block2_coords[0][0]:block2_coords[1][0]])
            # If the MSE is greater than the threshold, draw red and green boxes around the blocks
            # in the first and second images, respectively
            if mse > seuil:
                draw_red_box(img1, [(x, y), (x+block_width, y+block_height)])
                draw_green_box(img2, block2_coords)

    # Show the first and second images with the boxes drawn around the blocks
    cv2.imshow("Image 1", img1)
    cv2.imshow("Image 2", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

   
