SELECT * FROM tasks;-- list every task
SELECT * FROM tasks WHERE done = 1;-- only completed tasks
SELECT COUNT(*) FROM tasks;-- how many tasks are there?
UPDATE tasks SET done = 1;-- mark every task completed
DELETE FROM tasks WHERE done = 1;-- delete all completed tasks