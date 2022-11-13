from proceso import Proceso
import os
import time
import random
import msvcrt
import sys

cont_global = 0
nuevos = [] #cola de nuevos
listos = [] #cola de listos
ejecucion = [] #cola de ejecucion
bloqueados = [] #cola de bloqueados
terminados = [] #cola de terminados

def definir(cantidad_procesos):
    
    for i in range(0,cantidad_procesos):
        print("Proceso: ",i)
        llenadoAutomatico(i)

    mostrar()
    if (len(terminados) == cantidad_procesos):
        print("Procesos Terminados: ",len(terminados))
        print("ID\tT. Llegada\tT. Finalizacion\tT. Retorno\t T.Respuesta\tT. Espera \tT. Servicio \tOperacion y Resultado")
        for i in range(0,len(terminados)):
            terminados[i].tretorno = terminados[i].tfinalizacion - terminados[i].tllegada
            terminados[i].espera = terminados[i].tretorno - terminados[i].tt
            terminados[i].trespuestanuevo = terminados[i].trespuesta - terminados[i].tllegada
            print(str(terminados[i].id) +"\t\t"+ str(terminados[i].tllegada) +"\t\t" + str(terminados[i].tfinalizacion) 
            +"\t\t"+ str(terminados[i].tretorno) +"\t\t"+ str(terminados[i].trespuestanuevo) +"\t\t"+ str(terminados[i].espera)
            +"\t \t"+ str(terminados[i].tt)+ "\t\t ", end="")

            if(terminados[i].error == 0):
                print((str(realizarOperacion(terminados[i]))))
            elif(terminados[i].error == 1):
                print(" ¡ERROR! ")

            print("")

def llenadoAutomatico(i):
    id = i
    num1 = random.randint(0, 10)
    num2 = random.randint(0, 10)
    operacion = random.randint(1, 6)
    tme = random.randint(6, 16) #Genera un tiempo aleatorio de tiempo de ejecucion entre 6 y 16

    pro = Proceso(id,operacion,tme,num1,num2)
    nuevos.append(pro)

def mostrar():

    cantidad_procesos = len(nuevos)
    
    cont_ext = 0
    
    i = 0
    cont = 0
    esprimero = True
    while(cont<cantidad_procesos):
        #Entra lote listo (3)
        if (i == 4):
            #Procesame todo el lote
            #Procesame esta
            #cont_ext = 0
            procesar()
            i = 0;
            ##
            if (len(nuevos) > 0 and esprimero):    
                nuevos[0].tllegada = cont_global
                listos.append(nuevos[0])
                nuevos.remove (nuevos[0])
                listos[0].trespuesta = cont_global
                esprimero = False
            ##
            if (len(listos) == 1):
                #listos[0].trespuesta = cont_global
                ejecucion.append(listos[0])
                listos.remove(listos[0])
                imprimirEjecucion()

        ##Crea Lotes
        else:
            if (len(nuevos) > 0):
                nuevos[0].tllegada = cont_global
                listos.append(nuevos[0])
                nuevos.remove(nuevos[0])
        i+=1
        cont +=1  
    

def procesar():

    i = 0
    long = len(nuevos) + 1
    while (i<=long and len(listos) > 0): 
        ejecucion.append(listos[0])
        listos.remove(listos[0])
        imprimirEjecucion()
        ejecucion[0].tfinalizacion = cont_global
        terminados.append(ejecucion[0])
        if (len(nuevos) > 0):
            nuevos[0].tllegada = cont_global
            listos.append(nuevos[0])
            nuevos.remove(nuevos[0])
        ejecucion.remove(ejecucion[0])
        i+=1
        

