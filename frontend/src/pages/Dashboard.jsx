import { useState } from "react";
import { useEffect } from "react";

export default function Dashboard() {

  const [resume, setResume] = useState(null);
  const [jd, setJd] = useState(null);

  const [days, setDays] = useState("");
  const [hours, setHours] = useState("");

  const [loading, setLoading] = useState(false);

  const [profileStep, setProfileStep] = useState(false);

  const [detectedGithub, setDetectedGithub] = useState(null);
  const [detectedCF, setDetectedCF] = useState(null);

  const [github, setGithub] = useState("");
  const [codeforces, setCodeforces] = useState("");

  const [githubSkipped, setGithubSkipped] = useState(false);
  const [cfSkipped, setCfSkipped] = useState(false);

  const [tasks, setTasks] = useState(null);

  // 🔥 RESCHEDULE STATE
  const [rescheduledDays, setRescheduledDays] = useState([]);

  // ✅ GET USERNAME
const username = localStorage.getItem("username");

// 🔥 AUTH CHECK (RUN ONLY ONCE)
useEffect(() => {
  const storedUser = localStorage.getItem("username");

  if (!storedUser) {
    window.location.href = "/";
  }
}, []);

// 🔥 LOAD PLAN ON REFRESH
useEffect(() => {
  const storedUser = localStorage.getItem("username");
  if (!storedUser) return;

  const loadPlan = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/get-plan/${storedUser}`);

      if (!res.ok) return;

      const data = await res.json();

      if (data?.daily_tasks) {
        setTasks(data.daily_tasks);
        setRescheduledDays(data.rescheduled_days || []);
        setProfileStep(true);
      }
    } catch (err) {
      console.error(err);
    }
  };

  loadPlan();
}, []);

  // ---------------------------
  // STEP 1 → VERIFY
  // ---------------------------
  const handleAnalyze = async () => {

    if (!resume || !jd) {
      alert("Upload Resume and JD");
      return;
    }

    if (!days || !hours) {
      alert("Enter days and hours");
      return;
    }

    const formData = new FormData();

    formData.append("resume_file", resume);
    formData.append("jd_file", jd);
    formData.append("username", username);
    formData.append("days_until_interview", days);
    formData.append("hours_per_day", hours);
    formData.append("verify_only", true);

    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/analyze-jd", {
        method: "POST",
        body: formData
      });

      const data = await res.json();

      setDetectedGithub(data.github || null);
      setDetectedCF(data.codeforces || null);

      setProfileStep(true);

    } catch (err) {
      console.error(err);
      alert("Error analyzing");
    }

    setLoading(false);
  };

  // ---------------------------
  // STEP 2 → FINAL PLAN
  // ---------------------------
  const handleConfirm = async () => {

    const finalGithub = githubSkipped ? "" : (github || detectedGithub);
    const finalCF = cfSkipped ? "" : (codeforces || detectedCF);

    const formData = new FormData();

    formData.append("resume_file", resume);
    formData.append("jd_file", jd);
    formData.append("username", username);
    formData.append("days_until_interview", days);
    formData.append("hours_per_day", hours);

    formData.append("github_username", finalGithub);
    formData.append("cf_username", finalCF);

    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/analyze-jd", {
        method: "POST",
        body: formData
      });

      const data = await res.json();

      setTasks(data.daily_tasks);

    } catch (err) {
      console.error(err);
      alert("Error generating plan");
    }

    setLoading(false);
  };

  // ---------------------------
  // RESCHEDULE FUNCTION
  // ---------------------------
  const handleReschedule = async (day) => {

    if (rescheduledDays.includes(Number(day))) {
      alert("Already rescheduled");
      return;
    }

    try {
      await fetch("http://127.0.0.1:8000/reschedule", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          username,
          missed_day: Number(day)
        })
      });

      setRescheduledDays([...rescheduledDays, Number(day)]);

      const res = await fetch(`http://127.0.0.1:8000/get-plan/${username}`);
      const data = await res.json();

      setTasks(data.daily_tasks);

    } catch (err) {
      console.error(err);
      alert("Reschedule failed");
    }
  };

  const handleCheck = async (day, index, value) => {
  // update UI instantly
      setTasks(prev => {
        const updated = { ...prev };
        updated[day] = updated[day].map((task, i) =>
          i === index ? { ...task, completed: value } : task
        );
        return updated;
      });

      // update backend
      await fetch("http://127.0.0.1:8000/update-task", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          username,
          day,
          task_index: index,
          completed: value
        })
      });
    };

  return (
    <div className="dashboard">

      <h2 className="title">Preparation Planner</h2>

      {/* ================= STEP 1 ================= */}
      {!profileStep && (
        <>
          <div className="dashboard-controls">

            <div className="input-group">
              <label>No of Days</label>
              <input
                value={days}
                onChange={(e) => setDays(e.target.value)}
              />
            </div>

            <div className="input-group">
              <label>No of Hours</label>
              <input
                value={hours}
                onChange={(e) => setHours(e.target.value)}
              />
            </div>

          </div>

          <div className="upload-box">

            <label className="drop-area">
              {resume ? resume.name : "Upload Resume"}
              <input
                type="file"
                hidden
                onChange={(e) => setResume(e.target.files[0])}
              />
            </label>

            <label className="drop-area">
              {jd ? jd.name : "Upload JD"}
              <input
                type="file"
                hidden
                onChange={(e) => setJd(e.target.files[0])}
              />
            </label>

          </div>

          <button className="generate-btn" onClick={handleAnalyze}>
            Verify Profiles
          </button>
        </>
      )}

      {/* ================= STEP 2 ================= */}
      {profileStep && !tasks && (
        <div className="profile-section">

          <h3>Verify Profiles</h3>

          <div className="dashboard-controls">

            <div className="input-group">
              <label>GitHub</label>

              {detectedGithub ? (
                <>
                  <span className="detected-text">{detectedGithub}</span>
                  <input
                    placeholder="Edit"
                    value={github}
                    onChange={(e) => setGithub(e.target.value)}
                  />
                </>
              ) : (
                <>
                  <span className="error-text">Not found</span>
                  <input
                    placeholder="Enter GitHub"
                    value={github}
                    onChange={(e) => setGithub(e.target.value)}
                  />
                  <button
                    className="secondary-btn"
                    onClick={() => setGithubSkipped(true)}
                  >
                    Skip
                  </button>
                </>
              )}
            </div>

            <div className="input-group">
              <label>Codeforces</label>

              {detectedCF ? (
                <>
                  <span className="detected-text">{detectedCF}</span>
                  <input
                    placeholder="Edit"
                    value={codeforces}
                    onChange={(e) => setCodeforces(e.target.value)}
                  />
                </>
              ) : (
                <>
                  <span className="error-text">Not found</span>
                  <input
                    placeholder="Enter CF"
                    value={codeforces}
                    onChange={(e) => setCodeforces(e.target.value)}
                  />
                  <button
                    className="secondary-btn"
                    onClick={() => setCfSkipped(true)}
                  >
                    Skip
                  </button>
                </>
              )}
            </div>

          </div>

          <button className="generate-btn" onClick={handleConfirm}>
            Generate Plan
          </button>

        </div>
      )}

      {/* ================= FINAL TASKS ================= */}
      {tasks && (
        <>

            <button
            className="secondary-btn"
            style={{ marginBottom: "10px" }}
            onClick={async () => {
              await fetch("http://127.0.0.1:8000/delete-resume", {
                method: "POST",
                headers: {
                  "Content-Type": "application/json"
                },
                body: JSON.stringify({ username })
              });

              // 🔥 ALSO DELETE PLAN (important)
              await fetch(`http://127.0.0.1:8000/delete-plan/${username}`, {
                method: "DELETE"
              });

              // 🔥 RESET UI STATE
              setTasks(null);
              setProfileStep(false);
              setResume(null);
              setJd(null);
              setRescheduledDays([]);

              alert("Data cleared. Start fresh.");
            }}>
            Delete Stored Resume
          </button>

          {Object.entries(tasks).map(([day, dayTasks]) => (
            <div key={day} className="day-card">

              <h3>Day {day}</h3>

              {dayTasks.map((task, i) => (
                <div key={i} className="task-row">
                  <input
                    type="checkbox"
                    checked={task.completed || false}
                    disabled={task.skipped}
                    onChange={(e) => handleCheck(day, i, e.target.checked)}/>

                  {/* ✅ MODIFIED PART */}
                  <div className="task-content">
                    <span
                      style={{
                        textDecoration: task.completed ? "line-through" : "none",
                        opacity: task.completed ? 0.6 : 1,
                        transition: "0.2s"
                      }}
                    >
                      {task.task}
                    </span>

                    <div style={{ display: "flex", gap: "10px", fontSize: "12px" }}>
                      <span style={{ color: "#888" }}>
                        {task.skill?.charAt(0).toUpperCase() + task.skill?.slice(1)}
                      </span>

                      <span>
                        {task.blocks ? `${task.blocks} hr` : "1 hr"}
                      </span>
                    </div>
                  </div>

                </div>
              ))}

              <button
                className="reschedule-btn"
                disabled={rescheduledDays.includes(Number(day))}
                onClick={() => handleReschedule(day)}
              >
                {rescheduledDays.includes(Number(day))
                  ? "Rescheduled"
                  : `Reschedule Day ${day}`}
              </button>

            </div>
          ))}

            <button
            style={{
              marginTop: "20px",
              backgroundColor: "#e53935",
              color: "white",
              padding: "12px 20px",
              fontSize: "16px",
              border: "none",
              borderRadius: "6px",
              cursor: "pointer",
            }}
            onClick={() => {
              localStorage.removeItem("username"); 
              setTasks(null); 
              setProfileStep(false); 
              window.location.href = "/";
            }}
          >
            Logout
          </button>
        </>
      )}

      {loading && <p style={{ textAlign: "center" }}>Processing...</p>}

    </div>
      
  );
}