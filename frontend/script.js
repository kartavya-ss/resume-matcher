const form = document.getElementById("analyze-form");
const resultsDiv = document.getElementById("results");

form.addEventListener("submit", async function (event) {
  event.preventDefault();

  const resumeText = document.getElementById("resume_text").value;
  const jobDescription = document.getElementById("job_description").value;
  const candidateName = document.getElementById("candidate_name").value;

    
    // Add this guardrail!
    if (!candidateName.trim() || !resumeText.trim() || !jobDescription.trim()) {
        resultsDiv.innerHTML = `<p style="color:red;">Error: Please fill out all fields before analyzing.</p>`;
        return; // This stops the function from running the fetch() request
    }

  resultsDiv.innerHTML = "Analyzing...";

const response = await fetch("http://127.0.0.1:8000/analyze", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    resume_text: resumeText,
    job_description: jobDescription,
    candidate_name: candidateName
  })
});

const data = await response.json();

if (!response.ok) {
  resultsDiv.innerHTML = `<p style="color:red;">Error: ${JSON.stringify(data.detail)}</p>`;
  return;
}

resultsDiv.innerHTML = `
  <h3>Match Score: ${data.match_score}</h3>
  <p><strong>Matched Skills:</strong> ${data.matched_skills.join(", ") || "None"}</p>
  <p><strong>Missing Skills:</strong> ${data.missing_skills.join(", ") || "None"}</p>
`;
loadHistory();
});

async function loadHistory() {
  const historyDiv = document.getElementById("history");
  historyDiv.innerHTML = "Loading history...";

  const response = await fetch("http://127.0.0.1:8000/history");
  const data = await response.json();

  if (!response.ok || data.length === 0) {
    historyDiv.innerHTML = "<p>No past analyses yet.</p>";
    return;
  }

  historyDiv.innerHTML = data.map(item => `
    <div class="history-card">
      <p><strong>Score:</strong> ${item.match_score}</p>
      <p><strong>Matched:</strong> ${item.matched_skills.join(", ") || "None"}</p>
      <p><strong>Missing:</strong> ${item.missing_skills.join(", ") || "None"}</p>
      <p class="timestamp">${new Date(item.created_at).toLocaleString()}</p>
    </div>
  `).join("");
}

document.addEventListener("DOMContentLoaded", loadHistory);
document.getElementById("refresh-button").addEventListener("click", loadHistory);