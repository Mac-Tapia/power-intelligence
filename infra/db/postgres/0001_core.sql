-- UNITESIS core schema v1 — PostgreSQL 16 + PostGIS 3.
-- Content-addressed and append-only: identities are SHA-256 digests computed by the
-- domain (ElectricalSnapshot v2, StudyRequest/StudyResult, dataset manifest).
-- Mirrors packages/python/power-adapters/src/unitesis_adapters/sql_repository.py.

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE SCHEMA IF NOT EXISTS unitesis;
SET search_path = unitesis, public;

CREATE TABLE source_manifest (
    source_sha256      char(64) PRIMARY KEY,
    source_id          text        NOT NULL,
    file_name          text,
    parser             text        NOT NULL,
    authorization_ref  text        NOT NULL DEFAULT 'not_declared',
    crs                text,
    manifest           jsonb       NOT NULL,
    ingested_at        timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE electrical_snapshot (
    snapshot_sha256    char(64) PRIMARY KEY,
    schema_version     text        NOT NULL CHECK (schema_version = 'unitesis.electrical-snapshot/v2'),
    source_sha256      char(64) REFERENCES source_manifest(source_sha256),
    name               text,
    canonical          jsonb       NOT NULL,
    created_at         timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE quarantine_record (
    id                 bigserial PRIMARY KEY,
    source_sha256      char(64) NOT NULL REFERENCES source_manifest(source_sha256),
    element_id         text NOT NULL,
    field              text NOT NULL,
    reason             text NOT NULL,
    source_ref         text NOT NULL
);
CREATE INDEX quarantine_record_source_idx ON quarantine_record(source_sha256);

-- Spatial representation is separate from electrical topology (MODULE-BOUNDARIES):
-- geometry never implies connectivity; joined to the snapshot by element id.
CREATE TABLE asset_geometry (
    snapshot_sha256    char(64) NOT NULL REFERENCES electrical_snapshot(snapshot_sha256),
    element_id         text NOT NULL,
    element_kind       text NOT NULL CHECK (element_kind IN ('bus','line','switch','load')),
    source_crs         text NOT NULL,
    geom               geometry NOT NULL,
    PRIMARY KEY (snapshot_sha256, element_id)
);
CREATE INDEX asset_geometry_gix ON asset_geometry USING gist (geom);

CREATE TABLE study_result (
    result_sha256      char(64) PRIMARY KEY,
    request_sha256     char(64) NOT NULL,
    snapshot_sha256    char(64) NOT NULL REFERENCES electrical_snapshot(snapshot_sha256),
    scenario_id        text NOT NULL,
    engine             text NOT NULL,
    engine_version     text NOT NULL,
    status             text NOT NULL CHECK (status IN ('computed','failed','unavailable')),
    payload            jsonb NOT NULL,
    evidence_path      text,
    created_at         timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX study_result_snapshot_idx ON study_result(snapshot_sha256, scenario_id);

CREATE TABLE forecast_dataset (
    dataset_sha256     char(64) PRIMARY KEY,
    source_sha256      char(64) NOT NULL,
    schema_version     text NOT NULL,
    manifest           jsonb NOT NULL,
    created_at         timestamptz NOT NULL DEFAULT now()
);

-- Append-only enforcement: evidence rows are never updated or deleted by the application.
CREATE OR REPLACE FUNCTION forbid_mutation() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN RAISE EXCEPTION 'unitesis evidence tables are append-only'; END $$;
CREATE TRIGGER snapshot_immutable BEFORE UPDATE OR DELETE ON electrical_snapshot
    FOR EACH ROW EXECUTE FUNCTION forbid_mutation();
CREATE TRIGGER result_immutable BEFORE UPDATE OR DELETE ON study_result
    FOR EACH ROW EXECUTE FUNCTION forbid_mutation();
CREATE TRIGGER dataset_immutable BEFORE UPDATE OR DELETE ON forecast_dataset
    FOR EACH ROW EXECUTE FUNCTION forbid_mutation();
