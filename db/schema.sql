-- Tokyo-IA Agent Orchestration Database Schema
-- PostgreSQL 14+

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Agents table - Stores all registered agents
CREATE TABLE agents (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(200) NOT NULL,
    model VARCHAR(100) NOT NULL,
    specialties TEXT[] NOT NULL,
    backstory TEXT,
    personality_emoji VARCHAR(10),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'maintenance')),
    total_tasks_completed INTEGER DEFAULT 0,
    total_tokens_used BIGINT DEFAULT 0,
    average_latency_ms FLOAT DEFAULT 0,
    success_rate FLOAT DEFAULT 100.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Workflows table - Multi-agent workflow orchestration
CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
    workflow_type VARCHAR(100),
    initiator VARCHAR(100),
    total_tasks INTEGER DEFAULT 0,
    completed_tasks INTEGER DEFAULT 0,
    failed_tasks INTEGER DEFAULT 0,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_ms INTEGER,
    total_tokens_used INTEGER DEFAULT 0,
    total_cost_usd DECIMAL(10, 6) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Agent tasks table - Individual task execution records
CREATE TABLE agent_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id VARCHAR(50) NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    workflow_id UUID REFERENCES workflows(id) ON DELETE CASCADE,
    task_type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_ms INTEGER,
    tokens_used INTEGER DEFAULT 0,
    cost_usd DECIMAL(10, 6) DEFAULT 0,
    retry_count INTEGER DEFAULT 0,
    parent_task_id UUID REFERENCES agent_tasks(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Agent metrics table - Time-series performance metrics
CREATE TABLE agent_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id VARCHAR(50) NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    metric_type VARCHAR(50) NOT NULL,
    metric_value FLOAT NOT NULL,
    metric_unit VARCHAR(20),
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    context JSONB DEFAULT '{}'::jsonb
);

-- Agent interactions table - Communication between agents
CREATE TABLE agent_interactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID REFERENCES workflows(id) ON DELETE CASCADE,
    from_agent_id VARCHAR(50) NOT NULL REFERENCES agents(id),
    to_agent_id VARCHAR(50) NOT NULL REFERENCES agents(id),
    interaction_type VARCHAR(50) NOT NULL,
    message TEXT,
    payload JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- User sessions table - Track user interactions
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100) NOT NULL,
    session_token VARCHAR(255) UNIQUE NOT NULL,
    device_info JSONB,
    ip_address INET,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_activity_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Indexes for performance
CREATE INDEX idx_agent_tasks_agent_id ON agent_tasks(agent_id);
CREATE INDEX idx_agent_tasks_workflow_id ON agent_tasks(workflow_id);
CREATE INDEX idx_agent_tasks_status ON agent_tasks(status);
CREATE INDEX idx_agent_tasks_created_at ON agent_tasks(created_at DESC);
CREATE INDEX idx_workflows_status ON workflows(status);
CREATE INDEX idx_workflows_created_at ON workflows(created_at DESC);
CREATE INDEX idx_agent_metrics_agent_id ON agent_metrics(agent_id);
CREATE INDEX idx_agent_metrics_recorded_at ON agent_metrics(recorded_at DESC);
CREATE INDEX idx_agent_interactions_workflow_id ON agent_interactions(workflow_id);
CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_active ON user_sessions(is_active) WHERE is_active = true;

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for automatic updated_at
CREATE TRIGGER update_agents_updated_at BEFORE UPDATE ON agents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workflows_updated_at BEFORE UPDATE ON workflows
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert the 5 specialized agents
INSERT INTO agents (id, name, role, model, specialties, backstory, personality_emoji, status) VALUES
(
    'akira-001',
    'Akira',
    'Code Review Master',
    'claude-opus-4.1',
    ARRAY['security', 'performance', 'architecture', 'code-quality'],
    'A disciplined samurai of code quality. Akira has spent decades mastering the art of software craftsmanship, with a keen eye for security vulnerabilities and architectural flaws. Every line of code is reviewed with the precision of a master swordsman.',
    '侍',
    'active'
),
(
    'yuki-002',
    'Yuki',
    'Test Engineering Specialist',
    'openai-o3',
    ARRAY['unit-testing', 'integration-testing', 'e2e-testing', 'test-automation'],
    'Like the pristine snow, Yuki ensures purity in every aspect of code quality through comprehensive testing. With an analytical mind and methodical approach, no bug escapes her careful examination.',
    '❄️',
    'active'
),
(
    'hiro-003',
    'Hiro',
    'SRE & DevOps Guardian',
    'llama-4-405b',
    ARRAY['kubernetes', 'ci-cd', 'monitoring', 'infrastructure', 'reliability'],
    'A guardian who never sleeps. Hiro protects production systems with vigilant monitoring and automated defenses. Expert in building resilient infrastructure that scales effortlessly.',
    '🛡️',
    'active'
),
(
    'sakura-004',
    'Sakura',
    'Documentation Artist',
    'gemini-3.0-ultra',
    ARRAY['technical-writing', 'documentation', 'diagrams', 'api-docs'],
    'Like cherry blossoms bringing beauty to spring, Sakura transforms complex technical concepts into elegant, understandable documentation. Every word is carefully chosen, every diagram thoughtfully crafted.',
    '🌸',
    'active'
),
(
    'kenji-005',
    'Kenji',
    'Architecture Visionary',
    'openai-o3',
    ARRAY['system-design', 'architecture', 'design-patterns', 'scalability'],
    'A master architect who sees the grand design in every system. Kenji plans with wisdom gained from building countless systems, always considering scalability, maintainability, and elegance.',
    '🏗️',
    'active'
);

-- View for agent statistics
CREATE OR REPLACE VIEW agent_stats AS
SELECT 
    a.id,
    a.name,
    a.role,
    a.status,
    COUNT(DISTINCT at.id) as total_tasks,
    COUNT(DISTINCT at.id) FILTER (WHERE at.status = 'completed') as completed_tasks,
    COUNT(DISTINCT at.id) FILTER (WHERE at.status = 'failed') as failed_tasks,
    COALESCE(SUM(at.tokens_used), 0) as total_tokens,
    COALESCE(SUM(at.cost_usd), 0) as total_cost,
    COALESCE(AVG(at.duration_ms), 0) as avg_duration_ms,
    CASE 
        WHEN COUNT(at.id) > 0 THEN 
            ROUND((COUNT(at.id) FILTER (WHERE at.status = 'completed')::FLOAT / COUNT(at.id)) * 100, 2)
        ELSE 100.0
    END as success_rate
FROM agents a
LEFT JOIN agent_tasks at ON a.id = at.agent_id
GROUP BY a.id, a.name, a.role, a.status;
