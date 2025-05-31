-- Create Database
CREATE DATABASE ProjetBd;
USE ProjetBd;

-- Create Tables
CREATE TABLE Hotel (
    Id_Hotel INT AUTO_INCREMENT PRIMARY KEY,
    Ville TEXT,
    Pays TEXT,
    Code_postal INT
);

CREATE TABLE Type_Chambre (
    Id_Type INT AUTO_INCREMENT PRIMARY KEY,
    Type TEXT,
    Tarif DECIMAL(10,2)
);

CREATE TABLE Chambre (
    Id_Chambre INT AUTO_INCREMENT PRIMARY KEY,
    Etage INT,
    Fumeurs BOOLEAN,
    Id_Hotel INT NOT NULL,
    Id_Type INT,
    FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel),
    FOREIGN KEY (Id_Type) REFERENCES Type_Chambre(Id_Type)
);

CREATE TABLE Prestation (
    Id_Prestation INT AUTO_INCREMENT PRIMARY KEY,
    Prix DECIMAL(10,2),
    Description TEXT
);

CREATE TABLE Offre (
    Id_Hotel INT,
    Id_Prestation INT,
    PRIMARY KEY (Id_Hotel, Id_Prestation),
    FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel),
    FOREIGN KEY (Id_Prestation) REFERENCES Prestation(Id_Prestation)
);

CREATE TABLE Client (
    Nom_complet VARCHAR(255) PRIMARY KEY,
    Adresse TEXT,
    Ville TEXT,
    Code_postal INT,
    Email TEXT,
    Numero_de_telephone BIGINT
);
 
CREATE TABLE Reservation (
    Id_Reservation INT AUTO_INCREMENT PRIMARY KEY,
    Date_arrivee DATE,
    Date_depart DATE,
    Nom_complet VARCHAR(255),
    FOREIGN KEY (Nom_complet) REFERENCES Client(Nom_complet)
);

CREATE TABLE Concerner (
    Id_Reservation INT,
    Id_Type INT,
    PRIMARY KEY (Id_Reservation, Id_Type),
    FOREIGN KEY (Id_Reservation) REFERENCES Reservation(Id_Reservation),
    FOREIGN KEY (Id_Type) REFERENCES Type_Chambre(Id_Type)
);

CREATE TABLE Evaluation (
    Id_Evaluation INT AUTO_INCREMENT PRIMARY KEY,
    Date_arrivee DATE,
    La_note INT,
    Texte_descriptif TEXT,
    Nom_complet VARCHAR(255),
    Id_Hotel INT,
    FOREIGN KEY (Nom_complet) REFERENCES Client(Nom_complet),
    FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel)
);

