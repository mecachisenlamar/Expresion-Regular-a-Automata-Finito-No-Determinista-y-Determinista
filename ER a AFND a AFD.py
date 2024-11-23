##Code made by Nicolás Arellano
class Thomson:
    def __init__(self):
        self.K = []  # Lista de estados
        self.delta = []  # Lista de transiciones
        self.lista_er = []  # Lista de la expresión regular
        self.estado = 0  # Contador para los estados
        self.primera_iteracion = True
        self.cadena = []
        self.diccionario = []

    def juntar(self, er):
        agregar = "-"
        er2 = ""  
        while "-" in agregar: 
            agregar = input("Ingresar continuación (Expresión Regular): ")
            er += agregar
        
        for i in range(len(er)):
            if er[i] != "-": 
                er2 += er[i]
        
        return er2

    def juntar_cadena(self, cadena):
        agregar = "-"
        cadena2 = ""  
        while "-" in agregar: 
            agregar = input("Ingresar continuación (Cadena): ")
            cadena += agregar
        
        for i in range(len(cadena)):
            if cadena[i] != "-": 
                cadena2 += cadena[i]
        
        return cadena2


    def crear_estado(self):
        if self.primera_iteracion == True and self.estado != 0:
            self.estado -= 1
            estado = "q" + str(self.estado)
            self.primera_iteracion = False
            self.estado += 1
            return estado
        elif self.estado == 0:
            estado = "q" + str(self.estado)
            self.estado += 1
            self.primera_iteracion = False
            return estado
        else:
            estado = "q" + str(self.estado)
            self.estado += 1
            return estado
        
    def agregar_estado(self, *estados):
            for estado in estados:
                if estado not in self.K:
                    self.K.append(estado)

    def simplificacion_er(self, er):
        resultado = ""
        pila = []
        i = 0

        # Reglas para eliminar falencias y simplificar
        while i < len(er):
            char = er[i]

            # Ignorar caracteres no permitidos
            if char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ*|.0Φ_":
                print(f"Carácter inválido '{char}' eliminado.")
                i += 1
                continue

            # Manejar paréntesis, aunque no están permitidos en este caso
            if char in "([{)]}":
                print(f"Paréntesis o corchetes no permitidos '{char}' eliminado.")
                i += 1
                continue

            # Eliminar operadores consecutivos inválidos
            if char in "|*.":
                if resultado and resultado[-1] in "|*.":
                    print(f"Operador consecutivo '{resultado[-1]}{char}' corregido a '{char}'.")
                    resultado = resultado[:-1] + char
                elif not resultado or resultado[-1] in "|*.":
                    print(f"Operador mal posicionado '{char}' eliminado.")
                else:
                    resultado += char

            # Clausura de Kleene (*) correctamente usada
            elif char == "*" and (not resultado or resultado[-1] in "|*."):
                print(f"Clausura de Kleene mal usada '{char}' eliminada.")
            else:
                resultado += char

            i += 1

        # Eliminar '|' o '.' al final
        if resultado.endswith("|") or resultado.endswith("."):
            print(f"Operador '{resultado[-1]}' al final eliminado.")
            resultado = resultado[:-1]

        # Eliminar expresiones vacías resultantes
        if not resultado:
            print("Expresión regular vacía tras simplificación.")
            return "Φ"

        print(f"Expresión regular simplificada: {resultado}")
        return resultado

    
    def AFND(self, er):
        # Convertir la expresión regular en una lista de caracteres
        if "-" in er:
            er = self.juntar(er)
        #creacion del primero estado que acepta todos los caracteres de la cadena
        q_inicio = self.crear_estado()
        for simbolo in self.diccionario: # hace que todos los simmbolos del alfabeto vayan para ahi cosa que no se pueda salir, por algo sumidero lol
            self.delta.append([q_inicio, simbolo, q_inicio])
        self.primera_iteracion = True

        er = self.simplificacion_er(er)


        #creacion de los estados normalmente
        for i in er:
            self.lista_er.append(i) 
        i = 0
        while i < len(self.lista_er):
            # Si no es Φ o 0, procesamos normalmente
            if self.lista_er[i] != "Φ" and self.lista_er[i] != "0":
                if i+1 < len(self.lista_er) and self.lista_er[i+1] == "*":
                    # Como es clausura de Kleene, siempre se añaden 4 estados
                    q0 = self.crear_estado()
                    q1 = self.crear_estado()
                    q2 = self.crear_estado()
                    q3 = self.crear_estado()

                    # Añadir las transiciones (deltas)
                    self.delta.append([q0, "_", q1])
                    self.delta.append([q1, self.lista_er[i], q2]) 
                    self.delta.append([q2, "_", q1])
                    self.delta.append([q2, "_", q3])
                    self.delta.append([q0, "_", q3])

                    # Añadir los nuevos estados
                    self.agregar_estado(q0, q1, q2, q3)

                    # Saltar al siguiente símbolo (ya que el actual era parte de "*")
                    i += 2
                    self.primera_iteracion = True       
                ##si detecto un epsilon: 
                elif i == "_":
                    q0 = self.crear_estado()
                    q1 = self.crear_estado()

                    self.delta.append([q0, "_", q1])  
                    self.agregar_estado(q0, q1)
                    
                    i += 1 
                    self.primera_iteracion = True
                elif i+3 < len(self.lista_er) and self.lista_er[i+1] == "|" and self.lista_er[i+3] == "*":
                    q0 = self.crear_estado()
                    q1 = self.crear_estado()
                    q2 = self.crear_estado()
                    q3 = self.crear_estado()
                    q4 = self.crear_estado()
                    q5 = self.crear_estado()
                    q6 = self.crear_estado()
                    q7 = self.crear_estado()


                    self.delta.append([q0, "_", q1])  # Epsilon desde el inicio a la rama 'a'
                    self.delta.append([q1, self.lista_er[i], q2])
                    self.delta.append([q2, "_", q7])
                    self.delta.append([q0, "_", q3])
                    self.delta.append([q3, "_", q4])
                    self.delta.append([q4, self.lista_er[i+2], q5])
                    self.delta.append([q5, "_", q4])
                    self.delta.append([q5, "_", q6])
                    self.delta.append([q3, "_", q6])
                    self.delta.append([q6, "_", q7]) 

                    # Agregar todos los estados
                    self.agregar_estado(q0, q1, q2, q3, q4, q5, q6, q7)
                    i += 4
                    self.primera_iteracion = True
            

                elif i+1 < len(self.lista_er) and self.lista_er[i+1] == "|":
                    q0 = self.crear_estado()
                    q1 = self.crear_estado()
                    q2 = self.crear_estado()
                    q3 = self.crear_estado()
                    q4 = self.crear_estado()
                    q5 = self.crear_estado()

                    self.delta.append([q0, "_", q1])
                    self.delta.append([q1, self.lista_er[i], q2])
                    self.delta.append([q2, "_", q5])
                    self.delta.append([q0, "_", q3])
                    self.delta.append([q3, self.lista_er[i+2], q4])
                    self.delta.append([q4, "_",q5])

                    # Añadir los nuevos estados
                    self.agregar_estado(q0, q1, q2, q3, q4, q5)

                    # Saltar al sub-siguiente símbolo (ya que el actual era parte del or y el siguiente a ese)
                    if i+3 < len(self.lista_er) and self.lista_er[i+3] == "|":
                        i += 2
                    else:
                        i += 3
                    self.primera_iteracion = True
                else:
                    q0 = self.crear_estado()
                    q1 = self.crear_estado()

                    self.delta.append([q0, self.lista_er[i], q1])
                    self.agregar_estado(q0, q1)
                    if i+1 < len(self.lista_er) and self.lista_er[i+1] == ".":
                        i += 2
                    else:
                        i += 1
                    self.primera_iteracion = True

            # sumidero
            else:
                q_sumidero = self.crear_estado()
                for simbolo in self.diccionario: # hace que todos los simmbolos del alfabeto vayan para ahi cosa que no se pueda salir, por algo sumidero lol
                    self.delta.append([q_sumidero, simbolo, q_sumidero])

                i = len(self.lista_er)

    def sigma(self,cadena):
        diccionario = []
        if "-" in cadena:
            cadena = self.juntar_cadena(cadena)
        # Asegurarse de que delta no esté vacío y que cada elemento tenga al menos 3 elementos
        for i in cadena:
            if i not in diccionario:
                diccionario.append(i)
        self.diccionario = diccionario

