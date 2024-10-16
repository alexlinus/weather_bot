# Use the official Python image as the base image
FROM python:3.9-slim AS base

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

#RUN echo 'show directory'
#RUN ls -la /app
#RUN echo 'end directory'
RUN ls
#RUN #ls -la /app > /app_contents.txt && cat /app_contents.txt

# Install Poetry
RUN pip install poetry

# Install the dependencies
RUN poetry install --no-root

# Set environment variables
ENV PYTHONUNBUFFERED=1


# Make our pre-start script executable
RUN chmod +x /app/pre-start.sh

#
## Expose the port the app runs on
#EXPOSE 8000