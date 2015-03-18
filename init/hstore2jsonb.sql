ALTER TABLE ONLY node_node
ALTER COLUMN metadata
DROP NOT NULL
;

ALTER TABLE ONLY node_node
ALTER COLUMN metadata
DROP DEFAULT
;

ALTER TABLE ONLY node_node
ALTER COLUMN metadata
TYPE JSON
USING hstore_to_json(metadata)
;

ALTER TABLE ONLY node_node
ALTER COLUMN metadata
SET DEFAULT '{}'::json
;


ALTER TABLE ONLY node_node
ALTER COLUMN metadata
SET NOT NULL
;
