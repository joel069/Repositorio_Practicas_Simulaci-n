import simpy
import random
import numpy

class SimulacionLavadora():
    def __init__(self,env,maquinas):
        self.env = env
        self.maquinas = simpy.Resource(env,maquinas)

    def llega(self, tiempo):
        yield self.env.timeout(tiempo)

    def lavando(self,tiempo):
        yield self.env.timeout(tiempo)

    def sale(self,tiempo):
        yield self.env.timeout(tiempo)

    def llegaAuto(self,vehiculo):
        
        with self.maquinas.request() as maquina:
            print('El {} llega al minuto {:,.2f}'.format(vehiculo,self.env.now))
            yield maquina

           
            tlle = random.randint(1,5)
            #print('El {} llega al minuto {:,.2f}'.format(vehiculo,self.env.now))
            yield self.env.process(self.llega(tlle))
            print('El {} pasa a la maquina al minuto {:,.2f}'.format(vehiculo,self.env.now))

           
            tla = random.randint(5,11)
            yield self.env.process(self.lavando(tla))
            print('El {} termina el lavado al minuto {}'.format(vehiculo,self.env.now))

            
            tsa = random.randint(2,5)
            yield self.env.process(self.sale(tsa))
            print('El {} sale del lavado al minuto {}'.format(vehiculo,self.env.now))


class Simulacion():
    def __init__(self,inicio):
        self.inicio = inicio
        self.nombreVehiculo = 'Auto {}'

    def ejecutar(self,env,maquinas,intervalo):
        carwash = SimulacionLavadora(env,maquinas)
        self.inicioEntrada(env,carwash)

        while True:
            yield env.timeout(random.randint(intervalo-2,intervalo+2)) 
            self.inicio+=1
            yield env.process(carwash.llegaAuto(self.nombreVehiculo.format(self.inicio)))

    def inicioEntrada(self,env,carwash):
        for i in range(self.inicio):
            env.process(carwash.llegaAuto(self.nombreVehiculo.format(i)))


if __name__ == '__main__':
    autos = 10
    maquinas = 5
    intervalo = 10
    tiempoSimulacion = 90

    env = simpy.Environment()
    simulacion = Simulacion(autos)
    env.process(simulacion.ejecutar(env,maquinas,intervalo))
    env.run(until=tiempoSimulacion)