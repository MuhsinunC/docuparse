# Use Miniconda base image for Conda support
FROM continuumio/miniconda3

# Set the working directory inside the container
WORKDIR /app

# Copy the conda environment file
COPY conda.yml .

# Create the conda environment from the file
# The environment name 'docuparse-frontend' is taken from conda.yml
RUN conda env create -f conda.yml

# Make RUN commands use the new environment:
# Note: Adjust 'docuparse-frontend' if you change the name in conda.yml
SHELL ["conda", "run", "-n", "docuparse-frontend", "/bin/bash", "-c"]

# Copy the application code into the container
# Assumes your Streamlit app code (app.py, pages/, etc.) is in the frontend directory
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Define the command to run the Streamlit application
# This command runs within the 'docuparse-frontend' conda environment
CMD ["conda", "run", "-n", "docuparse-frontend", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"] 