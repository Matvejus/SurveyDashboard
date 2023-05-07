DROP DATABASE IF EXISTS survey;
CREATE DATABASE IF NOT EXISTS survey;


DROP TABLE IF EXISTS Answer_Option;
DROP TABLE IF EXISTS Answer;
DROP TABLE IF EXISTS Response;
DROP TABLE IF EXISTS Respondent;
DROP TABLE IF EXISTS Survey;
DROP TABLE IF EXISTS Survey_Status;
DROP TABLE IF EXISTS Question_Option;
DROP TABLE IF EXISTS Question;
DROP TABLE IF EXISTS Question_Type;


CREATE TABLE IF NOT EXISTS Survey_Status
(
	survey_status_id INT PRIMARY KEY auto_increment,
	survey_status VARCHAR(100)
);
    
CREATE TABLE IF NOT EXISTS Survey
(
	survey_id INT PRIMARY KEY auto_increment,
	survey_name VARCHAR(100) NOT NULL,
	description VARCHAR(8000) NOT NULL,
	start_date DATETIME,
	end_date DATETIME,
	min_responses INT,
	max_responses INT,
	survey_status_id INT NOT NULL,
	FOREIGN KEY fk_Survey_Survey_Status (survey_status_id)
		REFERENCES Survey_Status (survey_status_id)
		ON UPDATE CASCADE
		ON DELETE NO ACTION   
);

CREATE TABLE IF NOT EXISTS Question_Type
(
	question_type_id INT PRIMARY KEY auto_increment,
    question_type VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Question
(
	question_id INT PRIMARY KEY auto_increment,
    question_order INT,
    question_text VARCHAR(2000),
    is_mandatory BIT(64),
    question_type_id INT NOT NULL,
    FOREIGN KEY fk_Question_Question_Type (question_type_id)
		REFERENCES Question_Type (question_type_id)
		ON UPDATE CASCADE
		ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS Question_Option
(
	question_option_id INT PRIMARY KEY auto_increment,
    QO_order INT,
    QO_value VARCHAR(100),
    question_id INT NOT NULL,
    FOREIGN KEY fk_Question_Option_Question (question_id)
			REFERENCES Question (question_id)
            ON UPDATE CASCADE
			ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS Respondent
(
	respondent_id INT PRIMARY KEY auto_increment,
    first_name VARCHAR(100),
    last_name VARCHAR (100),
    email VARCHAR (100)
);

CREATE TABLE IF NOT EXISTS Response 
(
	response_id INT PRIMARY KEY auto_increment,
    respondent_id INT NOT NULL,
    FOREIGN KEY fk_Resopnse_Respondent (respondent_id)
			REFERENCES Respondent (respondent_id)
            ON UPDATE CASCADE
			ON DELETE NO ACTION,
	survey_id INT NOT NULL,
    FOREIGN KEY fk_Resopnse_Survey (survey_id)
			REFERENCES Survey (survey_id)
            ON UPDATE CASCADE
			ON DELETE NO ACTION,
    begin_date DATETIME,
    end_date datetime
);

CREATE TABLE IF NOT EXISTS Answer
(
	answer_id INT PRIMARY KEY auto_increment,
    response_id INT NOT NULL,
    FOREIGN KEY fk_Answer_Response (response_id)
			REFERENCES Response (response_id)
            ON UPDATE CASCADE
			ON DELETE NO ACTION,
    question_id INT NOT NULL,
	FOREIGN KEY fk_Answer_Question (question_id)
			REFERENCES Question (question_id)
            ON UPDATE CASCADE
			ON DELETE NO ACTION,
    answer VARCHAR (6000)
);

CREATE TABLE IF NOT EXISTS Answer_Option
(
	answer_option_id INT PRIMARY KEY auto_increment,
    answer_id INT NOT NULL,
    FOREIGN KEY fk_Answer_Option_Answer (answer_id)
			REFERENCES Answer (answer_id)
            ON UPDATE CASCADE
			ON DELETE NO ACTION,
    question_option_id INT NOT NULL,
    FOREIGN KEY fk_Answer_Option_Question_Option (question_option_id)
			REFERENCES Question_Option (question_option_id)
            ON UPDATE CASCADE
			ON DELETE NO ACTION
);