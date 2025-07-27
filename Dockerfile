# Use Node.js base image
FROM node:18

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN npm install

# Expose the port (relay server listens here)
EXPOSE 3000

# Launch relay server
CMD ["node", "index.js"]
