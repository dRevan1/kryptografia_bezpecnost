# pravdepodobnosti znakov v sk a en
slovak_frequencies = {
    'A': 0.11160,
    'B': 0.01778,
    'C': 0.02463,
    'D': 0.03760,
    'E': 0.09316,
    'F': 0.00165,
    'G': 0.00175,
    'H': 0.02482,
    'I': 0.05745,
    'J': 0.02158,
    'K': 0.03961,
    'L': 0.04375,
    'M': 0.03578,
    'N': 0.05949,
    'O': 0.09540,
    'P': 0.03007,
    'Q': 0.00000,
    'R': 0.04706,
    'S': 0.06121,
    'T': 0.05722,
    'U': 0.03308,
    'V': 0.04604,
    'W': 0.00001,
    'X': 0.00028,
    'Y': 0.02674,
    'Z': 0.03064
}
english_frequencies = {
    'A': 0.0856,
    'B': 0.0139,
    'C': 0.0279,
    'D': 0.0378,
    'E': 0.1304,
    'F': 0.0289,
    'G': 0.0199,
    'H': 0.0526,
    'I': 0.0627,
    'J': 0.0019,
    'K': 0.0042,
    'L': 0.0339,
    'M': 0.0249,
    'N': 0.0707,
    'O': 0.0797,
    'P': 0.0199,
    'Q': 0.0012,
    'R': 0.0977,
    'S': 0.0607,
    'T': 0.1045,
    'U': 0.0249,
    'V': 0.0092,
    'W': 0.0149,
    'X': 0.0017,
    'Y': 0.0199,
    'Z': 0.0008
}
#---------------------------------------------------
# vráti početnosť znakov v texte v podobe dictionary
#---------------------------------------------------
def get_character_count(text):
    letter_count = {
    'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0,
    'W': 0, 'X': 0, 'Y': 0, 'Z': 0
    }
    
    # predpokladáme v capslocku
    for char in text:
        if char in letter_count:
            letter_count[char] += 1

    return letter_count
#----------------------
# načíta text zo súbora
#----------------------
def load_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        
    return text
#----------------------------------------------------------------------------------------
# vráti chybu pre daný stĺpec a posun - použije sa v cykle pre každý stĺpec a každý posun
#----------------------------------------------------------------------------------------
def compute_column_error(column, shift, lang):
    probabilities = []
    shifted_column = ''.join(chr((ord(char) - ord('A') - shift) % 26 + ord('A')) for char in column)
    
    if lang == 'sk':
        lang_frequencies = slovak_frequencies
    elif lang == 'en':
        lang_frequencies = english_frequencies
    
    probabilities = {char: shifted_column.count(char) / len(shifted_column) for char in lang_frequencies}
    error = sum((probabilities[char] - lang_frequencies[char]) ** 2 for char in probabilities) / 26
    
    return error
#--------------------------------------------------------------
# prejde každý stĺpec a pre každý posun vypočíta a vypíše chybu
#--------------------------------------------------------------
def get_shift_column_errors(text, password_length, lang):
    min_errors = [float('inf') for _ in range(password_length)]
    password_guess = '' # tu bude odhadnuté heslo podľa minimálnych chýb pre každý stĺpec
    print(f"Password Length: {password_length}")
    print(f"Language: {lang}")
    # rozdelíme text na 'stĺpce' podľa dĺžky hesla
    text = ''.join(char for char in text if 'A' <= char <= 'Z')
    best_shifts = [0 for _ in range(password_length)]
    parts = ['' for _ in range(password_length)]

    for i, char in enumerate(text):
        parts[i % password_length] += char
        
    for i, part in enumerate(parts):
        print(f"Column: {i + 1}")
        for shift in range(26):
            error = compute_column_error(part, shift, lang)
            if error < min_errors[i]:
                min_errors[i] = error
                best_shifts[i] = shift
            print(f"Shift: {shift}, Error: {error}")
        password_guess += chr(best_shifts[i] + ord('A'))
    
    return min_errors, password_guess
