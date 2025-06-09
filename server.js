const express = require("express");
const bodyParser = require("body-parser");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = 3000;

// Middleware to parse form data
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

// Serve static files from the "templates" directory
app.use(express.static(path.join(__dirname, "templates")));

// Redirect root route ("/") to "about.html"
app.get("/", (req, res) => {
    res.redirect("/about.html");
});

// Path to the text file for storing submissions
const filePath = path.join(__dirname, "suggestions.txt");
console.log("Submissions will be saved at:", filePath);

// Endpoint to handle form submissions
app.post("/submit", (req, res) => {
console.log("POST /submit route hit!");
    const { infrastructure, challenges, infobot, suggestion } = req.body;

    // Format the data to save in the text file
    const submission = `
Timestamp: ${new Date().toLocaleString()}
Infrastructure Rating: ${infrastructure}
Communication Challenges: ${challenges || "No response"}
InfoBot Feedback: ${infobot}
Suggestions: ${suggestion || "No response"}
-------------------------------
`;

    // Append the submission to the text file
    fs.appendFile(filePath, submission, (err) => {
        if (err) {
            console.error("Error writing to suggestions.txt:", err); // Log error if file write fails
            res.status(500).send(`<h3 style="color: red;">Internal Server Error: Could not save the submission.</h3>`);
        } else {
            console.log(`Submission successfully saved to: ${filePath}`); // Log success
            console.log("Submission Details:");
            console.log(submission); // Log the content of the submission
            res.send(`<h3 style="color: green;">Submitted Successfully! Your submission has been saved.</h3>`);
        }
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});