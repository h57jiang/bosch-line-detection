-- Initialize the database.
-- Create files table which saves information of each uploaded file.

DROP TABLE IF EXISTS files;

CREATE TABLE files(
  name TEXT PRIMARY KEY,  -- name needs to be unique
  type TEXT,              -- type can be "train" or "predict"
  is_used INTEGER,        -- boolean typ, 0 for true, 1 for false
  updated_on TEXT         -- datetime type, ISO8601 strings ("YYYY-MM-DD HH:MM:SS.SSS")
);