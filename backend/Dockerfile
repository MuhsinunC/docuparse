# Use Miniconda base image for Conda support
FROM continuumio/miniconda3

# Set the working directory inside the container
WORKDIR /app

# Copy the conda environment file
COPY conda.yml .

# Create the conda environment from the file
# The environment name 'docuparse-backend' is taken from conda.yml
RUN conda env create -f conda.yml

# Initialize conda for bash and activate the environment by default for interactive shells
# Using bash -c to ensure commands run correctly in a single layer
RUN bash -c "conda init bash && echo 'conda activate docuparse-backend' >> /root/.bashrc"

# Make RUN commands use the new environment:
# Note: Adjust 'docuparse-backend' if you change the name in conda.yml
# SHELL ["conda", "run", "-n", "docuparse-backend", "/bin/bash", "-c"]

# Copy the application code into the container
# Assumes your FastAPI app code is in an 'app' directory next to the Dockerfile
# COPY ./app ./app
COPY . .

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the port the application will run on
EXPOSE 8000

# Define the command to run the application using Uvicorn
# This command runs within the 'docuparse-backend' conda environment
# CMD ["/bin/bash", "-c", "source activate docuparse-backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"]
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 