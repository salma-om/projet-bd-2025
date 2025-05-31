import sqlite3

# Connexion à la base de données SQLite
conn = sqlite3.connect('projet_bd.db')
cursor = conn.cursor()

# Création des tables
cursor.executescript('''
CREATE TABLE IF NOT EXISTS Hotel (
    Id_Hotel INTEGER PRIMARY KEY AUTOINCREMENT,
    Ville TEXT,
    Pays TEXT,
    Code_postal INTEGER
);

CREATE TABLE IF NOT EXISTS Type_Chambre (
    Id_Type INTEGER PRIMARY KEY AUTOINCREMENT,
    Type TEXT,
    Tarif REAL
);

CREATE TABLE IF NOT EXISTS Chambre (
    Id_Chambre INTEGER PRIMARY KEY AUTOINCREMENT,
    Etage INTEGER,
    Fumeurs BOOLEAN,
    Id_Hotel INTEGER,
    Id_Type INTEGER,
    FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel),
    FOREIGN KEY (Id_Type) REFERENCES Type_Chambre(Id_Type)
);

CREATE TABLE IF NOT EXISTS Prestation (
    Id_Prestation INTEGER PRIMARY KEY AUTOINCREMENT,
    Prix REAL,
    Description TEXT
);

CREATE TABLE IF NOT EXISTS Offre (
    Id_Hotel INTEGER,
    Id_Prestation INTEGER,
    PRIMARY KEY (Id_Hotel, Id_Prestation),
    FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel),
    FOREIGN KEY (Id_Prestation) REFERENCES Prestation(Id_Prestation)
);

CREATE TABLE IF NOT EXISTS Client (
    Nom_complet TEXT PRIMARY KEY,
    Adresse TEXT,
    Ville TEXT,
    Code_postal INTEGER,
    Email TEXT,
    Numero_de_telephone INTEGER
);

CREATE TABLE IF NOT EXISTS Reservation (
    Id_Reservation INTEGER PRIMARY KEY AUTOINCREMENT,
    Date_arrivee TEXT,
    Date_depart TEXT,
    Nom_complet TEXT,
    FOREIGN KEY (Nom_complet) REFERENCES Client(Nom_complet)
);

CREATE TABLE IF NOT EXISTS Concerner (
    Id_Reservation INTEGER,
    Id_Type INTEGER,
    PRIMARY KEY (Id_Reservation, Id_Type),
    FOREIGN KEY (Id_Reservation) REFERENCES Reservation(Id_Reservation),
    FOREIGN KEY (Id_Type) REFERENCES Type_Chambre(Id_Type)
);

CREATE TABLE IF NOT EXISTS Evaluation (
    Id_Evaluation INTEGER PRIMARY KEY AUTOINCREMENT,
    Date_arrivee TEXT,
    La_note INTEGER,
    Texte_descriptif TEXT,
    Nom_complet TEXT,
    Id_Hotel INTEGER,
    FOREIGN KEY (Nom_complet) REFERENCES Client(Nom_complet),
    FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel)
);
''')

# Ajout d'index pour optimiser les performances
cursor.executescript('''
CREATE INDEX IF NOT EXISTS idx_reservation_dates ON Reservation(Date_arrivee, Date_depart);
CREATE INDEX IF NOT EXISTS idx_concerner_reservation ON Concerner(Id_Reservation);
CREATE INDEX IF NOT EXISTS idx_chambre_hotel ON Chambre(Id_Hotel);
''')

# Insertion des données
cursor.executescript('''
INSERT OR IGNORE INTO Hotel (Id_Hotel, Ville, Pays, Code_postal) VALUES
(1, 'Paris', 'France', 75001),
(2, 'Lyon', 'France', 69002);

INSERT OR IGNORE INTO Client (Nom_complet, Adresse, Ville, Code_postal, Email, Numero_de_telephone) VALUES
('Jean Dupont', '12 Rue de Paris', 'Paris', 75001, 'jean.dupont@email.fr', 612345678),
('Marie Leroy', '5 Avenue Victor Hugo', 'Lyon', 69002, 'marie.leroy@email.fr', 623456789),
('Paul Moreau', '8 Boulevard Saint-Michel', 'Marseille', 13005, 'paul.moreau@email.fr', 634567890),
('Lucie Martin', '27 Rue Nationale', 'Lille', 59800, 'lucie.martin@email.fr', 645678901),
('Emma Giraud', '3 Rue des Fleurs', 'Nice', 06000, 'emma.giraud@email.fr', 656789012);

INSERT OR IGNORE INTO Prestation (Id_Prestation, Prix, Description) VALUES
(1, 15.00, 'Petit-déjeuner'),
(2, 30.00, 'Navette aéroport'),
(3, 0.00, 'Wi-Fi gratuit'),
(4, 50.00, 'Spa et bien-être'),
(5, 20.00, 'Parking sécurisé');

INSERT OR IGNORE INTO Offre (Id_Hotel, Id_Prestation) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5);

INSERT OR IGNORE INTO Type_Chambre (Id_Type, Type, Tarif) VALUES
(1, 'Simple', 80.00),
(2, 'Double', 120.00);

INSERT OR IGNORE INTO Chambre (Id_Chambre, Etage, Fumeurs, Id_Hotel, Id_Type) VALUES
(1, 2, 0, 1, 1),
(2, 5, 1, 1, 2),
(3, 3, 0, 2, 1),
(4, 4, 0, 2, 2),
(5, 1, 1, 2, 2),
(6, 2, 0, 1, 1),
(7, 3, 1, 1, 2),
(8, 1, 0, 1, 1);

INSERT OR IGNORE INTO Reservation (Id_Reservation, Date_arrivee, Date_depart, Nom_complet) VALUES
(1, '2025-06-15', '2025-06-18', 'Jean Dupont'),
(2, '2025-07-01', '2025-07-05', 'Marie Leroy'),
(3, '2025-08-10', '2025-08-14', 'Paul Moreau'),
(4, '2025-09-05', '2025-09-07', 'Lucie Martin'),
(5, '2025-09-20', '2025-09-25', 'Emma Giraud'),
(7, '2025-11-12', '2025-11-14', 'Marie Leroy'),
(9, '2026-01-15', '2026-01-18', 'Lucie Martin'),
(10, '2026-02-01', '2026-02-05', 'Marie Leroy');

INSERT OR IGNORE INTO Concerner (Id_Reservation, Id_Type) VALUES
(1, 1), (2, 2), (3, 1), (4, 2), (5, 2), (7, 2), (9, 1), (10, 1);

INSERT OR IGNORE INTO Evaluation (Id_Evaluation, Date_arrivee, La_note, Texte_descriptif, Nom_complet, Id_Hotel) VALUES
(1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 'Jean Dupont', 1),
(2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 'Marie Leroy', 1),
(3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 'Paul Moreau', 2),
(4, '2025-09-05', 5, 'Service impeccable, je recommande.', 'Lucie Martin', 2),
(5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 'Emma Giraud', 2);
''')

# Valider et fermer
conn.commit()
conn.close()

print("Base de données SQLite créée avec succès.")