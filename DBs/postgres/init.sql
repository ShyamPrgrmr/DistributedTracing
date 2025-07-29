
CREATE TABLE application_partition_mapping (
    id SERIAL PRIMARY KEY,
    application_id VARCHAR NOT NULL,
    partition_id VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_app_partition UNIQUE (application_id, partition_id)
);

-- Create trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.updated_at = NOW();
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach the trigger to the table
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON application_partition_mapping
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Grant privileges to user `dt_user`
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE application_partition_mapping TO dt_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE application_partition_mapping_id_seq TO dt_user;
