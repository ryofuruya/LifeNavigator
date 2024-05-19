PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "values_value" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL UNIQUE, "description" text NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL);
INSERT INTO values_value VALUES(8,'1','1','2024-05-15 12:11:25.824992','2024-05-15 12:11:25.825031');
COMMIT;
