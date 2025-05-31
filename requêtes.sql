-- Requête a
SELECT 
    R.idReservation,
    C.nomComplet,
    H.ville AS villeHotel
FROM Reservation R
JOIN Client C ON R.idClient = C.idClient
JOIN ReservationChambre RC ON R.idReservation = RC.idReservation
JOIN Chambre CH ON RC.idChambre = CH.idChambre
JOIN Hotel H ON CH.idHotel = H.idHotel;


-- Requête b
SELECT * FROM Client WHERE ville = 'Paris';

-- Requête c
SELECT idClient, COUNT(*) AS nbReservations
FROM Reservation
GROUP BY idClient;

-- Requête d
SELECT idType, COUNT(*) AS nbChambres
FROM Chambre
GROUP BY idType;

-- Requête e (exemple pour dates 2025-07-01 à 2025-07-10)
SELECT * FROM Chambre
WHERE idChambre NOT IN (
    SELECT idChambre
    FROM Reservation
    WHERE NOT (
        dateFin < '2025-07-01' OR dateDebut > '2025-07-10'
    )
);
