import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Charger et appliquer le CSS (uniquement le thème clair)
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache_resource
def get_connection():
    # Activer le mode thread-safe en désactivant la vérification de thread
    return sqlite3.connect('projet_bd.db', check_same_thread=False)

def fetch_data(query, params=None):
    conn = get_connection()
    try:
        if params:
            df = pd.read_sql_query(query, conn, params=params)
        else:
            df = pd.read_sql_query(query, conn)
        return df
    finally:
        pass

st.title("Gestion d'Hôtel - Projet BD 2025")
st.markdown("**Une application intuitive pour gérer vos réservations hôtelières.**")

tabs = st.tabs(["Consulter Réservations", "Consulter Clients", "Chambres Disponibles", "Ajouter Client", "Ajouter Réservation"])

with tabs[0]:
    st.header("Liste des Réservations")
    sort_by = st.selectbox("Trier par", ["Date d'arrivée", "Ville"])
    query = '''
    SELECT r.Id_Reservation, r.Nom_complet, h.Ville, r.Date_arrivee, r.Date_depart
    FROM Reservation r
    JOIN Concerner c ON r.Id_Reservation = c.Id_Reservation
    JOIN Chambre ch ON c.Id_Type = ch.Id_Type
    JOIN Hotel h ON ch.Id_Hotel = h.Id_Hotel
    '''
    if sort_by == "Date d'arrivée":
        query += " ORDER BY r.Date_arrivee"
    else:
        query += " ORDER BY h.Ville"
    df = fetch_data(query)
    st.dataframe(df.style.set_properties(**{'background-color': 'rgba(255, 255, 255, 0.9)', 'color': '#333'}))
    reservation_to_delete = st.selectbox("Sélectionner une réservation à supprimer", df['Id_Reservation'].tolist(), format_func=lambda x: f"Réservation {x} - {df[df['Id_Reservation'] == x]['Nom_complet'].iloc[0]}", key="delete_reservation")
    if st.button("Supprimer la réservation", key="delete_button"):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Concerner WHERE Id_Reservation = ?", (reservation_to_delete,))
            cursor.execute("DELETE FROM Reservation WHERE Id_Reservation = ?", (reservation_to_delete,))
            conn.commit()
            st.success(f"Réservation {reservation_to_delete} supprimée avec succès !")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Erreur lors de la suppression : {str(e)}. Vérifiez les données.")

with tabs[1]:
    st.header("Liste des Clients")
    search_name = st.text_input("Rechercher par nom", placeholder="Entrez un nom...")
    ville_filter = st.selectbox("Filtrer par ville", ["Tous"] + fetch_data("SELECT DISTINCT Ville FROM Client")["Ville"].tolist())
    query = "SELECT Nom_complet, Adresse, Ville, Code_postal, Email, Numero_de_telephone FROM Client WHERE 1=1"
    params = []
    if search_name:
        query += " AND Nom_complet LIKE ?"
        params.append(f"%{search_name}%")
    if ville_filter != "Tous":
        query += " AND Ville = ?"
        params.append(ville_filter)
    try:
        df = fetch_data(query, tuple(params))
        if df.empty:
            st.warning("Aucun client trouvé.")
        else:
            st.dataframe(df.style.format({"Code_postal": "{:,.0f}", "Numero_de_telephone": "{:,.0f}"}))
    except Exception as e:
        st.error(f"Erreur : {str(e)}")

