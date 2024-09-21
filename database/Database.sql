USE WFHSystem;

-- Creating the Role table
CREATE TABLE Role (
    Role INT PRIMARY KEY,
    Role_Name VARCHAR(50)
);

-- Creating the Employee table
CREATE TABLE Employee (
    Staff_ID INT PRIMARY KEY,
    Staff_FName VARCHAR(50),
    Staff_LName VARCHAR(50),
    Dept VARCHAR(50),
    Position VARCHAR(50),
    Country VARCHAR(50),
    Email VARCHAR(50),
    Reporting_Manager VARCHAR(50),
    Role INT,
    FOREIGN KEY (Role) REFERENCES Role(Role)
);

-- Creating the WFH_Application table
CREATE TABLE WFH_Application (
    Application_ID INT PRIMARY KEY,
    Staff INT,
    Start_Date DATETIME,
    End_Date DATETIME,
    Status ENUM('Pending', 'Rejected', 'Approved', 'Withdrawn'),
    Time_Slot ENUM('AM', 'PM', 'Day'),
    Email VARCHAR(50),
    Reporting_Manager VARCHAR(50),
    Role VARCHAR(50)
);

-- Creating the WFH_Approval table
CREATE TABLE WFH_Approval (
    Approval_ID INT PRIMARY KEY,
    Application_ID INT,
    Approver_ID INT,
    Approval_Status BOOLEAN,
    Approval_Date DATETIME,
    FOREIGN KEY (Application_ID) REFERENCES WFH_Application(Application_ID)
);

-- Creating the WFH_Schedule table
CREATE TABLE WFH_Schedule (
    Schedule_ID INT PRIMARY KEY,
    Staff_ID INT,
    Application_ID INT,
    Date DATETIME,
    Time_Slot ENUM('AM', 'PM', 'Day'),
    Status ENUM('Passed', 'Upcoming', 'Cancelled'),
    FOREIGN KEY (Staff_ID) REFERENCES Employee(Staff_ID),
    FOREIGN KEY (Application_ID) REFERENCES WFH_Application(Application_ID)
);

-- Creating the Viewing_Rights table
CREATE TABLE Viewing_Rights (
    Viewer_ID INT,
    Viewee_ID INT,
    PRIMARY KEY (Viewer_ID, Viewee_ID),
    FOREIGN KEY (Viewer_ID) REFERENCES Employee(Staff_ID),
    FOREIGN KEY (Viewee_ID) REFERENCES Employee(Staff_ID)
);
