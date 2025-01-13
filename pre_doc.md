# **Presentation Script: User-Assisted Shadow Detection and Removal Algorithm Based on Thresholding and Region Growing**

---

## **Slide 1: Title Slide**

Good morning, everyone.  
Today, we will present our work on **"User-Assisted Shadow Detection and Removal Algorithm Based on Thresholding and Region Growing."**  
This project was conducted by Yining Jiang, Zhaojun Ni, and Lanxuan Zhang.
The presentation will cover the problem we addressed, the methods we applied, our proposed solution pipeline, and the results we achieved.

---

## **Slide 2: Problem**

As we know, shadows in images can significantly affect **object recognition** and **scene understanding**.  
Shadows can make it difficult to **separate objects from their shadows**, which is crucial for accurate image analysis.  
While deep learning (DL) approaches exist, they often require **extensive computational resources**, which may not always be feasible.  
Our goal is to develop a simpler, user-assisted method for shadow detection and removal while maintaining accuracy.



To reach this goal, we applied several image-processing techniques from this lecture:  
1. **Color Space Analysis** (from Lecture 08) – We used the **YCbCr color space** to get luminance information to detect shadows.
2. **Thresholding** (from Lecture 10) – This helped us distinguish between shadow and non-shadow regions.  
3. **Region Growing** (from Lecture 10) – Specifically, we used **Seeded Region Growing** to expand regions from user-defined seed points.  
4. **Morphological Image Processing** (from Lecture 08) – This included operations like **erosion** and **dilation** to refine the shadow mask.  
5. **Gaussian Filtering** (from Lecture 06) – We used this for smooth transitions in the final image.  

These methods allow us to remove shadows both efficiently and effectively.

---

## **Slide 3: Shadow Detection**

In the first step, we first convert the RGB image to YCbCr color space. Then Calculate the mean (μ_Y) and the standard deviation (σ_Y) of the luminance (**Y**) channel, and use the equation shown below to get **Threshold**. Then apply thresholding to detect shadow regions. 
Notice that This ratio is a **user-tunable parameter**, allowing flexibility depending on the image characteristics.  
The goal is to identify regions that are likely to be shadows based on their luminance and chrominance values in the YCbCr color space.

---

## **Slide 4: Seed Selection**

Next, we move to the 2nd step **seed selection**.  
User can select seed points using MATLAB’s **ginput function**, and in our algorithm we will check whether the selected points are within the image range and mark them.
We then apply **morphological operations** (opening or closing) to refine the shadow mask.  

- A **positive radius** corresponds to **opening** (erosion followed by dilation).  
- A **negative radius** corresponds to **closing** (dilation followed by erosion).  

And we can change the strength of opening or closing by changing the value of Radius. But you can notice that, when we using opening operation, shadow mask may be separated and not connected, and when we using closing operation, the shadow mask background may be not very clean.

But don't worry, SRG helps!!

---

## **Slide 5: Region Growing**

So let's turn to the next step, **region growing**.  
Starting from the seed points, we **dilate** the region using a disk-shaped structuring element while we can also change the **Radius** of the structuring element.
This growth process continues until the grown region no longer changes.
We then merge all the grown regions using **OR operation**.  
These steps are repeated till the region growing for all seeds is completed.

---

## **Slide 6: Boundary Extraction**

Once the shadow region is identified, we extract its boundary.  
We use **erosion** to shrink the shadow region and isolate the inner boundary.  
Then, we apply **dilation** to expand the boundary and create a smooth transition area. 
The Region are shown in these equation. 
The size of the erosion and dilation radius are also **user-tunable parameters**, allowing control over the thickness and smoothness of the boundary.
For example, the larger the erosion radius is, the thicker the boundary will be and The larger the dilation radius is, the wider the smooth region will be.

---

## **Slide 7: Shadow Removal**

In the final step, we remove the shadow, from the equations below,
We calculate the **mean (μ)** and **standard deviation (σ)** for the shadow, light, and boundary regions.  
Using these values, we apply a **linear transformation** to adjust the brightness of the shadow and boundary regions.  
Finally, we perform **Gaussian smoothing** on the smooth region to ensure smooth transitions between the shadow and light regions.  
This step is applied to the R, G, and B channels respectively to maintain color consistency.

Also, you can increase **offset** to gain brightness compensation and adjust **sigma** to have a more pronounced blurring effect.

## **Slide 8: Video**
Now let us show our whole shadow removal process from this video.

## **Slide 9-16: Results and Discussion**

Now, let’s look at some results.  

[Slide9] This image shows a quite good shadow removal effect.

[Slide10] The effect of shadow removal on this picture is also acceptable. However, it can be seen that we have made the smooth region of the boundary rather thick (large sigma in Gaussian filter). As a result, although the color transition on the boundary appears smooth, it seems that there is no texture on the boundary.

[Slide11] This picture is challenging because of its grassland background, not as smooth as the ground. Initially, our shadow mask was messy. But with our algorithm, we can well extract shadow boundary, and the shadow removal effect is acceptable. We used brightness offset compensation here.

[Slide12] The problem with this picture is that the brightness of the gaps between the floor tiles is lower than that of the human shadow. So when extracting the shadow mask, the human shadow and the gaps between the floor tiles will be connected together. You can see that in the result, the colors of some gaps have also been brightened.

[Slide15] We did well in shadow extraction for this picture. But in color restoration, using global mean and variance for estimation made the walls and ground restored to similar colors.

[Slide16] This picture has a similar issue. As sand takes up a large proportion, the shoe shadow's restored color is too close to sand's. A future solution is to use different neighboring pixels for estimation based on shadow area proportions.

---

## **Slide 18: References**

Our work builds on several key studies:  

These references provided the foundation for our approach.

---

## **Slide 19: END**

In conclusion, we have developed a **user-assisted shadow detection and removal algorithm** that combines **thresholding** and **region growing**.  

Our method is **simple**, **user-friendly**, and produces high-quality results.  
---