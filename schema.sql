CREATE TABLE accounts(
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    pass TEXT,
    account_type TEXT
);

CREATE TABLE courses(
    id SERIAL PRIMARY KEY,
    course_name TEXT UNIQUE,
    creator INTEGER_REFERENCES accounts,
    course_description TEXT
);

CREATE TABLE course-attendance(
    course_id INTEGER_REFERENCES courses,
    account_id INTEGER REFERENCES accounts,
    completion_status TEXT
);

CREATE TABLE exercises(
    id SERIAL PRIMARY KEY,
    course_id INTEGER_REFERENCES courses,
    max_points INTEGER
);

CREATE TABLE exercise-completions(
    exercise_id INTEGER_REFERENCES exercises,
    user_id INTEGER_REFERENCES accounts,
    exercise_answer TEXT,
    points INTEGER
);