with tabs[2]:
    st.header("Chambres Disponibles")
    date_debut = st.date_input("Date de début")
    date_fin = st.date_input("Date de fin")
    type_filter = st.selectbox("Type de chambre", ["Tous"] + fetch_data("SELECT DISTINCT Type FROM Type_Chambre")["Type"].tolist())
    if date_debut and date_fin:
        query = '''
        SELECT ch.Id_Chambre, ch.Etage, h.Ville, tc.Type
        FROM Chambre ch
        JOIN Hotel h ON ch.Id_Hotel = h.Id_Hotel
        JOIN Type_Chambre tc ON ch.Id_Type = tc.Id_Type
        WHERE ch.Id_Type NOT IN (
            SELECT c.Id_Type
            FROM Reservation r
            JOIN Concerner c ON r.Id_Reservation = c.Id_Reservation
            WHERE (r.Date_arrivee <= ? AND r.Date_depart >= ?)
        )
        '''
        if type_filter != "Tous":
            query += " AND tc.Type = ?"
        try:
            conn = get_connection()
            params = (str(date_fin), str(date_debut)) if type_filter == "Tous" else (str(date_fin), str(date_debut), type_filter)
            df = pd.read_sql_query(query, conn, params=params)
            if df.empty:
                st.warning("Aucune chambre disponible.")
            else:
                st.subheader("Disponibilité par étage :")
                etage_summary = df.groupby('Etage').size().reset_index(name='NombreChambres')
                st.write(etage_summary)
                st.subheader("Détails des chambres :")
                st.dataframe(df)
        except Exception as e:
            st.error(f"Erreur : {str(e)}")
    else:
        st.warning("Sélectionne les dates.")

with tabs[3]:
    st.header("Ajouter un Client")
    with st.form("form_client"):
        nom_complet = st.text_input("Nom complet", help="Entrez le nom complet du client.")
        adresse = st.text_input("Adresse")
        ville = st.text_input("Ville")
        code_postal = st.number_input("Code postal", min_value=1000, max_value=99999, step=1)
        email = st.text_input("Email", help="Exemple: nom@email.com")
        telephone = st.number_input("Numéro de téléphone", min_value=100000000, max_value=999999999, step=1)
        submit = st.form_submit_button("Ajouter")
        if submit:
            if all([nom_complet, adresse, ville, email]) and code_postal > 1000 and telephone > 100000000:
                if "@" in email and "." in email:
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute('SELECT COUNT(*) FROM Client WHERE Email = ?', (email,))
                        if cursor.fetchone()[0] > 0:
                            st.error("Cet email existe déjà. Veuillez utiliser un autre email.")
                        else:
                            cursor.execute('''
                            INSERT INTO Client (Nom_complet, Adresse, Ville, Code_postal, Email, Numero_de_telephone)
                            VALUES (?, ?, ?, ?, ?, ?)
                            ''', (nom_complet, adresse, ville, code_postal, email, telephone))
                            conn.commit()
                            st.success(f"Client {nom_complet} ajouté ! Email : {email}, Téléphone : {telephone}")
                    except sqlite3.IntegrityError:
                        st.error("Nom complet existe déjà.")
                    except Exception as e:
                        st.error(f"Erreur : {str(e)}")
                    finally:
                        pass  # La connexion est gérée par st.cache_resource
                else:
                    st.error("L'email doit contenir '@' et '.'.")
            else:
                st.error("Remplis tous les champs correctement.")

with tabs[4]:
    st.header("Ajouter une Réservation")
    with st.form("form_reservation"):
        nom_complet = st.selectbox("Nom du client", fetch_data("SELECT Nom_complet FROM Client")["Nom_complet"])
        date_arrivee = st.date_input("Date d'arrivée")
        date_depart = st.date_input("Date de départ")
        type_chambre = st.selectbox("Type de chambre", fetch_data("SELECT Type FROM Type_Chambre")["Type"])
        submit = st.form_submit_button("Ajouter")
        if submit:
            if nom_complet and date_arrivee and date_depart and type_chambre:
                if date_depart > date_arrivee:
                    try:
                        query_dispo = '''
                        SELECT ch.Id_Chambre
                        FROM Chambre ch
                        JOIN Type_Chambre tc ON ch.Id_Type = tc.Id_Type
                        WHERE tc.Type = ? AND ch.Id_Type NOT IN (
                            SELECT c.Id_Type
                            FROM Reservation r
                            JOIN Concerner c ON r.Id_Reservation = c.Id_Reservation
                            WHERE (r.Date_arrivee <= ? AND r.Date_depart >= ?)
                        )
                        LIMIT 1
                        '''
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute(query_dispo, (type_chambre, str(date_depart), str(date_arrivee)))
                        chambre_dispo = cursor.fetchone()
                        if chambre_dispo:
                            cursor.execute("SELECT Id_Type FROM Type_Chambre WHERE Type = ?", (type_chambre,))
                            id_type = cursor.fetchone()[0]
                            cursor.execute('''
                            INSERT INTO Reservation (Date_arrivee, Date_depart, Nom_complet)
                            VALUES (?, ?, ?)
                            ''', (str(date_arrivee), str(date_depart), nom_complet))
                            id_reservation = cursor.lastrowid
                            cursor.execute('''
                            INSERT INTO Concerner (Id_Reservation, Id_Type)
                            VALUES (?, ?)
                            ''', (id_reservation, id_type))
                            conn.commit()
                            st.success(f"Réservation ajoutée pour {nom_complet} du {date_arrivee} au {date_depart} !")
                        else:
                            st.error(f"Aucune chambre de type {type_chambre} disponible pour ces dates.")
                    except Exception as e:
                        st.error(f"Erreur lors de l'ajout de la réservation : {str(e)}. Vérifiez les dates ou la disponibilité.")
                    finally:
                        pass  # La connexion est gérée par st.cache_resource
                else:
                    st.error("La date de départ doit être postérieure à la date d'arrivée.")
            else:
                st.error("Veuillez remplir tous les champs du formulaire.")

