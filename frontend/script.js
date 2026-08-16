const API_BASE_URL = "https://resume-matcher-api-fr74.onrender.com";

const form = document.getElementById("analyze-form");
const resultsDiv = document.getElementById("results");

form.addEventListener("submit", async function (event) {
  event.preventDefault();

  const candidateName = document.getElementById("candidate_name").value;
  const resumeText = document.getElementById("resume_text").value;
  const jobDescription = document.getElementById("job_description").value;
  const resumeFile = document.getElementById("resume_file").files[0];

  if (!jobDescription.trim() || (!resumeText.trim() && !resumeFile)) {
    resultsDiv.innerHTML = `<p style="color:red;">Error: Please provide a job description and either resume text or a PDF file.</p>`;
    return;
  }

  resultsDiv.innerHTML = "Analyzing...";

  let response;

  if (resumeFile) {
    const formData = new FormData();
    formData.append("job_description", jobDescription);
    formData.append("resume_file", resumeFile);

    response = await fetch(`${API_BASE_URL}/analyze-pdf`, {
      method: "POST",
      body: formData
    });
  } else {
    response = await fetch(`${API_BASE_URL}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        resume_text: resumeText,
        job_description: jobDescription,
        candidate_name: candidateName
      })
    });
  }

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

const response = await fetch(`${API_BASE_URL}/history`);
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