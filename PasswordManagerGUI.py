import tkinter as tk
from tkinter import filedialog, messagebox
from PasswordManager import *
from KeyManager import *
from PasswordGenerator import *
from tkinter.scrolledtext import ScrolledText 
import pyperclip      


class MainWindow(tk.Frame,PasswordManager,KeyManager,PasswordGenerator):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # calcola la posizione della finestra per centrarla
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (800 // 2)
        y = (screen_height // 2) - (600 // 2)
        self.master.geometry(f"800x600+{x}+{y}")            
        self.pack()
        self.create_widgets()
        self.passwordfile = None
        self.keyfile = None
        self.key = None
        self.cipher_suite = None

    #elementi della finestra
    def create_widgets(self):
        # imposto lo sfondo scuro
        self.master.configure(bg="#2d2d2d")
        #Title
        self.title_label = tk.Label(self.master, text="Password Manager",font=("Arial",24), bg="#2d2d2d", fg="white")
        self.title_label.pack(side="top", pady=20, anchor="center")
        #Creo un frame 
        self.button_frame = tk.Frame(self.master, bg="#2d2d2d")
        self.button_frame.pack(side = "top")
        #Title
        self.titleFile_label = tk.Label(self.button_frame, text="Imposta un PasswordFile:",font=("Arial",16), bg="#2d2d2d", fg="white")
        self.titleFile_label.grid(row=0, column=0,padx=10,pady=10, columnspan=2, sticky="ew")
        #Button per il Password File
        self.button_crea = tk.Button(self.button_frame, text = "Crea un Password File", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2",command = self.create_passwordfile)
        self.button_crea.grid(row=1, column=0,padx=10,pady=10)#posizionato a sinistra all'interno del frame
        self.button_importa = tk.Button(self.button_frame, text = "Importa un Password File", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2",command=self.set_password_file)
        self.button_importa.grid(row=1, column=1,padx=10,pady=10)#posizionato a destra all'interno del frame
        #Title label con il percorso del password file
        self.password_file_label = tk.Label(self.button_frame, text="Nessun Password File impostato.",font=("Arial",10), bg="#2d2d2d", fg="white")
        self.password_file_label.grid(row=2, column=0,padx=10,pady=10, columnspan=2, sticky="ew")
        #Title
        self.titleKey_label = tk.Label(self.button_frame, text="Imposta una Chiave:",font=("Arial",16), bg="#2d2d2d", fg="white")
        self.titleKey_label.grid(row=3, column=0,padx=10,pady=10, columnspan=2, sticky="ew")#posizionato a sinistra all'interno del frame
        #Button per la Key
        self.button_creaKey = tk.Button(self.button_frame, text = "Crea una nuova Chiave", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e",font=("Arial", 12),command = self.create_Keyfile)
        self.button_creaKey.grid(row=4, column=0,padx=10,pady=10)#posizionato a sinistra all'interno del frame
        self.button_importaKey = tk.Button(self.button_frame, text = "Importa una Chiave", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e",font=("Arial", 12),command = self.import_keyfile)
        self.button_importaKey.grid(row=4, column=1,padx=10,pady=10)#posizionato a destra all'interno del frame
        #Title label con il percorso della chiave
        self.key_file_label = tk.Label(self.button_frame, text="Nessun Chiave impostata.",font=("Arial",10), bg="#2d2d2d", fg="white")
        self.key_file_label.grid(row=5, column=0,padx=10,pady=10, columnspan=2, sticky="ew")
        
        #Button Menu
        self.button_menu = tk.Button(self.button_frame, text = "Menu", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2",command = self.create_MenuWindow)
        self.button_menu.grid(row=6, column=0, columnspan=2, sticky="ew")
        # Aggiungo uno stile personalizzato per il cursore quando si passa sopra i bottoni
        self.button_crea.bind("<Enter>", lambda event: self.button_crea.config(cursor="hand2"))
        self.button_crea.bind("<Leave>", lambda event: self.button_crea.config(cursor=""))
        self.button_importa.bind("<Enter>", lambda event: self.button_importa.config(cursor="hand2"))
        self.button_importa.bind("<Leave>", lambda event: self.button_importa.config(cursor=""))
        self.button_creaKey.bind("<Enter>", lambda event: self.button_creaKey.config(cursor="hand2"))
        self.button_creaKey.bind("<Leave>", lambda event: self.button_creaKey.config(cursor=""))
        self.button_importaKey.bind("<Enter>", lambda event: self.button_importaKey.config(cursor="hand2"))
        self.button_importaKey.bind("<Leave>", lambda event: self.button_importaKey.config(cursor=""))
        self.button_menu.bind("<Enter>", lambda event: self.button_menu.config(cursor="hand2"))
        self.button_menu.bind("<Leave>", lambda event: self.button_menu.config(cursor=""))
        
        
        
        
        #Importa un Password File già esistente
    def set_password_file(self):
        # Importo un file password.csv o .txt già esistente
        filename = filedialog.askopenfilename(initialdir="/", title="Seleziona un Password File ", filetypes=(("CSV files", "*.csv"), ("TXT files", "*.txt"), ("All files", "*.*")))
        self.set_passwordfile(filename)
        self.password_file_label.config(text=f"Password File impostato: {filename}") #label che indica il percorso del passwordfile
        messagebox.showinfo("Successo", "Password File importato con successo.")
        #self.create_window()
        
    
    #Funzione per creare un nuovo PasswordFile    
    def create_passwordfile(self):
        # Creo il nuovo file password.csv
        filename = filedialog.asksaveasfilename(initialdir="/",title="Crea un nuovo Password File", defaultextension=".csv",filetypes=(("CSV files", "*.csv"),("TXT files", "*.txt")), initialfile="Password")  
        self.create_new_passwordfile(filename)
        self.password_file_label.config(text=f"File password impostato: {filename}") #label che indica il percorso del passwordfile
        
    #Funzione per creare un nuova Key    
    def create_Keyfile(self):
        # Creo il nuovo file Key.txt
        messagebox.showinfo("Attenzione", "Salvare in un luogo sicuro la Chiave Generata")
        filename = filedialog.asksaveasfilename(initialdir="/",title="Crea una nuova Chiave", defaultextension=".txt", initialfile="Key")  
        self.key, self.keyfile , self.chipher_suite = self.create_new_keyfile(filename) #uso la classe importata di PasswordManager
        #print(self.key.decode()) Prova: stampa la stringa su terminale in formato string, senza decode sarebbe in formato byte string
        self.key_file_label.config(text=f"Chiave impostata: {self.keyfile}") #label che indica il percorso della Chiave
        
    
    #Importa una chiave
    def import_keyfile(self):
        # Importo una file contenente la Key in txt
        filename = filedialog.askopenfilename(initialdir="/", title="Importa una Chiave", filetypes=(("TXT files", "*.txt"),("All files", "*.*")))
        self.key , self.keyfile , self.chipher_suite = self.import_exist_keyfile(filename)
        self.key_file_label.config(text=f"Chiave impostata: {self.keyfile}")
        messagebox.showinfo("Successo", "Chiave importata con successo.")
        
    #Crea una finestra Menu    
    def create_MenuWindow(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = MenuWindow(self.new_window, self.master, self.passwordfile, self.keyfile, self.key , self.cipher_suite)
        self.master.withdraw()
        

class MenuWindow(tk.Frame,PasswordManager,KeyManager,PasswordGenerator):
    def __init__(self, master=None, previous=None, passwordfile = None, keyfile = None , key = None , cipher_suite = None):
        super().__init__(master= None)
        self.master = master
        self.previous = previous
        self.passwordfile = passwordfile
        self.key = key
        self.keyfile = keyfile
        self.cipher_suite = cipher_suite
        # calcola la posizione della finestra per centrarla
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (800 // 2)
        y = (screen_height // 2) - (600 // 2)
        self.master.geometry(f"800x600+{x}+{y}")
        self.pack()
        self.create_widgets()
        
        
    def create_widgets(self):
        # imposto lo sfondo scuro
        self.master.configure(bg="#2d2d2d")
        #back
        self.back_button = tk.Button(self.master, text="⬅️", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.go_back)
        self.back_button.pack(side="top", anchor="nw")
        #Creo un frame 
        self.button_frame = tk.Frame(self.master, bg="#2d2d2d")
        self.button_frame.pack( side = "top")
        #Title 1
        self.title_label = tk.Label(self.button_frame, text="Menu Password Manager",font=("Arial",24), bg="#2d2d2d", fg="white")
        self.title_label.grid(row=0, column=0,padx=10,pady=10, columnspan=2, sticky="ew")
        #Title 2
        self.titleMenu_label = tk.Label(self.button_frame, text="Seleziona un'operazione:",font=("Arial",16), bg="#2d2d2d", fg="white")
        self.titleMenu_label.grid(row=2, column=0,padx=10,pady=10, columnspan=2, sticky="ew")
        #button
        self.add_password_button = tk.Button(self.button_frame, text="Aggiungi Password", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.create_window)
        self.add_password_button.grid(row=3, column=0, columnspan=2, sticky="ew")
        
        self.view_passwords_button = tk.Button(self.button_frame, text="Visualizza Password", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.create_VisualizzaPasswordWindow)
        self.view_passwords_button.grid(row=4, column=0, columnspan=2, sticky="ew")
        
        self.view_passwords_button = tk.Button(self.button_frame, text="Genera Password", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.create_GeneraPasswordWindow)
        self.view_passwords_button.grid(row=5, column=0, columnspan=2, sticky="ew")
        #Cerca le password per sito
        self.view_passwords_for_site_button = tk.Button(self.button_frame, text="Cerca le Password per sito", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.create_view_password_site)
        self.view_passwords_for_site_button.grid(row=6, column=0, columnspan=2, sticky="ew")
        #Cerca le password per nome
        self.view_passwords_for_name_button = tk.Button(self.button_frame, text="Cerca le Password per Username", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.create_view_password_username)
        self.view_passwords_for_name_button.grid(row=7, column=0, columnspan=2, sticky="ew")
         
        #Modifica la password
        self.modify_password_button = tk.Button(self.button_frame, text="Modifica Password", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.create_ModifyPasswordWindow)
        self.modify_password_button.grid(row=8, column=0, columnspan=2, sticky="ew")
        
        #Chiudi il programma
        self.quit_button = tk.Button(self.button_frame, text="Chiudi", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.master.quit)
        self.quit_button.grid(row=9, column=0, columnspan=2)
        
        #Passwordfile impostato
        self.password_file_label = tk.Label(self.button_frame, text=f"File password impostato: {self.passwordfile}", font=("Arial", 10), bg="#2d2d2d", fg="white")
        self.password_file_label.grid(row=10, column=0, columnspan=2)
            
    # AggiungiPassword Window
    def create_window(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = AggiungiPasswordWindow(self.new_window, self.master,self.passwordfile,self.keyfile,self.key , self.cipher_suite)
        self.master.withdraw()
        
    # VisualizzaPassword Window
    def create_VisualizzaPasswordWindow(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = VisualizzaPasswordWindow(self.new_window, self.master,self.passwordfile,self.keyfile,self.key, self.cipher_suite)
        self.master.withdraw()
        
     # VisualizzaPassword Window
    def create_view_password_site(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = VisualizzaPasswordSiteWindow(self.new_window, self.master,self.passwordfile,self.keyfile,self.key,self.cipher_suite)
        self.master.withdraw()
        
     # VisualizzaPassword Window
    def create_view_password_username(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = VisualizzaPasswordUsernameWindow(self.new_window, self.master,self.passwordfile,self.keyfile,self.key,self.cipher_suite)
        self.master.withdraw()
        
    # GeneraPassword Window       
    def create_GeneraPasswordWindow(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = GeneraPasswordWindow(self.new_window, self.master,self.passwordfile,self.keyfile,self.key)
        self.master.withdraw()  
    
    # ModifyPassword Window
    def create_ModifyPasswordWindow(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = ModifyPasswordWindow(self.new_window, self.master,self.passwordfile,self.keyfile,self.key,self.cipher_suite)
        self.master.withdraw()  
        
    def go_back(self):
        self.previous.deiconify()
        self.master.destroy()
        
class ModifyPasswordWindow(tk.Frame,PasswordManager,KeyManager,PasswordGenerator):
    def __init__(self, master = None, previous = None, passwordfile = None, keyfile = None, key = None, cipher_suite = None):
        super().__init__(master)
        self.master = master
        self.previous = previous
        self.passwordfile = passwordfile
        self.keyfile = keyfile
        self.key = key
        self.cipher_suite = cipher_suite
        # calcola la posizione della finestra per centrarla
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (900 // 2)
        y = (screen_height // 2) - (800 // 2)
        self.master.geometry(f"900x800+{x}+{y}") 
        self.pack()
        self.create_widgets()
        
    def create_widgets(self):
        # imposto lo sfondo scuro
        self.master.configure(bg="#2d2d2d") 
        #back
        self.back_button = tk.Button(self.master, text="⬅️", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.go_back)
        self.back_button.pack(side="top", anchor="nw") 
        #button_frame
        self.button_frame = tk.Frame(self.master, bg="#2d2d2d")
        self.button_frame.pack(side = "top")
        
        #Title 1
        self.title_label = tk.Label(self.button_frame, text="Modifica Password",font=("Arial",24), bg="#2d2d2d", fg="white")
        self.title_label.grid(row=0, column=0,padx=10,pady=10, columnspan=3, sticky="ew")
        
        #Label con scritte degli elementi
        self.site_label = tk.Label(self.button_frame, text="Sito:",font=("Arial",14), bg="#2d2d2d", fg="white")
        self.site_label.grid(row=1, column=0,padx=10,pady=10)
        
        self.username_label = tk.Label(self.button_frame, text="Username:",font=("Arial",14), bg="#2d2d2d", fg="white")
        self.username_label.grid(row=2, column=0,padx=10,pady=10)
        
        self.new_password_label = tk.Label(self.button_frame, text="New Password:",font=("Arial",14), bg="#2d2d2d", fg="white")
        self.new_password_label.grid(row=3, column=0,padx=10,pady=10)
        
        self.modify_password_button = tk.Button(self.button_frame, text="Modifica Password:",font=("Arial",14), bg="#2d2d2d", fg="white",command=self.modify_password_account)
        self.modify_password_button.grid(row=4, column=0,padx=10,pady=10)
        
        #Label con il risultato
        self.result_label = tk.Label(self.button_frame, text="",font=("Arial",14), bg="#2d2d2d", fg="white")
        self.result_label.grid(row=5, column=0, columnspan=2)
        
        
        
        # Input
        #input site
        self.site_input = tk.Entry(self.button_frame,font=("Arial",14), bg="#2d2d2d", fg="white")
        self.site_input.grid(row=1, column=1,padx=10,pady=10)
        
        #input username
        self.username_input = tk.Entry(self.button_frame,font=("Arial",14), bg="#2d2d2d", fg="white")
        self.username_input.grid(row=2, column= 1, padx=10,pady=10)
        
        #input new_password
        self.new_password_input = tk.Entry(self.button_frame,font=("Arial",14), bg="#2d2d2d", fg="white", show="*")
        self.new_password_input.grid(row=3, column= 1, padx=10,pady=10)
        
        
        #Aggiungere i Metodi#
    def modify_password_account(self):
        sito = self.site_input.get()
        username = self.username_input.get()
        new_password = self.new_password_input.get()
        
        if sito and username and new_password:
            self.modify_password(sito, username, new_password)
        else:
            messagebox.showinfo("Errore", "Compila tutti i campi.")
      
    def go_back(self):
        self.previous.deiconify()
        self.master.destroy()
           
        
class AggiungiPasswordWindow(tk.Frame,PasswordManager,KeyManager,PasswordGenerator):
    def __init__(self, master=None, previous=None, passwordfile = None, keyfile = None , key = None,cipher_suite = None, value = 0,min_value=0, max_value=12, min_length_value= 8, max_length_value = 30):
        super().__init__(master)
        self.master = master
        self.previous = previous
        self.passwordfile = passwordfile
        self.key = key
        self.keyfile = keyfile
        self.cipher_suite = cipher_suite
        # calcola la posizione della finestra per centrarla
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (900 // 2)
        y = (screen_height // 2) - (800 // 2)
        self.master.geometry(f"900x800+{x}+{y}")
        self.pack()
        self.value = value
        self.password_length = 8
        self.charactersUp = 0
        self.charactersL = 0
        self.numbers = 0
        self.symbols = 0
        self.min_value = min_value
        self.max_value = max_value
        self.min_length_value = min_length_value
        self.max_length_value = max_length_value
        self.create_widgets()
        

    def create_widgets(self):
        # imposto lo sfondo scuro
        self.master.configure(bg="#2d2d2d")
        #back
        self.back_button = tk.Button(self.master, text="⬅️", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.go_back)
        self.back_button.pack(side="top", anchor="nw")  
   
        self.button_frame = tk.Frame(self.master, bg="#2d2d2d")
        self.button_frame.pack(side = "top")
        
        #Title 1
        self.title_label = tk.Label(self.button_frame, text="Aggiungi una Password",font=("Arial",24), bg="#2d2d2d", fg="white")
        self.title_label.grid(row=0, column=0,padx=10,pady=10, columnspan=3, sticky="ew")
        
        #Label con scritte degli elementi
        self.site_label = tk.Label(self.button_frame, text="Sito:",font=("Arial",14), bg="#2d2d2d", fg="white")
        self.site_label.grid(row=1, column=0,padx=10,pady=10)
        
        self.username_label = tk.Label(self.button_frame, text="Nome utente:",font=("Arial",14), bg="#2d2d2d", fg="white")
        self.username_label.grid(row=2, column=0,padx=10,pady=10)
        
        self.password_label = tk.Label(self.button_frame, text="Password:",font=("Arial",14), bg="#2d2d2d", fg="white")
        self.password_label.grid(row=3, column=0,padx=10,pady=10)
        
        self.notes_label = tk.Label(self.button_frame, text="Note",font=("Arial",14), bg="#2d2d2d", fg="white")
        self.notes_label.grid(row=4, column=0,padx=10,pady=10)
        
        #input
        self.site_input = tk.Entry(self.button_frame,font=("Arial",14), bg="#2d2d2d", fg="white")
        self.site_input.grid(row=1, column=1,padx=10,pady=10)
        
        self.username_input = tk.Entry(self.button_frame,font=("Arial",14), bg="#2d2d2d", fg="white")
        self.username_input.grid(row=2, column=1,padx=10,pady=10)
        
        self.password_input = tk.Entry(self.button_frame, show="*",font=("Arial",14), bg="#2d2d2d", fg="white")
        self.password_input.grid(row=3, column=1,padx=10,pady=10)
        
        self.notes_input = tk.Entry(self.button_frame,font=("Arial",14), bg="#2d2d2d", fg="white")
        self.notes_input.grid(row=4, column=1,padx=10,pady=10)
              
        #bottoni genera password
        self.select_button = tk.Button(self.button_frame, text="Random Password", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.generate_password)
        self.select_button.grid(row=3, column=2)
        #copia password negli appunti
        self.select_copy_button = tk.Button(self.button_frame, text="Copia Password", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.copy_password)
        self.select_copy_button.grid(row=4, column=2)
        
        
        self.add_button = tk.Button(self.button_frame,  text="Aggiungi password", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.add_password )
        self.add_button.grid(row=5, column=0,padx=10,pady=10, columnspan=3)
        
        #Title Password Custom
        self.titlePassCustom_label = tk.Label(self.button_frame, text="Genera una Password Custom",font=("Arial",16), bg="#2d2d2d", fg="white")
        self.titlePassCustom_label.grid(row=6, column=0,padx=10,pady=10, columnspan=3, sticky="ew")
        # Lunghezza password
        self.password_length_label = tk.Label(self.button_frame, text="Lunghezza Password: " + str(self.password_length), font=("Arial", 14), bg="#2d2d2d", fg="white")
        self.password_length_label.grid(row=7, column=0, padx=10, pady=10)
        self.dec_password_length_button = tk.Button(self.button_frame, text="-", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.decrement_length_value('password_length',self.password_length_label))
        self.dec_password_length_button.grid(row=7, column=1)
        self.inc_password_length_button = tk.Button(self.button_frame, text="+", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.increment_length_value('password_length',self.password_length_label))
        self.inc_password_length_button.grid(row=7, column=2)
        # Caratteri Upper
        self.charactersUp_label = tk.Label(self.button_frame, text="Caratteri Upper: " + str(self.charactersUp), font=("Arial", 14), bg="#2d2d2d", fg="white")
        self.charactersUp_label.grid(row=8, column=0, padx=10, pady=10)
        self.dec_charactersUp_button = tk.Button(self.button_frame, text="-", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.decrement_value('charactersUp',self.charactersUp_label))
        self.dec_charactersUp_button.grid(row=8, column=1)
        self.inc_charactersUp_button = tk.Button(self.button_frame, text="+", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.increment_value('charactersUp',self.charactersUp_label))
        self.inc_charactersUp_button.grid(row=8, column=2)
        # Caratteri Lower
        self.charactersL_label = tk.Label(self.button_frame, text="Caratteri Lower: " + str(self.charactersL), font=("Arial", 14), bg="#2d2d2d", fg="white")
        self.charactersL_label.grid(row=9, column=0, padx=10, pady=10)
        self.dec_charactersL_button = tk.Button(self.button_frame, text="-", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.decrement_value('charactersL',self.charactersL_label))
        self.dec_charactersL_button.grid(row=9, column=1)
        self.inc_charactersL_button = tk.Button(self.button_frame, text="+", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.increment_value('charactersL',self.charactersL_label))
        self.inc_charactersL_button.grid(row=9, column=2)
        #numeri
        self.numbers_label = tk.Label(self.button_frame, text="Numeri: " + str(self.numbers), font=("Arial", 14), bg="#2d2d2d", fg="white")
        self.numbers_label.grid(row=10, column=0,padx=10,pady=10)
        self.dec_numbers_button = tk.Button(self.button_frame, text="-", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.decrement_value('numbers',self.numbers_label))
        self.dec_numbers_button.grid(row=10, column=1)
        self.inc_numbers_button = tk.Button(self.button_frame, text="+", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10,  activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.increment_value('numbers',self.numbers_label))
        self.inc_numbers_button.grid(row=10, column=2)
        #caratteri speciali
        self.symbols_label = tk.Label(self.button_frame, text="Simboli: " + str(self.symbols), font=("Arial", 14), bg="#2d2d2d", fg="white")
        self.symbols_label.grid(row=11, column=0, padx=10, pady=10)
        self.dec_symbols_button = tk.Button(self.button_frame, text="-", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.decrement_value('symbols',self.symbols_label))
        self.dec_symbols_button.grid(row=11, column=1)
        self.inc_symbols_button = tk.Button(self.button_frame, text="+", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10,  activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.increment_value('symbols',self.symbols_label))
        self.inc_symbols_button.grid(row=11, column=2)
        #bottoni genera password
        self.select_button = tk.Button(self.button_frame, text="Custom Password", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.generate_custom_password)
        self.select_button.grid(row=12, column=1,padx=10,pady=10)
        
        
    def generate_password(self):
        self.password_input.delete(0 , 'end')
        password_length = int(self.password_length_label["text"].split(": ")[1])
        password = self.random_password(password_length)
        self.password_input.insert(0, password)
    #da ricontrollare
    def generate_custom_password(self):
        self.password_input.delete(0 , 'end')
        password_length = int(self.password_length_label["text"].split(": ")[1])
        charactersUpper = int(self.charactersUp_label["text"].split(": ")[1])
        charactersLower = int(self.charactersL_label["text"].split(": ")[1])
        numbers = int(self.numbers_label["text"].split(": ")[1])
        symbols = int(self.symbols_label["text"].split(": ")[1])
        
        password = self.custom_password(password_length, charactersUpper,charactersLower, numbers, symbols)
        self.password_input.insert(0, password)
    
    #per la lunghezza della password    
    def set_length(self, variable, label):
        setattr(self, variable, getattr(self, variable))
        label.config(text=f"{label.cget('text').split(':')[0]}: {getattr(self, variable)}")  
          
    def increment_length_value(self, variable, label):
        if self.max_length_value is None or getattr(self, variable) < self.max_length_value:
            setattr(self, variable, getattr(self, variable) + 1)
            self.set_length(variable, label)

    def decrement_length_value(self, variable, label):
        if self.min_length_value is None or getattr(self, variable) > self.min_length_value:
            setattr(self, variable, getattr(self, variable) - 1)
            self.set_length(variable, label)     
    #per gli altri elementi che costituiscono la password custom
    def set_value(self, variable, label):
        setattr(self, variable, getattr(self, variable))
        label.config(text=f"{label.cget('text').split(':')[0]}: {getattr(self, variable)}")

    def increment_value(self, variable, label):
        if self.max_value is None or getattr(self, variable) < self.max_value:
            setattr(self, variable, getattr(self, variable) + 1)
            self.set_value(variable, label)

    def decrement_value(self, variable, label):
        if self.min_value is None or getattr(self, variable) > self.min_value:
            setattr(self, variable, getattr(self, variable) - 1)
            self.set_value(variable, label) 
        
    def add_password(self):
        # Creo il nuovo file password.csv
        self.add_new_password() 
        self.site_input.delete(0, 'end')
        self.username_input.delete(0, 'end')
        self.password_input.delete(0, 'end')
        self.notes_input.delete(0, 'end')
        
            
    def set_password_file(self):
        # Importo un file password.csv o .txt già esistente
        filename = filedialog.askopenfilename(initialdir="/", title="Seleziona un Password File ", filetypes=(("CSV files", "*.csv"), ("TXT files", "*.txt"), ("All files", "*.*")))
        self.set_passwordfile(filename)
        messagebox.showinfo("Successo", "Password File importato con successo.")
    def go_back(self):
        self.previous.deiconify()
        self.master.destroy()
    # Funzione per copiare la password negli appunti
    def copy_password(self):
        pyperclip.copy(self.password_input.get())
        messagebox.showinfo("Password Copiata", "La password è stata copiata negli appunti.")
    
        
class GeneraPasswordWindow(tk.Frame,PasswordManager,KeyManager,PasswordGenerator):
    def __init__(self, master=None, previous=None, passwordfile = None, keyfile = None , key = None,min_value=0, max_value=12, min_length_value= 8, max_length_value = 30):
        super().__init__(master)
        self.master = master
        self.previous = previous
        self.passwordfile = passwordfile
        self.key = key
        self.keyfile = keyfile
        # calcola la posizione della finestra per centrarla
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (800 // 2)
        y = (screen_height // 2) - (600 // 2)
        self.master.geometry(f"800x600+{x}+{y}")
        self.password_length = 8
        self.charactersUp = 0
        self.charactersL = 0
        self.numbers = 0
        self.symbols = 0
        self.min_value = min_value
        self.max_value = max_value
        self.min_length_value = min_length_value
        self.max_length_value = max_length_value
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # imposto lo sfondo scuro
        self.master.configure(bg="#2d2d2d")
        #back
        self.back_button = tk.Button(self.master, text="⬅️", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.go_back)
        self.back_button.pack(side="top", anchor="nw")  
   
        self.button_frame = tk.Frame(self.master, bg="#2d2d2d")
        self.button_frame.pack(side = "top")
        
        #Title 1
        self.title_label = tk.Label(self.button_frame, text="Genera una Password",font=("Arial",24), bg="#2d2d2d", fg="white")
        self.title_label.grid(row=0, column=0,padx=10,pady=10, columnspan=3, sticky="ew")
        
        #Label con scritte degli elementi
        self.password_label = tk.Label(self.button_frame, text="Password:",font=("Arial",14), bg="#2d2d2d", fg="white")
        self.password_label.grid(row=1, column=0)
        
        #input
        self.password_input = tk.Entry(self.button_frame, show="*",font=("Arial",14), bg="#2d2d2d", fg="white")
        self.password_input.grid(row=1, column=1,padx=10,pady=10)
        #button
        self.select_button = tk.Button(self.button_frame, text="Genera Password", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.generate_password)
        self.select_button.grid(row=2, column=0, sticky="ew")
        #copia password negli appunti
        self.select_copy_button = tk.Button(self.button_frame, text="Copia Password", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.copy_password)
        self.select_copy_button.grid(row=2, column=1)
        #Title Password Custom
        self.titlePassCustom_label = tk.Label(self.button_frame, text="Genera una Password Custom",font=("Arial",16), bg="#2d2d2d", fg="white")
        self.titlePassCustom_label.grid(row=3, column=0,padx=10,pady=10, columnspan=3, sticky="ew")
        # Lunghezza password
        self.password_length_label = tk.Label(self.button_frame, text="Lunghezza Password: " + str(self.password_length), font=("Arial", 14), bg="#2d2d2d", fg="white")
        self.password_length_label.grid(row=4, column=0, padx=10, pady=10)
        self.dec_password_length_button = tk.Button(self.button_frame, text="-", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.decrement_length_value('password_length',self.password_length_label))
        self.dec_password_length_button.grid(row=4, column=1)
        self.inc_password_length_button = tk.Button(self.button_frame, text="+", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.increment_length_value('password_length',self.password_length_label))
        self.inc_password_length_button.grid(row=4, column=2)
        # Caratteri Upper
        self.charactersUp_label = tk.Label(self.button_frame, text="Caratteri Upper: " + str(self.charactersUp), font=("Arial", 14), bg="#2d2d2d", fg="white")
        self.charactersUp_label.grid(row=5, column=0, padx=10, pady=10)
        self.dec_charactersUp_button = tk.Button(self.button_frame, text="-", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.decrement_value('charactersUp',self.charactersUp_label))
        self.dec_charactersUp_button.grid(row=5, column=1)
        self.inc_charactersUp_button = tk.Button(self.button_frame, text="+", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.increment_value('charactersUp',self.charactersUp_label))
        self.inc_charactersUp_button.grid(row=5, column=2)
        # Caratteri Lower
        self.charactersL_label = tk.Label(self.button_frame, text="Caratteri Lower: " + str(self.charactersL), font=("Arial", 14), bg="#2d2d2d", fg="white")
        self.charactersL_label.grid(row=6, column=0, padx=10, pady=10)
        self.dec_charactersL_button = tk.Button(self.button_frame, text="-", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.decrement_value('charactersL',self.charactersL_label))
        self.dec_charactersL_button.grid(row=6, column=1)
        self.inc_charactersL_button = tk.Button(self.button_frame, text="+", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.increment_value('charactersL',self.charactersL_label))
        self.inc_charactersL_button.grid(row=6, column=2)
        #numeri
        self.numbers_label = tk.Label(self.button_frame, text="Numeri: " + str(self.numbers), font=("Arial", 14), bg="#2d2d2d", fg="white")
        self.numbers_label.grid(row=7, column=0,padx=10,pady=10)
        self.dec_numbers_button = tk.Button(self.button_frame, text="-", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.decrement_value('numbers',self.numbers_label))
        self.dec_numbers_button.grid(row=7, column=1)
        self.inc_numbers_button = tk.Button(self.button_frame, text="+", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10,  activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.increment_value('numbers',self.numbers_label))
        self.inc_numbers_button.grid(row=7, column=2)
        #caratteri speciali
        self.symbols_label = tk.Label(self.button_frame, text="Simboli: " + str(self.symbols), font=("Arial", 14), bg="#2d2d2d", fg="white")
        self.symbols_label.grid(row=8, column=0, padx=10, pady=10)
        self.dec_symbols_button = tk.Button(self.button_frame, text="-", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.decrement_value('symbols',self.symbols_label))
        self.dec_symbols_button.grid(row=8, column=1)
        self.inc_symbols_button = tk.Button(self.button_frame, text="+", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10,  activebackground="#5e5e5e", font=("Arial", 12), command=lambda: self.increment_value('symbols',self.symbols_label))
        self.inc_symbols_button.grid(row=8, column=2)
        #bottoni genera password
        self.select_button = tk.Button(self.button_frame, text="Genera Password Custom", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.generate_custom_password)
        self.select_button.grid(row=9, column=0,padx=10,pady=10,columnspan=3)
        
    def generate_password(self):
        self.password_input.delete(0 , 'end')
        password_length = int(self.password_length_label["text"].split(": ")[1])
        password = self.random_password(password_length)
        self.password_input.insert(0, password)
        
    def generate_custom_password(self):
        self.password_input.delete(0 , 'end')
        password_length = int(self.password_length_label["text"].split(": ")[1])
        charactersUpper = int(self.charactersUp_label["text"].split(": ")[1])
        charactersLower = int(self.charactersL_label["text"].split(": ")[1])
        numbers = int(self.numbers_label["text"].split(": ")[1])
        symbols = int(self.symbols_label["text"].split(": ")[1])
        
        password = self.custom_password(password_length, charactersUpper,charactersLower, numbers, symbols)
        self.password_input.insert(0, password)
    
    #per la lunghezza della password    
    def set_length(self, variable, label):
        setattr(self, variable, getattr(self, variable))
        label.config(text=f"{label.cget('text').split(':')[0]}: {getattr(self, variable)}")  
          
    def increment_length_value(self, variable, label):
        if self.max_length_value is None or getattr(self, variable) < self.max_length_value:
            setattr(self, variable, getattr(self, variable) + 1)
            self.set_length(variable, label)

    def decrement_length_value(self, variable, label):
        if self.min_length_value is None or getattr(self, variable) > self.min_length_value:
            setattr(self, variable, getattr(self, variable) - 1)
            self.set_length(variable, label)     
    #per gli altri elementi che costituiscono la password custom
    def set_value(self, variable, label):
        setattr(self, variable, getattr(self, variable))
        label.config(text=f"{label.cget('text').split(':')[0]}: {getattr(self, variable)}")

    def increment_value(self, variable, label):
        if self.max_value is None or getattr(self, variable) < self.max_value:
            setattr(self, variable, getattr(self, variable) + 1)
            self.set_value(variable, label)

    def decrement_value(self, variable, label):
        if self.min_value is None or getattr(self, variable) > self.min_value:
            setattr(self, variable, getattr(self, variable) - 1)
            self.set_value(variable, label)    
     
        # Funzione per copiare la password negli appunti
    def copy_password(self):
        pyperclip.copy(self.password_input.get())
        messagebox.showinfo("Password Copiata", "La password è stata copiata negli appunti.")   
        
    def go_back(self):
        self.previous.deiconify()
        self.master.destroy()
    

    

class VisualizzaPasswordWindow(tk.Frame,PasswordManager,KeyManager):
    def __init__(self, master=None, previous=None, passwordfile = None, keyfile = None , key = None, cipher_suite = None):
        super().__init__(master)
        self.master = master
        self.previous = previous
        self.passwordfile = passwordfile
        self.keyfile = keyfile
        self.key = key
        self.cipher_suite = cipher_suite
        # calcola la posizione della finestra per centrarla
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (800 // 2)
        y = (screen_height // 2) - (600 // 2)
        self.master.geometry(f"800x600+{x}+{y}")
        self.pack()
        self.create_widgets()
        self.passwordfile

    def create_widgets(self):
        # imposto lo sfondo scuro
        self.master.configure(bg="#2d2d2d")
        #back
        self.back_button = tk.Button(self.master, text="⬅️", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.go_back)
        self.back_button.pack(side="top", anchor="nw")  
   
        self.button_frame = tk.Frame(self.master, bg="#2d2d2d")
        self.button_frame.pack(side = "top")
        
        #Title 1
        self.title_label = tk.Label(self.button_frame, text="Visualizza le Password",font=("Arial",24), bg="#2d2d2d", fg="white")
        self.title_label.grid(row=0, column=0,padx=10,pady=10, columnspan=2, sticky="nswe")
        # Widget ScrolledText
        #self.text_box = ScrolledText(self.button_frame, width=50, height=10, bg="#4b4b4b", fg="white", font=("Arial", 12))
        #self.text_box.grid(row=2, column=0, padx=10, pady=10, sticky="nswe")
        self.text_box = ScrolledText(self.master, width=60, height=20)
        self.text_box.pack() 
        # Abilita la funzionalità di copia
        self.text_box.bind("<Control-C>", lambda e: self.text_box.event_generate("<<Copy>>"))
        self.print_button = tk.Button(self.button_frame, text="Stampa password", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.Stampa_Passwrdfile)
        self.print_button.grid(row=1, column=0,padx=10,pady=10, columnspan=2)
        
        self.delete_print_button = tk.Button(self.button_frame,text="Pulisci", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.DeletePrint)
        self.delete_print_button.grid(row=2, column=0,padx=10,pady=10, columnspan=2)

    def DeletePrint(self):
        # Cancella il contenuto della casella di testo
        self.text_box.delete(1.0, tk.END)
        
    def go_back(self):
        self.previous.deiconify()
        self.master.destroy()
    
    def Stampa_Passwrdfile(self):
        self.print_passwordfile()
                
class VisualizzaPasswordSiteWindow(tk.Frame,PasswordManager,KeyManager):
    def __init__(self, master=None, previous=None, passwordfile = None, keyfile = None , key = None, cipher_suite = None):
        super().__init__(master)
        self.master = master
        self.previous = previous
        self.passwordfile = passwordfile
        self.key = key
        self.keyfile = keyfile
        self.cipher_suite = cipher_suite
        # calcola la posizione della finestra per centrarla
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (800 // 2)
        y = (screen_height // 2) - (600 // 2)
        self.master.geometry(f"800x600+{x}+{y}")
        self.pack()
        self.create_widgets()
        self.passwordfile

    def create_widgets(self):
        # imposto lo sfondo scuro
        self.master.configure(bg="#2d2d2d")
        #back
        self.back_button = tk.Button(self.master, text="⬅️", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.go_back)
        self.back_button.pack(side="top", anchor="nw")  
   
        self.button_frame = tk.Frame(self.master, bg="#2d2d2d")
        self.button_frame.pack(side = "top")
        
        #Title 1
        self.title_label = tk.Label(self.button_frame, text="Cerca le Password per Sito",font=("Arial",24), bg="#2d2d2d", fg="white")
        self.title_label.grid(row=0, column=0,padx=10,pady=10, columnspan=2, sticky="nswe")
        #inserimeto sito da cercare
        self.site_label = tk.Label(self.button_frame, text="Sito:",font=("Arial",14), bg="#2d2d2d", fg="white")
        self.site_label.grid(row=1, column=0,padx=10,pady=10)
        #input
        self.site_input = tk.Entry(self.button_frame,font=("Arial",14), bg="#2d2d2d", fg="white")
        self.site_input.grid(row=1, column=1,padx=10,pady=10)
        #Stampa
        self.print_button = tk.Button(self.button_frame, text="Cerca password", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.view_password_site)
        self.print_button.grid(row=2, column=0,padx=10,pady=10, columnspan=2)
        
        # Widget ScrolledText
        #self.text_box = ScrolledText(self.button_frame, width=50, height=10, bg="#4b4b4b", fg="white", font=("Arial", 12))
        #self.text_box.grid(row=2, column=0, padx=10, pady=10, sticky="nswe")
        self.text_box = ScrolledText(self.master, width=60, height=20)
        self.text_box.pack() 
        # Abilita la funzionalità di copia
        self.text_box.bind("<Control-C>", lambda e: self.text_box.event_generate("<<Copy>>"))
        
    def go_back(self):
        self.previous.deiconify()
        self.master.destroy()
        
    def view_password_site(self):
        sito = self.site_input.get()
        self.print_passwords_site(sito)
        self.site_input.delete(0, 'end')

class VisualizzaPasswordUsernameWindow(tk.Frame,PasswordManager,KeyManager):
    def __init__(self, master=None, previous=None, passwordfile = None, keyfile = None , key = None, cipher_suite = None):
        super().__init__(master)
        self.master = master
        self.previous = previous
        self.passwordfile = passwordfile
        self.key = key
        self.keyfile = keyfile
        self.cipher_suite = cipher_suite
        # calcola la posizione della finestra per centrarla
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (800 // 2)
        y = (screen_height // 2) - (600 // 2)
        self.master.geometry(f"800x600+{x}+{y}")
        self.pack()
        self.create_widgets()
        self.passwordfile

    def create_widgets(self):
        # imposto lo sfondo scuro
        self.master.configure(bg="#2d2d2d")
        #back
        self.back_button = tk.Button(self.master, text="⬅️", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.go_back)
        self.back_button.pack(side="top", anchor="nw")  
   
        self.button_frame = tk.Frame(self.master, bg="#2d2d2d")
        self.button_frame.pack(side = "top")
        
        #Title 1
        self.title_label = tk.Label(self.button_frame, text="Cerca le Password per Username",font=("Arial",24), bg="#2d2d2d", fg="white")
        self.title_label.grid(row=0, column=0,padx=10,pady=10, columnspan=2, sticky="nswe")
        #inserimeto sito da cercare
        self.Username_label = tk.Label(self.button_frame, text="Username:",font=("Arial",14), bg="#2d2d2d", fg="white")
        self.Username_label.grid(row=1, column=0,padx=10,pady=10)
        #input
        self.username_input = tk.Entry(self.button_frame,font=("Arial",14), bg="#2d2d2d", fg="white")
        self.username_input.grid(row=1, column=1,padx=10,pady=10)
        #Stampa
        self.print_button = tk.Button(self.button_frame, text="Cerca password", bg="#4b4b4b", fg="white", bd=0, padx=10, pady=10, relief="flat", activebackground="#5e5e5e", font=("Arial", 12), cursor="hand2", command=self.view_password_username)
        self.print_button.grid(row=2, column=0,padx=10,pady=10, columnspan=2)
        
        # Widget ScrolledText
        self.text_box = ScrolledText(self.master, width=60, height=20)
        self.text_box.pack() 
        # Abilita la funzionalità di copia
        self.text_box.bind("<Control-C>", lambda e: self.text_box.event_generate("<<Copy>>")) 
        
    def go_back(self):
        self.previous.deiconify()
        self.master.destroy()
        
    def view_password_username(self):
        username = self.username_input.get()
        self.print_passwords_username(username)
        self.username_input.delete(0, 'end')

                
def main():
    root = tk.Tk()
    root.title("Password Manager")#imposto un titolo alla finestra
    app = MainWindow(root)
    app.mainloop()
if __name__ == "__main__":
    main()