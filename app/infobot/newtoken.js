// Import the jsonwebtoken library
const jwt = require('jsonwebtoken');

// Replace this with the encryption key you will set in Botpress
const encryptionKey = 'my-secure-encryption-key-1234567890'; // Replace with your actual key

// Define the payload for the JWT
const payload = {
  id: 'user-123', // Replace with the actual user ID or claims needed
};

// Define token options
const options = {
  algorithm: 'HS256', // Ensure this matches the algorithm configured in Botpress
  expiresIn: '1h',    // Token expiration (e.g., 1 hour)
};

// Generate the JWT token
const token = jwt.sign(payload, encryptionKe`y, options);

// Output the token
console.log('Generated JWT Token:', token);