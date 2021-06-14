import simpy
import random
import datetime as dt
import pandas as pd

class lugarV():
    def __init__(self,env,mesas):
        self.env = env
        self.mesas = simpy.Resource(env,mesas)

  
    def salida(self):
        tiempo = random.randint(2,7)
        yield self.env.timeout(tiempo)


    def esperaSegundaDosis(self):
        yield self.env.timeout(43200) # Equivalencia de 30 dias en minutos

    def filas(self):
        tiempo = random.randint(10,30)
        yield self.env.timeout(tiempo)
   

    def chequeoSalud(self):
        yield self.env.timeout(20)

    
    def vacunacion(self):
        tiempo = random.randint(5,10)
        yield self.env.timeout(tiempo)

  
    def certificado(self):
        espera = random.randint(2,3)
        yield self.env.timeout(espera)

    def pacientell(self,paciente):
        
        for i in range (2):
            with self.mesas.request() as mesa:
                
                yield mesa
                yield self.env.process(self.filas())
                print('La persona {} pasa a la mesa a el {}'.format(paciente))
                yield self.env.process(self.vacunacion())
                print('La persona {} se termina de vacunar el {}'.format(paciente))
            yield self.env.process(self.chequeoSalud())
            print('La persona {} espera 20 minutos para poder realizarse chequeos en su salud, termina estos chequeos el {}'.format(paciente))
            if i == 0:
                yield self.env.process(self.certificado())              
                print('La persona {} recibe su certificado a los {} minutos'.format(paciente))
                yield self.env.process(self.salida())               
                print('La persona {} abandona el recinto el {}'.format(paciente))
                print('La persona {} espera 30 dias para su segunda dosis'.format(paciente))            
                yield self.env.process(self.esperaSegundaDosis())
            else:
                yield self.env.process(self.salida())          
                print('La persona {} abandona el recinto el {}'.format(paciente))
      


class vacunacion():
    def __init__(self,vacunados):
        self.vacunados = vacunados * 0.8 
        self.vacunados = self.porcentaje(self.vacunados)

    def porcentaje(self,vacunados):    
        falso = 1-random.randint(5,10)/100
        self.vacunados = self.vacunados * falso
        print('Recibiran la vacuna ' + str(int(self.vacunados)) + ' pacientes de ' + str(int(vacunados)))
        return self.vacunados
        

    def empieza(self,env,mesas):
        lug = lugarV(env,mesas)
        for i in range(int(self.vacunados)): 
            if i < 7000:
                env.process(lug.pacientell(i))
            else:
                yield env.timeout(random.randint(4,20)) 
                yield env.process(lug.pacientell(i))

  
        

if __name__ == '__main__':

    ##Parametros de entrada
    mesa = 4
    timeV = 43200 
    pacientes = 15
    
    
    env = simpy.Environment()
    sim = vacunacion(pacientes)
    env.process(sim.empieza(env,mesa))
    env.run(until=timeV)