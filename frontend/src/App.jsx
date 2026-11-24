import { useEffect, useRef, useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000";

const getSpeechRecognition = () => {
  const w = window;
  return w.SpeechRecognition || w.webkitSpeechRecognition || null;
};

const initialAuthState = {
  name: "",
  email: "",
  password: "",
};

function App() {
  const [currentView, setCurrentView] = useState("login");
  const [authMode, setAuthMode] = useState("login");
  const [authData, setAuthData] = useState(initialAuthState);
  const [user, setUser] = useState(null);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [greeting, setGreeting] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [score, setScore] = useState(null);
  const [feedback, setFeedback] = useState("");
  const [report, setReport] = useState(null);
  const [reportDownloading, setReportDownloading] = useState(false);
  const [resumeData, setResumeData] = useState(null);
  const [jdMatch, setJdMatch] = useState(null);
  const [jdInput, setJdInput] = useState("");

  const [voiceInterviewStarted, setVoiceInterviewStarted] = useState(false);
  const [voiceSupported] = useState(() => Boolean(getSpeechRecognition()));
  const [listening, setListening] = useState(false);
  const [voicePreparing, setVoicePreparing] = useState(false);
  const [voiceStatus, setVoiceStatus] = useState("");
  const [communication, setCommunication] = useState(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [cameraStatus, setCameraStatus] = useState("Camera is off.");
  const [facePresence, setFacePresence] = useState("Not checked");
  const recognitionRef = useRef(null);
  const transcriptRef = useRef("");
  const interimTranscriptRef = useRef("");
  const clearAttemptRef = useRef(false);
  const cameraStreamRef = useRef(null);
  const videoRef = useRef(null);
  const faceDetectorRef = useRef(null);

  useEffect(() => {
    if (!voiceInterviewStarted || !question) return;
    speakText(question);
  }, [voiceInterviewStarted, question]);

  useEffect(() => () => {
    recognitionRef.current?.stop();
    cameraStreamRef.current?.getTracks().forEach((track) => track.stop());
  }, []);

  function speakText(text) {
    if (!text || !("speechSynthesis" in window)) return;

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-US";
    utterance.rate = 1;
    utterance.pitch = 1;
    window.speechSynthesis.speak(utterance);
  }

  const formatTranscript = (text) => text
    .replace(/\s+([,.!?;:])/g, "$1")
    .replace(/([.!?])(?=[A-Za-z])/g, "$1 ")
    .replace(/\s{2,}/g, " ")
    .trim();

  const startSpeechRecognition = async () => {
    if (!voiceSupported) {
      setVoiceStatus("Voice input is not supported in this browser. Please use text input.");
      return;
    }

    const SpeechRecognition = getSpeechRecognition();
    if (!SpeechRecognition) {
      setVoiceStatus("Voice input is not supported in this browser. Please use text input.");
      return;
    }

    setVoicePreparing(true);

    let useOnDeviceRecognition = false;
    try {
      if (
        "processLocally" in SpeechRecognition.prototype
        && typeof SpeechRecognition.available === "function"
      ) {
        setVoiceStatus("Checking on-device speech recognition...");
        const availability = await SpeechRecognition.available({
          langs: ["en-US"],
          processLocally: true,
        });

        if (availability === "available") {
          useOnDeviceRecognition = true;
        } else if (
          (availability === "downloadable" || availability === "downloading")
          && typeof SpeechRecognition.install === "function"
        ) {
          setVoiceStatus("Preparing on-device speech recognition...");
          useOnDeviceRecognition = await SpeechRecognition.install({ langs: ["en-US"] });
        }
      }
    } catch (setupError) {
      console.warn("On-device speech setup failed; falling back to the browser speech service.", setupError);
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = "en-US";
      if (useOnDeviceRecognition) {
        recognition.processLocally = true;
      } else {
        setVoiceStatus("Starting the browser's speech recognition service...");
      }

      recognition.onstart = () => {
        setVoicePreparing(false);
        transcriptRef.current = clearAttemptRef.current ? "" : answer.trim();
        clearAttemptRef.current = false;
        interimTranscriptRef.current = "";
        setListening(true);
        setVoiceStatus(useOnDeviceRecognition ? "Listening on this device..." : "Listening using the browser's speech service...");
        setError("");
      };

      recognition.onresult = (event) => {
        const interimParts = [];

        for (let i = event.resultIndex; i < event.results.length; i += 1) {
          const result = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            transcriptRef.current = formatTranscript(`${transcriptRef.current} ${result}`);
          } else {
            interimParts.push(result);
          }
        }

        interimTranscriptRef.current = formatTranscript(interimParts.join(" "));
        const displayedText = formatTranscript(`${transcriptRef.current} ${interimTranscriptRef.current}`);
        if (displayedText) {
          setAnswer(displayedText);
          setVoiceStatus("Transcript captured. Review and submit when ready.");
        } else {
          setVoiceStatus("Listening...");
        }
      };

      recognition.onerror = (event) => {
        const message = event.error === "not-allowed"
          ? "Microphone access is blocked for this site. Allow it in the site settings beside the address bar, then reload and try again."
          : event.error === "service-not-allowed"
            ? "Speech recognition is blocked by the browser. Check your browser's privacy settings and try again."
            : event.error === "audio-capture"
              ? "No microphone is available. Connect or enable a microphone, then try again."
              : event.error === "network"
                ? "The browser's speech recognition service could not be reached. This does not necessarily mean your internet is down. Try again, use a browser with on-device speech recognition, or type your answer."
                : event.error === "no-speech"
                  ? "No speech detected. Please try again."
                  : "Speech recognition error. Please use text input.";

        setVoicePreparing(false);
        setError(message);
        setVoiceStatus(message);
        setListening(false);
      };

      recognition.onend = () => {
        setVoicePreparing(false);
        setListening(false);
        interimTranscriptRef.current = "";
        setAnswer(formatTranscript(transcriptRef.current));
      };

      recognitionRef.current = recognition;
      recognition.start();
    } catch (startError) {
      console.error("Unable to start browser speech recognition.", startError);
      setVoicePreparing(false);
      setError("Unable to start microphone. Please try again or use text input.");
      setListening(false);
      setVoiceStatus("Unable to start microphone. Please use text input.");
    }
  };

  const stopSpeechRecognition = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    setListening(false);
    setAnswer(formatTranscript(transcriptRef.current));
    setVoiceStatus(transcriptRef.current ? "Transcript captured. Review and submit when ready." : "No speech detected. You can type an answer or retry.");
  };

  const retrySpeechRecognition = () => {
    clearAttemptRef.current = true;
    transcriptRef.current = "";
    interimTranscriptRef.current = "";
    setAnswer("");
    startSpeechRecognition();
  };

  const startCamera = async () => {
    if (!navigator.mediaDevices?.getUserMedia) {
      setCameraStatus("Camera access is unavailable in this browser. The interview can continue without it.");
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      cameraStreamRef.current = stream;
      setCameraActive(true);
      setCameraStatus("Camera is active. Indicators are processed locally.");
      setFacePresence("Camera active; face detection is not available in this browser.");
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }

      if ("FaceDetector" in window) {
        faceDetectorRef.current = new window.FaceDetector({ fastMode: true, maxDetectedFaces: 1 });
        const detectFace = async () => {
          if (!videoRef.current || !cameraStreamRef.current) return;
          try {
            const faces = await faceDetectorRef.current.detect(videoRef.current);
            setFacePresence(faces.length ? "Detected" : "Not detected");
          } catch {
            setFacePresence("Unavailable");
          }
        };
        detectFace();
        faceDetectorRef.current.interval = window.setInterval(detectFace, 1500);
      }
    } catch (err) {
      const denied = err?.name === "NotAllowedError";
      setCameraStatus(denied ? "Camera permission was denied. You can continue the interview without camera indicators." : "Camera could not be started. You can continue the interview without it.");
      setCameraActive(false);
    }
  };

  const stopCamera = () => {
    cameraStreamRef.current?.getTracks().forEach((track) => track.stop());
    cameraStreamRef.current = null;
    if (videoRef.current) videoRef.current.srcObject = null;
    if (faceDetectorRef.current?.interval) window.clearInterval(faceDetectorRef.current.interval);
    faceDetectorRef.current = null;
    setCameraActive(false);
    setFacePresence("Not checked");
    setCameraStatus("Camera is off.");
  };

  const startVoiceInterview = () => {
    if (!sessionId) {
      setVoiceStatus("Upload a resume and begin the interview first.");
      return;
    }

    setVoiceInterviewStarted(true);
    setVoiceStatus("Voice interview ready.");

    if (greeting) {
      speakText(greeting);
    } else if (question) {
      speakText(question);
    }
  };

  const handleAuthChange = (event) => {
    const { name, value } = event.target;
    setAuthData((prev) => ({ ...prev, [name]: value }));
  };

  const authSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");

    const payload = authMode === "login"
      ? { email: authData.email, password: authData.password }
      : {
          full_name: authData.name,
          email: authData.email,
          password: authData.password,
          role: "candidate",
        };

    try {
      const response = await fetch(`${API}${authMode === "login" ? "/auth/login" : "/auth/register"}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok || data.message === "User not found" || data.message === "Invalid password" || data.message === "Email already registered") {
        throw new Error(data.message || "Authentication failed.");
      }

      if (authMode === "signup") {
        setAuthMode("login");
        setAuthData(initialAuthState);
        setError("Registration successful. Please sign in.");
        setLoading(false);
        return;
      }

      setUser({ email: authData.email, role: data.role || "candidate" });
      setCurrentView("dashboard");
      setAuthData(initialAuthState);
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  };

  const uploadResume = async () => {
    if (!file) {
      setError("Please select your resume first.");
      return;
    }

    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API}/resume/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error("Resume upload failed.");
      }

      setGreeting(data.greeting || "");
      setSessionId(data.session_id || "");
      setQuestion(data.first_question || "");
      setResumeData(data.data || null);
      setReport(null);
      setScore(null);
      setFeedback("");
      setCommunication(null);
      setCurrentView("resume-analysis");

      if (voiceInterviewStarted) {
        speakText(data.greeting || data.first_question || "Welcome to DeepHire AI.");
      }
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  };

  const runJdMatch = async () => {
    if (!jdInput.trim()) {
      setError("Paste a job description to compare with the resume.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API}/resume/jd-match`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_description: jdInput }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "JD matching failed.");
      }

      setJdMatch(data.data || null);
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  };

  const submitAnswer = async () => {
    if (!answer.trim()) {
      setError("Please enter your answer.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      let communicationSnapshot = communication;
      const communicationResponse = await fetch(`${API}/interview/communication-confidence`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transcript: answer }),
      });

      if (communicationResponse.ok) {
        const communicationData = await communicationResponse.json();
        const communicationScore = communicationData.score > 10 ? communicationData.score / 10 : communicationData.score;

        communicationSnapshot = {
          level: communicationData.level.replace(" Communication", ""),
          score: Number(communicationScore.toFixed(1)),
          feedback: communicationData.communication_feedback,
          summary: communicationData.summary,
          strengths: communicationData.strengths,
          improvement_points: communicationData.improvement_points,
          visual_indicators: { face_presence: facePresence, camera_active: cameraActive },
        };

        setCommunication(communicationSnapshot);
      }

      const response = await fetch(`${API}/interview/answer`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          answer,
          communication: communicationSnapshot,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error("Unable to submit answer.");
      }

      if (data.message === "Interview Completed") {
        setReport(data.report);
        setCurrentView("results");
        setQuestion("");
        setScore(null);
        setFeedback("");
        setCommunication(null);
      } else {
        setScore(data.score);
        setFeedback(data.feedback);
        setQuestion(data.next_question || "");

        if (voiceInterviewStarted && data.next_question) {
          speakText(`Good answer. Let's go a little deeper. ${data.next_question}`);
        }
      }

      setAnswer("");
    } catch (err) {
      setError(err.message);
    }

    setLoading(false);
  };

  const startInterview = () => {
    if (!sessionId) {
      setError("Upload a resume first to start the interview.");
      return;
    }

    setCurrentView("interview");
    setVoiceInterviewStarted(true);
    setVoiceStatus("Voice interview ready.");

    if (greeting) {
      speakText(greeting);
    } else if (question) {
      speakText(question);
    }
  };

  const resetInterview = () => {
    setCurrentView("dashboard");
    setQuestion("");
    setGreeting("");
    setAnswer("");
    setSessionId("");
    setResumeData(null);
    setReport(null);
    setFile(null);
    setJdInput("");
    setJdMatch(null);
  };

  const downloadInterviewReport = async () => {
    if (!sessionId) {
      setError("Complete an interview to generate a report.");
      return;
    }

    setReportDownloading(true);
    setError("");

    try {
      const response = await fetch(`${API}/interview/download-report/${sessionId}`);
      if (!response.ok) {
        throw new Error("Unable to download the interview report.");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "DeepHire_Interview_Report.pdf";
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.message || "Report download failed.");
    }

    setReportDownloading(false);
  };

  const atsScore = resumeData?.ats_score ?? 0;
  const resumeSummary = resumeData?.resume_score ?? 0;
  const skills = resumeData?.skills || [];
  const strengths = resumeData?.strengths || [];
  const weaknesses = resumeData?.weaknesses || [];

  return (
    <div className="app-shell">
      <div className="orb orb-one" />
      <div className="orb orb-two" />
      <div className="orb orb-three" />

      {currentView === "login" || currentView === "signup" ? (
        <div className="auth-layout">
          <div className="auth-panel auth-copy">
            <div className="brand-block">
              <div className="brand brand-large"><span>DeepHire</span> AI</div>
              <p>AI-powered recruitment intelligence for modern hiring teams.</p>
            </div>

            <div className="feature-list">
              <div className="feature-item">
                <span className="feature-icon">✓</span>
                <div>
                  <strong>Resume Intelligence</strong>
                  <small>ATS scoring, skill extraction, and strengths analysis</small>
                </div>
              </div>
              <div className="feature-item">
                <span className="feature-icon">✓</span>
                <div>
                  <strong>Adaptive Interviewing</strong>
                  <small>Dynamic questions, coding prompts, and score calibration</small>
                </div>
              </div>
              <div className="feature-item">
                <span className="feature-icon">✓</span>
                <div>
                  <strong>Recruitment Insights</strong>
                  <small>JD match, communication feedback, and performance reports</small>
                </div>
              </div>
            </div>
          </div>

          <div className="auth-panel auth-form-panel">
            <div className="auth-header">
              <div className="brand tiny-brand"><span>DeepHire</span> AI</div>
              <h1>{authMode === "login" ? "Welcome back" : "Create your account"}</h1>
              <p>{authMode === "login" ? "Sign in to continue your hiring workflow." : "Create an account and start your interview journey."}</p>
            </div>

            <form className="auth-form" onSubmit={authSubmit}>
              {authMode === "signup" && (
                <label>
                  <span>Full name</span>
                  <input type="text" name="name" value={authData.name} onChange={handleAuthChange} placeholder="Jane Candidate" required />
                </label>
              )}

              <label>
                <span>Email address</span>
                <input type="email" name="email" value={authData.email} onChange={handleAuthChange} placeholder="name@company.com" required />
              </label>

              <label>
                <span>Password</span>
                <input type="password" name="password" value={authData.password} onChange={handleAuthChange} placeholder="••••••••" required />
              </label>

              {error && <div className="global-error">{error}</div>}

              <button type="submit" className="primary-button" disabled={loading}>
                {loading ? "Please wait..." : authMode === "login" ? "Log in" : "Create account"}
              </button>
            </form>

            <div className="auth-switcher">
              {authMode === "login" ? (
                <>
                  Don’t have an account? <button type="button" className="text-button" onClick={() => { setAuthMode("signup"); setError(""); }}>Sign up</button>
                </>
              ) : (
                <>
                  Already have an account? <button type="button" className="text-button" onClick={() => { setAuthMode("login"); setError(""); }}>Log in</button>
                </>
              )}
            </div>
          </div>
        </div>
      ) : (
        <>
          <header className="topbar">
            <div className="brand"><span>DeepHire</span> AI</div>
            <nav className="nav-bar">
              <button type="button" className={currentView === "dashboard" ? "nav-button active" : "nav-button"} onClick={() => setCurrentView("dashboard")}>Dashboard</button>
              <button type="button" className={currentView === "resume-analysis" ? "nav-button active" : "nav-button"} onClick={() => setCurrentView("resume-analysis")}>Resume Analysis</button>
              <button type="button" className={currentView === "interview" ? "nav-button active" : "nav-button"} onClick={() => setCurrentView("interview")}>Interview</button>
              <button type="button" className={currentView === "results" ? "nav-button active" : "nav-button"} onClick={() => setCurrentView("results")}>Results</button>
            </nav>
            <div className="user-badge">
              {user?.email || "Candidate Profile"}
              <button type="button" className="text-button right" onClick={() => setCurrentView("login")}>Logout</button>
            </div>
          </header>

          <main className="content-shell">
            {currentView === "dashboard" && (
              <section className="page-grid">
                <div className="panel hero-panel">
                  <div className="eyebrow">AI recruitment platform</div>
                  <h1>Candidate dashboard</h1>
                  <p>Review resume insights, launch interview workflows, and track your recruitment readiness with DeepHire AI.</p>
                  <div className="hero-actions">
                    <button type="button" className="primary-button" onClick={() => setCurrentView("resume-analysis")}>Open Resume Analysis</button>
                    <button type="button" className="secondary-button" onClick={() => setCurrentView("interview")}>Start Interview</button>
                  </div>
                </div>

                <div className="overview-grid">
                  <div className="stat-card">
                    <span className="stat-label">ATS score</span>
                    <strong>{resumeData ? `${atsScore}/100` : "—"}</strong>
                    <small>Resume optimization</small>
                  </div>
                  <div className="stat-card">
                    <span className="stat-label">Resume score</span>
                    <strong>{resumeData ? `${resumeSummary}/100` : "—"}</strong>
                    <small>Overall fit</small>
                  </div>
                  <div className="stat-card">
                    <span className="stat-label">Interview status</span>
                    <strong>{sessionId ? "Ready" : "Pending"}</strong>
                    <small>Assessment flow</small>
                  </div>
                </div>

                <div className="panel upload-panel">
                  <div className="panel-header-row">
                    <div>
                      <div className="eyebrow">Resume intake</div>
                      <h2>Upload & analyze resume</h2>
                    </div>
                  </div>

                  <div className="upload-box">
                    <input type="file" accept=".pdf" onChange={(event) => setFile(event.target.files[0])} />
                    {file && <p className="file-label">Selected: {file.name}</p>}
                    <button type="button" className="primary-button" onClick={uploadResume} disabled={loading}>
                      {loading ? "Analyzing..." : "Analyze Resume"}
                    </button>
                  </div>
                </div>

                <div className="panel jd-panel">
                  <div className="eyebrow">JD match</div>
                  <h2>Compare against a job description</h2>
                  <textarea value={jdInput} onChange={(e) => setJdInput(e.target.value)} placeholder="Paste the job description here..." rows="5" />
                  <button type="button" className="secondary-button" onClick={runJdMatch} disabled={loading}>Run JD Match</button>
                  {jdMatch && (
                    <div className="jd-result-box">
                      <div className="pill">Match score: {jdMatch.match_score ?? jdMatch.score ?? "—"}</div>
                      <ul>
                        {(jdMatch.matched_skills || []).slice(0, 5).map((skill, index) => <li key={index}>{skill}</li>)}
                      </ul>
                    </div>
                  )}
                </div>
              </section>
            )}

            {currentView === "resume-analysis" && (
              <section className="page-grid">
                <div className="panel summary-panel">
                  <div className="eyebrow">Resume profile</div>
                  <h2>Resume analysis</h2>
                  {resumeData ? (
                    <>
                      <div className="score-ring-wrap">
                        <div className="score-ring">
                          <span>{atsScore}</span>
                          <small>ATS</small>
                        </div>
                        <div className="score-ring secondary-ring">
                          <span>{resumeSummary}</span>
                          <small>Resume</small>
                        </div>
                      </div>

                      <div className="detail-grid">
                        <div>
                          <h3>Strengths</h3>
                          <ul>
                            {strengths.length ? strengths.map((item, index) => <li key={index}>{item}</li>) : <li>No strengths recorded yet.</li>}
                          </ul>
                        </div>
                        <div>
                          <h3>Gaps</h3>
                          <ul>
                            {weaknesses.length ? weaknesses.map((item, index) => <li key={index}>{item}</li>) : <li>No critical gaps identified.</li>}
                          </ul>
                        </div>
                      </div>
                    </>
                  ) : (
                    <div className="empty-state">Upload your resume to generate ATS, skills, and strengths analysis.</div>
                  )}
                </div>

                <div className="panel insight-panel">
                  <div className="eyebrow">Key insights</div>
                  <h2>Profile summary</h2>

                  <div className="chip-list">
                    {skills.length ? skills.map((skill, index) => <span key={index} className="chip">{skill}</span>) : <span className="chip muted">No skills available</span>}
                  </div>

                  <div className="insight-box">
                    <h3>AI greeting</h3>
                    <p>{greeting || "Your resume analysis will personalize the next interview questions."}</p>
                  </div>

                  <div className="insight-box">
                    <h3>Interview readiness</h3>
                    <p>{sessionId ? "Your adaptive interview has been initialized. You are ready to proceed." : "Please upload a resume to start the interview session."}</p>
                  </div>

                  <button type="button" className="primary-button" onClick={startInterview} disabled={!sessionId}>Start interview</button>
                </div>
              </section>
            )}

            {currentView === "interview" && (
              <section className="page-grid interview-layout">
                <div className="panel interview-panel">
                  <div className="panel-header-row">
                    <div>
                      <div className="eyebrow">Smart interview</div>
                      <h2>AI interviewer</h2>
                    </div>
                    <span className="live-pill">LIVE</span>
                  </div>

                  <div className="question-card">
                    <div className="mini-label">DeepHire AI</div>
                    <h3>{question || "Your next interview question will appear here."}</h3>
                  </div>

                  <div className="camera-box">
                    <div className="panel-header-row compact">
                      <h3>Camera preview</h3>
                      <div className="inline-actions">
                        <button type="button" className="secondary-button compact" onClick={startCamera} disabled={cameraActive}>Start Camera</button>
                        <button type="button" className="secondary-button compact ghost" onClick={stopCamera} disabled={!cameraActive}>Stop</button>
                      </div>
                    </div>
                    <video ref={videoRef} className="camera-preview" muted playsInline aria-label="Live camera preview" />
                    <p>{cameraStatus}</p>
                  </div>

                  <div className="voice-box">
                    <div className="inline-actions wrap">
                      <button type="button" className="secondary-button compact" onClick={startVoiceInterview}>Voice Interview</button>
                      <button type="button" className="secondary-button compact" onClick={() => speakText(question)}>Speak Question</button>
                      <button type="button" className="primary-button compact" onClick={startSpeechRecognition} disabled={loading || listening || voicePreparing}>{voicePreparing ? "Preparing..." : "Start Answer"}</button>
                      <button type="button" className="secondary-button compact ghost" onClick={stopSpeechRecognition} disabled={!listening}>Stop</button>
                      <button type="button" className="secondary-button compact ghost" onClick={retrySpeechRecognition} disabled={loading || listening || voicePreparing}>Retry</button>
                    </div>
                    <div className="voice-status">{voiceSupported ? (listening ? "Listening..." : voiceStatus || "Ready for voice input.") : "Voice input is not supported in this browser. Please use text input."}</div>
                  </div>

                  <textarea
                    value={answer}
                    onChange={(event) => {
                      const nextAnswer = event.target.value;
                      setAnswer(nextAnswer);
                      if (!listening) {
                        transcriptRef.current = nextAnswer;
                        interimTranscriptRef.current = "";
                      }
                    }}
                    rows="6"
                    placeholder="Type your answer here or use voice input..."
                  />

                  <div className="inline-actions submit-row">
                    <button type="button" className="primary-button" onClick={submitAnswer} disabled={loading}>{loading ? "Evaluating..." : "Submit Answer"}</button>
                    <button type="button" className="secondary-button ghost" onClick={() => speakText(question)}>Repeat Question</button>
                  </div>

                  {score !== null && (
                    <div className="evaluation-box">
                      <h3>Previous answer</h3>
                      <div className="score-line">Score: {score}/10</div>
                      <p>{feedback}</p>
                    </div>
                  )}

                  {communication && (
                    <div className="communication-box">
                      <h3>Communication & visual indicators</h3>
                      <div className="pill">{communication.level}</div>
                      <p><strong>Communication score:</strong> {communication.score}/10</p>
                      <p><strong>Face presence:</strong> {facePresence}</p>
                      <p><strong>Feedback:</strong> {communication.feedback}</p>
                    </div>
                  )}
                </div>
              </section>
            )}

            {currentView === "results" && (
              <section className="panel results-panel">
                <div className="eyebrow">Final analysis</div>
                <h2>Interview report</h2>

                {report ? (
                  <>
                    <div className="report-summary">
                      <div className="report-score-box">
                        <span>{report.average_score}</span>
                        <small>/10</small>
                      </div>
                      <div>
                        <h3>Performance: {report.performance}</h3>
                        <p>{report.recommendation}</p>
                      </div>
                    </div>

                    <div className="detail-grid report-grid">
                      <div>
                        <strong>Questions</strong>
                        <p>{report.total_questions}</p>
                      </div>
                      <div>
                        <strong>Answered</strong>
                        <p>{report.answered_questions}</p>
                      </div>
                      <div>
                        <strong>Recommendation</strong>
                        <p>{report.recommendation}</p>
                      </div>
                    </div>

                    <div className="detail-grid two-col">
                      <div className="insight-box">
                        <h3>Strengths</h3>
                        <ul>
                          {(report.strengths || []).map((item, index) => <li key={index}>{item}</li>)}
                        </ul>
                      </div>
                      <div className="insight-box">
                        <h3>Areas to improve</h3>
                        <ul>
                          {(report.weaknesses || []).length ? report.weaknesses.map((item, index) => <li key={index}>{item}</li>) : <li>No major weaknesses identified.</li>}
                        </ul>
                      </div>
                    </div>

                    <div className="insight-box">
                      <h3>Communication performance</h3>
                      <p><strong>Score:</strong> {report.communication_score ?? 0}/10</p>
                      <p><strong>Level:</strong> {report.communication_level ?? "Needs Improvement"}</p>
                      <p><strong>Visual indicators:</strong> {report.visual_engagement_indicators?.face_presence || "Not available"}</p>
                    </div>
                  </>
                ) : (
                  <div className="empty-state">Your final report will appear here once the interview is complete.</div>
                )}

                <div className="inline-actions submit-row">
                  <button type="button" className="primary-button" onClick={downloadInterviewReport} disabled={reportDownloading || !sessionId}>
                    {reportDownloading ? "Preparing report..." : "Download Complete Interview Report"}
                  </button>
                  <button type="button" className="secondary-button" onClick={resetInterview}>Start New Interview</button>
                  <button type="button" className="secondary-button" onClick={() => setCurrentView("dashboard")}>Return to Dashboard</button>
                </div>
                {error && <div className="global-error inline-error">{error}</div>}
              </section>
            )}

            {error && currentView !== "results" && <div className="global-error inline-error">{error}</div>}
          </main>
        </>
      )}
    </div>
  );
}

export default App;