class Conversion:
    def __init__(self):
        self.clausura_estado = []  # hasta donde puede llegar con y solo transiciones epsilon
        self.diccionario = []
        self.delta_min = []
        self.estados_finales = []
        self.estados_totales = []
    
    def clausuras(self, estados, transiciones):
        epsilon_encontrado = False  # Variable para verificar si alguna vez encontramos epsilon
        for m in range(len(estados)):
            epsilon = False
            clausura_temporal = [estados[m], "U"]  # Inicializamos con el estado y "U"
            
            for n in range(len(transiciones)):
                if estados[m] == transiciones[n][0] and transiciones[n][1] == "_":
                    epsilon_encontrado = True
                    epsilon = True
                    state = transiciones[n][2]
                    clausura_temporal.append(state)
            
            # Si se encontraron transiciones epsilon, usamos la clausura completa.
            # Si no, dejamos solo el estado inicial sin duplicados ni "U".
            if epsilon:
                self.clausura_estado.append(clausura_temporal)
            else:
                self.clausura_estado.append([estados[m]])

        ####print("Clausuras: ", self.clausura_estado)  # Imprimimos las clausuras generadas

        self.AFD(transiciones, estados)  # Llama al objeto AFD para que comience el cambio de AFND a AFD


    
    def AFD(self, transiciones, estados):
        # Inicializamos con la primera clausura sin 'U'
        estado_inicial = [i for i in self.clausura_estado[0] if i != "U"]
        estados_2 = [estado_inicial]
        diccionario = p.diccionario
        trans = transiciones
        procesados = set()
        self.delta_min = []

        while estados_2:
            estado_actual = estados_2.pop(0)
            estado_actual_tuple = tuple(estado_actual)  # Convertimos a tupla para usar en el set
            if estado_actual_tuple in procesados:
                continue
            procesados.add(estado_actual_tuple)

            for c in diccionario:
                t = set()
                for estado in estado_actual:
                    for transicion in trans:
                        if estado == transicion[0] and transicion[1] == c:
                            destino = transicion[2]
                            for clausura in self.clausura_estado:
                                if clausura[0] == destino:
                                    t.update([s for s in clausura if s != "U"])

                if not t:
                    t = ['Φ']
                else:
                    t = list(t)  # Convertimos `t` a lista en lugar de tupla para mantener el formato original

                # Agregamos la transición a delta_min con formato de lista
                self.delta_min.append([estado_actual, c, t])

                # Si el estado destino no ha sido procesado ni está en la lista, lo agregamos
                if t != ['Φ'] and tuple(t) not in procesados and t not in estados_2:
                    estados_2.append(t)
        #estados iniciales, finales y totales
        for i in range(len(self.delta_min)):
            for j in range(len(self.delta_min[i])):
                for b in range(len(self.delta_min[i][j])):
                    if self.delta_min[i][j][b] == estados[-1] and self.delta_min[i][j] not in self.estados_finales and self.delta_min[i][j][b] not in diccionario:
                        self.estados_finales.append(self.delta_min[i][j])
                    if self.delta_min[i][j] not in self.estados_totales and self.delta_min[i][j][b] not in diccionario:
                        self.estados_totales.append(self.delta_min[i][j])



