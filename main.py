import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime,timedelta


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
 
    alegere=input("\nAlegeti o optiune: ")
    if alegere=="1":
        programare_noua()
    elif alegere=="2":
        afisare_clienti()
    elif alegere=="3":
        afiseaza_programari()
    elif alegere=="4":
        afisare_venituri()
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

    data = input("Data programarii (ZZ.LL.AAAA): ")
    try:
     data = datetime.strptime(data, "%d.%m.%Y").strftime("%Y-%m-%d")
    except ValueError:
     print("Data invalida. Folositi formatul ZZ.LL.AAAA.")
     return

    
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

def afiseaza_programari():
    print("\nPROGRAMARI\n")
    cursor.execute("""
    SELECT
            PROGRAMARI.id_programare,
            CLIENTI.nume,
            CLIENTI.telefon,
            CLIENTI.adresa,
            PROGRAMARI.tip_curatenie,
            PROGRAMARI.suprafata,
            PROGRAMARI.pret,
            PROGRAMARI.data,
            PROGRAMARI.ora,
            PROGRAMARI.status
        FROM PROGRAMARI
        JOIN CLIENTI
        ON PROGRAMARI.id_client = CLIENTI.id_client
        WHERE PROGRAMARI.status != "Finalizata"
        ORDER BY PROGRAMARI.data, PROGRAMARI.ora
    """)
    programari = cursor.fetchall()

    if not programari:
        print("Nu exista programari.")
        return

    for programare in programari:
         
        data_afisare = datetime.strptime(
        programare[7],
        "%Y-%m-%d"
        ).strftime("%d.%m.%Y")
    
        print(f"""
        ID Programare: {programare[0]}
        Nume Client: {programare[1]}
        Telefon Client: {programare[2]}
        Adresa Client: {programare[3]}
        Tip Curatenie: {programare[4]}
        Suprafata: {programare[5]} m²
        Pret: {programare[6]} RON
        Data: {data_afisare}
        Ora: {programare[8]}
        Status: {programare[9]}
        """)

    alegere = input("Introduceti ID-ul programarii: ")

    if alegere == "":
        return

    print("\nCe doriti sa faceti?")
    print("1. Finalizeaza programarea")
    print("2. Modifica programarea")

    actiune = input("Alegeti o optiune: ")

    if actiune == "1":

        cursor.execute("""
        UPDATE PROGRAMARI
        SET status = "Finalizata"
        WHERE id_programare = ?
        """, (alegere,))

        if cursor.rowcount > 0:
         print("Programarea a fost marcata ca finalizata.")
        else:
         print("Nu exista o programare cu acest ID.")

    elif actiune == "2":

        ora_noua = input("Introduceti ora noua: ")
        data_noua = input("Introduceti data noua (ZZ.LL.AAAA): ")
        try:
         data_noua = datetime.strptime(data_noua, "%d.%m.%Y").strftime("%Y-%m-%d")
        except ValueError:
         print("Data invalida. Folositi formatul ZZ.LL.AAAA.")
         return
        
        cursor.execute("""
        UPDATE PROGRAMARI
        SET ora = ?, data = ?
        WHERE id_programare = ?
        """, (ora_noua, data_noua, alegere))

        if cursor.rowcount > 0:
          print("Programarea a fost modificata cu succes.")
        else:
          print("Nu exista o programare cu acest ID.")

    else:
        print("Optiune invalida.")

    conexiune.commit()
  
def afisare_clienti():
    print("\nCLIENTI\n")

    cursor.execute("""
    SELECT NUME, TELEFON FROM CLIENTI
    """)

    clienti = cursor.fetchall()

    if not clienti:
        print("Nu exista clienti.")
        return

    for client in clienti:
        print(f"""
        Nume Client: {client[0]}
        Telefon Client: {client[1]}
        """)
    meniu_principal()

def afisare_venituri():
    print("\nVENITURI\n")

    an = input("Introduceti anul: ")
    luna = input("Introduceti luna : ")

    if len(luna) == 1:
        luna = "0" + luna

    cursor.execute("""
        SELECT SUM(pret)
        FROM PROGRAMARI
        WHERE status = "Finalizata"
        AND strftime('%Y', data) = ?
        AND strftime('%m', data) = ?
    """, (an, luna))

    venituri = cursor.fetchone()[0]

    if venituri is None:
        venituri = 0

    cursor.execute("""
        SELECT COUNT(*)
        FROM PROGRAMARI
        WHERE status = "Finalizata"
        AND strftime('%Y', data) = ?
        AND strftime('%m', data) = ?
    """, (an, luna))

    numar_programari = cursor.fetchone()[0]

    print(f"\nRAPORT {luna}.{an}")
    print(f"Venituri: {venituri} RON")
    print(f"Programari finalizate: {numar_programari}")
   
meniu_principal()











        
