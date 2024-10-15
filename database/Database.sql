-- Creating Role Table
CREATE TABLE Role (
    Role INT PRIMARY KEY,
    Role_Name VARCHAR(50) NOT NULL
);

INSERT INTO Role (Role, Role_Name)
VALUES 
(3, 'Manager'),
(2, 'Staff'),
(1, 'HR/Director');


-- Creating Employee Table
CREATE TABLE Employee (
    Staff_ID INT PRIMARY KEY,
    Staff_FName VARCHAR(50) NOT NULL,
    Staff_LName VARCHAR(50) NOT NULL,
    Dept VARCHAR(50) NOT NULL,
    Position VARCHAR(50) NOT NULL,
    Country VARCHAR(50) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    Reporting_Manager INT NOT NULL,
    Role INT NOT NULL,
    Password VARCHAR(50) NOT NULL,
    FOREIGN KEY (Role) REFERENCES Role(Role),
    FOREIGN KEY (Reporting_Manager) REFERENCES Employee(Staff_ID)
);

-- Creating WFH_Application Table
CREATE TABLE WFH_Application (
    Application_ID INT PRIMARY KEY,
    Staff_ID INT NOT NULL,
    Start_Date DATETIME NOT NULL,
    End_Date DATETIME NOT NULL,
    Status ENUM('Pending', 'Rejected', 'Approved', 'Withdrawn') NOT NULL,
    Time_Slot ENUM('AM', 'PM', 'Day') NOT NULL,
    Type ENUM('AdHoc', 'Recurring') NOT NULL,
    Days SET('Mon', 'Tue','Wed', 'Thu','Fri') NULL,
    Email VARCHAR(50) NOT NULL,
    Reporting_Manager INT NOT NULL,
    FOREIGN KEY (Staff_ID) REFERENCES Employee(Staff_ID),
    FOREIGN KEY (Reporting_Manager) REFERENCES Employee(Staff_ID),
);

-- Creating WFH_Schedule Table
CREATE TABLE WFH_Schedule (
    Schedule_ID INT PRIMARY KEY,
    Staff_ID INT NOT NULL,
    Application_ID INT NOT NULL,
    Team_ID INT NOT NULL,
    Date DATETIME NOT NULL,
    Time_Slot ENUM('AM', 'PM', 'Day') NOT NULL,
    Status ENUM('Passed', 'Upcoming', 'Cancelled') NOT NULL,
    FOREIGN KEY (Staff_ID) REFERENCES Employee(Staff_ID),
    FOREIGN KEY (Application_ID) REFERENCES WFH_Application(Application_ID),
    FOREIGN KEY (Team_ID) REFERENCES Employee(Staff_ID)
);
