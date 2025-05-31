-- Create Database
USE ProjetBd;
-- Insert Data (Adapted from Annexe)
INSERT INTO Hotel (Id_Hotel, Ville, Pays, Code_postal) VALUES
(1, 'Paris', 'France', 75001),
(2, 'Lyon', 'France', 69002);

INSERT INTO Client (Nom_complet, Adresse, Ville, Code_postal, Email, Numero_de_telephone) VALUES
('Jean Dupont', '12 Rue de Paris', 'Paris', 75001, 'jean.dupont@email.fr', 612345678),
('Marie Leroy', '5 Avenue Victor Hugo', 'Lyon', 69002, 'marie.leroy@email.fr', 623456789),
('Paul Moreau', '8 Boulevard Saint-Michel', 'Marseille', 13005, 'paul.moreau@email.fr', 634567890),
('Lucie Martin', '27 Rue Nationale', 'Lille', 59800, 'lucie.martin@email.fr', 645678901),
('Emma Giraud', '3 Rue des Fleurs', 'Nice', 06000, 'emma.giraud@email.fr', 656789012);

INSERT INTO Prestation (Id_Prestation, Prix, Description) VALUES
(1, 15.00, 'Petit-déjeuner'),
(2, 30.00, 'Navette aéroport'),
(3, 0.00, 'Wi-Fi gratuit'),
(4, 50.00, 'Spa et bien-être'),
(5, 20.00, 'Parking sécurisé');

-- Assuming all hotels offer all prestations (not specified in annexe)
INSERT INTO Offre (Id_Hotel, Id_Prestation) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5);

INSERT INTO Type_Chambre (Id_Type, Type, Tarif) VALUES
(1, 'Simple', 80.00),
(2, 'Double', 120.00);

INSERT INTO Chambre (Id_Chambre, Etage, Fumeurs, Id_Hotel, Id_Type) VALUES
(1, 2, FALSE, 1, 1),
(2, 5, TRUE, 1, 2),
(3, 3, FALSE, 2, 1),
(4, 4, FALSE, 2, 2),
(5, 1, TRUE, 2, 2),
(6, 2, FALSE, 1, 1),
(7, 3, TRUE, 1, 2),
(8, 1, FALSE, 1, 1);

INSERT INTO Reservation (Id_Reservation, Date_arrivee, Date_depart, Nom_complet) VALUES
(1, '2025-06-15', '2025-06-18', 'Jean Dupont'),
(2, '2025-07-01', '2025-07-05', 'Marie Leroy'),
(3, '2025-08-10', '2025-08-14', 'Paul Moreau'),
(4, '2025-09-05', '2025-09-07', 'Lucie Martin'),
(5, '2025-09-20', '2025-09-25', 'Emma Giraud'),
(7, '2025-11-12', '2025-11-14', 'Marie Leroy'),
(9, '2026-01-15', '2026-01-18', 'Lucie Martin'),
(10, '2026-02-01', '2026-02-05', 'Marie Leroy');

-- Assuming each reservation concerns a room type (based on annexe Chambre data)
INSERT INTO Concerner (Id_Reservation, Id_Type) VALUES
(1, 1), -- Jean Dupont, Simple
(2, 2), -- Marie Leroy, Double
(3, 1), -- Paul Moreau, Simple
(4, 2), -- Lucie Martin, Double
(5, 2), -- Emma Giraud, Double
(7, 2), -- Marie Leroy, Double
(9, 1), -- Lucie Martin, Simple
(10, 1); -- Marie Leroy, Simple

INSERT INTO Evaluation (Id_Evaluation, Date_arrivee, La_note, Texte_descriptif, Nom_complet, Id_Hotel) VALUES
(1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 'Jean Dupont', 1),
(2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 'Marie Leroy', 1),
(3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 'Paul Moreau', 2),
(4, '2025-09-05', 5, 'Service impeccable, je recommande.', 'Lucie Martin', 2),
(5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 'Emma Giraud', 2);

