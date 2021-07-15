
CREATE TABLE IF NOT EXISTS STAFF(
    st_id integer PRIMARY KEY,
--     st_invited_by integer,
    st_firstName text NOT NULL,
    st_lastName text NOT NULL,
    st_job integer NOT NULL,
    st_hospital integer NOT NULL,
    st_email text NOT NULL,
    st_registration_flag integer,
    st_isactif integer NOT NULL,
    st_code text
--     st_language text DEFAULT 'EN',
--     XP integer  DEFAULT 0,
--     XPLock text DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN  KEY(st_job) REFERENCES JOB(jo_id),
--     FOREIGN  KEY(st_specialty) REFERENCES SPECIALTY(sp_id),
--     FOREIGN KEY(st_hospital) REFERENCES HOSPITAL(ho_id),
--     FOREIGN KEY(st_invited_by) REFERENCES STAFF(st_id),
--     FOREIGN KEY(st_job) REFERENCES JOB(jo_id),
--     FOREIGN KEY(st_hospital) REFERENCES HOSPITAL(ho_id)
);

CREATE TABLE IF NOT EXISTS CAS_STAFF(
    st_id integer,
    ca_id integer,
    PRIMARY KEY(st_id, ca_id)
);


CREATE TABLE IF NOT EXISTS CAS(
    ca_id  integer PRIMARY KEY,
    ca_owner integer NOT NULL,
    ca_name text NOT NULL,
    ca_description text NOT NULL,
    ca_keywods text
);

CREATE TABLE IF NOT EXISTS SPE_STAFF(
    st_id integer,
    sp_id integer,
    PRIMARY KEY(sp_id, st_id)
);

CREATE TABLE IF NOT EXISTS SPECIALTY(
    sp_id integer PRIMARY KEY,
    sp_name text NOT NULL
);


CREATE TABLE IF NOT EXISTS JOB(
    jo_id integer PRIMARY KEY, --NOT NULL
    jo_name text --NOT NULL
);

CREATE TABLE IF NOT EXISTS HOSPITAL(
    ho_id integer PRIMARY KEY,
    ho_name text, --NOT NULL
    ho_location integer,
    ho_email text NOT NULL
);

CREATE TABLE IF NOT EXISTS LOCATION(
    lo_id integer PRIMARY KEY,
    lo_canton text, --NOT NULL
    lo_adress text DEFAULT 'En Suisse'
);
