class Seq:
    def __init__(self, str_bases):
        # Lógica del ejercicio anterior
        valid_bases = ['A', 'C', 'G', 'T']
        is_valid = True
        for letra in str_bases:
            if letra not in valid_bases:
                is_valid = False
                break

        if is_valid:
            self.bases = str_bases
        else:
            self.bases = "ERROR"
            print("ERROR!!")

    def __str__(self):
        return self.bases


# --- FUNCIÓN INDEPENDIENTE (Fuera de la clase) ---
def print_seqs(seq_list):
    # Usamos un contador manual para el índice (0, 1, 2...)
    indice = 0

    for s in seq_list:
        # Calculamos el largo directamente con len() sobre el atributo .bases
        largo = len(s.bases)

        # Imprimimos siguiendo el formato exacto del profesor
        print(f"Sequence {indice}: (Length: {largo}) {s.bases}")

        # Sumamos 1 al contador para la siguiente vuelta
        indice = indice + 1


# --- Programa Principal (Copiado del enunciado) ---
seq_list = [Seq("ACT"), Seq("GATA"), Seq("CAGATA")]

print_seqs(seq_list)