-- Backward-compatible acceptance of the transformer snapshot introduced by 008-B2.
ALTER TABLE electrical_snapshot DROP CONSTRAINT electrical_snapshot_schema_version_check;
ALTER TABLE electrical_snapshot ADD CONSTRAINT electrical_snapshot_schema_version_check
    CHECK (schema_version IN ('unitesis.electrical-snapshot/v2','unitesis.electrical-snapshot/v3'));
