# Use Miniconda base image for Conda support
FROM continuumio/miniconda3

# Set the working directory inside the container
WORKDIR /app

# Copy the conda environment file
COPY conda.yml .

# Create the conda environment from the file
# The environment name 'docuparse-backend' is taken from conda.yml
RUN conda env create -f conda.yml

# Make RUN commands use the new environment:
# Note: Adjust 'docuparse-backend' if you change the name in conda.yml
SHELL ["conda", "run", "-n", "docuparse-backend", "/bin/bash", "-c"]

# Copy the application code into the container
# Assumes your FastAPI app code is in an 'app' directory next to the Dockerfile
COPY ./app ./app

# Expose the port the application will run on
EXPOSE 8000

# Define the command to run the application using Uvicorn
# This command runs within the 'docuparse-backend' conda environment
CMD ["conda", "run", "-n", "docuparse-backend", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 