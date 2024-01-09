import random
import string
#   Classe Password Generator:
# - Generatore di password personalizzata in base alle scelte dell'utente
# - Generatore di password Random
# - Password length in input
#   Programma funzionante in tutti i casi particolari
class PasswordGenerator: 
    def __init__(self, length = 8,min_alpha=0,min_numeric=0,min_special=0,min_total=0):
        self.length=length
        self.min_alpha = min_alpha
        self.min_numeric = min_numeric
        self.min_special = min_special
        self.min_total = min_total
    
    # random password NEW
    def random_password(self, length):
        symbols = "@#£$%&/()=?^|*"
        chars = string.ascii_lowercase +string.ascii_uppercase+ string.digits + symbols 
        required_chars = [
            random.choice(string.ascii_lowercase),
            random.choice(string.ascii_uppercase),
            random.choice(string.digits),
            random.choice(symbols)
        ]
        password = ''.join(random.choice(chars)for i in range(length - len(required_chars)))
        password += ''.join(required_chars)
        random.shuffle(list(password))
        return password
    
    
    #password custom di prova
    def custom_password(self,password_length, charactersUp, charactersL, numbers, symbols):
        symbol_list = list("@#£$%&/()=?^|*")
        char_list = []
        if charactersUp > 0:
            char_list += string.ascii_uppercase
        if charactersL > 0:
            char_list += string.ascii_lowercase
        if numbers > 0:
            char_list += string.digits
        if symbols > 0:
            char_list += "".join(symbol_list)

        password = ""
        #counters
        charUp_count = 0
        charL_count = 0
        number_count = 0
        special_count = 0
        min_total = charactersUp + charactersL + numbers + symbols
        

        while len(password) < password_length:
            char = random.choice(char_list) # prendiamo un carattere random di char_list
            
            if char in string.ascii_uppercase and charUp_count < charactersUp :
                password += char
                charactersUp -= 1
            elif char in string.ascii_lowercase and charL_count < charactersL :
                password += char
                charactersL -= 1
            elif char in string.digits and number_count < numbers :
                password += char
                numbers -= 1
            elif char in symbol_list and special_count < symbols:
                password += char
                symbols -= 1
            elif (char in string.ascii_uppercase or string.ascii_lowercase or string.digits or symbol_list) and (charUp_count >= charactersUp or charL_count >= charactersL or number_count >= numbers or special_count >= symbols) and (min_total < password_length):
                password += char
                min_total += 1
                
            
            
        # Shuffle the password to make it more secure
        password = ''.join(random.sample(password, len(password)))

        return password
          
    #password personalizza da modificare
    def custom_passwordbase(self,password_length, characters, numbers, symbols):
        chars = ""
        if characters > 0:
            chars += string.ascii_letters
        if numbers > 0:
            chars += string.digits
        if symbols > 0:
            chars += string.punctuation

        password = ""
        for i in range(password_length):
            char_type = random.choice([char for char in [string.ascii_letters, string.digits, string.punctuation] if char in chars])
            if char_type == string.ascii_letters and characters > 0:
                password += random.choice(string.ascii_letters)
                characters -= 1
            elif char_type == string.digits and numbers > 0:
                password += random.choice(string.digits)
                numbers -= 1
            elif char_type == string.punctuation and symbols > 0:
                password += random.choice(string.punctuation)
                symbols -= 1
            else:
                password += random.choice(chars)

        # Add additional characters if necessary
        while len(password) < password_length:
            char_type = random.choice([char for char in [string.ascii_letters, string.digits, string.punctuation] if char in chars])
            if char_type == string.ascii_letters and characters > 0:
                password += random.choice(string.ascii_letters)
                characters -= 1
            elif char_type == string.digits and numbers > 0:
                password += random.choice(string.digits)
                numbers -= 1
            elif char_type == string.punctuation and symbols > 0:
                password += random.choice(string.punctuation)
                symbols -= 1

        # Shuffle the password to make it more secure
        password = ''.join(random.sample(password, len(password)))
        
        return password

def main():
    pg = PasswordGenerator()
        
        
if __name__ == "__main__":
    main()


       