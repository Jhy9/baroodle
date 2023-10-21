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
    privilege INTEGER
);

CREATE TABLE pages(
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses,
    title TEXT,
    content TEXT,
    position INTEGER
);

CREATE TABLE exercise_set(
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses,
    set_name TEXT,
    availability_status TEXT
);

CREATE TABLE exercises(
    id SERIAL PRIMARY KEY,
    set_id INTEGER REFERENCES exercise_set,
    assignment TEXT,
    max_points INTEGER,
    exercise_type INTEGER,
    answer TEXT,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT
);

CREATE TABLE exercise_submissions(
    exercise_id INTEGER REFERENCES exercises,
    user_id INTEGER REFERENCES accounts,
    answer TEXT,
    points INTEGER,
    feedback TEXT
);