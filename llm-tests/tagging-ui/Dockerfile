# Use an official Node.js runtime as a parent image
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Copy package.json and yarn.lock files
COPY package.json yarn.lock ./

# Install dependencies
RUN yarn install

# Copy the rest of the application's code
COPY . .

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run the app
CMD ["yarn", "start"]
