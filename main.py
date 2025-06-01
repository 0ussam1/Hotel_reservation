import streamlit as st
import sqlite3

def get_connection():
    conn = sqlite3.connect("hotel.db", check_same_thread=False)
    return conn

def show_reservations(conn):
    st.subheader("📅 Liste des réservations")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.id_reservation, r.date_debut, r.date_fin, r.nom_complet
        FROM Reservation r
    """)
    rows = cursor.fetchall()
    for row in rows:
        st.write(f"ID: {row[0]} | Client: {row[3]} | Du {row[1]} au {row[2]}")

def show_clients(conn):
    st.subheader("👥 Liste des clients")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Client")
    rows = cursor.fetchall()
    for row in rows:
        st.write(f"{row[0]} - {row[4]} - {row[5]}")

def add_client(conn):
    st.subheader("➕ Ajouter un client")
    with st.form("Ajouter un client"):
        nom = st.text_input("Nom complet")
        adresse = st.text_input("Adresse")
        ville = st.text_input("Ville")
        code_postal = st.number_input("Code postal", step=1)
        email = st.text_input("Email")
        tel = st.text_input("Téléphone")
        submitted = st.form_submit_button("Ajouter")
        if submitted:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Client VALUES (?, ?, ?, ?, ?, ?)",
                               (nom, adresse, ville, code_postal, email, tel))
                conn.commit()
                st.success("Client ajouté avec succès")
            except Exception as e:
                st.error(f"Erreur : {e}")

def add_reservation(conn):
    st.subheader("➕ Ajouter une réservation")
    cursor = conn.cursor()
    with st.form("Ajouter une réservation"):
        id_res = st.number_input("ID Réservation", step=1)
        client = st.text_input("Nom complet du client (doit exister)")
        date_debut = st.date_input("Date de début")
        date_fin = st.date_input("Date de fin")
        chambre_id = st.number_input("ID Chambre à réserver", step=1)
        submitted = st.form_submit_button("Réserver")
        if submitted:
            try:
                cursor.execute("INSERT INTO Reservation VALUES (?, ?, ?, ?)",
                               (id_res, date_debut, date_fin, client))
                cursor.execute("INSERT INTO ReservationChambre VALUES (?, ?)",
                               (id_res, chambre_id))
                conn.commit()
                st.success("Réservation ajoutée avec succès")
            except Exception as e:
                st.error(f"Erreur : {e}")

def available_rooms(conn):
    st.subheader("🏨 Chambres disponibles")
    cursor = conn.cursor()
    date_start = st.date_input("Date de début")
    date_end = st.date_input("Date de fin")
    if st.button("Chercher"):
        cursor.execute("""
            SELECT id_chambre FROM Chambre
            WHERE id_chambre NOT IN (
                SELECT id_chambre FROM ReservationChambre rc
                JOIN Reservation r ON rc.id_reservation = r.id_reservation
                WHERE NOT (
                    date_fin < ? OR date_debut > ?
                )
            )
        """, (date_start, date_end))
        chambres = cursor.fetchall()
        if chambres:
            st.write("Chambres disponibles :")
            for ch in chambres:
                st.write(f"Chambre ID: {ch[0]}")
        else:
            st.warning("Aucune chambre disponible pour cette période.")

# Interface principale
def main():
    st.title("🏨 Système de Gestion Hôtel")

    menu = ["Consulter Réservations", "Consulter Clients", "Chambres Disponibles", "Ajouter Client", "Ajouter Réservation"]
    choice = st.sidebar.selectbox("Menu", menu)

    conn = get_connection()

    if choice == "Consulter Réservations":
        show_reservations(conn)
    elif choice == "Consulter Clients":
        show_clients(conn)
    elif choice == "Chambres Disponibles":
        available_rooms(conn)
    elif choice == "Ajouter Client":
        add_client(conn)
    elif choice == "Ajouter Réservation":
        add_reservation(conn)

    conn.close()

if __name__ == '__main__':
    main()
