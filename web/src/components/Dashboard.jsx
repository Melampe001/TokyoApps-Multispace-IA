import React from 'react'

function Dashboard() {
  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      <div className="stats">
        <div className="stat-card">
          <h3>Active Users</h3>
          <p className="stat-value">0</p>
        </div>
        <div className="stat-card">
          <h3>API Requests</h3>
          <p className="stat-value">0</p>
        </div>
        <div className="stat-card">
          <h3>System Status</h3>
          <p className="stat-value">Active</p>
        </div>
      </div>
      <div className="info">
        <p>Welcome to Tokyo-IA Admin Dashboard</p>
      </div>
    </div>
  )
}

export default Dashboard
