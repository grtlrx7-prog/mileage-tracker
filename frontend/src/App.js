import { useState, useEffect } from "react";
import axios from "axios";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  Legend,
  ResponsiveContainer
} from "recharts";

function App() {

  const [token, setToken] = useState("");

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [summary, setSummary] = useState(null);
  const [monthly, setMonthly] = useState([]);
  const [locations, setLocations] = useState(null);

  const COLORS = ["#4F46E5", "#F97316"];

  // -----------------------------------
  // LOGIN
  // -----------------------------------

  const login = async () => {

    const res = await axios.post(
      `/auth/login?username=${username}&password=${password}`
    );

    setToken(res.data.access_token);

    alert("Logged in successfully!");
  };

  // -----------------------------------
  // LOAD DASHBOARD DATA
  // -----------------------------------

  const loadDashboard = async () => {

    const headers = {
      Authorization: `Bearer ${token}`
    };

    const [summaryRes, monthlyRes, locationRes] = await Promise.all([
      axios.get("/analytics/summary", { headers }),
      axios.get("/analytics/monthly", { headers }),
      axios.get("/analytics/locations/intelligence", { headers })
    ]);

    setSummary(summaryRes.data);
    setMonthly(monthlyRes.data);
    setLocations(locationRes.data);
  };

  // -----------------------------------
  // PIE DATA
  // -----------------------------------

  const pieData = summary
    ? [
        { name: "Business", value: summary.business_km },
        { name: "Personal", value: summary.personal_km }
      ]
    : [];

  return (
    <div style={{ display: "flex", fontFamily: "Arial" }}>

      {/* SIDEBAR */}
      <div style={{
        width: 200,
        height: "100vh",
        background: "#111827",
        color: "white",
        padding: 20
      }}>

        <h2>Mileage</h2>

        <button onClick={loadDashboard}>
          Dashboard
        </button>

        <button onClick={() => window.location.href = "/export/xlsx"}>
          Export
        </button>

      </div>

      {/* MAIN CONTENT */}
      <div style={{ flex: 1, padding: 20 }}>

        <h1>Dashboard</h1>

        {/* LOGIN */}
        {!token && (
          <div>
            <h2>Login</h2>

            <input
              placeholder="Username"
              onChange={(e) => setUsername(e.target.value)}
            />

            <input
              placeholder="Password"
              type="password"
              onChange={(e) => setPassword(e.target.value)}
            />

            <button onClick={login}>Login</button>
          </div>
        )}

        {/* KPI CARDS */}
        {summary && (
          <div style={{ display: "flex", gap: 20 }}>

            <div>🚗 Total KM: {summary.total_km}</div>
            <div>💼 Business: {summary.business_km}</div>
            <div>🏠 Personal: {summary.personal_km}</div>
            <div>💰 Claim: R {summary.estimated_claim}</div>

          </div>
        )}

        {/* HOME / WORK */}
        {locations && (
          <div style={{ marginTop: 20 }}>
            <h3>Smart Detection</h3>
            <p>🏠 Home: {locations.home}</p>
            <p>🏢 Work: {locations.work}</p>
          </div>
        )}

        {/* CHARTS */}
        <div style={{ display: "flex", marginTop: 30, gap: 40 }}>

          {/* PIE */}
          {summary && (
            <ResponsiveContainer width={300} height={250}>
              <PieChart>
                <Pie
                  data={pieData}
                  dataKey="value"
                  nameKey="name"
                  outerRadius={80}
                  label
                >
                  {pieData.map((entry, index) => (
                    <Cell key={index} fill={COLORS[index]} />
                  ))}
                </Pie>
                <Legend />
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          )}

          {/* LINE */}
          {monthly.length > 0 && (
            <ResponsiveContainer width={500} height={250}>
              <LineChart data={monthly}>
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />

                <Line
                  type="monotone"
                  dataKey="business_km"
                  stroke="#4F46E5"
                />

                <Line
                  type="monotone"
                  dataKey="personal_km"
                  stroke="#F97316"
                />
              </LineChart>
            </ResponsiveContainer>
          )}

        </div>

      </div>
    </div>
  );
}

export default App;