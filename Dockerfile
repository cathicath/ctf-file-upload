# Use a lightweight PHP + Apache image
FROM php:8.0-apache

# Install Python and Flask
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install flask

# Create necessary directories
RUN mkdir -p /app/uploads
WORKDIR /app

# Copy required files
COPY app.py /app/
COPY flag.txt /flag.txt
COPY translator.py /app/
COPY templates /app/templates
COPY static /app/static

# Secure the flag
RUN chmod 400 /flag.txt

# Expose Flask (5000) and PHP (8000)
EXPOSE 5000 8000

# Start both Flask and PHP server
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]

