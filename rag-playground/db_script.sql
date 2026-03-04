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

ALTER TABLE documents
ADD COLUMN content_tsv tsvector;

UPDATE documents
SET content_tsv = to_tsvector('english', content);

CREATE INDEX idx_fts ON documents USING GIN(content_tsv);