def crypt(input_name, output_name, keyword, decrypt=0):
    keyw_list = keyword.split()
    alphabet = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
    new_alpha = [" "]
    for letter in keyword:
        if letter not in new_alpha:
            new_alpha.append(letter)
    for i in range(len(alphabet)-1, -1, -1):
        if alphabet[i] not in new_alpha:
            new_alpha.append(alphabet[i])
    alphabet = alphabet.split(' ')
    alphabet.insert(0, ' ')
    encrypt_dict = dict(zip(alphabet, new_alpha))
    decrypt_dict = dict(zip(new_alpha, alphabet))
    r = open(input_name, 'r')
    line_list = r.readlines()
    line_list = [line.upper() for line in line_list]
    r.close()
    add = open(output_name, 'a')

    if decrypt:
        for line in line_list:
            for char in line:
                try:
                    add.write(decrypt_dict[char])
                except:
                    add.write(char)
        add.close()
    else:
        for line in line_list:
            for char in line:
                try:
                    add.write(encrypt_dict[char])
                except:
                    add.write(char)
        add.close()

def main():
    input_path = input("Please enter the name of the file you want to encrypt / decrypt: ")
    output = input("Please enter the name of the file that will be created: ")
    keyword = ''
    decrypt_answer = ''
    while len(decrypt_answer) < 1 or decrypt_answer[0] not in {'Y', 'y', 'N', 'n'}:
        decrypt_answer = input("Do you want to decrypt? 'Y' for decrypt, 'N' for encrypt")
    while len(keyword) == 0:
        keyword = input('Enter the keyword: ').upper()
    # input_path = 'input.txt'
    # output = 'output.txt'
    decrypt_bool = decrypt_answer[0] in {'Y', 'y'}
    crypt(input_path, output, keyword, decrypt_bool)

if __name__ == "__main__":
    main()
