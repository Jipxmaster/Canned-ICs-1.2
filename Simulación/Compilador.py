                                                # Constantes
code = {"JPI": "F7", "JPC": "EF", "STA": "9B", "NOP": "FF"}
skip = (" ", "\n", "\t", ",")
hexa = ("0123456789ABCDEF")
                                                # Variables iniciales
instruction = 0
operand = 0
ld = False                                      # Banderas
add = False
busy = False
word = ""                                       # Palabra

file = open(input("Nombre de archivo y su extensión [ejemplo.txt]: "), "r")
compiled = []

for line in file:
    line = line + " "
    for letter in line:
        if letter == "#":
            break
        if letter not in skip:                      # Si las letras no está en "skip"
            word = word + letter.upper()            # Añadirlas a una palabra
        else:
            if word != "":                          # Si la palabra no está vacía, interpetar

                if busy and ld:                     # Para instrucciones relacionadas a load
                    if word == "(P)":               # Dato a dirección "p" como fuente
                        instruction = "3E"
                        busy, ld = False, False
                    elif word == "A":               # Valor de acumulador "a" como fuente
                        instruction = "DE"
                        busy, ld = False, False
                    else:                           # Valor inmediato
                        instruction = "7E"
                        busy, ld = False, False
                    compiled.append(instruction)    # --Instrucción obtenido--
                    instruction = 0

                if add:                             # Para instrucciones de suma
                    if word == "(P)":               # Dato a dirección "p" como fuente
                        instruction = "3D"
                        add = False
                    elif word == "A":               # Valor de acumulador "a" como fuente
                        instruction = "DD"
                        add = False
                    else:                           # Valor inmediato
                        instruction = "7D"
                        add = False
                    compiled.append(instruction)    # --Instrucción obtenido--
                    instruction = 0

                if word == "LD" and not ld:         # Detección de "ld"
                    ld = True

                if word == "ADD" and not add:       # Detección de "add"
                    add = True

                if word in code:                    # Detección de instrucciones adicionales
                    compiled.append(code[word])

                if word == "P" and ld:              # Registro "p" como destino
                    busy = True

                if len(word) == 2:                  # El operando solo tiene dos caracteres
                    if word[0] in hexa and word[1] in hexa:     # Detección de operando
                        """
                        a = 16
                        for letter in word:                     # Revisar las cifras del operando
                            b = ord(letter)
                            if b < 0x3b:                        # Detectar caracteres de números
                                operand += (b - 48) * a
                            else:                               # Detectar caracteres alfabéticos
                                operand += (b - 55) * a
                            a = int(a / 16)
                        compiled.append(operand)                # --Operando obtenido--
                        operand = 0
                        """
                        compiled.append(word)

            word = ""                               # Finalmente vaciar la palabra

counter = 0
a = 0
line = ""
for element in compiled:
    line = line + element + " "
    counter += 1
    if counter == 16:
        print(line)
        line = ""
        counter = 0
    a += 1

if counter < 16:
    print(line)

print("Memory consumption: " + str(a) + " bytes out of 256 available.")
input("\nProgram successfully executed\nPress any key to exit...")
