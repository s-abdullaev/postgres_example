-- SELECT name, title
-- FROM (student NATURAL JOIN takes)
-- JOIN course USING (course_id);

-- CREATE VIEW faculty AS
-- SELECT id, name, dept_name
-- FROM instructor;

-- SELECT name
-- FROM faculty
-- WHERE dept_name = 'Biology';

-- drop view faculty;

-- CREATE VIEW physics_fall_2017 AS
--     SELECT course.course_id, sec_id, building, room_number
--     FROM course, section
--     WHERE course.course_id = section.course_id
--     AND course.dept_name = 'Physics'
--     AND section.semester = 'Fall'
--     AND section.year = '2017';

-- CREATE VIEW physics_fall_2017_watson AS
--     SELECT course_id, room_number
--     FROM physics_fall_2017
--     WHERE building = 'Watson';
-- DROP VIEW physics_fall_2017_watson;
-- CREATE VIEW physics_fall_2017_watson AS
-- SELECT course_id, room_number
-- FROM (SELECT course.course_id, building, room_number
--       FROM course, section
--       WHERE course.course_id = section.course_id
--       AND course.dept_name = 'Physics'
--       AND section.semester = 'Fall'
--       AND section.year = '2017')
-- WHERE building = 'Watson';

-- CREATE MATERIALIZED VIEW physics_summary AS SELECT course_id, room_number, building 
-- FROM course 
-- JOIN section USING (course_id) 
-- WHERE dept_name = 'Physics' WITH DATA;

-- REFRESH MATERIALIZED VIEW physics_summary;
-- SELECT course_id, room_number, building
-- FROM physics_summary;
-- UPDATE section
-- SET room_number = 100
-- WHERE course_id = 'PHY-101';

-- BEGIN TRANSACTION;

-- INSERT INTO instructor (id, name, dept_name, salary)
-- VALUES ('99999', 'John Smith', 'Physics', 85000);

-- INSERT INTO course (course_id, title, dept_name, credits)
-- VALUES ('PHY-999', 'Advanced Quantum Mechanics', 'Physics', 4);

-- UPDATE section
-- SET instructor_id = '99999'
-- WHERE course_id = 'PHY-999';

-- UPDATE instructor
-- SET salary = 90000
-- WHERE id = '99999';

-- COMMIT;

-- -- @block create dept_count function
-- CREATE OR REPLACE FUNCTION dept_count(d_name VARCHAR(20))
-- RETURNS INTEGER
-- LANGUAGE plpgsql
-- AS $$
-- DECLARE
--   d_count INTEGER;
-- BEGIN
--   SELECT COUNT(*) INTO d_count
--   FROM student
--   WHERE dept_name = d_name;
--   RETURN d_count;
-- END;
-- $$;

-- SELECT dept_count('Comp. Sci.');

-- WITH RECURSIVE all_prereqs(course_id, prereq_id) AS (
--   -- Base: direct prereqs
--   SELECT course_id, prereq_id
--   FROM prereq

--   UNION ALL

--   -- Recursive: prereqs of prereqs
--   SELECT p.course_id, p.prereq_id
--   FROM prereq p, all_prereqs ap
--   WHERE ap.prereq_id = p.course_id
-- )
-- SELECT * FROM all_prereqs;