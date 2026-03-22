require("dotenv").config();

const express = require("express");
const mongoose = require("mongoose");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
const cors = require("cors");
const axios = require("axios");

const User = require("./models/User");
const auth = require("./middleware/auth");

const app = express();

app.use(express.json());
app.use(cors());

/* ---------------- Database Connection ---------------- */

mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log("Database connected"))
  .catch(err => console.error("DB Error:", err));


/* ---------------- Signup ---------------- */

app.post("/signup", async (req, res) => {
  try {

    let { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ message: "Email and password required" });
    }

    email = email.trim().toLowerCase();

    if (password.length < 6) {
      return res.status(400).json({ message: "Password must be at least 6 characters" });
    }

    const existing = await User.findOne({ email });

    if (existing) {
      return res.status(400).json({ message: "User already exists" });
    }

    const hashed = await bcrypt.hash(password, 10);

    await User.create({
      email,
      password: hashed
    });

    res.status(201).json({ message: "Signup successful" });

  } catch (err) {

    console.error("Signup Error:", err);
    res.status(500).json({ message: "Server error" });

  }
});


/* ---------------- Login ---------------- */

app.post("/login", async (req, res) => {
  try {

    let { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ message: "Email and password required" });
    }

    email = email.trim().toLowerCase();

    const user = await User.findOne({ email });

    if (!user) {
      return res.status(400).json({ message: "Invalid credentials" });
    }

    const valid = await bcrypt.compare(password, user.password);

    if (!valid) {
      return res.status(400).json({ message: "Invalid credentials" });
    }

    const token = jwt.sign(
      { id: user._id },
      process.env.JWT_SECRET,
      { expiresIn: "7d" }
    );

    res.json({ token });

  } catch (err) {

    console.error("Login Error:", err);
    res.status(500).json({ message: "Server error" });

  }
});


/* ---------------- Profile ---------------- */

app.get("/profile", auth, async (req, res) => {
  try {

    const user = await User.findById(req.user.id)
      .select("-password -__v");

    res.json(user);

  } catch (err) {

    console.error("Profile Error:", err);
    res.status(500).json({ message: "Server error" });

  }
});


/* ---------------- Change Password ---------------- */

app.post("/change-password", auth, async (req, res) => {
  try {

    const { oldPassword, newPassword } = req.body;

    if (!oldPassword || !newPassword) {
      return res.status(400).json({ message: "All fields required" });
    }

    if (newPassword.length < 6) {
      return res.status(400).json({ message: "New password must be at least 6 characters" });
    }

    const user = await User.findById(req.user.id);

    if (!user) {
      return res.status(404).json({ message: "User not found" });
    }

    const valid = await bcrypt.compare(oldPassword, user.password);

    if (!valid) {
      return res.status(400).json({ message: "Old password incorrect" });
    }

    const hashed = await bcrypt.hash(newPassword, 10);

    user.password = hashed;
    await user.save();

    res.json({ message: "Password updated successfully" });

  } catch (err) {

    console.error("Change Password Error:", err);
    res.status(500).json({ message: "Server error" });

  }
});


/* ---------------- Analyze URL ---------------- */

app.post("/analyze", auth, async (req, res) => {
  try {

    const { url } = req.body;

    if (!url) {
      return res.status(400).json({ message: "URL required" });
    }

    console.log("Analyzing URL:", url);

    const mlResponse = await axios.post(
      "http://127.0.0.1:5000/predict",
      { url },
      { timeout: 5000 }   // prevent hanging requests
    );

    const { prediction, features } = mlResponse.data;

    let risk = prediction === 1 ? "danger" : "safe";

    let score = prediction === 1 ? 90 : 15;

    let message =
      prediction === 1
        ? "⚠️ Phishing website detected"
        : "✅ Website appears safe";

    res.json({
      risk,
      score,
      message,
      features
    });

  } catch (err) {

    console.error("Analyze Error:", err.message);

    if (err.response) {
      return res.status(500).json({
        message: "ML service error",
        details: err.response.data
      });
    }

    res.status(500).json({
      message: "Server error",
      details: err.message
    });

  }
});


/* ---------------- Server ---------------- */

app.listen(3000, () => {
  console.log("Server running on port 3000");
});