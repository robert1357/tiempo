import random
import time
import streamlit as st
import plotly.express as px
import pandas as pd
from fpdf import FPDF
from datetime import datetime

def busqueda_lineal(array, numero):
    inicio = time.time()
    iteraciones = 0
    for i in range(len(array)):
        iteraciones += 1
        if array[i] == numero:
            fin = time.time()
            return i, inicio, fin, iteraciones
    fin = time.time()
    return -1, inicio, fin, iteraciones

def generar_pdf(resultados, chart_image):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=16)
    
    ancho_pagina = pdf.w
    pdf.multi_cell(ancho_pagina, 10, txt="Facultad de Ingeniería Estadística e Informática               ", border=0, align='C')
    pdf.set_xy(0, pdf.get_y() + 10)  

    pdf.multi_cell(ancho_pagina, 10, txt="Escuela Profesional de Ingeniería Estadística e Informática", border=0, align='C')
    pdf.set_xy(0, pdf.get_y() + 10)  

    pdf.set_xy((pdf.w - 40) / 2, pdf.get_y())  
    pdf.image('una.png', x=pdf.get_x(), y=pdf.get_y(), w=40)
    pdf.ln(50)
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(ancho_pagina, 10, txt="Lenguajes de Programación I                   ", border=0, align='C')
    pdf.set_xy(0, pdf.get_y() + 10)  

    pdf.set_font("Arial", size=20)
    pdf.multi_cell(ancho_pagina, 10, txt="Evaluación del Código Fuente", border=0, align='C')
    pdf.set_xy(0, pdf.get_y() + 15)  

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(ancho_pagina, 10, txt="Profesor: Fred Torres Cruz", border=0, align='C')
    pdf.set_xy(0, pdf.get_y() + 10)  
    
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(ancho_pagina, 10, txt="Estudiante: Roberth Carlos Gonzales Mauricio", border=0, align='C')
    pdf.set_xy(0, pdf.get_y() + 10)  

    fecha_actual = datetime.now().strftime("%d de %B de %Y")
    pdf.multi_cell(ancho_pagina, 10, txt=f"Fecha: {fecha_actual}", border=0, align='C')
    pdf.set_xy(0, pdf.get_y() + 10)  

    semestre = "3ro B"
    grupo = ""

    pdf.multi_cell(ancho_pagina, 10, txt=f"Semestre: {semestre}  Grupo: {grupo}", border=0, align='C')
    pdf.ln(20)  

    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Búsqueda Lineal - Análisis de Rendimiento", ln=True, align='C')

    pdf.ln(10)
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(60, 10, 'Tamaño del array', 1)
    pdf.cell(60, 10, 'Tiempo total (s)', 1)
    pdf.cell(60, 10, 'Número de iteraciones', 1)
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    for resultado in resultados:
        pdf.cell(60, 10, f"{resultado['Tamaño del array']}", 1)
        pdf.cell(60, 10, f"{resultado['Tiempo total']:.6f}", 1)
        pdf.cell(60, 10, f"{resultado['Número de iteraciones']}", 1)
        pdf.ln(10)

    pdf.add_page()
    pdf.image(chart_image, x=10, y=20, w=190)

    return pdf

def main():
    st.title('Búsqueda Lineal - Análisis de Rendimiento')

    n = st.number_input('Ingrese la cantidad de búsquedas:', min_value=1, step=1, format='%d')

    a = 10
    resultados = []

    for _ in range(n):
        array = [random.randint(0, a) for _ in range(a)]  
        numero_a_buscar = random.randint(0, a)  

        resultado, inicio, fin, iteraciones = busqueda_lineal(array, numero_a_buscar)
        tiempo_total = fin - inicio

        resultados.append({
            'Tamaño del array': a,
            'Tiempo total': tiempo_total,
            'Número de iteraciones': iteraciones
        })

        a += 100  

    if resultados:
        col1, col2, col3 = st.columns(3)
        col1.write("Tamaño del array")
        col2.write("Tiempo total (s)")
        col3.write("Número de iteraciones")

        for resultado in resultados:
            col1, col2, col3 = st.columns(3)
            col1.write(f"{resultado['Tamaño del array']}")
            col2.write(f"{resultado['Tiempo total']:.6f}")
            col3.write(f"{resultado['Número de iteraciones']}")
            st.write("---------------------")

    df = pd.DataFrame(resultados)
    fig = px.line(df, x='Tamaño del array', y='Tiempo total', title='Tiempo total de búsqueda lineal por tamaño de array')
    st.plotly_chart(fig)

    chart_image = "chart.png"
    fig.write_image(chart_image)

    if st.button('Descargar PDF con resultados'):
        pdf = generar_pdf(resultados, chart_image)
        pdf_output = pdf.output(dest='S').encode('latin1')
        st.download_button(label='Descargar PDF', data=pdf_output, file_name='resultados_busqueda_lineal.pdf', mime='application/pdf')

if __name__ == '__main__':
    main()
