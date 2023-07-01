create table
  `DevContainer` (
    `id` INTEGER NOT NULL PRIMARY KEY autoincrement,
    `ProjectName` TEXT NULL UNIQUE,
    `MakeAccount` TEXT NULL,
    `DevContainerType` TEXT NULL,
    `DevContainerID` TEXT NOT NULL,
    `DevContainerStatus` BOOLEAN NOT NULL,
    `GPU` INT NULL,
    `Port` INT not NULL,
    `CreatedTimes` FLOAT NOT NULL
  );

create table
  `DatabaseContainer` (
    `DevContainerID` TEXT NOT NULL,
    `DataBaseID` TEXT NOT NULL,
    `DataBaseType` TEXT NOT NULL,
    `DataBaseIP` TEXT NOT NULL,
    `DataBaseStatus` BOOLEAN NOT NULL DEFAULT FALSE,
    `CreatedTimes` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`DevContainerID`)
  );