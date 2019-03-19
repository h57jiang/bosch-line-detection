-- Each test will create a new temporary database file and populate some data that will be used in the tests

INSERT INTO files (name, type, is_used, uploaded_on)
VALUES
  ('test1.csv', 'train', false, '2018-01-01 00:00:00'),
  ('test2.csv', 'predict', false, '2018-01-01 00:00:00');




