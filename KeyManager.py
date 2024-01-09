from cryptography.fernet import Fernet
from tkinter import messagebox
import os
import csv

#funzionante

class KeyManager:
    def __init__(self):
        self.keyfile = None
        self.key = None 
        self.chipher_suite = None 
    
    def create_new_keyfile(self,file):
        self.keyfile = file
        self.key = Fernet.generate_key()
        with open(self.keyfile, "wb") as f:
            if self.keyfile.endswith(".txt"):
                f.write(self.key)
                self.cipher_suite = Fernet(self.key)
                messagebox.showinfo("Successo", "Generazione della chiave avvenuta con successo.")
            else:
                messagebox.showinfo("Annullato", "Generazione della chiave annullata.")
        return self.key , self.keyfile , self.cipher_suite
        
        
    def set_keyfile(self, keyfile):
        """
        Imposta il percorso del file della chiave.
        """
        self.keyfile = keyfile
        
    def get_keyfile(self):
        """
        Restituisce il percorso del file della chiave.
        """
        return self.keyfile
    
    def import_exist_keyfile(self, file):
        # Importo una file contenente la Key in txt
        self.keyfile = file
        with open(self.keyfile, 'r') as f:
            if self.keyfile.endswith(".txt"):
                self.key = f.read()
                self.cipher_suite = Fernet(self.key)
            else:
                messagebox.showinfo("Annullato", "Chiave non importata.")
        return self.key , self.keyfile , self.cipher_suite
    
    #Metodo di prova per vedere la chiave, usato come aiuto per sviluppare il programma
    def print_keyfile(self):
        with open(self.keyfile, 'r') as f:
            print(f.read())

def main():
    key = KeyManager()
        
if __name__ == "__main__":
    main()