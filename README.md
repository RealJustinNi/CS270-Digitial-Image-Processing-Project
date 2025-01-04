# Shadow Detection and Removal

This project implements a MATLAB-based system for shadow detection and removal. It includes the project report, relevant source code, and final results. You can run the complete workflow by launching the MATLAB App file `shadowmover`.

## Project Structure

- **`dataset/`**: Contains the shadow dataset.
  - `shadow/`: Images with shadows.
  - `shadow_free/`: Corresponding shadow-free images.
- **`old/`**: Stores historical versions of the project and related works.
- **`src/`**: Contains the final source code.
  - `detect_shadow.m`: Shadow detection based on luminance.
  - `extract_boundary.m`: Module for boundary extraction.
  - `main.m`: Main script to execute the full pipeline.
  - `region_growing.m`: Implements region-growing shadow detection.
  - `select_seed.m`: Interactive seed point selection.
  - `shadow_removal.m`: Shadow removal using normal reference regions.
  - `shadowmover.mlapp`: MATLAB App providing a GUI to run the project.
- **`CS270_Project5.pdf`**: Project specification for the course.
- **`DIP2024_FinalProject_Group2_Report.pdf`**: Final report documenting the implementation and results.
- **`README.md`**: Project description and documentation.


## Quick Start

1. **Run the MATLAB App**  
   Double-click `src/shadowmover.mlapp` to launch the MATLAB App and experience the full workflow of shadow detection and removal.

2. **Run the Code**  
   To manually run the code:
   - Open MATLAB and set the working directory to `src/`.
   - Run the `main.m` file to execute the entire workflow.

3. **View Results**  
   The outputs of the code (e.g., shadow masks, shadow-free images) are saved in the `result/outputs/` folder. Two demo videos of the workflow is available in `result/demo/`.

## Module Descriptions

- `detect_shadow.m`: Shadow detection based on the luminance channel.
- `extract_boundary.m`: Extracts shadow boundaries for further processing.
- `main.m`: Main function that integrates all modules and executes the workflow.
- `region_growing.m`: Region growing algorithm based on seed points.
- `select_seed.m`: Interactive module for selecting shadow seed points.
- `shadow_removal.m`: Shadow removal algorithm that uses the surrounding normal region as a reference.
- `shadowmover.mlapp`: MATLAB App that provides a user-friendly interface for the entire project.

## Dataset

- `dataset/shadow/`: Contains test images with shadows.
- `dataset/shadow_free/`: Corresponding shadow-free images for comparison and evaluation.

## Reports and Documentation

- **CS270 Project 5**: Project description and initial requirements.
- **DIP2024_FinalProject_Group2_Report**: Final project report, detailing implementation, results, and analysis.

## Version Control

The `old/` folder contains historical versions of the project and reference materials related to shadow detection.

---

If you have any questions, please feel free to contact the development team!