#--------------------------------------------------------------------------------------------
# vráti index koinncidencie všetkých stĺpcov podľa dĺžky hesla a priemerný index koincidencie
#--------------------------------------------------------------------------------------------
def get_index_of_coincidence(text, password_length):
    # rozdelíme text na 'stĺpce' podľa dĺžky hesla
    char_counts = []
    text = ''.join(char for char in text if 'A' <= char <= 'Z')
    parts = ['' for _ in range(password_length)]
    
    for i, char in enumerate(text):
        parts[i % password_length] += char

    # vypočítame index koincidencie pre každú časť
    ic_values = []
    for part in parts:
        char_count = get_character_count(part)
        char_counts.append(char_count)
        total_chars = sum(char_count.values())
        ic = sum(count * (count - 1) for count in char_count.values()) / (total_chars * (total_chars - 1)) if total_chars > 1 else 0
        ic_values.append(ic)

    # priemerný index koincidencie
    return sum(ic_values) / len(ic_values) if ic_values else 0, ic_values, char_counts
#-------------------------------------------------------------------------------------
# vypočíta pre daný text a príslušný rozsah dĺžok hesla index koincidencie a vypíše ho
#-------------------------------------------------------------------------------------
def try_index_of_coincidence(text, min, max, step):
    for password_length in range(min, max + 1, step):
        index_of_coincidence, ic_values, char_counts = get_index_of_coincidence(text, password_length)
        print(f"Password Length: {password_length}")
        print(f"Index of Coincidence: {index_of_coincidence:.4f}")
        print(f"IC Values for each column: {['{:.4f}'.format(ic) for ic in ic_values]}")
        for i, char_count in enumerate(char_counts):
            print(f"Character Count for column {i + 1}: {char_count}")
        print("-" * 220) 
#----------------------------------------------------------
# dešifruje text pomocou Vigenerovej šifry a zadaného hesla
#----------------------------------------------------------
def decrypt_vigenere(text, password):
    deciphered_text = ''
    password_length = len(password)
    password_indices = [ord(char) - ord('A') for char in password]

    j = 0

    for char in text:
        if 'A' <= char <= 'Z':
            shift = password_indices[j % password_length]
            deciphered_char = chr(
                (ord(char) - ord('A') - shift) % 26 + ord('A')
            )
            deciphered_text += deciphered_char
            j += 1
        else:
            deciphered_text += char

    return deciphered_text

def run_text1_analysis():
    text = load_text_from_file('1_vigenere_sifra/text1_enc.txt')
    try_index_of_coincidence(text, 15, 25, 1)
    sk_errors, sk_password = get_shift_column_errors(text, 17, 'sk')
    en_errors, en_password = get_shift_column_errors(text, 17, 'en')
    for i in range(17):
        print(f"Column {i + 1}: SK min error: {sk_errors[i]:.6f}, EN min error: {en_errors[i]:.6f}")
        
    print(f"SK Password: {sk_password}")
    print(f"EN Password: {en_password}")
    
    decrrypted_text = decrypt_vigenere(text, "IDGKZQNOMYNTJOUIB")
    print(f"Decrypted Text with guessed password: {decrrypted_text}")

def run_text2_analysis():
    text = load_text_from_file('1_vigenere_sifra/text2_enc.txt')
    try_index_of_coincidence(text, 15, 25, 1)
    sk_errors, sk_password = get_shift_column_errors(text, 25, 'sk')
    en_errors, en_password = get_shift_column_errors(text, 25, 'en')
    for i in range(17):
        print(f"Column {i + 1}: SK min error: {sk_errors[i]:.6f}, EN min error: {en_errors[i]:.6f}")
        
    print(f"SK Password: {sk_password}")
    print(f"EN Password: {en_password}")
    
    decrrypted_text = decrypt_vigenere(text, "AUZDMZRNFUXQSXHORWQLCLZLS")
    print(f"Decrypted Text with guessed password: {decrrypted_text}")

def main():    
    #run_text1_analysis() # heslo IDGKZQNOMYNTJOUIB
    run_text2_analysis() # heslo AUZDMZRNFUXQSXHORWQLCLZLS

main()

# text 1 - index koincidencie priemerný pre dĺžku hesla 17 okolo 0.06, ostatné jednoznačne horšie
#        - pri EN jazyku nižšie chyby pri posune na stĺpec, odhadované heslo IDGKZQNOMYNTJOUIB

# text 2 - index koincidencie priemerný pre dĺžku hesla 25 okolo 0.0578, ostatné jednoznačne horšie
#        - nižšie chyby jednoznačne pri SK jazyku, odhadované heslo: AUZDMZRNFUXQSXHORWQLCLZLS