def imprimirEjecucion():
    
    global cont_global
    if len(listos) >= 0:
        tt = ejecucion[0].tt
        if tt == 0:
            ejecucion[0].trespuesta = cont_global
        while(tt<=ejecucion[0].tme):
            
            if(msvcrt.kbhit()):
                key = msvcrt.getwch()
                #69 = E key y 101 = e key
                if(key == chr(101) or key == chr(69)):
                    if len(listos) > 0 and len(bloqueados) < 3:        
                        bloqueados.append(ejecucion[0])
                        ejecucion.remove(ejecucion[0])
                        ejecucion.append(listos[0])
                        listos.remove(listos[0])
                        imprimirEjecucion()
                    break
                #87 = W key y 119 = w key
                elif(key == chr(87) or key == chr(119)):
                    ejecucion[0].tme = 0
                    ejecucion[0].error = 1
                    break
                #80 = P key y 112 = p key
                elif(key == chr(80) or key == chr(112)):
                    #->
                    print("******************************************")
                    print("Contador Global: " + str(cont_global))
                    print("******************************************\n")
                    print("******************************************")
                    print("***              Nuevos                ***")
                    print("******************************************")
                    print("ID\t|Tiempo Maximo Estimado")
                    if len(nuevos) > 0:
                        #lote en Listos
                        for proc in nuevos:
                            print(str(proc.id) + "\t\t" + str(proc.tme))
                    print("\n******************************************")
                    print("***               Listos                 ***")
                    print("********************************************")
                    print("ID\t|Tiempo Maximo Estimado\t|Tiempo Transcurrido")

                    #lote en Listos
                    for lote in listos:
                        if (lote != ejecucion[0]):
                            print(str(lote.id) + "\t\t" + str(lote.tme)+ "\t\t" + str(lote.tt))

                    #Proceso en ejecucion
                    if len(ejecucion) > 0 and ejecucion[0].error != 1:
                        print("\n******************************************")
                        print("***    Proceso en ejecución            ***" )
                        print("******************************************")
                        print("Id: " + str(ejecucion[0].id))
                        print("Operación: " + str(realizarOperacionAntes(ejecucion[0])))
                        print("Tiempo Maximo Estimado: " + str(ejecucion[0].tme))
                        print("Tiempo Transcurrido: " + str(tt))
                        print("Tiempo Restante: " + str(ejecucion[0].tme-tt))
                    cont_global += 1

                    #Procesos bloqueados
                    print("\n******************************************")
                    print("***         Procesos Bloqueados        ***")
                    print("******************************************")
                    print("ID\t|Tiempo Transcurrido en Bloqueado")
                    if(len(bloqueados) > 0):
                        for lote in bloqueados:
                            if lote.ttb <= 7:
                                print(str(lote.id) + "\t\t" + str(lote.ttb)+ "\t\t" + str(lote.tt))
                                lote.ttb += 1
                            else:
                                lote.ttb = 0
                                listos.append(lote)
                                bloqueados.remove(lote)
                                
                    tt += 1
                    ejecucion[0].tt = tt

                    print("\n******************************************")
                    print("***        Procesos Terminados         ***")
                    print("******************************************\n")
                    print("ID \t\t\t|Operacion" )
                    for terminado in terminados:
                        if(terminado.error == 0):
                            print(str(terminado.id) +  "\t\t\t| " + str(realizarOperacion(terminado)))
                        elif(terminado.error == 1):
                            print(str(terminado.id) +  "\t\t\t| ¡ERROR! ")

                    time.sleep(1)

                    if(len(ejecucion) == 1 and tt>ejecucion[0].tme and ejecucion[0].error == 0):
                        print(str(ejecucion[0].id) + "\t\t\t| " + str(realizarOperacion(ejecucion[0])))
                        #os.system("pause")
                    elif((len(ejecucion) == 1 and tt>ejecucion[0].tme and ejecucion[0].error != 0)):
                        print(str(ejecucion[0].id) +  "\t\t\t| ¡ERROR! ")
                        os.system("pause")
                    while(True):
                        c = input("Proceso pausado, ¿Quieres continuar? (c/C)")
                        if(c == "c" or c == "C"):
                            break
                    break
                sys.stdout.flush()
            print("******************************************")
            print("Contador Global: " + str(cont_global))
            print("******************************************\n")
            print("******************************************")
            print("***              Nuevos                ***")
            print("******************************************")
            print("ID\t|Tiempo Maximo Estimado")
            if len(nuevos) > 0:
                #lote en Listos
                for proc in nuevos:
                    print(str(proc.id) + "\t\t" + str(proc.tme))
            print("\n******************************************")
            print("***               Listos                 ***")
            print("********************************************")
            print("ID\t|Tiempo Maximo Estimado\t|Tiempo Transcurrido")

            #lote en Listos
            for lote in listos:
                if (lote != ejecucion[0]):
                    print(str(lote.id) + "\t\t" + str(lote.tme)+ "\t\t" + str(lote.tt))

            #Proceso en ejecucion
            if len(ejecucion) > 0 and ejecucion[0].error != 1:
                print("******************************************")
                print("***    Proceso en ejecución            ***" )
                print("******************************************")
                print("Id: " + str(ejecucion[0].id))
                print("Operación: " + str(realizarOperacionAntes(ejecucion[0])))
                print("Tiempo Maximo Estimado: " + str(ejecucion[0].tme))
                print("Tiempo Transcurrido: " + str(tt))
                print("Tiempo Restante: " + str(ejecucion[0].tme-tt))
            cont_global += 1

            #Procesos bloqueados
            print("\n******************************************")
            print("***         Procesos Bloqueados        ***")
            print("******************************************")
            print("ID\t|Tiempo Transcurrido en Bloqueado")
            if(len(bloqueados) > 0):
                for lote in bloqueados:
                    if lote.ttb <= 7:
                        print(str(lote.id) + "\t\t" + str(lote.ttb)+ "\t\t" + str(lote.tt))
                        lote.ttb += 1
                    else:
                        lote.ttb = 0
                        listos.append(lote)
                        bloqueados.remove(lote)
                        
            tt += 1
            ejecucion[0].tt = tt

            print("\n******************************************")
            print("***        Procesos Terminados         ***")
            print("******************************************")
            print("ID \t|Operacion" )
            for terminado in terminados:
                if(terminado.error == 0):
                    print(str(terminado.id) +  "\t\t\t| " + str(realizarOperacion(terminado)))
                elif(terminado.error == 1):
                    print(str(terminado.id) +  "\t\t\t| ¡ERROR! ")

            time.sleep(1)

            if(len(ejecucion) == 1 and tt>ejecucion[0].tme and ejecucion[0].error == 0):
                print(str(ejecucion[0].id) + "\t\t\t| " + str(realizarOperacion(ejecucion[0])))
                #os.system("pause")
            elif((len(ejecucion) == 1 and tt>ejecucion[0].tme and ejecucion[0].error != 0)):
                print(str(ejecucion[0].id) +  "\t\t\t| ¡ERROR! ")
                os.system("pause")
                
            clearConsole()

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def realizarOperacionAntes(lote):
    num1 = lote.num1
    num2 = lote.num2
    operacion = lote.operacion
    resultado = 0
    operando = ""
    if(operacion == 1): #Condicinal para la Suma
        resultado = num1 + num2
        operando = "+"
    elif(operacion == 2): #Condicinal para la Resta
        resultado = num1 - num2
        operando = "-"
    elif (operacion == 3): #Condicinal para la Multiplicacion
        resultado = num1 * num2
        operando = "*"
    elif (operacion == 4): #Condicinal para la Division
        if(num2 == 0): #Error, division entre 0
            resultado = "No se puede dividir entre 0"
            operando = "/"
        else:
            resultado = num1 / num2
            operando = "/"
    elif (operacion == 5):#Condicinal para el Residuo
        if(num2 == 0): #Error, division entre 0
            resultado = "No se puede dividir entre 0"
            operando = "%" #Residuo
        else:
            resultado = num1 % num2
            operando = "%"
    elif (operacion == 6): #Condicional para la potencia
        resultado = num1 ** num2
        operando = "**"
    res = str(num1) + " " + str(operando) + " " + str(num2)

    return res

def realizarOperacion(lote):
    num1 = lote.num1
    num2 = lote.num2
    operacion = lote.operacion
    resultado = 0
    operando = ""

    if(operacion == 1): #Condicinal para la Suma
        resultado = num1 + num2
        operando = "+"
    elif(operacion == 2): #Condicinal para la Resta
        resultado = num1 - num2
        operando = "-"
    elif (operacion == 3): #Condicinal para la Multiplicacion
        resultado = num1 * num2
        operando = "*"
    elif (operacion == 4): #Condicinal para la Division
        if(num2 == 0): #Error, division entre 0
            resultado = "En una division no se puede dividir entre 0"
            operando = "/"
        else:
            resultado = num1 / num2
            operando = "/"
    elif (operacion == 5):#Condicinal para el Residuo
        if(num2 == 0): #Error, division entre 0
            resultado = "En una division no se puede dividir entre 0"
            operando = "%" #Residuo
        else:
            resultado = num1 % num2
            operando = "%"
    elif (operacion == 6): #Condicional para la potencia
        resultado = num1 ** num2
        operando = "**"

    res = str(num1) + " " + str(operando) + " " + str(num2) + " = " + str(resultado)

    return res