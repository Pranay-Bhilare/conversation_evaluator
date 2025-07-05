# Dockerfile

# Use an official, lean Python base image.
# This is like choosing the model of our magic box.
FROM python:3.11-slim

# Set the working directory inside the magic box to /app
WORKDIR /app

# Copy the list of ingredients into the box first.
# Docker is smart; if this file doesn't change, it will re-use
# the cached result from the last build, making it faster.
COPY requirements.txt .

# Install all the Python libraries from the list inside the box.
RUN pip install --no-cache-dir -r requirements.txt

# Now, copy all the other files (your .py scripts, the data folder, etc.)
# into the /app directory inside the box.
COPY . .

# Tell Docker that the application inside the box will be using port 8501.
EXPOSE 8501

ENV RUNNING_IN_DOCKER=1

# This is the command that automatically runs when someone turns the box "on".
# It starts your Streamlit app.
CMD ["streamlit", "run", "ui.py", "--server.port=8501", "--server.address=0.0.0.0"]