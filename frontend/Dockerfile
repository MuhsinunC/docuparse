# Use Miniconda base image for Conda support
FROM continuumio/miniconda3

# Set the working directory inside the container
WORKDIR /app

# Copy the conda environment file
COPY conda.yml .

# Create the conda environment from the file
# The environment name 'docuparse-frontend' is taken from conda.yml
RUN conda env create -f conda.yml

# Copy the application code into the container
# Assumes your Streamlit app code (app.py, pages/, etc.) is in the frontend directory
COPY . .

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the port Streamlit runs on
EXPOSE 8501

# Set the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

# Define the command for the entrypoint script to execute
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"] 