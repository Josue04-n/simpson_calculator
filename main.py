'''
PROTOTIPO 1
# Autor: Josue Llumitasig
from services.plot_service import graficar_area_bajo_funcion
import numpy as np

f = lambda x:  x**2 - 4*x + 3  # Definimos la función f(x) = x^2 - 4x + 3
graficar_area_bajo_funcion(f, 0, 4)
'''
'''PROTIPTO 2
from services.plot_service import graficar_area_bajo_funcion_v2
import numpy as np

f = lambda x: x**2 - 4*x + 3 
a = 0
b = 4
resultado = 1.2521  # Puedes obtenerlo de simpson_13

graficar_area_bajo_funcion_v2(f, a, b, area_valor=resultado, texto_funcion="sqrt(x) - x/2")
'''
'''PROTIPTO 3'''
from services.plot_service import graficar_area
import numpy as np

f = lambda x: np.sqrt(x) - x/2
a, b = 0, 4
area = 1.2521

graficar_area(f1=f, a=a, b=b, area_valor=area, texto_funcion1="sqrt(x) - x/2")

from services.plot_service import graficar_area
import numpy as np

f1 = lambda x: np.sqrt(x)
f2 = lambda x: x / 2
a, b = 0, 4
area = 1.2521

graficar_area(f1=f1, f2=f2, a=a, b=b, area_valor=area,
              texto_funcion1="sqrt(x)", texto_funcion2="x/2",
              guardar_como="grafica_area_entre.png")
