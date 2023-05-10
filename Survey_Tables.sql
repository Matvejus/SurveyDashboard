DROP DATABASE IF EXISTS SurveyTest;
CREATE DATABASE IF NOT EXISTS SurveyTest;
USE SurveyTest;

DROP TABLE IF EXISTS Survey;
DROP TABLE IF EXISTS Survey_Status;
DROP TABLE IF EXISTS Question;
DROP TABLE IF EXISTS Choice;
DROP TABLE IF EXISTS Answer;
DROP TABLE IF EXISTS Submission;


CREATE TABLE IF NOT EXISTS Survey_Status
(
	status_id INT PRIMARY KEY auto_increment,
	survey_status VARCHAR(255)
);
    
CREATE TABLE IF NOT EXISTS Survey
(
	survey_id INT PRIMARY KEY auto_increment,
	tittle VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Question
(
	survey_id INT NOT NULL,
    FOREIGN KEY fk_Question_Survey (survey_id)
		REFERENCES Survey (survey_id)
		ON UPDATE CASCADE
		ON DELETE NO ACTION,
	question_id INT PRIMARY KEY auto_increment,
    text VARCHAR(200) NOT NULL,
    pub_date DATETIME
);

CREATE TABLE IF NOT EXISTS Choice
(
	choice_id INT PRIMARY KEY auto_increment,
    question_id INT NOT NULL,
	FOREIGN KEY fk_Choice_Question (question_id)
			REFERENCES Question (question_id)
            ON UPDATE CASCADE
			ON DELETE NO ACTION,
	text VARCHAR (255)
);
CREATE TABLE IF NOT EXISTS Answer
(
	answer_id INT PRIMARY KEY auto_increment,
    text VARCHAR (255)
);

CREATE TABLE IF NOT EXISTS Submission
(
	submission_id INT PRIMARY KEY auto_increment,
    participant_email varchar(255) NOT NULL UNIQUE,
    answer_id INT NOT NULL,
    FOREIGN KEY fk_Submission_Answer (answer_id)
			REFERENCES Answer (answer_id)
            ON UPDATE CASCADE
			ON DELETE NO ACTION,
    survey_id INT NOT NULL,
    FOREIGN KEY fk_Submission_Survey (survey_id)
			REFERENCES Survey (survey_id)
            ON UPDATE CASCADE
			ON DELETE NO ACTION,
	status_id INT NOT NULL,
    FOREIGN KEY fk_Submission_Survey_Status (status_id)
			REFERENCES Survey_Status (status_id)
            ON UPDATE CASCADE
			ON DELETE NO ACTION
);
