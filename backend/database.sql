-- Enable the pgvector extension for storing vector embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Enable uuid-ossp extension for uuid generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users Table (For Custom Authentication)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'user',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Admins Table
CREATE TABLE IF NOT EXISTS admins (
    id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    full_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Business Settings Table
CREATE TABLE IF NOT EXISTS business_settings (
    id VARCHAR(50) PRIMARY KEY DEFAULT 'default',
    business_name VARCHAR(255) NOT NULL DEFAULT 'My AI Business',
    business_description TEXT,
    business_hours JSONB DEFAULT '{"monday": "09:00-18:00", "tuesday": "09:00-18:00", "wednesday": "09:00-18:00", "thursday": "09:00-18:00", "friday": "09:00-18:00", "saturday": "Closed", "sunday": "Closed"}'::jsonb,
    phone VARCHAR(50),
    email VARCHAR(255),
    website VARCHAR(255),
    address TEXT,
    greeting_message TEXT DEFAULT 'Hello! Welcome to our business. How can I help you today?',
    fallback_message TEXT DEFAULT 'I am sorry, but I do not have that information at the moment. Would you like me to connect you to a human representative?',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. Prompt Settings Table
CREATE TABLE IF NOT EXISTS prompt_settings (
    id VARCHAR(50) PRIMARY KEY DEFAULT 'default',
    system_prompt TEXT NOT NULL DEFAULT 'You are a professional AI assistant representing this business. Answer only using the business knowledge provided. Never hallucinate. Be polite. Keep responses concise. If the answer is unavailable in the retrieved context, respond with the fallback message.',
    llm_temperature DOUBLE PRECISION NOT NULL DEFAULT 0.3,
    max_tokens INTEGER NOT NULL DEFAULT 800,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 5. Uploaded Files Table
CREATE TABLE IF NOT EXISTS uploaded_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    supabase_storage_path TEXT,
    file_size INTEGER,
    status VARCHAR(50) DEFAULT 'uploaded', -- 'uploaded', 'processing', 'indexed', 'failed'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 6. Knowledge Documents Table
CREATE TABLE IF NOT EXISTS knowledge_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    file_id UUID REFERENCES uploaded_files(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding VECTOR(768), -- Dimension for Google text-embedding-004
    metadata JSONB, -- page number, section, chunk index, source etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 7. FAQ Table (Quick direct Q&As)
CREATE TABLE IF NOT EXISTS faq (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 8. Chat Sessions Table
CREATE TABLE IF NOT EXISTS chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_phone VARCHAR(50) UNIQUE NOT NULL,
    customer_name VARCHAR(255),
    human_takeover BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 9. Messages Table
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    sender VARCHAR(50) NOT NULL, -- 'customer' or 'agent' or 'system'
    message_type VARCHAR(50) NOT NULL DEFAULT 'text', -- 'text', 'image', 'audio', 'document'
    content TEXT NOT NULL,
    meta_message_id VARCHAR(255), -- ID sent by Meta Graph API or received from webhook
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 10. Analytics Table
CREATE TABLE IF NOT EXISTS analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    metric_name VARCHAR(100) NOT NULL, -- 'message_count', 'token_usage', 'response_time_ms', 'knowledge_search'
    metric_value INTEGER DEFAULT 0,
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 11. Conversation Logs Table (for detailed RAG logging)
CREATE TABLE IF NOT EXISTS conversation_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES chat_sessions(id) ON DELETE CASCADE,
    input_text TEXT,
    retrieved_chunks TEXT[],
    output_text TEXT,
    tokens_used INTEGER,
    response_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Seed Initial Default Configs
INSERT INTO business_settings (id, business_name, business_description, email, phone, website)
VALUES ('default', 'EcoStore Support', 'Retail business selling eco-friendly products', 'support@ecostore.com', '+123456789', 'https://ecostore.com')
ON CONFLICT (id) DO NOTHING;

INSERT INTO prompt_settings (id, system_prompt, llm_temperature, max_tokens)
VALUES ('default', 'You are a professional AI assistant representing EcoStore. Answer only using the business knowledge provided. Never hallucinate. Be polite. Keep responses concise. If the answer is unavailable in the retrieved context, respond with the fallback message.', 0.3, 800)
ON CONFLICT (id) DO NOTHING;

-- Create pgvector helper function for cosine similarity search
CREATE OR REPLACE FUNCTION match_documents (
  query_embedding VECTOR(768),
  match_threshold FLOAT,
  match_count INT
)
RETURNS TABLE (
  id UUID,
  content TEXT,
  metadata JSONB,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    kd.id,
    kd.content,
    kd.metadata,
    1 - (kd.embedding <=> query_embedding) AS similarity
  FROM knowledge_documents kd
  WHERE 1 - (kd.embedding <=> query_embedding) > match_threshold
  ORDER BY kd.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
