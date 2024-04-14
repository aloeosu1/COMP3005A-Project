CREATE TABLE Members (
	MemberID SERIAL PRIMARY KEY,
	FirstName VARCHAR(20),
	LastName VARCHAR(20),
	Email VARCHAR(100),
	Password VARCHAR(100),
	Phone VARCHAR(100),
	Birthday DATE,
	Gender CHAR(1),
	Address VARCHAR(100),
	Goal VARCHAR(255),
	RegistrationDate DATE,
	PaymentMethod VARCHAR(100)
);

CREATE TABLE Trainers (
	TrainerID SERIAL PRIMARY KEY,
	FirstName VARCHAR(20),
	LastName VARCHAR(20),
	Email VARCHAR(100),
	Password VARCHAR(100),
	AvailTime TIME,
	StartDate DATE
);



CREATE TABLE Sessions (
	SessionID SERIAL PRIMARY KEY,
	MemberID INT NULL REFERENCES Members(MemberID),
	TrainerID INT REFERENCES Trainers(TrainerID),
	SessionName VARCHAR(20),
	SessionCost INT,
	SessionDate DATE,
	SessionTime TIME
	
);

CREATE TABLE Metrics (
	MetricID SERIAL PRIMARY KEY,
	MemberID INT REFERENCES Members(MemberID),
	Height DECIMAL,
	Weight DECIMAL

);

CREATE TABLE Exercises (
	MemberID INT REFERENCES Members(MemberID),
	Exercise VARCHAR(100)

);

CREATE TABLE Available (
	TrainerID INT REFERENCES Trainers(TrainerID),
	Day DATE,
	Time TIME
);