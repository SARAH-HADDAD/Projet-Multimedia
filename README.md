## Description

This code detects changes in video frames using a block comparison technique. It employs a binary search method to optimize performance.

The code will divide the frame into blocks of the defined size, then search for the similar block within a kxk neighborhood and calculate the residue. Similar blocks will be highlighted with a square of the defined color, and the residue image will be displayed. If a block hasn't changed, it will be shown as a black rectangle.

Binary search is used to optimize the performance of change detection. A reference document is also provided for further consultation.
