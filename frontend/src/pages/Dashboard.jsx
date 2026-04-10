import { useState } from "react";
import { useEffect } from "react";

export default function Dashboard() {

  const [resume, setResume] = useState(null);
  const [jd, setJd] = useState(null);

  const [days, setDays] = useState("");
  const [hours, setHours] = useState("");

  const [loading, setLoading] = useState(false);

  const [detectedGithub, setDetectedGithub] = useState(null);
  const [detectedCF, setDetectedCF] = useState(null);

  const [github, setGithub] = useState("");
  const [codeforces, setCodeforces] = useState("");

  const [githubSkipped, setGithubSkipped] = useState(false);
  const [cfSkipped, setCfSkipped] = useState(false);

  const [tasks, setTasks] = useState(null);

  //  RESCHEDULE STATE
  const [rescheduledDays, setRescheduledDays] = useState([]);

  //  GET USERNAME
  const username = localStorage.getItem("username");

  const [jdSkills, setJdSkills] = useState([]);
  const [confidenceMap, setConfidenceMap] = useState({});
 
  const [currentSkill, setCurrentSkill] = useState(null);
  const [allQuestions, setAllQuestions] = useState({});
  const [answers, setAnswers] = useState({});
  const [completedSkills, setCompletedSkills] = useState([]);

  const [testScores, setTestScores] = useState({});
  const [step, setStep] = useState("upload");

  const [totalDays, setTotalDays] = useState(0);
  const [visibleDays, setVisibleDays] = useState(0);


//  AUTH CHECK (RUN ONLY ONCE)
useEffect(() => {
  const storedUser = localStorage.getItem("username");

  if (!storedUser) {
    window.location.href = "/";
  }
}, []);

useEffect(() => {
  const storedUser = localStorage.getItem("username");
  if (!storedUser) return;

  const loadPlan = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/get-plan/${storedUser}`);

      if (!res.ok) return;

      const data = await res.json();

     if (data?.daily_tasks && Object.keys(data.daily_tasks).length > 0) {
        setTasks(data.daily_tasks);
        setRescheduledDays(data.rescheduled_days || []);
        setStep("plan");

        const nonEmptyDays = Object.entries(data.daily_tasks)
  .filter(([_, tasks]) => tasks.length > 0)
  .map(([day]) => Number(day));

const actualDays = nonEmptyDays.length > 0 ? Math.max(...nonEmptyDays) : 0;

setVisibleDays(actualDays);
setTotalDays(data.total_days || actualDays);
      } else {
        setStep("upload"); // fallback
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

      setStep("verify");

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

      const skills = Object.keys(data.jd_gap_report || {});
      const confidence = data.confidence_map || {};

      if (!skills || skills.length === 0) {
        alert("No JD skills extracted — backend failed");
        return null;
      }

      setJdSkills(skills);
      setConfidenceMap(confidence);


      return skills;
    } catch (err) {
      console.error(err);
      alert("Error generating plan");
    }

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

      if (visibleDays < totalDays) {
  setVisibleDays(prev => prev + 1);
}

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
  

const submitTest = () => {
  const questions = allQuestions[currentSkill];

  let score = 0;

  questions.forEach((q, i) => {
    if (answers[i] === q.answer) score++;
  });

  const percentage = (score / questions.length) * 100;

  alert(`${currentSkill} Score: ${percentage}`);

  //  STORE SCORE
  setTestScores(prev => ({
    ...prev,
    [currentSkill]: percentage
  }));

  // mark completed
  setCompletedSkills([...completedSkills, currentSkill]);

  setStep("skills");
};

const generatePlan = async () => {

  if (Object.keys(testScores).length === 0) {
    alert("Complete tests first");
    return;
  }

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

  // IMPORTANT
  formData.append("test_scores", JSON.stringify(testScores));

  setLoading(true);

  try {
    const res = await fetch("http://127.0.0.1:8000/analyze-jd", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (data.daily_tasks) {
      setTasks(data.daily_tasks);
      setStep("plan");

      const nonEmptyDays = Object.entries(data.daily_tasks)
  .filter(([_, tasks]) => tasks.length > 0)
  .map(([day]) => Number(day));

const actualDays = nonEmptyDays.length > 0 ? Math.max(...nonEmptyDays) : 0;

setVisibleDays(actualDays);
setTotalDays(Number(days) || actualDays);
} else {
      alert("Plan generation failed");
    }

  } catch (err) {
    console.error(err);
    alert("Error generating plan");
  }

  setLoading(false);
};

if (step === "plan" && !tasks) {
  return <h2>Loading plan...</h2>;
}

if (step === "plan" && Object.keys(tasks).length === 0) {
  return <h2>No plan found. Start again.</h2>;
}
  return (
    <div className="dashboard">

      <h2 className="title">Preparation Planner</h2>

      {/* ================= STEP 1 ================= */}
      {step === "upload" &&  (
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

          <button
            className="generate-btn"
            disabled={!resume || !jd}
            onClick={handleAnalyze}>
            Verify Profiles
          </button>
        </>
      )}

      {/* ================= STEP 2 ================= */}
     {step === "verify" && (
        <div className="profile-section">

          <h3>Verify Profiles</h3>

          <div className="verify-card">

            <div className="verify-item">
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

            <div className="verify-item">
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
         <button className="generate-btn"
  onClick={async () => {
    setLoading(true);
    const skills = await handleConfirm();

    console.log("SKILLS FROM BACKEND:", skills);

    if (!skills || skills.length === 0) {
      return;
    }

    //  Generate questions immediately AFTER skills confirmed
    try {
      const res = await fetch("http://127.0.0.1:8000/generate-test", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          skills: skills
        })
      });

      const data = await res.json();

      console.log("QUESTIONS:", data);

      if (!data.questions || Object.keys(data.questions).length === 0) {
        alert("Question generation failed");
        return;
      }

      setAllQuestions(data.questions);

      // ONLY NOW move to skills page
      setStep("skills");

    } catch (err) {
      console.error(err);
      alert("Failed to generate questions");
    }
    setLoading(false);
  }}
>
  Continue
</button>
        </div>
      )}

      {step === "skills" && (
  jdSkills.length === 0 ? (
    <h2>No skills found</h2>
  ) :  (
          <div>

            {jdSkills.map((skill) => (
              <div key={skill} className="skill-card">
                <span className="skill-name">{skill}</span>

                <div className="skill-action">
                  {completedSkills.includes(skill) ? (
                    <button className="generate-btn">Completed</button>
                  ) : (
                    <button
                      className="generate-btn"
                      onClick={() => {
                        setCurrentSkill(skill);
                        setAnswers({});
                        setStep("test");
                      }}
                    >
                      Take Test
                    </button>
                    )}
                  </div>
              </div>
            ))}

            {completedSkills.length === jdSkills.length && (
              <button
                className="generate-btn full-width-btn"
                onClick={generatePlan}
              >
                Generate Plan
              </button>
            )}
          </div>
        ))}
        {step === "test" && currentSkill &&  (
          <div className="test-container">
            <h2>{currentSkill} Test</h2>

            {allQuestions[currentSkill]?.map((q, i) => (
              <div key={i} className="question-card">
                <div className="question-title">
                  {i + 1}. {q.question}
                </div>

                {q.options.map((opt, idx) => (
                  <div
                      key={idx}
                      className={`option ${answers[i] === opt ? "selected" : ""}`}
                      onClick={() => setAnswers({ ...answers, [i]: opt })}
                    >
                    {opt}
                  </div>
                ))}
              </div>
            ))}

            <button className="generate-btn" onClick={submitTest}>
              Submit Test
            </button>
          </div>
        )}

      {/* ================= FINAL TASKS ================= */}
      {step === "plan" && tasks &&  (
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

              // ALSO DELETE PLAN (important)
              await fetch(`http://127.0.0.1:8000/delete-plan/${username}`, {
                method: "DELETE"
              });

              // CORE DATA
              setTasks(null);
              setResume(null);
              setJd(null);

              // INPUTS
              setDays("");
              setHours("");

              // VERIFY STATE (YOU MISSED THIS)
              setDetectedGithub(null);
              setDetectedCF(null);
              setGithub("");
              setCodeforces("");
              setGithubSkipped(false);
              setCfSkipped(false);

              // SKILLS + TEST STATE
              setJdSkills([]);
              setConfidenceMap({});
              setCompletedSkills([]);
              setAllQuestions({});
              setAnswers({});
              setCurrentSkill(null);
              setTestScores({});

              // PLAN STATE
              setRescheduledDays([]);

              // STEP RESET
              setStep("upload");
              alert("Data cleared. Start fresh.");
            }}>
            Delete Stored Resume
          </button>

          {Object.entries(tasks)
  .filter(([day]) => Number(day) <= visibleDays)
  .sort((a, b) => Number(a[0]) - Number(b[0]))
  .map(([day, dayTasks]) => (
            <div key={day} className="day-card">

              <h3>Day {day}</h3>

              {dayTasks.map((task, i) => (
                <div key={i} className="task-row">
                  <input
                    type="checkbox"
                    checked={task.completed || false}
                    disabled={task.skipped}
                    onChange={(e) => handleCheck(day, i, e.target.checked)}/>

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