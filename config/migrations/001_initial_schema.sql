-- Tokyo-IA Database Schema
-- Version: 1.0.0
-- Description: Initial schema for Tokyo-IA features

-- ============================================================================
-- Phase 1: AI Intelligence & Learning
-- ============================================================================

-- Reinforcement Learning
CREATE TABLE IF NOT EXISTS agent_feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id VARCHAR(50) NOT NULL,
    task_id VARCHAR(100) NOT NULL,
    feedback_type VARCHAR(20) NOT NULL CHECK (feedback_type IN ('approved', 'rejected', 'needs_fix')),
    reward_value FLOAT NOT NULL,
    user_comments TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_agent_feedback_agent_id ON agent_feedback(agent_id);
CREATE INDEX idx_agent_feedback_task_id ON agent_feedback(task_id);
CREATE INDEX idx_agent_feedback_created_at ON agent_feedback(created_at);

-- Cost Prediction Historical Data
CREATE TABLE IF NOT EXISTS cost_predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    request_id VARCHAR(100) NOT NULL,
    tokens INT NOT NULL,
    model_name VARCHAR(50) NOT NULL,
    request_type VARCHAR(50) NOT NULL,
    complexity FLOAT NOT NULL,
    predicted_cost FLOAT NOT NULL,
    actual_cost FLOAT,
    confidence_level FLOAT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_cost_predictions_model ON cost_predictions(model_name);
CREATE INDEX idx_cost_predictions_created_at ON cost_predictions(created_at);

-- ============================================================================
-- Phase 2: Security & Monitoring
-- ============================================================================

-- Vulnerability Scans
CREATE TABLE IF NOT EXISTS vulnerability_scans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    repo_url VARCHAR(500) NOT NULL,
    branch VARCHAR(100),
    commit_sha VARCHAR(40),
    scan_date TIMESTAMP NOT NULL DEFAULT NOW(),
    vulnerabilities JSONB NOT NULL DEFAULT '[]',
    compliance_score INT NOT NULL CHECK (compliance_score >= 0 AND compliance_score <= 100),
    status VARCHAR(20) NOT NULL CHECK (status IN ('PASS', 'FAIL', 'WARNING')),
    scan_duration_ms INT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_vulnerability_scans_repo ON vulnerability_scans(repo_url);
CREATE INDEX idx_vulnerability_scans_scan_date ON vulnerability_scans(scan_date);
CREATE INDEX idx_vulnerability_scans_status ON vulnerability_scans(status);

-- Detected Vulnerabilities
CREATE TABLE IF NOT EXISTS detected_vulnerabilities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scan_id UUID NOT NULL REFERENCES vulnerability_scans(id) ON DELETE CASCADE,
    vulnerability_id VARCHAR(100) NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO')),
    category VARCHAR(100) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    line_number INT NOT NULL,
    code_snippet TEXT,
    cwe VARCHAR(20),
    cve VARCHAR(30),
    fix_suggestion TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'fixed', 'ignored', 'false_positive')),
    detected_at TIMESTAMP NOT NULL DEFAULT NOW(),
    resolved_at TIMESTAMP
);

CREATE INDEX idx_detected_vulnerabilities_scan ON detected_vulnerabilities(scan_id);
CREATE INDEX idx_detected_vulnerabilities_severity ON detected_vulnerabilities(severity);
CREATE INDEX idx_detected_vulnerabilities_status ON detected_vulnerabilities(status);

-- Incident Predictions
CREATE TABLE IF NOT EXISTS incident_predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    predicted_at TIMESTAMP NOT NULL DEFAULT NOW(),
    incident_type VARCHAR(100) NOT NULL,
    probability FLOAT NOT NULL CHECK (probability >= 0 AND probability <= 1),
    expected_time TIMESTAMP NOT NULL,
    recommended_actions JSONB NOT NULL DEFAULT '[]',
    confidence_level FLOAT NOT NULL CHECK (confidence_level >= 0 AND confidence_level <= 1),
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'occurred', 'prevented', 'false_alarm')),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_incident_predictions_expected_time ON incident_predictions(expected_time);
CREATE INDEX idx_incident_predictions_status ON incident_predictions(status);

-- ============================================================================
-- Phase 3: Gamification
-- ============================================================================

-- User Achievements
CREATE TABLE IF NOT EXISTS user_achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(100) NOT NULL,
    achievement_id VARCHAR(100) NOT NULL,
    achievement_name VARCHAR(200) NOT NULL,
    achievement_description TEXT,
    points INT NOT NULL DEFAULT 0,
    earned_at TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(user_id, achievement_id)
);

CREATE INDEX idx_user_achievements_user ON user_achievements(user_id);
CREATE INDEX idx_user_achievements_earned_at ON user_achievements(earned_at);

