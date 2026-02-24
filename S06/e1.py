class Seq:
    def __init__(self, str_bases):
        valid_bases = ['A', 'C', 'G', 'T']

        # 2. Variable para saber si todo está bien (asumimos que sí al principio)
        is_valid = True

        # 3. Revisamos cada letra de la cadena que nos han pasado
        for letra in str_bases:
            if letra not in valid_bases:
                is_valid = False
                break  # Si encontramos una mala, no hace falta seguir mirando

        # 4. Decidimos qué guardar según el resultado del bucle
        if is_valid:
            self.bases = str_bases
            print("New sequence created!")
        else:
            self.bases = "ERROR"
            print("ERROR!!")
            print("INCORRECT Sequence detected")

    # Este método sirve para que al hacer print(objeto) salga el texto
    def __str__(self):
        return self.bases


# --- Programa Principal (Main) ---
s1 = Seq("ACCTGC")
s2 = Seq("Hello? Am I a valid sequence?")

print(f"Sequence 1: {s1}")
print(f"Sequence 2: {s2}")