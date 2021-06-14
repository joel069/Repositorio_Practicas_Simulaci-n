import argparse
import papermill as pm

def main(datos):
    pm.execute_notebook(
    './entrada.ipynb',
    './out/salida.ipynb',
    parameters=dict(uno=datos[0],dos=datos[1])
    )
    
        
if __name__ == '__main__':
    args = argparse.ArgumentParser()

    args.add_argument('int',
          help='Uno y Dos',
      type=str
    )

    arguments = args.parse_args()
    main([i for i in arguments.int.split(',')])
    
