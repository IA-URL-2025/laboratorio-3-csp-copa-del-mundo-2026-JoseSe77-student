# Laboratorio 3 - CSP: Sorteo Copa Mundial 2026

## Introducción

En este laboratorio se modeló el problema del sorteo de la Copa Mundial 2026 como un Problema de Satisfacción de Restricciones (CSP). El objetivo principal fue asignar 48 equipos a 12 grupos, identificados de la A a la L, cumpliendo un conjunto de restricciones relacionadas con bombos, confederaciones y tamaño de los grupos.

El problema fue abordado mediante un enfoque de búsqueda con backtracking, complementado con heurísticas y técnicas de propagación de restricciones para mejorar la eficiencia del proceso.

---

## Modelado del Problema

El problema se representó como un CSP en el cual cada equipo constituye una variable que debe ser asignada a un grupo específico. El dominio de cada variable está conformado por todos los grupos disponibles, lo que implica que inicialmente cualquier equipo puede ser asignado a cualquier grupo.

Se definieron restricciones fundamentales para asegurar la validez del sorteo. Cada grupo puede contener un máximo de cuatro equipos, garantizando así la estructura correcta del torneo. Además, no puede haber más de un equipo del mismo bombo en un mismo grupo, lo que permite una distribución equilibrada de los equipos.

En cuanto a las confederaciones, se estableció que únicamente puede existir un equipo por confederación en cada grupo, con la excepción de UEFA, donde se permite un máximo de dos equipos. Estas restricciones aseguran que la solución cumpla con las reglas del torneo internacional.

---

## Estrategia de Solución

Para resolver el problema se utilizó un algoritmo de backtracking, el cual construye la solución de manera incremental. Este enfoque asigna equipos a grupos y retrocede en caso de detectar una violación de restricciones.

Con el fin de mejorar la eficiencia, se incorporaron dos técnicas clave. La primera es la heurística MRV (Minimum Remaining Values), la cual selecciona la siguiente variable a asignar basándose en el tamaño de su dominio. De esta forma, se priorizan las variables más restringidas, reduciendo el espacio de búsqueda.

La segunda técnica utilizada es el forward checking, que permite eliminar valores inválidos de los dominios de las variables no asignadas. Esto ayuda a detectar inconsistencias de manera anticipada y evita explorar soluciones que no son viables.

La combinación de estas técnicas permitió optimizar significativamente el rendimiento del algoritmo.

---

## Implementación

La solución fue desarrollada en Python, organizando el código en distintos módulos para mantener una estructura clara y modular.

El archivo `world_cup_csp.py` contiene la lógica principal del CSP, incluyendo la validación de restricciones, la selección de variables mediante MRV, el forward checking y el algoritmo de backtracking.

El archivo `solver.py` se encarga de ejecutar el proceso completo de resolución del problema.

El archivo `data.py` define los equipos, sus confederaciones, bombos y los grupos disponibles.

Finalmente, el archivo `main.py` permite ejecutar el programa y visualizar el resultado final del sorteo.

---

## Validación

Para verificar el correcto funcionamiento de la solución, se utilizaron pruebas automatizadas mediante la herramienta `pytest`.

Las pruebas están orientadas a validar tres aspectos principales: el cumplimiento de las restricciones, el funcionamiento correcto de las heurísticas y la capacidad del solver para encontrar una solución válida.

Durante la ejecución de las pruebas, todos los tests fueron superados exitosamente, lo que confirma que la implementación cumple con los requisitos del laboratorio.

---

## Resultados

Al ejecutar el programa, se obtiene una asignación válida de los equipos a los distintos grupos. Cada grupo contiene exactamente cuatro equipos y se respetan todas las restricciones definidas.

Se observa que no existen conflictos entre bombos y que las confederaciones se distribuyen correctamente. En particular, los equipos de UEFA cumplen con la restricción de un máximo de dos por grupo, mientras que el resto de confederaciones no se repiten dentro de un mismo grupo.

Esto demuestra que el modelo CSP implementado es adecuado para resolver este tipo de problemas de asignación.

---

## Conclusiones

Este laboratorio permitió aplicar de forma práctica los conceptos fundamentales de los Problemas de Satisfacción de Restricciones.

Se logró modelar un problema real utilizando variables, dominios y restricciones, y resolverlo mediante técnicas de búsqueda.

El uso de heurísticas como MRV y técnicas de propagación como forward checking resultó clave para mejorar la eficiencia del algoritmo.

El enfoque CSP demostró ser una herramienta efectiva para resolver problemas complejos de asignación con múltiples restricciones.

# Parte 3 — Reporte: Análisis del Caso de Estudio del Grupo K

## 1. Modelado del Problema como CSP

Para modelar el sorteo real de la Copa Mundial 2026 como un Problema de Satisfacción de Restricciones (CSP), se definieron tres componentes fundamentales: variables, dominios y restricciones.

Las variables corresponden a cada uno de los equipos participantes. Cada variable debe ser asignada a un grupo específico entre los doce grupos disponibles (A-L). El dominio de cada variable está compuesto por todos los grupos, aunque este dominio se reduce dinámicamente conforme se aplican restricciones.

