import React, { useState } from 'react';

function App() {
  const [fileContent, setFileContent] = useState('');
  const [fileName, setFileName] = useState('');

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setFileName(file.name);

    const reader = new FileReader();
    reader.onload = (e) => {
      setFileContent(e.target.result);
    };
    reader.readAsText(file);
  };

  const handleSubmit = () => {
    alert("Submit button clicked! (You could now send this to an API.)");
    console.log("Transcript:", fileContent);
  };

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      height: "100vh",
      backgroundColor: "#f9f9f9",
      fontFamily: "'Helvetica Neue', Arial, sans-serif",
      color: "#333",
    }}>
      <div style={{
        width: "90%",
        maxWidth: "600px",
        backgroundColor: "#fff",
        borderRadius: "10px",
        boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
        padding: "20px",
        textAlign: "center",
      }}>
        <h2 style={{ marginBottom: "20px", fontSize: "24px", fontWeight: "bold" }}>Meeting Transcript Uploader</h2>
        <input
          type="file"
          accept=".txt"
          onChange={handleFileUpload}
          style={{
            display: "block",
            margin: "0 auto 20px auto",
            padding: "10px",
            borderRadius: "5px",
            border: "1px solid #ccc",
            fontSize: "16px",
          }}
        />
        <button
          onClick={handleSubmit}
          style={{
            backgroundColor: "#007BFF",
            color: "#fff",
            border: "none",
            borderRadius: "5px",
            padding: "10px 20px",
            fontSize: "16px",
            cursor: "pointer",
            transition: "background-color 0.3s",
          }}
          onMouseOver={(e) => e.target.style.backgroundColor = "#0056b3"}
          onMouseOut={(e) => e.target.style.backgroundColor = "#007BFF"}
        >
          Submit
        </button>

        {fileName && (
          <div style={{ marginTop: "20px", textAlign: "left" }}>
            <h4 style={{ fontSize: "18px", fontWeight: "bold" }}>File: {fileName}</h4>
            <textarea
              value={fileContent}
              readOnly
              rows="10"
              cols="80"
              style={{
                width: "100%",
                borderRadius: "5px",
                border: "1px solid #ccc",
                padding: "10px",
                fontSize: "14px",
                resize: "none",
              }}
            />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
