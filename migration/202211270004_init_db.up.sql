BEGIN;

CREATE TABLE call_billing
(
    id          serial PRIMARY KEY,
    user_name   character varying(255) NOT NULL,
    call_count  integer DEFAULT 0,
    block_count integer DEFAULT 0,
    created_at  timestamp without time zone,
    updated_at  timestamp without time zone
);

CREATE UNIQUE INDEX call_billing_user_name_index ON call_billing USING btree (user_name);

COMMIT;
