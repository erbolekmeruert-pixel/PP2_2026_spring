CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO groups (name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;

CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES groups(id),
    created_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE contacts
    ADD COLUMN IF NOT EXISTS email VARCHAR(100),
    ADD COLUMN IF NOT EXISTS birthday DATE,
    ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id),
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW();

CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) NOT NULL CHECK (type IN ('home', 'work', 'mobile')),
    UNIQUE (contact_id, phone)
);

CREATE INDEX IF NOT EXISTS idx_contacts_name ON contacts (LOWER(name));
CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts (LOWER(email));
CREATE INDEX IF NOT EXISTS idx_phones_phone ON phones (phone);