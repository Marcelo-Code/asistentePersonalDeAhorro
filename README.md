# Asistente Personal de Ahorros

## Problema

Muchas personas enfrentan dificultades para administrar sus finanzas de manera efectiva, lo que a menudo resulta en la incapacidad de ahorrar. La falta de conocimiento sobre cómo crear un presupuesto adecuado, junto con la tendencia a gastar más de lo planeado, puede generar estrés y preocupación financiera. Esta situación es especialmente crítica para aquellos que desean alcanzar metas de ahorro específicas, como un viaje o un fondo de emergencia, pero no saben por dónde empezar. El problema es significativo, ya que en un mundo donde las finanzas personales son cada vez más complejas, es esencial que las personas cuenten con herramientas que les ayuden a tomar el control de sus gastos y fomentar hábitos de ahorro saludables.

## Solución

Este proyecto proporciona una herramienta para ayudar a los usuarios a administrar sus finanzas personales de manera efectiva. Ofrece funciones como:

- Creación y seguimiento de presupuestos
- Monitoreo de gastos
- Establecimiento de metas de ahorro
- Información y recomendaciones financieras

## Cómo ejecutar el proyecto

1.  Asegúrese de tener Python instalado (versión 3.7 o superior).
2.  Instale las dependencias necesarias:

    pip install -r requirements.txt

3.  Ejecute la aplicación Streamlit:

    streamlit run app.py

## Cómo utilizar la aplicación

Esta aplicación te ayuda a gestionar tus finanzas personales y alcanzar tus metas de ahorro. A continuación, se explica cómo funciona cada sección:

### Selección de Idioma

En la barra lateral izquierda, puedes seleccionar el idioma de la aplicación (English o Español).

### Pestaña 'Meta de Ahorro'

En esta pestaña, puedes establecer tu meta de ahorro y el plazo en el que deseas alcanzarla. También debes ingresar tu ingreso mensual.

-   **Ingrese su meta de ahorro:** Ingresa la cantidad total que deseas ahorrar.
-   **Ingrese el plazo en meses:** Ingresa el número de meses en los que deseas alcanzar tu meta de ahorro.
-   **Ingrese su ingreso mensual:** Ingresa tu ingreso mensual neto (después de impuestos).

### Pestaña 'Gastos'

En esta pestaña, puedes registrar tus gastos diarios.

-   **Seleccione una fecha:** Selecciona la fecha para la que deseas registrar los gastos.
-   **Categoría de Gasto:** Selecciona la categoría del gasto (Comida, Transporte, Vivienda, Entretenimiento, Servicios Públicos, Compras, Otro).
-   **Monto del Gasto:** Ingresa el monto del gasto.
-   **Agregar Gasto:** Haz clic en este botón para agregar el gasto a la lista de gastos diarios.

Debajo del formulario, verás una lista de los gastos registrados para la fecha seleccionada.

#### Gráfico de Pareto de Gastos por Fecha

Este gráfico muestra los gastos por fecha, ordenados de mayor a menor. La línea roja representa el porcentaje acumulado de los gastos.

#### Gráfico de Gastos por Categoría

Este gráfico muestra la distribución de los gastos por categoría.

### Pestaña 'Estrategias'

En esta pestaña, se muestran estrategias de ahorro personalizadas, basadas en tus ingresos y gastos. Estas estrategias son generadas por un modelo de inteligencia artificial.

### Comandos

La aplicación no utiliza comandos directamente. La interacción se realiza a través de la interfaz gráfica.
