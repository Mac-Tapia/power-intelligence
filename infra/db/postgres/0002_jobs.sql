CREATE TABLE study_job (
    job_id text PRIMARY KEY,
    kind text NOT NULL CHECK(kind IN ('study','new_load','alternatives')),
    request jsonb NOT NULL,
    status text NOT NULL CHECK(status IN ('queued','running','finished','failed')),
    outcome jsonb NOT NULL DEFAULT '{}',
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE FUNCTION guard_job_terminal() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    IF TG_OP = 'DELETE' OR OLD.status IN ('finished','failed') THEN
        RAISE EXCEPTION 'job terminal is immutable';
    END IF;
    RETURN NEW;
END $$;
CREATE TRIGGER job_terminal_immutable BEFORE UPDATE OR DELETE ON study_job
    FOR EACH ROW EXECUTE FUNCTION guard_job_terminal();
