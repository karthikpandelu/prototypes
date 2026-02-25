CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(384)
);

--To enable ANN
CREATE INDEX ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

ALTER TABLE documents
ADD COLUMN document_id TEXT,
ADD COLUMN source TEXT;