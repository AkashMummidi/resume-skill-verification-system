import React, { useState } from "react";

const UploadResume = () => {
  const [file, setFile] = useState(null);
  const [sortOption, setSortOption] = useState(null);

  const handleFileChange = (e) => {
  const selectedFile = e.target.files[0];
  if (selectedFile && selectedFile.type !== "application/pdf") {
    alert("Only PDF files are allowed");
    return;
  }
  setFile(selectedFile);
};


  const handleUpload = () => {
    if (!file) {
      alert("Please upload a PDF resume");
      return;
    }
    console.log("File uploaded:", file);
  };

  return (
    <div style={styles.page}>
      {/* Sort Dropdown */}
      <div style={styles.sortBox}>
        <label for="selectOption">Sort by </label>
        <select
          value={sortOption}
          onChange={(e) => setSortOption(e.target.value)}
          style={styles.select}
        >
            <option value="selectOption">Select an option</option>
          <option value="rating">Rating</option>
          <option value="domain">Domain</option>
        </select>
      </div>

      {/* Main Card */}
      <div style={styles.card}>
        <h1 style={styles.title}>Resume Upload Portal</h1>
        <p style={styles.subtitle}>
          Upload your resume for AI-based skill evaluation
        </p>

        {/* Upload Area */}
        <label htmlFor="fileUpload" style={styles.dropBox}>
          <div>
            <p style={styles.dropText}>
              {file ? file.name : "Drag & drop your resume here"}
            </p>
            <span style={styles.browse}>or click to browse</span>
          </div>
        </label>

        <input
          id="fileUpload"
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          style={{ display: "none" }}
        />

        <button onClick={handleUpload} style={styles.button}>
          Upload Resume
        </button>

        {/* Instructions */}
        <div style={styles.rulesBox}>
          <h3 style={styles.rulesTitle}>Submission Guidelines</h3>
          <ul style={styles.instructions}>
            <li>Resume must be in PDF format</li>
            <li>GitHub profile link is mandatory</li>
            <li>Include Codeforces / LeetCode links</li>
            <li>Include project repository or live links</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

const styles = {
  page: {
    minHeight: "100vh",
    background: "linear-gradient(135deg, #eef2ff, #f8fafc)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    fontFamily: "Inter, Arial, sans-serif",
    position: "relative",
  },

  sortBox: {
    position: "absolute",
    top: "20px",
    right: "20px",
  },

  select: {
    padding: "8px 12px",
    borderRadius: "6px",
    border: "1px solid #cbd5e1",
    fontSize: "14px",
    cursor: "pointer",
  },

  card: {
    width: "480px",
    background: "#ffffff",
    padding: "30px",
    borderRadius: "14px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
    textAlign: "center",
  },

  title: {
    margin: "0",
    fontSize: "24px",
    fontWeight: "600",
    color: "#1e293b",
  },

  subtitle: {
    margin: "8px 0 24px",
    fontSize: "14px",
    color: "#64748b",
  },

  dropBox: {
    height: "160px",
    border: "2px dashed #94a3b8",
    borderRadius: "10px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    cursor: "pointer",
    marginBottom: "20px",
    background: "#f8fafc",
  },

  dropText: {
    fontSize: "15px",
    fontWeight: "500",
    color: "#334155",
    marginBottom: "6px",
  },

  browse: {
    fontSize: "13px",
    color: "#6366f1",
  },

  button: {
    width: "100%",
    padding: "12px",
    background: "#6366f1",
    color: "#ffffff",
    border: "none",
    borderRadius: "8px",
    fontSize: "15px",
    fontWeight: "500",
    cursor: "pointer",
    marginBottom: "20px",
  },

  rulesBox: {
    textAlign: "left",
    background: "#f1f5f9",
    padding: "16px",
    borderRadius: "10px",
  },

  rulesTitle: {
    margin: "0 0 10px",
    fontSize: "15px",
    fontWeight: "600",
    color: "#1e293b",
  },

  instructions: {
    paddingLeft: "18px",
    margin: 0,
    fontSize: "14px",
    color: "#475569",
  },
};

export default UploadResume;
