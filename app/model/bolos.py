class Juego:
    def __init__(self):
        self.frames = []

    def jugar(self):
        for _ in range(10):
            self.frames.append(Frame())

        for frame in self.frames:
            for _ in range(2):
                tiro = None
                while tiro is None or not tiro.valido():
                    try:
                        pinos_derribados = int(input(f"Ingrese el número de pines derribados: "))
                        tiro = Tiro(pinos_derribados)
                    except ValueError:
                        print("Error: Debe ingresar un número entero.")

                frame.agregar_tiro(tiro)

        self.calcular_puntaje_total()
        print(f"Puntaje final: {self.puntaje_total}")

    def calcular_puntaje_total(self):
        self.puntaje_total = 0

        for frame in self.frames:
            self.puntaje_total += frame.puntaje()

        # Manejo especial del frame 10
        if self.frames[9].es_strike() or self.frames[9].es_spare():
            puntaje_frame_10 = self.frames[9].puntaje()

            if self.frames[9].es_strike():
                puntaje_frame_10 += self.frames[10].puntaje_primer_tiro()

                if self.frames[10].es_strike():
                    puntaje_frame_10 += self.frames[11].puntaje_primer_tiro()

            self.puntaje_total += puntaje_frame_10


class Frame:
    def __init__(self):
        self.tiros = []

    def agregar_tiro(self, tiro):
        self.tiros.append(tiro)

    def puntaje(self):
        puntaje = 0

        for tiro in self.tiros:
            puntaje += tiro.pines

        if self.es_strike():
            puntaje += self.puntaje_siguiente_tiro() + self.puntaje_siguiente_siguiente_tiro()
        elif self.es_spare():
            puntaje += self.puntaje_siguiente_tiro()

        return puntaje

    def es_strike(self):
        return self.tiros[0].strike()

    def es_spare(self):
        return len(self.tiros) == 2 and self.tiros[0].pines + self.tiros[1].pines == 10

    def puntaje_siguiente_tiro(self):
        if len(self.tiros) >= 2:
            return self.tiros[1].pines
        else:
            return 0

    def puntaje_siguiente_siguiente_tiro(self):
        if len(self.tiros) >= 3:
            return self.tiros[2].pines
        else:
            return 0


class Tiro:
    def __init__(self, pines):
        self.pines = pines

    def strike(self):
        return self.pines == 10

    def spare(self):
        return self.pines == 10

    def valido(self):
        if not isinstance(self.pines, int):
            print("Error: Debe ingresar un número entero.")
            return False
        elif self.pines < 0 or self.pines > 10:
            print(f"Error: La cantidad de pines debe estar entre 0 y 10. Valor ingresado: {self.pines}")
            return False
        else:
            return True


class TiroInvalido(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje


if __name__ == "__main__":
    juego = Juego()
    juego.jugar()
