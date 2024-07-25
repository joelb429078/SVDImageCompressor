# SVD based - Image Compressor

![image](https://github.com/user-attachments/assets/ac2c1d55-d937-49ed-b24b-2389934c46d6)
![image](https://github.com/user-attachments/assets/cfa7a762-f958-4053-88f5-a2d1f7a30c85)

## Overview
The **Image Compressor** application is a simple yet powerful tool designed to compress images using Singular Value Decomposition (SVD). It allows users to upload an image, choose a compression ratio, and download the compressed version. The compression process significantly reduces the image size while maintaining acceptable visual quality, making it ideal for example web usage or even storage optimisation.

## Features
- **User-Friendly Interface**: Easy-to-use graphical interface built with Tkinter.
- **Image Upload**: Supports multiple image formats (PNG, JPG, JPEG, BMP, GIF).
- **Compression Ratio Slider**: Allows users to adjust the level of compression.
- **Preview**: View before and after images to compare compression results.
- **Download Option**: Download the compressed image in PNG format.

## Technical Details
### Image Compression with SVD
The core of this application is the use of **Singular Value Decomposition (SVD)**, a powerful technique in linear algebra. SVD decomposes a matrix into three other matrices, capturing essential data features. For images, this process can be visualised as breaking down the image into its component textures and patterns.

Given an image represented as a matrix \( A \), SVD allows us to express it as:
\[ A = U \Sigma V^T \]
- **\( U \)**: An orthogonal matrix containing the left singular vectors.
- **\( \Sigma \)**: A diagonal matrix with non-negative real numbers (singular values) sorted in descending order.
- **\( V^T \)**: An orthogonal matrix containing the right singular vectors.

To compress the image, we reduce the rank of \( \Sigma \) by retaining only the top \( k \) singular values. This reduction simplifies the image data, effectively compressing it. The reconstructed matrix, \( A_k \), is an approximation of the original:
\[ A_k = U_k \Sigma_k V_k^T \]
Where \( U_k \) and \( V_k^T \) are the matrices containing the first \( k \) columns and rows, respectively, and \( \Sigma_k \) is a truncated diagonal matrix.

### Implementation in the Application
- **Upload Image**: Reads and normalises the image.
- **Select Compression Ratio**: Slider determines the number of singular values to retain.
- **Compress Image**: Uses the SVD method to compress the image.
- **Display & Download**: Shows the original and compressed images, and allows the user to download the compressed version.

## License
This project is licensed under the MIT License.
