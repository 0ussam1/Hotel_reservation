import sqlite3

conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

cursor.executescript("""
CREATE TABLE Hotel (
  id_hotel INT PRIMARY KEY,
  ville VARCHAR(100),
  pays VARCHAR(100),
  code_postal INT
);

CREATE TABLE Prestation (
  id_prestation INT PRIMARY KEY,
  prix DECIMAL(10,2),
  nom VARCHAR(100)
);

CREATE TABLE HotelPrestation (
  id_hotel INT,
  id_prestation INT,
  PRIMARY KEY (id_hotel, id_prestation),
  FOREIGN KEY (id_hotel) REFERENCES Hotel(id_hotel),
  FOREIGN KEY (id_prestation) REFERENCES Prestation(id_prestation)
);

CREATE TABLE TypeChambre (
  id_type INT PRIMARY KEY,
  type VARCHAR(50),
  tarif DECIMAL(10,2)
);

CREATE TABLE Chambre (
  id_chambre INT PRIMARY KEY,
  etage INT,
  fumeur BOOLEAN,
  id_type_chambre INT,
  id_hotel INT,
  FOREIGN KEY (id_type_chambre) REFERENCES TypeChambre(id_type),
  FOREIGN KEY (id_hotel) REFERENCES Hotel(id_hotel)
);

CREATE TABLE ReservationChambre (
  id_reservation INT,
  id_chambre INT,
  PRIMARY KEY (id_reservation, id_chambre),
  FOREIGN KEY (id_reservation) REFERENCES Reservation(id_reservation),
  FOREIGN KEY (id_chambre) REFERENCES Chambre(id_chambre)
);

CREATE TABLE Client (
  nom_complet VARCHAR(100) PRIMARY KEY,
  adresse VARCHAR(255),
  ville VARCHAR(100),
  code_postal INT,
  email VARCHAR(100),
  telephone VARCHAR(20)
);

CREATE TABLE Reservation (
  id_reservation INT PRIMARY KEY,
  date_debut DATE,
  date_fin DATE,
  nom_complet VARCHAR(100),
  FOREIGN KEY (nom_complet) REFERENCES Client(nom_complet)
);

CREATE TABLE Evaluation
(
    id_evaluation INT PRIMARY KEY,
    date_arrive   DATE,
    note          INT,
    commantaire   TEXT,
    nom_complet   VARCHAR(100),
    FOREIGN KEY (nom_complet) REFERENCES Client (nom_complet)
);


""")


cursor.executemany("INSERT INTO Hotel VALUES (?, ?, ?, ?)", [
    (1, 'Paris', 'France', 75001),
    (2, 'Lyon', 'France', 69002)
])

cursor.executemany("INSERT INTO Client VALUES (?, ?, ?, ?, ?, ?) ", [
    ('Jean Dupont', '12 Rue de Paris', 'Paris', 75001, 'jean.dupont@email.fr', '0612345678'),
    ('Marie Leroy', '5 Avenue Victor Hugo', 'Lyon', 69002, 'marie.leroy@email.fr', '0623456789'),
    ('Paul Moreau', '8 Boulevard Saint-Michel', 'Marseille', 13005, 'paul.moreau@email.fr', '0634567890'),
    ('Lucie Martin', '27 Rue Nationale', 'Lille', 59800, 'lucie.martin@email.fr', '0645678901'),
    ('Emma Giraud', '3 Rue des Fleurs', 'Nice', 60000, 'emma.giraud@email.fr', '0656789012')
])

cursor.executemany("INSERT INTO Prestation VALUES (?, ?, ?)", [
    (1, 15.00, 'Petit-déjeuner'),
    (2, 30.00, 'Navette aéroport'),
    (3, 0.00, 'Wi-Fi gratuit'),
    (4, 50.00, 'Spa et bien-être'),
    (5, 20.00, 'Parking sécurisé')
])

cursor.executemany("INSERT INTO TypeChambre VALUES (?, ?, ?)", [
    (1, 'Simple', 80.00),
    (2, 'Double', 120.00)
])

cursor.executemany("INSERT INTO Chambre VALUES (?, ?, ?, ?, ?)", [
    (1, 2, 0, 1, 1),
    (2, 5, 1, 1, 2),
    (3, 3, 0, 2, 1),
    (4, 4, 0, 2, 2),
    (5, 1, 1, 2, 2),
    (6, 2, 0, 1, 1),
    (7, 3, 1, 1, 2),
    (8, 1, 0, 1, 1)
])

cursor.executemany("INSERT INTO Reservation VALUES (?, ?, ?, ?)", [
    (1, '2025-06-15', '2025-06-18', 'Jean Dupont'),
    (2, '2025-07-01', '2025-07-05', 'Marie Leroy'),
    (7, '2025-11-12', '2025-11-14', 'Marie Leroy'),
    (10, '2026-02-01', '2026-02-05', 'Marie Leroy'),
    (3, '2025-08-10', '2025-08-14', 'Paul Moreau'),
    (4, '2025-09-05', '2025-09-07', 'Lucie Martin'),
    (9, '2026-01-15', '2026-01-18', 'Lucie Martin'),
    (5, '2025-09-20', '2025-09-25', 'Emma Giraud')
])

cursor.executemany("INSERT INTO Evaluation VALUES (?, ?, ?, ?, ?) ", [
    (1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 'Jean Dupont'),
    (2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 'Marie Leroy'),
    (3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 'Paul Moreau'),
    (4, '2025-09-05', 5, 'Service impeccable, je recommande.', 'Lucie Martin'),
    (5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 'Emma Giraud')
])

cursor.executemany("INSERT INTO ReservationChambre VALUES (?, ?) ", [
    (1, 1),
    (2, 2),
    (7, 7),
    (10, 2),
    (3, 3),
    (4, 4),
    (9, 5),
    (5, 8)

])
conn.commit()
conn.close()

print("✅ Base de données créée et remplie avec succès.")
