CREATE TABLE users
(
    id String NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE packs
(
    id String NOT NULL,
    name String,
    intro_file String,
    outro_file String,
    PRIMARY KEY (id)
);

CREATE TABLE pack_questions
(
    id String NOT NULL,
    pack_id Int32,
    question String,
    order Int32,
    PRIMARY KEY (id),
    INDEX pack_id_idk GLOBAL ON (pack_id)
);

CREATE TABLE interviews
(
    id String NOT NULL,
    user_id Int32,
    pack_id Int32,
    status String,
    PRIMARY KEY (id),
    INDEX user_id_idk GLOBAL ON (user_id),
    INDEX pack_id_idk GLOBAL ON (pack_id)
);

CREATE TABLE interview_answers
(
    id String NOT NULL,
    user_id Int32,
    interview_id Int32,
    question Int32,
    answer String,
    question_order Int32,
    PRIMARY KEY (id),
    INDEX user_id_idk GLOBAL ON (user_id),
    INDEX interview_id_idk GLOBAL ON (interview_id)
);
