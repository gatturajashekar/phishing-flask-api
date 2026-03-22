const express = require("express");
const router = express.Router();
const auth = require("../middleware/auth");
const { URL } = require("url");

/* ---------------- Helper: Analyze URL ---------------- */
function analyzeURL(inputUrl) {
  let score = 0;
  let reasons = [];

  let parsed;
  try {
    parsed = new URL(inputUrl);
  } catch {
    return {
      error: "Invalid URL format"
    };
  }

  const hostname = parsed.hostname.toLowerCase();
  const fullUrl = inputUrl.toLowerCase();

  /* 🔹 1. Suspicious Keywords */
  const keywords = ["login", "verify", "secure", "account", "bank", "update", "signin"];
  keywords.forEach(word => {
    if (fullUrl.includes(word)) {
      score += 8;
      reasons.push(`Contains suspicious keyword: ${word}`);
    }
  });

  /* 🔹 2. IP Address instead of domain */
  if (/^\d+\.\d+\.\d+\.\d+$/.test(hostname)) {
    score += 25;
    reasons.push("Uses IP address instead of domain");
  }

  /* 🔹 3. Too many subdomains */
  const subdomainCount = hostname.split(".").length - 2;
  if (subdomainCount > 2) {
    score += 15;
    reasons.push("Too many subdomains");
  }

  /* 🔹 4. Suspicious TLDs */
  const suspiciousTLDs = [".xyz", ".top", ".tk", ".ru", ".ml", ".ga"];
  if (suspiciousTLDs.some(tld => hostname.endsWith(tld))) {
    score += 20;
    reasons.push("Suspicious top-level domain");
  }

  /* 🔹 5. Long URL */
  if (inputUrl.length > 80) {
    score += 10;
    reasons.push("URL is unusually long");
  }

  /* 🔹 6. Special characters */
  if (inputUrl.includes("@")) {
    score += 20;
    reasons.push("Contains '@' symbol (URL redirection trick)");
  }

  if (inputUrl.includes("%")) {
    score += 10;
    reasons.push("Contains encoded characters");
  }

  /* 🔹 7. Multiple // */
  if ((inputUrl.match(/\/\//g) || []).length > 2) {
    score += 10;
    reasons.push("Multiple '//' detected");
  }

  /* 🔹 8. HTTPS check */
  if (parsed.protocol !== "https:") {
    score += 15;
    reasons.push("Not using HTTPS");
  }

  /* 🔹 9. Hyphen abuse */
  if ((hostname.match(/-/g) || []).length >= 3) {
    score += 10;
    reasons.push("Too many hyphens in domain");
  }

  /* 🔹 10. Lookalike domains (basic) */
  const brands = ["paypal", "google", "facebook", "amazon", "bank"];
  brands.forEach(brand => {
    if (hostname.includes(brand) && !hostname.endsWith(`${brand}.com`)) {
      score += 20;
      reasons.push(`Possible impersonation of ${brand}`);
    }
  });

  /* 🔹 Normalize score */
  if (score > 100) score = 100;

  /* 🔹 Risk classification */
  let risk = "safe";
  if (score >= 60) risk = "danger";
  else if (score >= 30) risk = "warning";

  return {
    risk,
    score,
    reasons
  };
}

/* ---------------- Route ---------------- */
router.post("/", async (req, res) => {
  const { url } = req.body;

  if (!url) {
    return res.status(400).json({ message: "URL required" });
  }

  const result = analyzeURL(url);

  if (result.error) {
    return res.status(400).json({ message: result.error });
  }

  return res.json({
    url,
    risk: result.risk,
    score: result.score,
    reasons: result.reasons,
    timestamp: new Date()
  });
});

module.exports = router;