-- Leaderboard
CREATE TABLE IF NOT EXISTS leaderboard (
    user_id VARCHAR(100) PRIMARY KEY,
    username VARCHAR(200) NOT NULL,
    total_points INT NOT NULL DEFAULT 0,
    rank INT,
    achievements_count INT NOT NULL DEFAULT 0,
    prs_count INT NOT NULL DEFAULT 0,
    issues_count INT NOT NULL DEFAULT 0,
    reviews_count INT NOT NULL DEFAULT 0,
    last_updated TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_leaderboard_rank ON leaderboard(rank);
CREATE INDEX idx_leaderboard_points ON leaderboard(total_points DESC);

-- ============================================================================
-- Phase 4: Voice Commands
-- ============================================================================

-- Voice Command History
CREATE TABLE IF NOT EXISTS voice_command_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(100) NOT NULL,
    command_text TEXT NOT NULL,
    confidence FLOAT NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
    language VARCHAR(10) NOT NULL,
    executed_at TIMESTAMP NOT NULL DEFAULT NOW(),
    success BOOLEAN NOT NULL,
    error_message TEXT,
    execution_time_ms INT
);

CREATE INDEX idx_voice_command_user ON voice_command_history(user_id);
CREATE INDEX idx_voice_command_executed_at ON voice_command_history(executed_at);

-- ============================================================================
-- Phase 5: Collaboration
-- ============================================================================

-- Chat Messages
CREATE TABLE IF NOT EXISTS chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_id VARCHAR(100) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    username VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    message_type VARCHAR(20) NOT NULL DEFAULT 'text' CHECK (message_type IN ('text', 'code', 'system')),
    metadata JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_chat_messages_room ON chat_messages(room_id, created_at DESC);
CREATE INDEX idx_chat_messages_user ON chat_messages(user_id);

-- User Presence
CREATE TABLE IF NOT EXISTS user_presence (
    user_id VARCHAR(100) PRIMARY KEY,
    username VARCHAR(200) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'offline' CHECK (status IN ('online', 'away', 'busy', 'offline')),
    current_room VARCHAR(100),
    last_seen TIMESTAMP NOT NULL DEFAULT NOW(),
    metadata JSONB
);

CREATE INDEX idx_user_presence_status ON user_presence(status);
CREATE INDEX idx_user_presence_room ON user_presence(current_room);

-- ============================================================================
-- Audit Log
-- ============================================================================

CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(100),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id VARCHAR(100),
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_log_user ON audit_log(user_id);
CREATE INDEX idx_audit_log_created_at ON audit_log(created_at);
CREATE INDEX idx_audit_log_action ON audit_log(action);

-- ============================================================================
-- Functions and Triggers
-- ============================================================================

-- Update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to tables with updated_at
CREATE TRIGGER update_agent_feedback_updated_at
    BEFORE UPDATE ON agent_feedback
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Update leaderboard rank
CREATE OR REPLACE FUNCTION update_leaderboard_ranks()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE leaderboard
    SET rank = subquery.row_num
    FROM (
        SELECT user_id, ROW_NUMBER() OVER (ORDER BY total_points DESC) as row_num
        FROM leaderboard
    ) AS subquery
    WHERE leaderboard.user_id = subquery.user_id;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_ranks_after_points
    AFTER INSERT OR UPDATE ON leaderboard
    FOR EACH STATEMENT
    EXECUTE FUNCTION update_leaderboard_ranks();

-- ============================================================================
-- Initial Data
-- ============================================================================

-- Sample achievements
INSERT INTO user_achievements (user_id, achievement_id, achievement_name, achievement_description, points)
VALUES 
    ('system', 'first_pr', 'First PR', 'Submitted your first pull request', 10),
    ('system', 'code_reviewer', 'Code Reviewer', 'Reviewed 10 pull requests', 30),
    ('system', 'bug_hunter', 'Bug Hunter', 'Fixed 5 bugs', 50),
    ('system', 'security_champion', 'Security Champion', 'Fixed 3 security vulnerabilities', 100)
ON CONFLICT (user_id, achievement_id) DO NOTHING;

-- ============================================================================
-- Comments
-- ============================================================================

COMMENT ON TABLE agent_feedback IS 'Stores feedback for reinforcement learning';
COMMENT ON TABLE cost_predictions IS 'Historical cost prediction data for model training';
COMMENT ON TABLE vulnerability_scans IS 'Security scan results';
COMMENT ON TABLE detected_vulnerabilities IS 'Individual vulnerabilities found during scans';
COMMENT ON TABLE incident_predictions IS 'Predicted incidents for proactive alerts';
COMMENT ON TABLE user_achievements IS 'User achievement records';
COMMENT ON TABLE leaderboard IS 'User rankings and statistics';
COMMENT ON TABLE voice_command_history IS 'Voice command execution history';
COMMENT ON TABLE chat_messages IS 'Collaboration chat messages';
COMMENT ON TABLE user_presence IS 'Real-time user presence information';
COMMENT ON TABLE audit_log IS 'System audit trail';
