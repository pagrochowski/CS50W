# Base image: Use an official Python image with your desired version
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV WORKDIR /workspaces/CS50W

# Set the Working Directory
WORKDIR ${WORKDIR}
COPY .  /workspaces/CS50W 

# Install Dependencies 
RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-contrib \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and Install Django
RUN python -m pip install --upgrade pip
RUN pip install Django
RUN pip install -r requirements.txt


#Expose port 8000
EXPOSE 8000

# Keep the container running in interactive mode
CMD ["bash", "-c", "source /opt/venv/bin/activate && bash"]