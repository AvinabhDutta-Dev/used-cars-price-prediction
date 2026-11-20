# Deploying to Hugging Face Spaces

This guide explains how to deploy the Used Cars Price Prediction application on [Hugging Face Spaces](https://huggingface.co/spaces).

The project uses Gradio to provide an interactive web interface for predicting used-car resale prices. The deployed application is publicly accessible through Hugging Face Spaces.

**Live Application:** [Used Cars Price Prediction](https://huggingface.co/spaces/AvinabhDutta-Dev/used-cars-price-prediction)

## 1. Deployment Overview

The project maintains two separate application environments:

| Environment | Purpose |
|---|---|
| GitHub repository | Contains the original project, including the Flask application, frontend, backend, tests, and Gradio application source. |
| Hugging Face Space | Hosts the deployed Gradio application and its deployment-specific configuration. |

The Hugging Face deployment uses Gradio rather than the original Flask frontend and REST API workflow.

## 2. Hugging Face Space Configuration

The Hugging Face Space was configured with the following settings:

| Setting | Configuration |
|---|---|
| Space name | `used-cars-price-prediction` |
| SDK | Gradio |
| Visibility | Public |
| Python version | Python 3.12 |
| License | MIT |
| Gradio version | 6.31.0 |
| Hardware | ZeroGPU |

The deployed Space is available at:

`https://huggingface.co/spaces/AvinabhDutta-Dev/used-cars-price-prediction`

## 3. Application Files and Dependencies

The Space requires the Gradio application, trained machine learning model, supporting Python modules, and optimized car images.

Important application components include:

- `app.py` — Gradio application entry point.
- `model/car_price_prediction_model.pkl` — trained machine learning model.
- `server/prediction.py` — prediction-related functionality.
- `server/car_images.py` — car image handling.
- `assets/cars/optimized/` — optimized WebP images used by the interface.
- `requirements.txt` — Python dependencies.

The application uses Gradio 6.31.0 and scikit-learn 1.9.1, along with the other dependencies specified in the deployment environment.

## 4. Uploading Large Files

The trained machine learning model is a relatively large file. Git LFS and Hugging Face's Xet-backed storage support were used to upload the model and image assets.

The deployment includes:

- The trained `.pkl` model.
- Fifteen optimized `.webp` car images.
- The Python application and supporting modules.

Using optimized WebP images helps reduce the size of the image assets while retaining their visual purpose in the interface.

## 5. ZeroGPU Compatibility

The Hugging Face Space uses ZeroGPU hardware. During deployment, the application initially encountered the following startup error:

`No @spaces.GPU function detected during startup`

To resolve this issue, a ZeroGPU compatibility handler was added to the Hugging Face-specific version of `app.py`.

The deployment-specific implementation includes:

- Importing the `spaces` package.
- Defining a function decorated with `@spaces.GPU`.
- Connecting the function to a hidden Gradio button.

This provides the GPU function registration required by the Space during startup.

**Important:** This compatibility implementation belongs to the Hugging Face deployment copy. It is not part of the original GitHub application's `app.py`. Keep the two versions separate unless the deployment architecture is intentionally changed.

## 6. Running and Testing the Deployment

After uploading the application files and dependencies, Hugging Face Spaces builds and starts the application.

The deployed application was verified through the following checks:

1. The Space completed its build and startup process.
2. The Gradio interface loaded successfully.
3. The vehicle specification inputs were displayed correctly.
4. A prediction was generated successfully using the trained model.
5. The predicted resale price was displayed in Indian Rupees (INR).

The deployed application was also tested using a sample Maruti Swift prediction.

## 7. Troubleshooting

### ZeroGPU startup error

**Error:**

`No @spaces.GPU function detected during startup`

**Resolution:**

Check that the Hugging Face-specific application contains the required `spaces` import, GPU-decorated handler, and hidden Gradio button connection.

### Application build failure

If the Space fails to build:

- Check the build logs for missing dependencies.
- Verify that the required packages are available in the deployment environment.
- Confirm that the application entry point and supporting files have been uploaded.
- Check that the model and image assets are present in the Space repository.

### Missing model or image files

Verify that the trained model and optimized image assets were uploaded successfully. Large files should be handled using the appropriate Git LFS/Xet storage support.

## 8. Important Deployment Notes

- The Hugging Face Space hosts the Gradio application, not the original Flask frontend.
- The original Flask application and REST API remain part of the GitHub project.
- The ZeroGPU compatibility handler is specific to the Hugging Face deployment.
- The car photographs are provided for visual reference and do not influence the predicted resale price.
- The hosted application uses the trained machine learning pipeline to generate predictions from the supplied vehicle specifications.

## 9. Live Deployment

Access the deployed application here:

**[Launch Used Cars Price Prediction on Hugging Face Spaces](https://huggingface.co/spaces/AvinabhDutta-Dev/used-cars-price-prediction)**

For the complete source code and project documentation, visit the [GitHub repository](https://github.com/AvinabhDutta-Dev/used-cars-price-prediction).