Las restricciones principales del problema son las siguientes. Cada grupo puede contener un máximo de cuatro equipos, lo que define la estructura del torneo. Además, no puede haber más de un equipo del mismo bombo dentro de un mismo grupo, asegurando una distribución equilibrada según el ranking. En cuanto a las confederaciones, únicamente se permite un equipo por confederación en cada grupo, con la excepción de UEFA, donde se permite un máximo de dos equipos por grupo.

A partir de la ejecución del algoritmo, se obtiene una tabla de grupos válida donde todas estas restricciones son respetadas. Sin embargo, al analizar los resultados, se identifican ciertos grupos que representan situaciones críticas o potencialmente conflictivas en el modelo, específicamente los grupos K, D e I. Estos grupos son relevantes porque presentan combinaciones que requieren un análisis más profundo para entender cómo las restricciones interactúan entre sí.

---

## 2. El Conflicto

¿Por qué el Grupo K contiene 2 equipos de AFC (Irán + Uzbekistán) sin violar las reglas de la FIFA? ¿Cómo interactúa esto con el Playoff Inter-2?

El Grupo K es considerado un caso de estudio debido a la aparente violación de las restricciones de confederación. En este grupo aparecen Irán y Uzbekistán, ambos pertenecientes a la confederación AFC, lo que en principio contradice la regla de un equipo por confederación.

Sin embargo, esta situación se explica al considerar la naturaleza del equipo "Playoff Inter-2". Este equipo no pertenece inicialmente a una confederación fija, ya que representa un enfrentamiento intercontinental entre distintas regiones. Debido a esta incertidumbre, el sistema de sorteo permite cierta flexibilidad en la asignación, ya que el equipo ganador aún no está definido al momento del sorteo.

En términos del modelo CSP, esto introduce una ambigüedad en la restricción de confederaciones. El Playoff Inter-2 puede representar múltiples posibles confederaciones, lo que permite que el grupo contenga temporalmente combinaciones que, bajo condiciones normales, serían inválidas. De esta manera, el Grupo K no viola realmente las reglas, sino que refleja una condición especial del sistema de sorteo.

---

## 3. La Causa

¿Qué heurística (MRV, LCV, Forward Checking) habría detectado el conflicto anticipadamente? ¿Cómo se refleja esto en la ejecución del algoritmo?

Desde el punto de vista técnico, el conflicto observado en el Grupo K puede analizarse en función del comportamiento de las heurísticas utilizadas en el algoritmo.

La heurística MRV (Minimum Remaining Values) selecciona las variables con menor cantidad de opciones disponibles en su dominio. En este caso, equipos con restricciones más fuertes, como los de ciertas confederaciones, son asignados primero. Esto puede llevar a decisiones tempranas que condicionan fuertemente el resto del proceso.

El forward checking juega un papel aún más importante, ya que reduce los dominios de las variables no asignadas al eliminar opciones inválidas. Sin embargo, en el caso del Playoff Inter-2, esta técnica no puede eliminar completamente las inconsistencias debido a la incertidumbre en su confederación. Esto provoca que algunas configuraciones aparentemente válidas se mantengan durante la búsqueda.

Como resultado, el algoritmo puede avanzar sin detectar inmediatamente el conflicto, ya que desde el punto de vista del dominio, las asignaciones siguen siendo válidas. Esto evidencia una limitación del modelo, donde ciertas restricciones dependen de información futura que no está completamente definida al momento de la asignación.

---

## 4. La Solución IA

¿Cómo resuelve tu implementación de CSP este problema? Incluye pseudocódigo del backtracking con propagación y análisis de complejidad.

La implementación desarrollada resuelve el problema utilizando un enfoque de backtracking con propagación de restricciones. El algoritmo construye la solución de manera incremental, asignando equipos a grupos y verificando en cada paso si las restricciones se mantienen.

El proceso puede describirse mediante el siguiente pseudocódigo:

BACKTRACK(assignment, domains):
    si todas las variables están asignadas:
        retornar assignment

seleccionar variable no asignada usando MRV

para cada valor en el dominio de la variable:
    si la asignación es válida:
        asignar valor
        aplicar forward checking

        si forward checking no falla:
            resultado = BACKTRACK(nueva asignación, nuevos dominios)
            si resultado no es None:
                retornar resultado

        deshacer asignación

retornar None


Este enfoque permite explorar el espacio de soluciones de manera eficiente, descartando tempranamente aquellas ramas que no cumplen con las restricciones.

En términos de complejidad, el backtracking tiene un comportamiento exponencial en el peor de los casos. Sin embargo, el uso de heurísticas como MRV y técnicas como forward checking reduce significativamente el espacio de búsqueda, haciendo viable la resolución del problema en tiempos razonables.

En conclusión, el modelo CSP implementado es capaz de manejar correctamente las restricciones del problema, incluyendo casos especiales como el Grupo K, donde la incertidumbre en la información introduce desafíos adicionales en la validación de las asignaciones.