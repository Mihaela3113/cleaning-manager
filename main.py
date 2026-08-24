import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

database = os.getenv("DATABASE")

conexiune = sqlite3.connect(database)
cursor = conexiune.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS CLIENTI (
    id_client INTEGER PRIMARY KEY AUTOINCREMENT,
    nume TEXT NOT NULL,
    telefon TEXT NOT NULL,
    adresa TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS PROGRAMARI (
    id_programare INTEGER PRIMARY KEY AUTOINCREMENT,
    id_client INTEGER NOT NULL,
    tip_curatenie TEXT NOT NULL,
    suprafata REAL NOT NULL,
    pret REAL NOT NULL,
    data TEXT NOT NULL,
    ora TEXT NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (id_client) REFERENCES CLIENTI(id_client)
)
""")

conexiune.commit()

def meniu_principal():
   
    print("\nCLEANING MANAGER\n")
    print("1. Adauga programare noua")
    print("2. Clienti")
    print("3. Programari")
    print("4. Venituri")
    print("5. Rapoarte")
 
    alegere=input("\nAlegeti o optiune: ")
    if alegere=="1":
        programare_noua()
    else:
        print("Optiune invalida. Va rugam sa alegeti o optiune valida.") 
        
        

def programare_noua():
    print("\nPROGRAMARE NOUA")

    nume = input("Nume client: ")
    telefon=input("Telefon client: ")
    adresa=input("Adresa client: ")

    print("\nTip curatenie:")
    print("1. Intretinere")
    print("2. Generala")
    print("3. O camera")

    alegere_tip = input("Alege tipul de curatenie: ")

    if alegere_tip == "1":
        tip_curatenie = "Intretinere"
    elif alegere_tip == "2":
        tip_curatenie = "Generala"
    elif alegere_tip == "3":
        tip_curatenie = "O camera"
    else:
        print("Optiune invalida.")
        return

    suprafata=float(input("Suprafata in metri patrati:"))

    pret=float(input("Pretul estimativ:"))

    data=input("Data programarii: ")

    ora=input("Ora programarii: ")

    cursor.execute(
        "SELECT id_client FROM CLIENTI WHERE telefon = ?",
        (telefon,)
    )

    client = cursor.fetchone()

    if client is None:
        cursor.execute(
            """
            INSERT INTO CLIENTI (nume, telefon, adresa)
            VALUES (?, ?, ?)
            """,
            (nume, telefon, adresa)
        )

        id_client = cursor.lastrowid

        print("\nClient adaugat cu succes.")

    else:
        id_client = client[0]

        print("\nClient existent. Nu am creat un client nou.")

    cursor.execute(
        """
        INSERT INTO PROGRAMARI
        (id_client, tip_curatenie, suprafata, pret, data, ora, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            id_client,
            tip_curatenie,
            suprafata,
            pret,
            data,
            ora,
            "Programata"
        )
    )
    
    conexiune.commit()
    
    print("\nProgramarea a fost adaugata cu succes.")

meniu_principal()











        
