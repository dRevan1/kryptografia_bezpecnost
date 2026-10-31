import numpy as np
from sympy import Matrix

#---------------------------------------------------------------------------------------------
# custom funkcia na inverznú meticu cez deteminant, lebo sympy matrrix inv dával nejaký error
#---------------------------------------------------------------------------------------------
def inverse_matrix_mod(matrix):
    M = Matrix(matrix.tolist())
    det = int(M.det()) % 26
    det_inverse = pow(det, -1, 26)
    inverse = (det_inverse * M.adjugate()) % 26

    return np.array(inverse).astype(int)
#------------------------------------------------------------------------------------------------------------------------------
# vypočíta na základe sústavy rovníc maticu, ktorá je kľúčom Hillovskej šifry, vráti aj inverzný kľúč - maticu, na dešifrovanie
#------------------------------------------------------------------------------------------------------------------------------
def get_key_matrix(text):
    X = np.array([
        [ord('D') - 65, ord('H') - 65, ord('U') - 65],
        [ord('R') - 65, ord('Y') - 65, ord('R') - 65],
        [ord('A') - 65, ord('J') - 65, ord('A') - 65]
    ])

    Y = np.array([
        [ord(text[0]) - 65, ord(text[3]) - 65, ord(text[6]) - 65],
        [ord(text[1]) - 65, ord(text[4]) - 65, ord(text[7]) - 65],
        [ord(text[2]) - 65, ord(text[5]) - 65, ord(text[8]) - 65]
    ])

    X_inv = inverse_matrix_mod(X)
    key_matrix = (Y @ X_inv) % 26
    inverse_key_matrix = inverse_matrix_mod(key_matrix, 26)
    
    return key_matrix, inverse_key_matrix
#----------------------------------------------------------------------------------------------------------------------------------------------
# dešifruje s daným inverzným kľúčom (maticou) zadaný text a vráti ho, text sa dá do 1 matice a z výslednej sa dešifrovaný poskladá po stĺpcoch
#----------------------------------------------------------------------------------------------------------------------------------------------
def decrypt_hill(text, key_inverse_matrix):
    decrypted_text = ""
    text_matrix = np.array([ord(char) - 65 for char in text]).reshape(len(text) // 3, 3).T
    decrypted_matrix = (key_inverse_matrix @ text_matrix) % 26
    for column in decrypted_matrix.T:
        decrypted_text += ''.join(chr(int(num) + 65) for num in column)
        
    return decrypted_text

def main():
    text1 = "BALQTGFGYNFUHVLOIVCGPRZJUTHGWOVWCWAJGWN"
    text2 = "PCPOVZOJYEJXJLVINLJMIAVAVEUKZLERO"
    text3 = "NMUSMRFJGRWSWVKKDJKYTYTNSVMOJW"
    
    _, text1_inverse_key = get_key_matrix(text1)
    _, text2_inverse_key = get_key_matrix(text2)
    _, text3_inverse_key = get_key_matrix(text3)
    
    print(f"Decrypted text 1: {decrypt_hill(text1, text1_inverse_key)}")
    print(f"Decrypted text 2: {decrypt_hill(text2, text2_inverse_key)}")
    print(f"Decrypted text 3: {decrypt_hill(text3, text3_inverse_key)}")

main()