import { useState } from "react";
import api from "./api"; // assumed Axios instance

type JobPosting = {
  job_title: string | null;
  company_name: string | null;
  time_posted: string | null;
  num_applicants: string | null;
  job_info: string | null;
  job_link: string | null;
};

export default function Jobs() {
  const [jobTitle, setJobTitle] = useState("");
  const [location, setLocation] = useState("");
  const [jobs, setJobs] = useState<JobPosting[]>([]);
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);

    if (!jobTitle || !location) {
      setErr("Please enter both job title and location.");
      return;
    }

    setLoading(true);
    try {
      // GET with query params to match FastAPI (recommended)
      const res = await api.get<JobPosting[]>("/jobs/fetch/", {
        params: {
          job_title: jobTitle,
          location: location,
        },
      });
      setJobs(res.data ?? []);
    } catch (e: any) {
      console.error(e);
      setErr(e?.message ?? "Failed to fetch jobs");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: 16 }}>
      <h2>Find Jobs</h2>

      <form onSubmit={handleSubmit} style={{ display: "grid", gap: 12 }}>
        <label style={{ display: "grid", gap: 6 }}>
          Job Title
          <input
            name="jobTitle"
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
            placeholder="e.g. Python Developer"
          />
        </label>

        <label style={{ display: "grid", gap: 6 }}>
          Location
          <input
            name="location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="e.g. California"
          />
        </label>

        <button type="submit" disabled={loading || !jobTitle || !location}>
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {err && <p style={{ color: "crimson", marginTop: 12 }}>{err}</p>}

      {!loading && jobs.length > 0 && (
        <div style={{ marginTop: 24 }}>
          <h3>Results ({jobs.length})</h3>
          <ul
            style={{ listStyle: "none", padding: 0, display: "grid", gap: 12 }}
          >
            {jobs.map((j, idx) => (
              <li
                key={j.job_link ?? `${j.job_title}-${idx}`}
                style={{
                  border: "1px solid #e5e7eb",
                  borderRadius: 8,
                  padding: 12,
                }}
              >
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    gap: 12,
                  }}
                >
                  <div>
                    <strong>{j.job_title ?? "Untitled role"}</strong>
                    <div style={{ color: "#4b5563" }}>
                      {j.company_name ?? "Unknown company"}
                      {j.time_posted ? ` • ${j.time_posted}` : ""}
                    </div>
                  </div>
                  {j.job_link && (
                    <a href={j.job_link} target="_blank" rel="noreferrer">
                      View
                    </a>
                  )}
                </div>
                {j.num_applicants && (
                  <div style={{ marginTop: 6, color: "#6b7280" }}>
                    Applicants: {j.num_applicants}
                  </div>
                )}
                {j.job_info && (
                  <p style={{ marginTop: 8, color: "#374151" }}>
                    {j.job_info.slice(0, 300)}
                    {j.job_info.length > 300 ? "…" : ""}
                  </p>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}

      {!loading && jobs.length === 0 && !err && (
        <p style={{ marginTop: 16, color: "#6b7280" }}>
          Enter a job title and location, then click Search.
        </p>
      )}
    </div>
  );
}
