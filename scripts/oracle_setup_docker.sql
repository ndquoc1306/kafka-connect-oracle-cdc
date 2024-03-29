prompt Starting Setup

prompt Check if the ORACLE database is in archive log mode
select log_mode from v$database;

prompt Turn on ARCHIVELOG mode
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
ALTER DATABASE ARCHIVELOG;
ALTER DATABASE OPEN;

prompt Check if the ORACLE database is in archive log mode
select log_mode from v$database;

prompt Enable supplemental logging for all columns
ALTER SESSION SET CONTAINER=cdb$root;
ALTER DATABASE ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS;

-- to be run in the CDB
-- credit : https://docs.confluent.io/kafka-connect-oracle-cdc/current
CREATE ROLE C##CDC_PRIVS;
GRANT CREATE SESSION,
EXECUTE_CATALOG_ROLE,
SELECT ANY TRANSACTION,
SELECT ANY DICTIONARY TO C##CDC_PRIVS;
GRANT SELECT ON SYSTEM.LOGMNR_COL$ TO C##CDC_PRIVS;
GRANT SELECT ON SYSTEM.LOGMNR_OBJ$ TO C##CDC_PRIVS;
GRANT SELECT ON SYSTEM.LOGMNR_USER$ TO C##CDC_PRIVS;
GRANT SELECT ON SYSTEM.LOGMNR_UID$ TO C##CDC_PRIVS;

CREATE USER C##BLOGWEBSITE IDENTIFIED BY 123456; CONTAINER=ALL;
GRANT C##CDC_PRIVS TO C##BLOGWEBSITE CONTAINER=ALL;
ALTER USER C##BLOGWEBSITE QUOTA UNLIMITED ON sysaux;
ALTER USER C##BLOGWEBSITE SET CONTAINER_DATA = (CDB$ROOT, ORCLPDB1) CONTAINER=CURRENT;

ALTER SESSION SET CONTAINER=CDB$ROOT;
GRANT CREATE SESSION, ALTER SESSION, SET CONTAINER, LOGMINING, EXECUTE_CATALOG_ROLE TO C##BLOGWEBSITE CONTAINER=ALL;
GRANT SELECT ON GV_$DATABASE TO C##BLOGWEBSITE CONTAINER=ALL;
GRANT SELECT ON V_$LOGMNR_CONTENTS TO C##BLOGWEBSITE CONTAINER=ALL;
GRANT SELECT ON GV_$ARCHIVED_LOG TO C##BLOGWEBSITE CONTAINER=ALL;
GRANT CONNECT TO C##BLOGWEBSITE CONTAINER=ALL;
GRANT CREATE TABLE TO C##BLOGWEBSITE CONTAINER=ALL;
GRANT CREATE SEQUENCE TO C##BLOGWEBSITE CONTAINER=ALL;
GRANT CREATE TRIGGER TO C##BLOGWEBSITE CONTAINER=ALL;

ALTER SESSION SET CONTAINER=cdb$root;
ALTER DATABASE ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS;

GRANT FLASHBACK ANY TABLE TO C##BLOGWEBSITE;
GRANT FLASHBACK ANY TABLE TO C##BLOGWEBSITE container=all;


exit;

