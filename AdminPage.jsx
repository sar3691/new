import React, { useState, useEffect } from "react";
import "./AdminPage.css"; // 👈 Import external CSS

const AdminPage = () => {
  const [students, setStudents] = useState([]);
  const [teams, setTeams] = useState([]);
  const [activeTab, setActiveTab] = useState("students");
  const [teamFilter, setTeamFilter] = useState("");
  const [eventFilter, setEventFilter] = useState("");

  const API_URL = import.meta.env.VITE_URL;

  const fetchStudents = () => {
    fetch(`${API_URL}/students`)
      .then((res) => res.json())
      .then((data) => setStudents(data))
      .catch((err) => console.error("Error fetching students:", err));
  };

  const fetchTeams = () => {
    fetch(`${API_URL}/teams`)
      .then((res) => res.json())
      .then((data) => setTeams(data))
      .catch((err) => console.error("Error fetching teams:", err));
  };

  useEffect(() => {
    fetchStudents();
    fetchTeams();
  }, []);

  const filteredStudents = students.filter((student) => {
    const teamMatch = teamFilter
      ? student.teamNo?.toLowerCase().includes(teamFilter.toLowerCase())
      : true;

    const eventMatch = eventFilter
      ? student.events.some((e) =>
          e.toLowerCase().includes(eventFilter.toLowerCase())
        )
      : true;

    return teamMatch && eventMatch;
  });

  const handleStatusChange = async (studentId, currentStatus) => {
    const newStatus = currentStatus === "Present" ? "Absent" : "Present";
    try {
      const response = await fetch(`${API_URL}/students/${studentId}/status`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ status: newStatus }),
      });

      if (response.ok) {
        setStudents((prevStudents) =>
          prevStudents.map((s) =>
            s._id === studentId ? { ...s, status: newStatus } : s
          )
        );
      } else {
        console.error("Failed to update student status");
      }
    } catch (error) {
      console.error("Error updating student status:", error);
    }
  };

  return (
    <div className="admin-container">
      <h1 className="admin-title">Admin Panel</h1>

      <div className="tabs">
        <button
          className={activeTab === "students" ? "active" : ""}
          onClick={() => setActiveTab("students")}
        >
          Students
        </button>
        <button
          className={activeTab === "teams" ? "active" : ""}
          onClick={() => setActiveTab("teams")}
        >
          Teams
        </button>
      </div>

      {activeTab === "students" && (
        <div className="tab-content">
          <h2>Student Details</h2>

          <div className="filters">
            <input
              type="text"
              value={teamFilter}
              onChange={(e) => setTeamFilter(e.target.value)}
              placeholder="Search by Team No (e.g., VT01)"
            />
            <input
              type="text"
              value={eventFilter}
              onChange={(e) => setEventFilter(e.target.value)}
              placeholder="Search by Event (e.g., Web Design)"
            />
          </div>

          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Student No</th>
                  <th>Name</th>
                  <th>Reg No</th>
                  <th>Team No</th>
                  <th>Team Name</th>
                  <th>Events</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredStudents.length > 0 ? (
                  filteredStudents.map((s) => (
                    <tr key={s._id}>
                      <td>{s.studentNo}</td>
                      <td>{s.name}</td>
                      <td>{s.regNo}</td>
                      <td>{s.teamNo}</td>
                      <td>{s.teamName}</td>
                      <td>{s.events.join(", ")}</td>
                      <td>{s.status}</td>
                      <td>
                        <button
                          className={`status-btn ${
                            s.status === "Present" ? "danger" : "success"
                          }`}
                          onClick={() =>
                            handleStatusChange(s._id, s.status)
                          }
                        >
                          Mark {s.status === "Present" ? "Absent" : "Present"}
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="8" className="empty-msg">
                      No students found matching your criteria.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === "teams" && (
        <div className="tab-content">
          <h2>Team Details</h2>

          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Team No</th>
                  <th>Team Name</th>
                  <th>College</th>
                  <th>Department</th>
                  <th>Members</th>
                  <th>Events</th>
                </tr>
              </thead>
              <tbody>
                {teams.length > 0 ? (
                  teams.map((t) => (
                    <tr key={t._id}>
                      <td>{t.teamNo}</td>
                      <td>{t.teamName}</td>
                      <td>{t.collegeName}</td>
                      <td>{t.dept}</td>
                      <td>
                        {t.members.map((m, i) => (
                          <div key={i}>
                            {m.studentNo} - {m.name} ({m.regNo}) -{" "}
                            <strong>{m.status}</strong>
                          </div>
                        ))}
                      </td>
                      <td>
                        {Object.keys(t.event).length > 0
                          ? Object.keys(t.event).join(", ")
                          : "No events"}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="6" className="empty-msg">
                      No teams found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminPage;
