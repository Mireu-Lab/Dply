create table
  `devContainer` (
    `id` INTEGER NOT NULL PRIMARY KEY autoincrement,
    `projectName` TEXT NULL UNIQUE,
    `makeAccount` TEXT NULL,
    `devContainerType` TEXT NULL,
    `devContainerID` TEXT NOT NULL,
    `devContainerStatus` BOOLEAN NOT NULL,
    `gpu` INT NULL,
    `port` INT NOT NULL,
    `createdTimes` FLOAT NOT NULL,
    `updateTimes` FLOAT NOT NULL
  );

create table
  `databaseContainer` (
    `devContainerID` TEXT NOT NULL,
    `databaseID` TEXT NOT NULL,
    `databaseType` TEXT NOT NULL,
    `databaseIP` TEXT NOT NULL,
    `databaseStatus` BOOLEAN NOT NULL,
    `createdTimes` FLOAT NOT NULL,
    `updateTimes` FLOAT NOT NULL
  );