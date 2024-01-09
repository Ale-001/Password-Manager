import csv
from tkinter import messagebox
from cryptography.fernet import Fernet
import base64
from KeyManager import *

class PasswordManager(KeyManager):
    
    def __init__(self):
        self.passwordfile = None  # percorso del file delle password
        self.password_dict = {}  # dizionario delle password
        
        
     
    #Crea un nuovo Password File   
    def create_new_passwordfile(self, path):
        self.passwordfile = path
        with open(self.passwordfile, 'w', newline="") as f:
            if self.passwordfile.endswith(".csv"):
                writer = csv.writer(f ,delimiter=";") #oppure delimiter="\t"
                writer.writerow(["Sito", "Nome Utente", "Password", "Note"])
                messagebox.showinfo("Successo", "Generazione del password file in csv avvenuta con successo.")
            elif self.passwordfile.endswith(".txt"):
                f.write("Sito;\tNome Utente;\tPassword;\tNote;\n")  #da decidere che modificatore usare
                messagebox.showinfo("Successo", "Generazione del password file in txt avvenuta con successo.")
            else:
                messagebox.showerror("Errore", f"Impossibile creare il file {path}.")
    
    
    
    #Aggiunge gli elementi nel file
    def add_new_password(self):
        site = self.site_input.get()
        username = self.username_input.get()
        password = self.password_input.get()
        notes = self.notes_input.get()
        try:
            encrypted_password = self.encrypt_password(password)
            encoded_password = base64.b64encode(encrypted_password).decode("utf-8")
        except ValueError as e:
            messagebox.showerror("Errore", str(e))
            return
            
        row = [site, username, encoded_password, notes]
            
        with open(self.passwordfile, 'a', newline='') as f:
            if self.passwordfile.endswith(".csv"):
                writer = csv.writer(f,delimiter=";")
                writer.writerow(row)
                messagebox.showinfo("Successo", "Password aggiunta con successo.")
            elif self.passwordfile.endswith(".txt"):
                f.write("\t".join(map(str,row)) + "\n")
                messagebox.showinfo("Successo", "Password aggiunta con successo.")
            else:
                messagebox.showinfo("Errore", "Password non aggiunta.")
                
    #Prova Crea un lista di tuple con le password
    def create_password_list(self ):
        password_list = []  # Inizializza un dizionario vuoto
        
        try:
            with open(self.passwordfile, 'r', newline='') as f:
                if self.passwordfile.endswith(".csv"):
                    reader = csv.reader(f, delimiter=";")
                elif self.passwordfile.endswith(".txt"):
                    reader = csv.reader(f, delimiter="\t")
                else:
                    messagebox.showinfo("Errore", "Formato file non supportato.")
                    return

                next(reader)  # Salta la prima riga del file

                for row in reader:
                    site = row[0]
                    username = row[1]
                    encoded_password = row[2]
                    notes = row[3]

                    encrypted_password = base64.b64decode(encoded_password)
                    password = self.decrypt_password(encrypted_password)
                    if password is None:
                        password = "Errore nella decrittografia della password"
                        
                    # Aggiungi una tupla rappresentante la password alla lista
                    password_tuple = (site, username, password, notes)
                    password_list.append(password_tuple)
                
        except Exception as e:
            print(f"Errore durante la lettura del file: {e}")
        
        return password_list

                    
    #Crittografa la password funziona
    def encrypt_password(self, password):
        if self.cipher_suite is None:
            raise ValueError("La chiave di crittografia non è stata impostata.")
        password_bytes = password.encode()
        encrypted_password = self.cipher_suite.encrypt(password_bytes)
        return encrypted_password
    
    
    
    #Decrypta le password 
    def decrypt_password(self, encrypted_password):
        try:
            if self.cipher_suite is None:
                raise ValueError("La chiave di crittografia non è stata impostata")
            password_bytes = self.cipher_suite.decrypt(encrypted_password)
            password = password_bytes.decode()
            return password
        except Exception as e:
            print(f"Errore nella decrittografia della password: {e}")
            return None
    
    # Stampa il contenuto del passwordfile
    def print_passwordfile(self):
        password_list = self.create_password_list()

        # Iterate over the list of tuples and print the contents
        for password_tuple in password_list:
            site, username, password, notes = password_tuple
            text = f"Sito: {site}\nUsername: {username}\nPassword: {password}\nNotes: {notes}\n\n"
            self.text_box.insert("end", text)
            self.text_box.insert("end", "--------------------------\n")
        
    # Stampa le password in base alla ricerca per Site
    def print_passwords_site(self, sito):
        password_list = self.create_password_list()

        found = False
        for password_tuple in password_list:
            site, username, password, notes = password_tuple
            if site.lower() == sito.lower():
                text = f"Sito: {site}\nUsername: {username}\nPassword: {password}\nNotes: {notes}\n\n"
                self.text_box.insert("end", text)
                self.text_box.insert("end", "--------------------------\n")
                found = True

        if not found:
            self.text_box.insert('end', "Sito non trovato.\n")

    # Stampa le password in base alla ricerca per Username
    def print_passwords_username(self, username):
        password_list = self.create_password_list()

        found = False
        for password_tuple in password_list:
            site, user, password, notes = password_tuple
            if user.lower() == username.lower():
                text = f"Sito: {site}\nUsername: {user}\nPassword: {password}\nNotes: {notes}\n\n"
                self.text_box.insert("end", text)
                self.text_box.insert("end", "--------------------------\n")
                found = True

        if not found:
            self.text_box.insert('end', "Username non trovato.\n")
            
        #Modifica la password di un account
    def modify_password(self, sito, username, new_password):
        try:
            # Sovrascrivi solo l'elemento specifico nel file delle password
            self.write_modify_password_list(sito, username, new_password)

            # Leggi il file delle password e crea una lista di tuple
            password_list = self.create_password_list()
            for i, password_tuple in enumerate(password_list):
                site, user, password, notes = password_tuple
                if site.lower() == sito.lower() and user.lower() == username.lower():
            
                # Aggiorna il testo della Label con il risultato
                    self.result_label.config(text=f"Password modificata per il sito {sito} e l'utente {username}.")
                else:
                     self.result_label.config(text=f"I dati inseriti sono errati, verifica se il sito {sito} o l'utente {username} esistano.")
        except Exception as e:
            self.result_label.config(text=f"Errore durante la modifica della password: {e}")

    # FUNZIONANO Sovrascrive solo l'elemento specifico nel file delle password
    def write_modify_password_list(self, site, username, new_password):
        try:
            # Leggi il file delle password e crea una lista di tuple
            password_list = self.create_password_list()

            found = False
            for i, password_tuple in enumerate(password_list):
                current_site, current_username, current_password, notes = password_tuple
                if current_site.lower() == site.lower() and current_username.lower() == username.lower():
                    # Modifica la password nella tupla
                    password_list[i] = (current_site, current_username, new_password, notes)
                    found = True
                    break  # Esci dal loop una volta trovato l'elemento

            if found:
                # Sovrascrivi solo l'elemento specifico nel file delle password
                with open(self.passwordfile, 'w', newline='') as f:
                    if self.passwordfile.endswith(".csv"):
                        writer = csv.writer(f, delimiter=";")
                        # Scrivi l'intestazione
                        writer.writerow(['Sito', 'Username', 'Password', 'Notes'])

                        # Scrivi ogni riga nel file
                        for password_tuple in password_list:
                            site, username, password, notes = password_tuple
                            # Crittografa la nuova password
                            encrypted_password = self.encrypt_password(password)
                            encoded_password = base64.b64encode(encrypted_password).decode('utf-8')
                            writer.writerow([site, username, encoded_password, notes])
                    elif self.passwordfile.endswith(".txt"):
                        f.write("Sito;\tNome Utente;\tPassword;\tNote;\n")
                        for password_tuple in password_list:
                            site, username, password, notes = password_tuple
                            # Crittografa la nuova password
                            encrypted_password = self.encrypt_password(password)
                            encoded_password = base64.b64encode(encrypted_password).decode('utf-8')
                            f.write(f"{site};\t{username};\t{encoded_password};\t{notes}\n")
                    else:
                        raise ValueError("Formato file non supportato.")
            else:
                raise ValueError("Sito o username non trovato. Impossibile modificare la password.")
        except Exception as e:
            print(f"Errore durante la modifica della password nel file: {e}")

         
    def set_passwordfile(self, passwordfile):
        """
        Imposta il percorso del file delle password.
        """
        self.passwordfile = passwordfile
        
    def get_passwordfile(self):
        """
        Restituisce il percorso del file delle password.
        """
        return self.passwordfile
    

        
def main():
    pm=PasswordManager()
if __name__ == "__main__":
    main()