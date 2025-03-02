-- Create newsletters table
CREATE TABLE IF NOT EXISTS newsletters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    delivery_platform TEXT NOT NULL DEFAULT 'whatsapp',
    status TEXT NOT NULL DEFAULT 'draft',
    sent_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES auth.users (id) ON DELETE CASCADE
);

-- Create index on user_id for faster queries
CREATE INDEX IF NOT EXISTS idx_newsletters_user_id ON newsletters (user_id);

-- Enable Row Level Security
ALTER TABLE newsletters ENABLE ROW LEVEL SECURITY;

-- Create policy to allow users to see only their own newsletters
CREATE POLICY "Users can view their own newsletters" ON newsletters
    FOR SELECT USING (auth.uid() = user_id);

-- Create policy to allow users to insert their own newsletters
CREATE POLICY "Users can insert their own newsletters" ON newsletters
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Create policy to allow users to update their own newsletters
CREATE POLICY "Users can update their own newsletters" ON newsletters
    FOR UPDATE USING (auth.uid() = user_id);

-- Create policy to allow users to delete their own newsletters
CREATE POLICY "Users can delete their own newsletters" ON newsletters
    FOR DELETE USING (auth.uid() = user_id);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to update updated_at timestamp
CREATE TRIGGER update_newsletters_updated_at
BEFORE UPDATE ON newsletters
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();