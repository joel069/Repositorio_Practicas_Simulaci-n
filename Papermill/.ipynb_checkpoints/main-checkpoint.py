import argparse
import papermill as pm

def main(numeros):
    pm.execute_notebook(
    './entrada.ipynb',
    './out/salida.ipynb',
    parameters=dict(uno=numeros[0],dos=numeros[1])
    )
    
        
if __name__ == '__main__':
    args = argparse.ArgumentParser()

    args.add_argument('Numeros',
          help='Uno y Dos',
      type=str
    )

    arguments = args.parse_args()
    main([i for i in arguments.date.split(',')])
    