# Modo de uso
expresion_regular = input("Ingrese su expresión regular: ")
string = input("Ingrese una Cadena: ")

if "ñ" in expresion_regular or "Ñ" in expresion_regular:
    print("Expresion regular inválida: contiene 'ñ' o 'Ñ'")
else:
    p = Thomson()
    p.sigma(string)
    p.AFND(expresion_regular)
    if expresion_regular not in ["0", "Φ", "0Φ", "Φ0","*","*|","|*", "|", "."] and string != "":
        if len(expresion_regular) <= 50:
            print("AFND")
            print("Estado Inicial", p.K[0])
            print("Estado final", p.K[-1])
            print("Estados:", p.K)
            print("Transiciones:", p.delta)
            print("Diccionario", p.diccionario)

            print("\t")
            b = Conversion()
            b.clausuras(p.K, p.delta)
            print("AFD")
            print("Clausulas Epsilon", b.clausura_estado)
            print("Estado Inicial", p.K[0])
            print("Estados Finales", b.estados_finales)
            print("Estados Totales", b.estados_totales)
            print("Transiciones:", b.delta_min)
            print("Diccionario", p.diccionario)
        else:
            print("Expresion Regular tiene más de 50 caracteres")
    else:
        print("Expresion regular vacia o cadena invalida")
