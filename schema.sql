CREATE TABLE accounts(
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    passw TEXT,
    account_type TEXT
);

CREATE TABLE courses(
    id SERIAL PRIMARY KEY,
    course_name TEXT UNIQUE,
    creator INTEGER REFERENCES accounts,
    course_description TEXT
);

CREATE TABLE course_attendance(
    course_id INTEGER REFERENCES courses,
    account_id INTEGER REFERENCES accounts,
    completion_status TEXT
);

CREATE TABLE exercises(
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses,
    max_points INTEGER
);

CREATE TABLE exercise_completions(
    exercise_id INTEGER REFERENCES exercises,
    user_id INTEGER REFERENCES accounts,
    exercise_answer TEXT,
    points INTEGER
);