# Tableau de Bord des Statistiques
st.header("Tableau de Bord des Statistiques")
st.markdown("### Analyse personnalisée des réservations")
col1, col2 = st.columns(2)
with col1:
    date_debut_stats = st.date_input("Date de début (stats)", value=datetime(2025, 1, 1))
with col2:
    date_fin_stats = st.date_input("Date de fin (stats)", value=datetime(2025, 12, 31))

total_reservations = len(fetch_data("SELECT * FROM Reservation"))
st.metric("Nombre total de réservations", total_reservations)

stat_type = st.selectbox("Type de statistique", ["Par Ville", "Par Type de Chambre", "Par Mois"])

if stat_type == "Par Ville":
    query = '''
    SELECT h.Ville, COUNT(DISTINCT r.Id_Reservation) as NombreReservations
    FROM Reservation r
    JOIN Concerner c ON r.Id_Reservation = c.Id_Reservation
    JOIN Chambre ch ON c.Id_Type = ch.Id_Type
    JOIN Hotel h ON ch.Id_Hotel = h.Id_Hotel
    WHERE r.Date_arrivee >= ? AND r.Date_depart <= ?
    GROUP BY h.Ville
    '''
    chart_index = 'Ville'
    chart_color = '#FF6384'
elif stat_type == "Par Type de Chambre":
    query = '''
    SELECT tc.Type, COUNT(DISTINCT r.Id_Reservation) as NombreReservations
    FROM Reservation r
    JOIN Concerner c ON r.Id_Reservation = c.Id_Reservation
    JOIN Type_Chambre tc ON c.Id_Type = tc.Id_Type
    WHERE r.Date_arrivee >= ? AND r.Date_depart <= ?
    GROUP BY tc.Type
    '''
    chart_index = 'Type'
    chart_color = '#36A2EB'
else:  # Par Mois
    query = '''
    SELECT strftime('%Y-%m', r.Date_arrivee) as Mois, COUNT(DISTINCT r.Id_Reservation) as NombreReservations
    FROM Reservation r
    WHERE r.Date_arrivee >= ? AND r.Date_depart <= ?
    GROUP BY strftime('%Y-%m', r.Date_arrivee)
    ORDER BY Mois
    '''
    chart_index = 'Mois'
    chart_color = '#FFCE56'

try:
    df = fetch_data(query, params=(str(date_debut_stats), str(date_fin_stats)))
    if df.empty:
        st.warning("Aucune donnée pour cette période.")
    else:
        st.write("Vérification des réservations :", fetch_data("SELECT * FROM Reservation"))
        st.subheader(f"Résumé {stat_type} :")
        st.write("Données brutes pour le graphique :", df)
        st.dataframe(df.style.format({"NombreReservations": "{:,.0f}"}))
        chart_data = df.set_index(chart_index)[['NombreReservations']]
        st.bar_chart(chart_data, color=chart_color)
except Exception as e:
    st.error(f"Erreur lors du chargement des statistiques : {str(e)}. Vérifiez la période sélectionnée.")