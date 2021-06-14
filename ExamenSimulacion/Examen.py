import simpy
import random
import datetime as dt
import pandas as pd

class lugares():
    def __init__(self,env,mesas):
        self.env = env
        self.mesas = simpy.Resource(env,mesas)

 
    def filas(self):
        tiempo = random.randint(10,30)
        yield self.env.timeout(tiempo)

 
    def salir(self):
        tiempo = random.randint(2,5)
        yield self.env.timeout(tiempo)


    def segunda(self):
        yield self.env.timeout(43200) 


    def espera(self):
        yield self.env.timeout(20)

    
    def vacunacion(self):
        tiempo = random.randint(5,10)
        yield self.env.timeout(tiempo)

 
    def vacCert(self):
        espera = random.randint(2,3)
        yield self.env.timeout(espera)

    def llegada(self,persona):
        
        for i in range (2):
            with self.mesas.request() as mesa:
                yield mesa
                yield self.env.process(self.filas())
                print('Paciente {} pasa a su lugar  {} '.format(persona,self.env.now) + 'minutos')
                yield self.env.process(self.vacunacion())
                print('Paciente{} vacunado {}'.format(persona,self.env.now) + 'minutos')
            yield self.env.process(self.espera())
            print('Paciente {} espera ante posibles reacciones {}'.format(persona,self.env.now) + 'minutos')
            if i == 0:
                yield self.env.process(self.vacCert())
                print('Paciente {} con certificado {} '.format(persona,self.env.now) + 'minutos')
                yield self.env.process(self.salir())
                print('Paciente {} espera por su segunda dosis {} '.format(persona,self.env.now) + 'minutos')
                yield self.env.process(self.segunda())
            else:
                yield self.env.process(self.salir())
                print('Paciente {} sale vacunado   {}'.format(persona,self.env.now) + 'minutos')

class Vacunas():
    def __init__(self,sdas):
        self.electores = electores * 0.8 
        self.electores = self.calcularPersonas(self.electores)
        
    def calcularPersonas(self,electores):    
        no_vacuna = 1-random.randint(5,10)/100
        self.electores = self.electores * no_vacuna
        return self.electores

    def ejecutar(self,env,mesas):
        lug = lugares(env,mesas)
        for i in range(int(self.electores)): 
            if i < 5:
                env.process(lug.llegada(i))
            else:
                yield env.timeout(random.randint(4,20)) 
                yield env.process(lug.llegada(i))
        

if __name__ == '__main__':
    lugar = 3
    t = 43200
    electores = 5
    
    env = simpy.Environment()
    simulacion = Vacunas(electores)
    env.process(simulacion.ejecutar(env,lugar))
    env.run(until=t)