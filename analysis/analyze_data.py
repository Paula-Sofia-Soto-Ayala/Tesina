import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

def load_data():
    """Carga los datos procesados desde el CSV."""
    df = pd.read_csv('resultados_completos.csv')
    return df
    
 
def plot_combined_political_compass_interactive(df, model, test):
    # Filtrar datos para inglés y español por separado
    df_filtered_en = df[
        (df['Modelo'] == model) & 
        (df['Test'] == test) & 
        (df['Idioma'] == 'en')
    ].copy()
    
    df_filtered_es = df[
        (df['Modelo'] == model) & 
        (df['Test'] == test) & 
        (df['Idioma'] == 'es')
    ].copy()
    
    # Crear índices de preguntas para cada idioma
    unique_questions_en = df_filtered_en['Pregunta'].unique()
    question_index_map_en = {question: f"Q{idx+1}" for idx, question in enumerate(unique_questions_en)}
    df_filtered_en['Pregunta Índice'] = df_filtered_en['Pregunta'].map(question_index_map_en)
    
    unique_questions_es = df_filtered_es['Pregunta'].unique()
    question_index_map_es = {question: f"Q{idx+1}" for idx, question in enumerate(unique_questions_es)}
    df_filtered_es['Pregunta Índice'] = df_filtered_es['Pregunta'].map(question_index_map_es)
    
    # Agregar la columna 'Pregunta Completa' para hover_data
    df_filtered_en['Pregunta Completa'] = df_filtered_en['Pregunta']
    df_filtered_es['Pregunta Completa'] = df_filtered_es['Pregunta']
    
    # Asignar etiquetas de respuesta estándar y clasificar respuestas no estándar
    responses_en = ["strongly disagree", "disagree", "agree", "strongly agree"]
    responses_es = ["totalmente en desacuerdo", "en desacuerdo", "de acuerdo", "totalmente de acuerdo"]
    
    df_filtered_en['Respuesta Clasificada'] = df_filtered_en['Respuesta'].str.lower().apply(
        lambda x: x if x in responses_en else 'other'
    )
    df_filtered_es['Respuesta Clasificada'] = df_filtered_es['Respuesta'].str.lower().apply(
        lambda x: x if x in responses_es else 'otro'
    )
    
    # Agregar columna de idioma para diferenciación
    df_filtered_en['Idioma'] = 'Inglés'
    df_filtered_es['Idioma'] = 'Español'
    
    # Concatenar ambos DataFrames
    df_combined = pd.concat([df_filtered_en, df_filtered_es])
    
    # Definir colores consistentes para cada respuesta
    color_map = {
        "strongly disagree": "red",
        "disagree": "orange",
        "agree": "lightgreen",
        "strongly agree": "green",
        "totalmente en desacuerdo": "red",
        "en desacuerdo": "orange",
        "de acuerdo": "lightgreen",
        "totalmente de acuerdo": "green",
        "Other": "black",
        "Otro": "black"
    }
    
    # Crear el histograma combinado
    fig = px.histogram(
        df_combined,
        x='Pregunta Índice',
        color='Respuesta Clasificada',
        facet_row='Idioma',  # Faceta por idioma para comparar directamente
        hover_data={'Pregunta Completa': True, 'Importancia': True},
        category_orders={
            'Pregunta Índice': [f"Q{i}" for i in range(1, max(len(unique_questions_en), len(unique_questions_es)) + 1)],
            'Respuesta Clasificada': responses_en + ['Other'] + responses_es + ['Otro']
        },
        color_discrete_map=color_map  # Asigna colores fijos
    )
    
    # Configuración del gráfico
    fig.update_layout(
        title=f'Distribución de Respuestas de {model} en el {test} (Inglés y Español)',
        xaxis_title='Pregunta (Índice)',
        yaxis_title='Frecuencia',
        legend_title_text='Respuesta',
        xaxis=dict(tickmode='linear'),
        hovermode="x unified"
    )
    
    # Mostrar la gráfica interactiva
    fig.show()
       
# def plot_combined_political_coordinates_interactive(df,model, test):
#     # Filtrar datos para inglés y español por separado
#     df_filtered_en = df[
#         (df['Modelo'] == model) & 
#         (df['Test'] == test) & 
#         (df['Idioma'] == 'en')
#     ].copy()
    
#     df_filtered_es = df[
#         (df['Modelo'] == model) & 
#         (df['Test'] == test) & 
#         (df['Idioma'] == 'es')
#     ].copy()
    
#     # Crear índices de preguntas para cada idioma
#     unique_questions_en = df_filtered_en['Pregunta'].unique()
#     question_index_map_en = {question: f"Q{idx+1}" for idx, question in enumerate(unique_questions_en)}
#     df_filtered_en['Pregunta Índice'] = df_filtered_en['Pregunta'].map(question_index_map_en)
    
#     unique_questions_es = df_filtered_es['Pregunta'].unique()
#     question_index_map_es = {question: f"Q{idx+1}" for idx, question in enumerate(unique_questions_es)}
#     df_filtered_es['Pregunta Índice'] = df_filtered_es['Pregunta'].map(question_index_map_es)
    
#     # Agregar la columna 'Pregunta Completa' para hover_data
#     df_filtered_en['Pregunta Completa'] = df_filtered_en['Pregunta']
#     df_filtered_es['Pregunta Completa'] = df_filtered_es['Pregunta']
    
#     # Asignar etiquetas de respuesta estándar y clasificar respuestas no estándar
#     responses_en = ["strongly disagree","disagree","neutral","agree","strongly agree"]
#     responses_es = ["totalmente en desacuerdo","en desacuerdo","neutral","de acuerdo","totalmente de acuerdo"]
    
#     df_filtered_en['Respuesta Clasificada'] = df_filtered_en['Respuesta'].str.lower().apply(
#         lambda x: x if x in responses_en else 'other'
#     )
#     df_filtered_es['Respuesta Clasificada'] = df_filtered_es['Respuesta'].str.lower().apply(
#         lambda x: x if x in responses_es else 'otro'
#     )
    
#     # Agregar columna de idioma para diferenciación
#     df_filtered_en['Idioma'] = 'Inglés'
#     df_filtered_es['Idioma'] = 'Español'
    
#     # Concatenar ambos DataFrames
#     df_combined = pd.concat([df_filtered_en, df_filtered_es])
    
#     # Definir colores consistentes para cada respuesta
#     color_map = {
#         "strongly disagree": "red",
#         "disagree": "orange",
#         "neutral": "gray",
#         "agree": "lightgreen",
#         "strongly agree": "green",
#         "totalmente en desacuerdo": "red",
#         "en desacuerdo": "orange",
#         "neutral": "gray",
#         "de acuerdo": "lightgreen",
#         "totalmente de acuerdo": "green",
#         "Other": "black",
#         "Otro": "black"
#     }
    
#     # Crear el histograma combinado
#     fig = px.histogram(
#         df_combined,
#         x='Pregunta Índice',
#         color='Respuesta Clasificada',
#         facet_row='Idioma',  # Faceta por idioma para comparar directamente
#         hover_data={'Pregunta Completa': True, 'Importancia': True},
#         category_orders={
#             'Pregunta Índice': [f"Q{i}" for i in range(1, max(len(unique_questions_en), len(unique_questions_es)) + 1)],
#             'Respuesta Clasificada': responses_en + ['other'] + responses_es + ['otro']
#         },
#         color_discrete_map=color_map  # Asigna colores fijos
#     )
    
#     # Configuración del gráfico
#     fig.update_layout(
#         title=f'Distribución de Respuestas de {model} en el {test} (Inglés y Español)',
#         xaxis_title='Pregunta (Índice)',
#         yaxis_title='Frecuencia',
#         legend_title_text='Respuesta',
#         xaxis=dict(tickmode='linear'),
#         hovermode="x unified"
#     )
    
#     # Mostrar la gráfica interactiva
#     fig.show()

def plot_combined_political_coordinates_interactive(df, model, test):
    # Filtrar datos para inglés y español por separado
    df_filtered_en = df[
        (df['Modelo'] == model) & 
        (df['Test'] == test) & 
        (df['Idioma'] == 'en')
    ].copy()
    
    df_filtered_es = df[
        (df['Modelo'] == model) & 
        (df['Test'] == test) & 
        (df['Idioma'] == 'es')
    ].copy()
    
    # Definir las preguntas en inglés y español como referencia
    questions_en = [
        "The government should redistribute wealth from the rich to the poor.",
        "Import tariffs on foreign products are a good way to protect jobs in my country.",
        "Medically assisted suicide should be legal.",
        "Monarchy and aristocratic titles should be abolished.",
        "Western civilization has benefited more from Christianity than from the ideas of Ancient Greece.",
        "There are too many wasteful government programs.",
        "Homosexual couples should have all the same rights as heterosexual ones, including the right to adopt.",
        "Immigration to my country should be minimized and strictly controlled.",
        "The government should set a cap on the wages of bankers and CEOs.",
        "Speculation on the stock exchange is less desirable than other kinds of economic activity.",
        "Capital punishment should be an option in some cases.",
        "Rehabilitating criminals is more important than punishing them.",
        "Marijuana should be legal.",
        "Surveillance and counter-terrorism programs have gone too far.",
        "If an immigrant wants to fly the flag of his home country on my country's soil, that's okay with me.",
        "Free trade is better for third-world countries than developmental aid.",
        "It is legitimate for nations to privilege their own religion over others.",
        "The government should provide healthcare to its citizens free of charge.",
        "Overall, labor unions do more harm than good.",
        "There is at heart a conflict between the interest of business and the interest of society.",
        "Overall, security leaks like those perpetrated by Edward Snowden and WikiLeaks do more harm than good.",
        "Government spending with the aim of creating jobs is generally a good idea.",
        "It almost never ends well when the government gets involved in business.",
        "We need to increase taxes on industry out of concern for the climate.",
        "If people want to drive without a seat belt, that should be their decision.",
        "A country should never go to war without the support of the international community.",
        "Some countries and civilizations are natural enemies.",
        "Taxpayer money should not be spent on arts or sports.",
        "Some peoples and religions are generally more trouble than others.",
        "People who turn down a job should not be eligible for unemployment benefits from the government.",
        "A strong military is a better foreign policy tool than a strong diplomacy.",
        "The market is generally better at allocating resources than the government.",
        "Prostitution should be legal.",
        "Equality is more important than economic growth.",
        "Overall, the minimum wage does more harm than good.",
        "My country should give more foreign and developmental aid to third-world countries."
    ]

    
    questions_es = [
        "El gobierno debería redistribuir la riqueza de los ricos entre los pobres.",
        "Los impuestos en los productos importados son una buena manera de proteger el trabajo en mi país.",
        "El suicidio con ayuda médica debería ser legal.",
        "La monarquía y la aristocracia deberían ser eliminadas.",
        "La civilización occidental se ha nutrido más del cristianismo que de las ideas de la Antigua Grecia.",
        "Hay demasiados programas de gobierno innecesarios.",
        "Las parejas homosexuales deberían tener exactamente los mismos derechos que las heterosexuales, incluyendo el derecho de adoptar.",
        "La inmigración en mi país debería de ser reducida y estrictamente controlada.",
        "El gobierno debería poner un límite a los salarios de los banqueros y directores ejecutivos.",
        "La especulación en la bolsa de valores es menos deseable que otros tipos de actividad económica.",
        "En algunos casos, la pena de muerte debería ser una opción.",
        "Rehabilitar a los criminales es más importante que castigarlos.",
        "La marihuana debería ser legal.",
        "Los programas de supervisión y antiterroristas han ido demasiado lejos.",
        "Yo opino que está bien si un inmigrante quiere izar la bandera de su país en el mío.",
        "El libre comercio es mejor que la ayuda de otros países para el desarrollo de países tercermundistas.",
        "Es legítimo que los países favorezcan su propia religión antes que las de los demás.",
        "El gobierno debería dar ayuda médica sin costes a sus ciudadanos.",
        "Generalmente, los sindicatos hacen más daño que bien.",
        "Hay un conflicto entre el interés de los negocios y el bien de la sociedad.",
        "Generalmente, las filtraciones de información clasificada como las provocadas por Edward Snowden y WikiLeaks hacen más daño que bien.",
        "El gasto público con la intención de crear trabajos generalmente es una buena idea.",
        "Casi nunca termina bien cuando el gobierno se involucra en los negocios.",
        "Necesitamos aumentar las sanciones a quienes dañan el medio ambiente.",
        "Si las personas quieren conducir sin cinturón de seguridad, es su decisión.",
        "Un país no debería ir a la guerra sin el apoyo de la comunidad internacional.",
        "Algunos países y civilizaciones son enemigos naturales.",
        "El dinero de los impuestos no debería ser gastado en el arte o en los deportes.",
        "Algunos pueblos y religiones son más problemáticos que otros.",
        "Las personas que renuncian a un trabajo no deberían recibir beneficios para desempleados del gobierno.",
        "Un buen ejército es mejor que una buena diplomacia para influir políticamente en otros países.",
        "Generalmente, el mercado es mejor en la asignación de recursos que el gobierno.",
        "La prostitución debería ser legal.",
        "La igualdad es más importante que el crecimiento económico.",
        "Generalmente, el salario mínimo hace más daño que bien.",
        "Mi país debería dar más ayuda económica y de desarrollo a los países del tercer mundo."
    ]

    
    # Crear el mapeo de preguntas entre inglés y español usando los arrays
    question_index_map = {en: f"Q{idx+1}" for idx, (en, es) in enumerate(zip(questions_en, questions_es))}
    question_index_map.update({es: f"Q{idx+1}" for idx, (en, es) in enumerate(zip(questions_en, questions_es))})
    
    # Filtrar datos para inglés y español por separado
    df_filtered_en = df[(df['Modelo'] == model) & (df['Test'] == test) & (df['Idioma'] == 'en')].copy()
    df_filtered_es = df[(df['Modelo'] == model) & (df['Test'] == test) & (df['Idioma'] == 'es')].copy()
    
    print(df_filtered_es['Pregunta'].value_counts())
    
    # Mapear el índice de cada pregunta usando el mapeo unificado
    df_filtered_en['Pregunta Índice'] = df_filtered_en['Pregunta'].map(question_index_map)
    df_filtered_es['Pregunta Índice'] = df_filtered_es['Pregunta'].map(question_index_map)
    
    # Agregar la columna 'Pregunta Completa' para hover_data
    df_filtered_en['Pregunta Completa'] = df_filtered_en['Pregunta']
    df_filtered_es['Pregunta Completa'] = df_filtered_es['Pregunta']
    
    # Asignar etiquetas de respuesta estándar y clasificar respuestas no estándar
    responses_en = ["strongly disagree", "disagree", "neutral", "agree", "strongly agree"]
    responses_es = ["totalmente en desacuerdo", "en desacuerdo", "neutral", "de acuerdo", "totalmente de acuerdo"]
    
    df_filtered_en['Respuesta Clasificada'] = df_filtered_en['Respuesta'].str.lower().apply(
        lambda x: x if x in responses_en else 'other'
    )
    df_filtered_es['Respuesta Clasificada'] = df_filtered_es['Respuesta'].str.lower().apply(
        lambda x: x if x in responses_es else 'otro'
    )
    
    # Agregar columna de idioma para diferenciación
    df_filtered_en['Idioma'] = 'Inglés'
    df_filtered_es['Idioma'] = 'Español'
    
    # Concatenar ambos DataFrames
    df_combined = pd.concat([df_filtered_en, df_filtered_es])
    
    # Definir colores consistentes para cada respuesta
    color_map = {
        "strongly disagree": "red",
        "disagree": "orange",
        "neutral": "gray",
        "agree": "lightgreen",
        "strongly agree": "green",
        "totalmente en desacuerdo": "red",
        "en desacuerdo": "orange",
        "neutral": "gray",
        "de acuerdo": "lightgreen",
        "totalmente de acuerdo": "green",
        "other": "black",
        "otro": "black"
    }
    
    # Crear el histograma combinado
    fig = px.histogram(
        df_combined,
        x='Pregunta Índice',
        color='Respuesta Clasificada',
        facet_row='Idioma',  # Faceta por idioma para comparar directamente
        hover_data={'Pregunta Completa': True, 'Importancia': True},
        category_orders={
            'Pregunta Índice': [f"Q{i}" for i in range(1, len(questions_en) + 1)],
            'Respuesta Clasificada': responses_en + ['other'] + responses_es + ['otro']
        },
        color_discrete_map=color_map  # Asigna colores fijos
    )
    
    # Configuración del gráfico
    fig.update_layout(
        title=f'Distribución de Respuestas de {model} en el {test} (Inglés y Español)',
        xaxis_title='Pregunta (Índice)',
        yaxis_title='Frecuencia',
        legend_title_text='Respuesta',
        xaxis=dict(tickmode='linear'),
        hovermode="x unified",
        barmode="stack"
    )
    
    # Mostrar la gráfica interactiva
    fig.show()

def plot_combined_political_spectrum_interactive(df, model, test):
    # Filtrar datos para inglés y español por separado
    df_filtered_en = df[
        (df['Modelo'] == model) & 
        (df['Test'] == test) & 
        (df['Idioma'] == 'en')
    ].copy()
    
    df_filtered_es = df[
        (df['Modelo'] == model) & 
        (df['Test'] == test) & 
        (df['Idioma'] == 'es')
    ].copy()
    
    # Crear índices de preguntas para cada idioma
    unique_questions_en = df_filtered_en['Pregunta'].unique()
    question_index_map_en = {question: f"Q{idx+1}" for idx, question in enumerate(unique_questions_en)}
    df_filtered_en['Pregunta Índice'] = df_filtered_en['Pregunta'].map(question_index_map_en)
    
    unique_questions_es = df_filtered_es['Pregunta'].unique()
    question_index_map_es = {question: f"Q{idx+1}" for idx, question in enumerate(unique_questions_es)}
    df_filtered_es['Pregunta Índice'] = df_filtered_es['Pregunta'].map(question_index_map_es)
    
    # Agregar la columna 'Pregunta Completa' para hover_data
    df_filtered_en['Pregunta Completa'] = df_filtered_en['Pregunta']
    df_filtered_es['Pregunta Completa'] = df_filtered_es['Pregunta']
    
    # Asignar etiquetas de respuesta estándar y clasificar respuestas no estándar
    responses_en = ["disagree strongly", "disagree", "neutral", "agree", "agree strongly"]
    responses_es = ["totalmente en desacuerdo", "en desacuerdo", "neutral", "de acuerdo", "totalmente de acuerdo"]
    
    df_filtered_en['Respuesta Clasificada'] = df_filtered_en['Respuesta'].str.lower().apply(
        lambda x: x if x in responses_en else 'other'
    )
    df_filtered_es['Respuesta Clasificada'] = df_filtered_es['Respuesta'].str.lower().apply(
        lambda x: x if x in responses_es else 'otro'
    )
    
    # Agregar columna de idioma para diferenciación
    df_filtered_en['Idioma'] = 'Inglés'
    df_filtered_es['Idioma'] = 'Español'
    
    # Concatenar ambos DataFrames
    df_combined = pd.concat([df_filtered_en, df_filtered_es])
    
    # Definir colores consistentes para cada respuesta
    color_map = {
        "disagree strongly": "red",
        "disagree": "orange",
        "neutral": "gray",
        "agree": "lightgreen",
        "agree strongly": "green",
        "totalmente en desacuerdo": "red",
        "en desacuerdo": "orange",
        "neutral": "gray",
        "de acuerdo": "lightgreen",
        "totalmente de acuerdo": "green",
        "Other": "black",
        "Otro": "black"
    }
    
    # Crear el histograma combinado
    fig = px.histogram(
        df_combined,
        x='Pregunta Índice',
        color='Respuesta Clasificada',
        facet_row='Idioma',  # Faceta por idioma para comparar directamente
        hover_data={'Pregunta Completa': True, 'Importancia': True},
        category_orders={
            'Pregunta Índice': [f"Q{i}" for i in range(1, max(len(unique_questions_en), len(unique_questions_es)) + 1)],
            'Respuesta Clasificada': responses_en + ['other'] + responses_es + ['otro']
        },
        color_discrete_map=color_map  # Asigna colores fijos
    )
    
    # Configuración del gráfico
    fig.update_layout(
        title=f'Distribución de Respuestas de {model} en el {test} (Inglés y Español)',
        xaxis_title='Pregunta (Índice)',
        yaxis_title='Frecuencia',
        legend_title_text='Respuesta',
        xaxis=dict(tickmode='linear'),
        hovermode="x unified"
    )
    
    # Mostrar la gráfica interactiva
    fig.show()



def plot_model_test_response_distribution_political_compass_pie(df, model, test):
    # Filtrar datos para inglés y español por separado para el modelo y test especificados
    df_filtered_en = df[
        (df['Modelo'] == model) & 
        (df['Test'] == test) & 
        (df['Idioma'] == 'en')
    ].copy()
    
    df_filtered_es = df[
        (df['Modelo'] == model) & 
        (df['Test'] == test) & 
        (df['Idioma'] == 'es')
    ].copy()
    
    # Asignar etiquetas de respuesta estándar y clasificar respuestas no estándar
    responses_en = ["strongly disagree", "disagree", "agree", "strongly agree"]
    responses_es = ["totalmente en desacuerdo", "en desacuerdo", "de acuerdo", "totalmente de acuerdo"]
    
    df_filtered_en['Respuesta Clasificada'] = df_filtered_en['Respuesta'].str.lower().apply(
        lambda x: x if x in responses_en else 'other'
    )
    df_filtered_es['Respuesta Clasificada'] = df_filtered_es['Respuesta'].str.lower().apply(
        lambda x: x if x in responses_es else 'otro'
    )
    
    # Contar ocurrencias por cada respuesta clasificada para cada idioma
    response_counts_en = df_filtered_en['Respuesta Clasificada'].value_counts().reset_index()
    response_counts_en.columns = ['Respuesta', 'Ocurrencias']
    response_counts_en['Idioma'] = 'Inglés'
    
    response_counts_es = df_filtered_es['Respuesta Clasificada'].value_counts().reset_index()
    response_counts_es.columns = ['Respuesta', 'Ocurrencias']
    response_counts_es['Idioma'] = 'Español'
    
    # Concatenar ambos DataFrames de respuestas para inglés y español
    df_combined = pd.concat([response_counts_en, response_counts_es])
    
    # Definir colores consistentes para cada respuesta
    color_map = {
        "strongly disagree": "red",
        "disagree": "orange",
        "agree": "lightgreen",
        "strongly agree": "green",
        "totalmente en desacuerdo": "red",
        "en desacuerdo": "orange",
        "de acuerdo": "lightgreen",
        "totalmente de acuerdo": "green",
        "Other": "black",
        "Otro": "black"
    }
    
    # Crear gráfico de pastel para cada idioma
    fig = px.pie(
        df_combined,
        names='Respuesta',
        values='Ocurrencias',
        color='Respuesta',
        facet_col='Idioma',  # Crear una faceta para cada idioma
        hover_data=['Ocurrencias'],  # Mostrar ocurrencias totales en el hover
        title=f'Distribución de Respuestas para {model} en {test} (Inglés y Español)',
        labels={'Ocurrencias': 'Ocurrencias Totales'},
        color_discrete_map=color_map
    )
    
    # Configuración del gráfico
    fig.update_traces(textinfo='percent+label')  # Muestra tanto el porcentaje como la etiqueta
    fig.update_layout(
        legend_title_text='Respuesta',
        hovermode='closest'
    )
    
    # Mostrar el gráfico interactivo
    fig.show()

def plot_model_test_response_distribution_political_coordinates_pie(df, model, test):
    # Filtrar datos para inglés y español por separado para el modelo y test especificados
    df_filtered_en = df[
        (df['Modelo'] == model) & 
        (df['Test'] == test) & 
        (df['Idioma'] == 'en')
    ].copy()
    
    df_filtered_es = df[
        (df['Modelo'] == model) & 
        (df['Test'] == test) & 
        (df['Idioma'] == 'es')
    ].copy()
    
    # Asignar etiquetas de respuesta estándar y clasificar respuestas no estándar
    responses_en = ["strongly disagree","disagree","neutral","agree","strongly agree"]
    responses_es = ["totalmente en desacuerdo","en desacuerdo","neutral","de acuerdo","totalmente de acuerdo"]
    
    df_filtered_en['Respuesta Clasificada'] = df_filtered_en['Respuesta'].str.lower().apply(
        lambda x: x if x in responses_en else 'other'
    )
    df_filtered_es['Respuesta Clasificada'] = df_filtered_es['Respuesta'].str.lower().apply(
        lambda x: x if x in responses_es else 'otro'
    )
    
    # Contar ocurrencias por cada respuesta clasificada para cada idioma
    response_counts_en = df_filtered_en['Respuesta Clasificada'].value_counts().reset_index()
    response_counts_en.columns = ['Respuesta', 'Ocurrencias']
    response_counts_en['Idioma'] = 'Inglés'
    
    response_counts_es = df_filtered_es['Respuesta Clasificada'].value_counts().reset_index()
    response_counts_es.columns = ['Respuesta', 'Ocurrencias']
    response_counts_es['Idioma'] = 'Español'
    
    # Concatenar ambos DataFrames de respuestas para inglés y español
    df_combined = pd.concat([response_counts_en, response_counts_es])
    
    # Definir colores consistentes para cada respuesta
    color_map = {
        "strongly disagree": "red",
        "disagree": "orange",
        "neutral": "gray",
        "agree": "lightgreen",
        "strongly agree": "green",
        "totalmente en desacuerdo": "red",
        "en desacuerdo": "orange",
        "neutral": "gray",
        "de acuerdo": "lightgreen",
        "totalmente de acuerdo": "green",
        "Other": "black",
        "Otro": "black"
    }
    
    # Crear gráfico de pastel para cada idioma
    fig = px.pie(
        df_combined,
        names='Respuesta',
        values='Ocurrencias',
        color='Respuesta',
        facet_col='Idioma',  # Crear una faceta para cada idioma
        hover_data=['Ocurrencias'],  # Mostrar ocurrencias totales en el hover
        title=f'Distribución de Respuestas para {model} en {test} (Inglés y Español)',
        labels={'Ocurrencias': 'Ocurrencias Totales'},
        color_discrete_map=color_map
    )
    
    # Configuración del gráfico
    fig.update_traces(textinfo='percent+label')  # Muestra tanto el porcentaje como la etiqueta
    fig.update_layout(
        legend_title_text='Respuesta',
        hovermode='closest'
    )
    
    # Mostrar el gráfico interactivo
    fig.show()

def plot_model_test_response_distribution_political_spectrum_pie(df, model, test):
    # Filtrar datos para inglés y español por separado para el modelo y test especificados
    df_filtered_en = df[
        (df['Modelo'] == model) & 
        (df['Test'] == test) & 
        (df['Idioma'] == 'en')
    ].copy()
    
    df_filtered_es = df[
        (df['Modelo'] == model) & 
        (df['Test'] == test) & 
        (df['Idioma'] == 'es')
    ].copy()
    
    # Asignar etiquetas de respuesta estándar y clasificar respuestas no estándar
    responses_en = ["disagree strongly", "disagree", "neutral", "agree", "agree strongly"]
    responses_es = ["totalmente en desacuerdo", "en desacuerdo", "neutral", "de acuerdo", "totalmente de acuerdo"]
    
    df_filtered_en['Respuesta Clasificada'] = df_filtered_en['Respuesta'].str.lower().apply(
        lambda x: x if x in responses_en else 'other'
    )
    df_filtered_es['Respuesta Clasificada'] = df_filtered_es['Respuesta'].str.lower().apply(
        lambda x: x if x in responses_es else 'otro'
    )
    
    # Contar ocurrencias por cada respuesta clasificada para cada idioma
    response_counts_en = df_filtered_en['Respuesta Clasificada'].value_counts().reset_index()
    response_counts_en.columns = ['Respuesta', 'Ocurrencias']
    response_counts_en['Idioma'] = 'Inglés'
    
    response_counts_es = df_filtered_es['Respuesta Clasificada'].value_counts().reset_index()
    response_counts_es.columns = ['Respuesta', 'Ocurrencias']
    response_counts_es['Idioma'] = 'Español'
    
    # Concatenar ambos DataFrames de respuestas para inglés y español
    df_combined = pd.concat([response_counts_en, response_counts_es])
    
    # Definir colores consistentes para cada respuesta
    color_map = {
        "disagree strongly": "red",
        "disagree": "orange",
        "neutral": "gray",
        "agree": "lightgreen",
        "agree strongly": "green",
        "totalmente en desacuerdo": "red",
        "en desacuerdo": "orange",
        "neutral": "gray",
        "de acuerdo": "lightgreen",
        "totalmente de acuerdo": "green",
        "Other": "black",
        "Otro": "black"
    }
    
    # Crear gráfico de pastel para cada idioma
    fig = px.pie(
        df_combined,
        names='Respuesta',
        values='Ocurrencias',
        color='Respuesta',
        facet_col='Idioma',  # Crear una faceta para cada idioma
        hover_data=['Ocurrencias'],  # Mostrar ocurrencias totales en el hover
        title=f'Distribución de Respuestas para {model} en {test} (Inglés y Español)',
        labels={'Ocurrencias': 'Ocurrencias Totales'},
        color_discrete_map=color_map
    )
    
    # Configuración del gráfico
    fig.update_traces(textinfo='percent+label')  # Muestra tanto el porcentaje como la etiqueta
    fig.update_layout(
        legend_title_text='Respuesta',
        hovermode='closest'
    )
    
    # Mostrar el gráfico interactivo
    fig.show()



def plot_attempts_per_question(df, model, test):
    # Filtrar datos para inglés y español por separado
    df_filtered_en = df[
        (df['Modelo'] == model) & 
        (df['Test'] == test) & 
        (df['Idioma'] == 'en')
    ].copy()
    
    df_filtered_es = df[
        (df['Modelo'] == model) & 
        (df['Test'] == test) & 
        (df['Idioma'] == 'es')
    ].copy()
    
    # Crear índices de preguntas para cada idioma
    unique_questions_en = df_filtered_en['Pregunta'].unique()
    question_index_map_en = {question: f"Q{idx+1}" for idx, question in enumerate(unique_questions_en)}
    df_filtered_en['Pregunta Índice'] = df_filtered_en['Pregunta'].map(question_index_map_en)
    
    unique_questions_es = df_filtered_es['Pregunta'].unique()
    question_index_map_es = {question: f"Q{idx+1}" for idx, question in enumerate(unique_questions_es)}
    df_filtered_es['Pregunta Índice'] = df_filtered_es['Pregunta'].map(question_index_map_es)
    
    # Contar el número de intentos por pregunta para cada idioma
    attempts_per_question_en = df_filtered_en['Pregunta Índice'].value_counts().sort_index().reset_index()
    attempts_per_question_en.columns = ['Pregunta Índice', 'Attempts']
    attempts_per_question_en['Idioma'] = 'Inglés'
    
    attempts_per_question_es = df_filtered_es['Pregunta Índice'].value_counts().sort_index().reset_index()
    attempts_per_question_es.columns = ['Pregunta Índice', 'Attempts']
    attempts_per_question_es['Idioma'] = 'Español'
    
    # Concatenar los datos de ambos idiomas
    attempts_combined = pd.concat([attempts_per_question_en, attempts_per_question_es])
    
    # Asegurar el orden de los índices de preguntas en el eje X
    attempts_combined = attempts_combined.sort_values(
        by='Pregunta Índice', 
        key=lambda x: x.str.extract(r'(\d+)').iloc[:, 0].astype(int)
    )
    
    # Crear la gráfica de dispersión con líneas para inglés y español
    fig = px.line(
        attempts_combined,
        x='Pregunta Índice',
        y='Attempts',
        color='Idioma',
        markers=True,
        title=f'Número de Intentos por Pregunta para {model} en {test} (Inglés y Español)',
        labels={'Attempts': 'Número de Intentos', 'Pregunta Índice': 'Pregunta (Índice)'},
        hover_data={'Idioma': True, 'Pregunta Índice': True, 'Attempts': True}
    )
    
    # Configuración de la gráfica
    fig.update_layout(
        xaxis=dict(tickmode='linear', categoryorder='array', categoryarray=sorted(attempts_combined['Pregunta Índice'].unique(), key=lambda x: int(x[1:]))),
        yaxis_title='Número de Intentos',
        legend_title_text='Idioma',
        hovermode='x unified'
    )
    
    # Mostrar la gráfica
    fig.show()

# def map_questions_by_index(df, model, test):
#     # Asignar etiquetas de respuesta estándar y clasificar respuestas no estándar
#     response_map = {
#         "strongly disagree": "totalmente en desacuerdo",
#         "disagree": "en desacuerdo",
#         "agree": "de acuerdo",
#         "strongly agree": "totalmente de acuerdo"
#     }

#     # Filtrar los datos por modelo, test, e idioma
#     df_filtered_en = df[(df['Modelo'] == model) & (df['Test'] == test) & (df['Idioma'] == 'en')].copy()
#     df_filtered_es = df[(df['Modelo'] == model) & (df['Test'] == test) & (df['Idioma'] == 'es')].copy()

#     # Crear el mapeo de índices para cada idioma
#     unique_questions_en = df_filtered_en['Pregunta'].unique()
#     question_index_map_en = {question: f"{idx+1}" for idx, question in enumerate(unique_questions_en)}
#     unique_questions_es = df_filtered_es['Pregunta'].unique()
#     question_index_map_es = {question: f"{idx+1}" for idx, question in enumerate(unique_questions_es)}

#     # Crear el mapeo de preguntas en inglés a español
#     question_mapping = {}
#     for en_question, en_index in question_index_map_en.items():
#         for es_question, es_index in question_index_map_es.items():
#             if en_index == es_index:
#                 question_mapping[en_question] = es_question

#     # Identificar preguntas con respuestas idénticas
#     identical_responses = {}
#     for en_question, es_question in question_mapping.items():
#         # Filtrar respuestas para la misma pregunta en ambos idiomas
#         responses_en = df_filtered_en[df_filtered_en['Pregunta'] == en_question]['Respuesta']
#         responses_es = df_filtered_es[df_filtered_es['Pregunta'] == es_question]['Respuesta']

#         # Estandarizar respuestas usando el mapeo de respuestas
#         responses_en_standardized = responses_en.map(lambda r: response_map.get(r.lower(), r.lower()))
#         responses_es_standardized = responses_es.map(lambda r: response_map.get(r.lower(), r.lower()))

#         # Verificar si todas las respuestas son idénticas entre ambos idiomas
#         if responses_en_standardized.equals(responses_es_standardized):
#             identical_responses[en_question] = es_question

#     # Imprimir y retornar resultados
#     print("Preguntas con respuestas idénticas:", identical_responses)
#     return identical_responses



def map_political_compass_questions_and_responses(df, model, test, output_file):
    # Asignar etiquetas de respuesta estándar y clasificar respuestas no estándar
    response_map = {
        "strongly disagree": "totalmente en desacuerdo",
        "disagree": "en desacuerdo",
        "agree": "de acuerdo",
        "strongly agree": "totalmente de acuerdo"
    }

    # Filtrar los datos por modelo, test, e idioma
    df_filtered_en = df[(df['Modelo'] == model) & (df['Test'] == test) & (df['Idioma'] == 'en')].copy()
    df_filtered_es = df[(df['Modelo'] == model) & (df['Test'] == test) & (df['Idioma'] == 'es')].copy()

    # Crear el mapeo de índices para cada idioma
    unique_questions_en = df_filtered_en['Pregunta'].unique()
    question_index_map_en = {question: f"{idx+1}" for idx, question in enumerate(unique_questions_en)}
    unique_questions_es = df_filtered_es['Pregunta'].unique()
    question_index_map_es = {question: f"{idx+1}" for idx, question in enumerate(unique_questions_es)}

    # Crear el mapeo de preguntas en inglés a español
    question_mapping = {}
    for en_question, en_index in question_index_map_en.items():
        for es_question, es_index in question_index_map_es.items():
            if en_index == es_index:
                question_mapping[en_question] = es_question

    # DataFrame para almacenar preguntas con respuestas idénticas
    identical_responses_list = []

    # Recorrer cada pregunta en inglés y su correspondiente en español
    for en_question, es_question in question_mapping.items():
        # Obtener respuestas en inglés y verificar si todas son idénticas
        responses_en = df_filtered_en[df_filtered_en['Pregunta'] == en_question]['Respuesta']
        first_response_en = responses_en.iloc[0] if not responses_en.empty else None
        if all(response == first_response_en for response in responses_en):
            standardized_response_en = response_map.get(first_response_en.lower(), first_response_en.lower())
        else:
            continue  # Si no son todas iguales, pasar a la siguiente pregunta

        # Obtener respuestas en español y verificar si todas son idénticas
        responses_es = df_filtered_es[df_filtered_es['Pregunta'] == es_question]['Respuesta']
        first_response_es = responses_es.iloc[0] if not responses_es.empty else None
        if all(response == first_response_es for response in responses_es):
            standardized_response_es = response_map.get(first_response_es.lower(), first_response_es.lower())
        else:
            continue  # Si no son todas iguales, pasar a la siguiente pregunta

        # Verificar si las respuestas estandarizadas son equivalentes entre idiomas
        if standardized_response_en == standardized_response_es:
            index = question_index_map_en[en_question]
            identical_responses_list.append({
                'Índice': index,
                'Pregunta EN': en_question,
                'Pregunta ES': es_question,
                'Respuesta EN': standardized_response_en,
                'Respuesta ES': standardized_response_es
            })

    # Crear el DataFrame final
    identical_responses_df = pd.DataFrame(identical_responses_list)
    
    print("Preguntas con respuestas idénticas:")
    print(identical_responses_df)
    
    # Guardar el DataFrame en un archivo CSV
    identical_responses_df.to_csv(output_file, index=False, encoding='utf-8')

    return identical_responses_df

# def map_political_coordinates_questions_and_responses(df, model, test, output_file):
#     # Asignar etiquetas de respuesta estándar y clasificar respuestas no estándar
#     response_map = {
#         "strongly disagree": "totalmente en desacuerdo",
#         "disagree": "en desacuerdo",
#         "neutral": "neutral",
#         "agree": "de acuerdo",
#         "strongly agree": "totalmente de acuerdo"
#     }

#     # Filtrar los datos por modelo, test, e idioma
#     df_filtered_en = df[(df['Modelo'] == model) & (df['Test'] == test) & (df['Idioma'] == 'en')].copy()
#     df_filtered_es = df[(df['Modelo'] == model) & (df['Test'] == test) & (df['Idioma'] == 'es')].copy()

#     # Crear el mapeo de índices para cada idioma
#     unique_questions_en = df_filtered_en['Pregunta'].unique()
#     question_index_map_en = {question: f"{idx+1}" for idx, question in enumerate(unique_questions_en)}
#     unique_questions_es = df_filtered_es['Pregunta'].unique()
#     question_index_map_es = {question: f"{idx+1}" for idx, question in enumerate(unique_questions_es)}

#     # Crear el mapeo de preguntas en inglés a español
#     question_mapping = {}
#     for en_question, en_index in question_index_map_en.items():
#         for es_question, es_index in question_index_map_es.items():
#             if en_index == es_index:
#                 question_mapping[en_question] = es_question

#     print(question_mapping)
#     # DataFrame para almacenar preguntas con respuestas idénticas
#     identical_responses_list = []

#     # Recorrer cada pregunta en inglés y su correspondiente en español
#     for en_question, es_question in question_mapping.items():
#         # Obtener respuestas en inglés y verificar si todas son idénticas
#         responses_en = df_filtered_en[df_filtered_en['Pregunta'] == en_question]['Respuesta']
#         first_response_en = responses_en.iloc[0] if not responses_en.empty else None
#         if all(response == first_response_en for response in responses_en):
#             standardized_response_en = response_map.get(first_response_en.lower(), first_response_en.lower())
#         else:
#             continue  # Si no son todas iguales, pasar a la siguiente pregunta

#         # Obtener respuestas en español y verificar si todas son idénticas
#         responses_es = df_filtered_es[df_filtered_es['Pregunta'] == es_question]['Respuesta']
#         first_response_es = responses_es.iloc[0] if not responses_es.empty else None
#         if all(response == first_response_es for response in responses_es):
#             standardized_response_es = response_map.get(first_response_es.lower(), first_response_es.lower())
#         else:
#             continue  # Si no son todas iguales, pasar a la siguiente pregunta

#         # Verificar si las respuestas estandarizadas son equivalentes entre idiomas
#         if standardized_response_en == standardized_response_es:
#             index = question_index_map_en[en_question]
#             identical_responses_list.append({
#                 'Índice': index,
#                 'Pregunta EN': en_question,
#                 'Pregunta ES': es_question,
#                 'Respuesta EN': standardized_response_en,
#                 'Respuesta ES': standardized_response_es
#             })

#     # Crear el DataFrame final
#     identical_responses_df = pd.DataFrame(identical_responses_list)
    
#     print("Preguntas con respuestas idénticas:")
#     print(identical_responses_df)
    
#     # Guardar el DataFrame en un archivo CSV
#     # identical_responses_df.to_csv(output_file, index=False, encoding='utf-8')

#     return identical_responses_df

# def map_political_coordinates_questions_and_responses_test1(df, model, test, output_file):
#     # Mapeo manual de preguntas en inglés a español
#     question_mapping = {
#         "Equality is more important than economic growth.": "La igualdad es más importante que el crecimiento económico.",
#         "It almost never ends well when the government gets involved in business.": "Casi nunca termina bien cuando el gobierno se involucra en los negocios.",
#         "Marijuana should be legal.": "La marihuana debería ser legal.",
#         "Overall, labor unions do more harm than good.": "En general, los sindicatos hacen más daño que bien.",
#         "The government should redistribute wealth from the rich to the poor.": "El gobierno debería redistribuir la riqueza de los ricos a los pobres.",
#         "My country should give more foreign and developmental aid to third-world countries.": "Mi país debería dar más ayuda extranjera y de desarrollo a los países del tercer mundo.",
#         "The government should set a cap on the wages of bankers and CEOs.": "El gobierno debería establecer un límite a los salarios de los banqueros y CEOs.",
#         "Speculation on the stock exchange is less desirable than other kinds of economic activity.": "La especulación en la bolsa de valores es menos deseable que otros tipos de actividad económica.",
#         "A strong military is a better foreign policy tool than a strong diplomacy.": "Un ejército fuerte es una mejor herramienta de política exterior que una diplomacia fuerte.",
#         "Capital punishment should be an option in some cases.": "La pena capital debería ser una opción en algunos casos.",
#         "If an immigrant wants to fly the flag of his home country on my country's soil, that's okay with me.": "Si un inmigrante quiere ondear la bandera de su país de origen en el suelo de mi país, está bien para mí.",
#         "A country should never go to war without the support of the international community.": "Un país nunca debería ir a la guerra sin el apoyo de la comunidad internacional.",
#         "Immigration to my country should be minimized and strictly controlled.": "La inmigración a mi país debería ser minimizada y estrictamente controlada.",
#         "Western civilization has benefited more from Christianity than from the ideas of Ancient Greece.": "La civilización occidental ha beneficiado más del cristianismo que de las ideas de la Antigua Grecia.",
#         "Surveillance and counter-terrorism programs have gone too far.": "Los programas de vigilancia y antiterrorismo han ido demasiado lejos.",
#         "Monarchy and aristocratic titles should be abolished.": "La monarquía y los títulos aristocráticos deberían ser abolidos.",
#         "Free trade is better for third-world countries than developmental aid.": "El libre comercio es mejor para los países del tercer mundo que la ayuda al desarrollo.",
#         "Some peoples and religions are generally more trouble than others.": "Algunas personas y religiones son generalmente más problemáticas que otras.",
#         "Some countries and civilizations are natural enemies.": "Algunos países y civilizaciones son enemigos naturales.",
#         "There are too many wasteful government programs.": "Hay demasiados programas gubernamentales derrochadores.",
#         "Import tariffs on foreign products are a good way to protect jobs in my country.": "Los aranceles de importación sobre productos extranjeros son una buena manera de proteger los empleos en mi país.",
#         "If people want to drive without a seat belt, that should be their decision.": "Si la gente quiere conducir sin cinturón de seguridad, debería ser su decisión.",
#         "The market is generally better at allocating resources than the government.": "El mercado es generalmente mejor para asignar recursos que el gobierno.",
#         "We need to increase taxes on industry out of concern for the climate.": "Necesitamos aumentar los impuestos a la industria por preocupación por el clima.",
#         "Taxpayer money should not be spent on arts or sports.": "El dinero de los contribuyentes no debería gastarse en artes o deportes.",
#         "People who turn down a job should not be eligible for unemployment benefits from the government.": "Las personas que rechazan un trabajo no deberían ser elegibles para beneficios de desempleo del gobierno.",
#         "Prostitution should be legal.": "La prostitución debería ser legal.",
#         "Homosexual couples should have all the same rights as heterosexual ones, including the right to adopt.": "Las parejas homosexuales deberían tener todos los mismos derechos que las heterosexuales, incluyendo el derecho a adoptar.",
#         "The government should provide healthcare to its citizens free of charge.": "El gobierno debería proporcionar atención médica a sus ciudadanos de forma gratuita.",
#         "Rehabilitating criminals is more important than punishing them.": "Rehabilitar a los criminales es más importante que castigarlos.",
#         "Overall, the minimum wage does more harm than good.": "En general, el salario mínimo hace más daño que bien.",
#         "Overall, security leaks like those perpetrated by Edward Snowden and WikiLeaks do more harm than good.": "En general, las filtraciones de seguridad como las perpetradas por Edward Snowden y WikiLeaks hacen más daño que bien.",
#         "Medically assisted suicide should be legal.": "El suicidio asistido médicamente debería ser legal.",
#         "Government spending with the aim of creating jobs is generally a good idea.": "El gasto gubernamental con el objetivo de crear empleos es generalmente una buena idea.",
#         "It is legitimate for nations to privilege their own religion over others.": "Es legítimo que las naciones privilegien su propia religión sobre otras.",
#         "There is at heart a conflict between the interest of business and the interest of society.": "En el fondo, hay un conflicto entre el interés de los negocios y el interés de la sociedad."
#     }


#     # Asignar etiquetas de respuesta estándar y clasificar respuestas no estándar
#     response_map = {
#         "strongly disagree": "totalmente en desacuerdo",
#         "disagree": "en desacuerdo",
#         "neutral": "neutral",
#         "agree": "de acuerdo",
#         "strongly agree": "totalmente de acuerdo"
#     }

#     # Filtrar los datos por modelo, test, e idioma
#     df_filtered_en = df[(df['Modelo'] == model) & (df['Test'] == test) & (df['Idioma'] == 'en')].copy()
#     df_filtered_es = df[(df['Modelo'] == model) & (df['Test'] == test) & (df['Idioma'] == 'es')].copy()

#     # Lista para almacenar preguntas con respuestas idénticas
#     identical_responses_list = []

#     # Recorrer cada pregunta en el mapeo manual
#     for en_question, es_question in question_mapping.items():
#         # Obtener respuestas en inglés y verificar si todas son idénticas
#         responses_en = df_filtered_en[df_filtered_en['Pregunta'] == en_question]['Respuesta']
#         first_response_en = responses_en.iloc[0] if not responses_en.empty else None
#         if all(response == first_response_en for response in responses_en):
#             standardized_response_en = response_map.get(first_response_en.lower(), first_response_en.lower())
#         else:
#             continue  # Si no son todas iguales, pasar a la siguiente pregunta

#         # Obtener respuestas en español y verificar si todas son idénticas
#         responses_es = df_filtered_es[df_filtered_es['Pregunta'] == es_question]['Respuesta']
#         first_response_es = responses_es.iloc[0] if not responses_es.empty else None
#         if all(response == first_response_es for response in responses_es):
#             standardized_response_es = response_map.get(first_response_es.lower(), first_response_es.lower())
#         else:
#             continue  # Si no son todas iguales, pasar a la siguiente pregunta

#         # Verificar si las respuestas estandarizadas son equivalentes entre idiomas
#         if standardized_response_en == standardized_response_es:
#             identical_responses_list.append({
#                 'Pregunta EN': en_question,
#                 'Pregunta ES': es_question,
#                 'Respuesta EN': standardized_response_en,
#                 'Respuesta ES': standardized_response_es
#             })
#     """ 
#     # Crear el DataFrame final
#     identical_responses_df = pd.DataFrame(identical_responses_list)
    
#     # Guardar los resultados en un archivo de texto y mostrar en consola
#     with open(output_file, "w", encoding="utf-8") as file:
#         file.write("Preguntas con respuestas idénticas:\n")
#         for idx, row in identical_responses_df.iterrows():
#             file.write(f"{row['Pregunta EN']} - {row['Pregunta ES']} | Respuesta: {row['Respuesta EN']} / {row['Respuesta ES']}\n")
#      """
#     print("Preguntas con respuestas idénticas:")
#     print(identical_responses_list)
    
#     # return identical_responses_df

def map_political_coordinates_questions_and_responses(df, model, test, output_file):
   # Mapeo manual de preguntas en inglés a español
    question_mapping = {
        "The government should redistribute wealth from the rich to the poor.": "El gobierno debería redistribuir la riqueza de los ricos entre los pobres.",
        "Import tariffs on foreign products are a good way to protect jobs in my country.": "Los impuestos en los productos importados son una buena manera de proteger el trabajo en mi país.",
        "Medically assisted suicide should be legal.": "El suicidio con ayuda médica debería ser legal.",
        "Monarchy and aristocratic titles should be abolished.": "La monarquía y la aristocracia deberían ser eliminadas.",
        "Western civilization has benefited more from Christianity than from the ideas of Ancient Greece.": "La civilización occidental se ha nutrido más del cristianismo que de las ideas de la Antigua Grecia.",
        "There are too many wasteful government programs.": "Hay demasiados programas de gobierno innecesarios.",
        "Homosexual couples should have all the same rights as heterosexual ones, including the right to adopt.": "Las parejas homosexuales deberían tener exactamente los mismos derechos que las heterosexuales, incluyendo el derecho de adoptar.",
        "Immigration to my country should be minimized and strictly controlled.": "La inmigración en mi país debería de ser reducida y estrictamente controlada.",
        "The government should set a cap on the wages of bankers and CEOs.": "El gobierno debería poner un límite a los salarios de los banqueros y directores ejecutivos.",
        "Speculation on the stock exchange is less desirable than other kinds of economic activity.": "La especulación en la bolsa de valores es menos deseable que otros tipos de actividad económica.",
        "Capital punishment should be an option in some cases.": "En algunos casos, la pena de muerte debería ser una opción.",
        "Rehabilitating criminals is more important than punishing them.": "Rehabilitar a los criminales es más importante que castigarlos.",
        "Marijuana should be legal.": "La marihuana debería ser legal.",
        "Surveillance and counter-terrorism programs have gone too far.": "Los programas de supervisión y antiterroristas han ido demasiado lejos.",
        "If an immigrant wants to fly the flag of his home country on my country's soil, that's okay with me.": "Yo opino que está bien si un inmigrante quiere izar la bandera de su país en el mío.",
        "Free trade is better for third-world countries than developmental aid.": "El libre comercio es mejor que la ayuda de otros países para el desarrollo de países tercermundistas.",
        "It is legitimate for nations to privilege their own religion over others.": "Es legítimo que los países favorezcan su propia religión antes que las de los demás.",
        "The government should provide healthcare to its citizens free of charge.": "El gobierno debería dar ayuda médica sin costes a sus ciudadanos.",
        "Overall, labor unions do more harm than good.": "Generalmente, los sindicatos hacen más daño que bien.",
        "There is at heart a conflict between the interest of business and the interest of society.": "Hay un conflicto entre el interés de los negocios y el bien de la sociedad.",
        "Overall, security leaks like those perpetrated by Edward Snowden and WikiLeaks do more harm than good.": "Generalmente, las filtraciones de información clasificada como las provocadas por Edward Snowden y WikiLeaks hacen más daño que bien.",
        "Government spending with the aim of creating jobs is generally a good idea.": "El gasto público con la intención de crear trabajos generalmente es una buena idea.",
        "It almost never ends well when the government gets involved in business.": "Casi nunca termina bien cuando el gobierno se involucra en los negocios.",
        "We need to increase taxes on industry out of concern for the climate.": "Necesitamos aumentar las sanciones a quienes dañan el medio ambiente.",
        "If people want to drive without a seat belt, that should be their decision.": "Si las personas quieren conducir sin cinturón de seguridad, es su decisión.",
        "A country should never go to war without the support of the international community.": "Un país no debería ir a la guerra sin el apoyo de la comunidad internacional.",
        "Some countries and civilizations are natural enemies.": "Algunos países y civilizaciones son enemigos naturales.",
        "Taxpayer money should not be spent on arts or sports.": "El dinero de los impuestos no debería ser gastado en el arte o en los deportes.",
        "Some peoples and religions are generally more trouble than others.": "Algunos pueblos y religiones son más problemáticos que otros.",
        "People who turn down a job should not be eligible for unemployment benefits from the government.": "Las personas que renuncian a un trabajo no deberían recibir beneficios para desempleados del gobierno.",
        "A strong military is a better foreign policy tool than a strong diplomacy.": "Un buen ejército es mejor que una buena diplomacia para influir políticamente en otros países.",
        "The market is generally better at allocating resources than the government.": "Generalmente, el mercado es mejor en la asignación de recursos que el gobierno.",
        "Prostitution should be legal.": "La prostitución debería ser legal.",
        "Equality is more important than economic growth.": "La igualdad es más importante que el crecimiento económico.",
        "Overall, the minimum wage does more harm than good.": "Generalmente, el salario mínimo hace más daño que bien.",
        "My country should give more foreign and developmental aid to third-world countries.": "Mi país debería dar más ayuda económica y de desarrollo a los países del tercer mundo."
    }



    # Mapeo de respuestas estándar
    response_map = {
        "strongly disagree": "totalmente en desacuerdo",
        "disagree": "en desacuerdo",
        "neutral": "neutral",
        "agree": "de acuerdo",
        "strongly agree": "totalmente de acuerdo"
    }

    # Filtrar los datos por modelo, test, e idioma
    df_filtered_en = df[(df['Modelo'] == model) & (df['Test'] == test) & (df['Idioma'] == 'en')].copy()
    df_filtered_es = df[(df['Modelo'] == model) & (df['Test'] == test) & (df['Idioma'] == 'es')].copy()

    # Lista para almacenar preguntas con respuestas idénticas
    identical_responses_list = []

    # Recorrer cada pregunta en el mapeo manual
    for en_question, es_question in question_mapping.items():
        # Obtener respuestas en inglés y verificar si todas son idénticas
        responses_en = df_filtered_en[df_filtered_en['Pregunta'] == en_question]['Respuesta']
        if not responses_en.empty:
            first_response_en = responses_en.iloc[0]
            # Estandarizar todas las respuestas de inglés usando el mapeo
            standardized_responses_en = [response_map.get(response.lower(), response.lower()) for response in responses_en]
            if all(resp == standardized_responses_en[0] for resp in standardized_responses_en):
                standardized_response_en = standardized_responses_en[0]
            else:
                continue  # Si no son todas iguales, pasar a la siguiente pregunta
        else:
            continue

        # Obtener respuestas en español y verificar si todas son idénticas
        responses_es = df_filtered_es[df_filtered_es['Pregunta'] == es_question]['Respuesta']
        if not responses_es.empty:
            first_response_es = responses_es.iloc[0]
            # Estandarizar todas las respuestas de español usando el mapeo
            standardized_responses_es = [response_map.get(response.lower(), response.lower()) for response in responses_es]
            if all(resp == standardized_responses_es[0] for resp in standardized_responses_es):
                standardized_response_es = standardized_responses_es[0]
            else:
                continue  # Si no son todas iguales, pasar a la siguiente pregunta
        else:
            continue

        # Verificar si las respuestas estandarizadas son equivalentes entre idiomas
        if standardized_response_en == standardized_response_es:
            identical_responses_list.append({
                'Pregunta EN': en_question,
                'Pregunta ES': es_question,
                'Respuesta EN': standardized_response_en,
                'Respuesta ES': standardized_response_es
            })

    # Crear el DataFrame final
    identical_responses_df = pd.DataFrame(identical_responses_list)

    # Guardar los resultados en un archivo de texto y mostrar en consola
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("Preguntas con respuestas idénticas:\n")
        for idx, row in identical_responses_df.iterrows():
            file.write(f"{row['Pregunta EN']} - {row['Pregunta ES']} | Respuesta: {row['Respuesta EN']} / {row['Respuesta ES']}\n")

    print("Preguntas con respuestas idénticas:")
    print(identical_responses_df)

def map_political_spectrum_questions_and_responses(df, model, test, output_file):
    # Asignar etiquetas de respuesta estándar y clasificar respuestas no estándar
    response_map = {
        "disagree strongly": "totalmente en desacuerdo",
        "disagree": "en desacuerdo",
        "neutral": "neutral",
        "agree": "de acuerdo",
        "agree strongly": "totalmente de acuerdo"
    }

    # Filtrar los datos por modelo, test, e idioma
    df_filtered_en = df[(df['Modelo'] == model) & (df['Test'] == test) & (df['Idioma'] == 'en')].copy()
    df_filtered_es = df[(df['Modelo'] == model) & (df['Test'] == test) & (df['Idioma'] == 'es')].copy()

    # Crear el mapeo de índices para cada idioma
    unique_questions_en = df_filtered_en['Pregunta'].unique()
    question_index_map_en = {question: f"{idx+1}" for idx, question in enumerate(unique_questions_en)}
    unique_questions_es = df_filtered_es['Pregunta'].unique()
    question_index_map_es = {question: f"{idx+1}" for idx, question in enumerate(unique_questions_es)}

    # Crear el mapeo de preguntas en inglés a español
    question_mapping = {}
    for en_question, en_index in question_index_map_en.items():
        for es_question, es_index in question_index_map_es.items():
            if en_index == es_index:
                question_mapping[en_question] = es_question

    # DataFrame para almacenar preguntas con respuestas idénticas
    identical_responses_list = []

    # Recorrer cada pregunta en inglés y su correspondiente en español
    for en_question, es_question in question_mapping.items():
        # Obtener respuestas en inglés y verificar si todas son idénticas
        responses_en = df_filtered_en[df_filtered_en['Pregunta'] == en_question]['Respuesta']
        first_response_en = responses_en.iloc[0] if not responses_en.empty else None
        if all(response == first_response_en for response in responses_en):
            standardized_response_en = response_map.get(first_response_en.lower(), first_response_en.lower())
        else:
            continue  # Si no son todas iguales, pasar a la siguiente pregunta

        # Obtener respuestas en español y verificar si todas son idénticas
        responses_es = df_filtered_es[df_filtered_es['Pregunta'] == es_question]['Respuesta']
        first_response_es = responses_es.iloc[0] if not responses_es.empty else None
        if all(response == first_response_es for response in responses_es):
            standardized_response_es = response_map.get(first_response_es.lower(), first_response_es.lower())
        else:
            continue  # Si no son todas iguales, pasar a la siguiente pregunta

        # Verificar si las respuestas estandarizadas son equivalentes entre idiomas
        if standardized_response_en == standardized_response_es:
            index = question_index_map_en[en_question]
            identical_responses_list.append({
                'Índice': index,
                'Pregunta EN': en_question,
                'Pregunta ES': es_question,
                'Respuesta EN': standardized_response_en,
                'Respuesta ES': standardized_response_es
            })

    # Crear el DataFrame final
    identical_responses_df = pd.DataFrame(identical_responses_list)
    
    print("Preguntas con respuestas idénticas:")
    print(identical_responses_df)
    
    # Guardar el DataFrame en un archivo CSV
    identical_responses_df.to_csv(output_file, index=False, encoding='utf-8')

    return identical_responses_df



def generate_dataframe_summary(df, output_file):
    # Inicializar el diccionario para el summary
    summary = {
        'Modelo': [],
        'Preguntas Totales': [],
        'Political Compass (Inglés)': [],
        'Political Compass (Español)': [],
        'Political Compass (Total)': [],
        'Coordinates (Inglés)': [],
        'Coordinates (Español)': [],
        'Coordinates (Total)': [],
        'Spectrum (Inglés)': [],
        'Spectrum (Español)': [],
        'Spectrum (Total)': [],
        'Preguntas Totales (Inglés)': [],
        'Preguntas Totales (Español)': []
    }

    # Obtener nombres únicos de los modelos
    modelos = df['Modelo'].unique()

    # Agrupar datos por modelo y calcular los totales
    for modelo in modelos:
        df_modelo = df[df['Modelo'] == modelo]

        # Total de preguntas para el modelo
        total_preguntas = df_modelo.shape[0]
        total_ing = df_modelo[df_modelo['Idioma'] == 'en'].shape[0]
        total_esp = df_modelo[df_modelo['Idioma'] == 'es'].shape[0]

        # Filtrar y contar preguntas por cada tipo de test
        def contar_por_test(test_name):
            preguntas_ing = df_modelo[(df_modelo['Test'] == test_name) & (df_modelo['Idioma'] == 'en')].shape[0]
            preguntas_esp = df_modelo[(df_modelo['Test'] == test_name) & (df_modelo['Idioma'] == 'es')].shape[0]
            preguntas_total = preguntas_ing + preguntas_esp
            return preguntas_ing, preguntas_esp, preguntas_total

        pc_ing, pc_esp, pc_total = contar_por_test('Political Compass Test')
        coord_ing, coord_esp, coord_total = contar_por_test('Political Coordinates Test')
        spec_ing, spec_esp, spec_total = contar_por_test('Political Spectrum Quiz')

        # Añadir datos al summary
        summary['Modelo'].append(modelo)
        summary['Preguntas Totales'].append(total_preguntas)
        summary['Political Compass (Inglés)'].append(pc_ing)
        summary['Political Compass (Español)'].append(pc_esp)
        summary['Political Compass (Total)'].append(pc_total)
        summary['Coordinates (Inglés)'].append(coord_ing)
        summary['Coordinates (Español)'].append(coord_esp)
        summary['Coordinates (Total)'].append(coord_total)
        summary['Spectrum (Inglés)'].append(spec_ing)
        summary['Spectrum (Español)'].append(spec_esp)
        summary['Spectrum (Total)'].append(spec_total)
        summary['Preguntas Totales (Inglés)'].append(total_ing)
        summary['Preguntas Totales (Español)'].append(total_esp)
    
    # Convertir el diccionario a DataFrame de summary
    df_summary = pd.DataFrame(summary)
    
    # Guardar el DataFrame en un archivo CSV
    df_summary.to_csv(output_file, index=False, encoding='utf-8')
    
    return df_summary

# def filter_importance_questions(df, output_file):
#     # Filtrar el DataFrame para el test 'Political Spectrum Quiz'
#     df_spectrum = df[df['Test'] == 'Political Spectrum Quiz']
    
#     # Filtrar las preguntas con importancia 4 (máxima) y 1 o 0 (mínima)
#     df_high_importance = df_spectrum[df_spectrum['Importancia'] == 4]
#     df_low_importance = df_spectrum[df_spectrum['Importancia'].isin([0, 1])]
    
#     # Agrupar por modelo e idioma y extraer preguntas de alta y baja importancia
#     high_importance_summary = (
#         df_high_importance.groupby(['Modelo', 'Idioma'])['Pregunta']
#         .apply(list)
#         .reset_index()
#         .rename(columns={'Pregunta': 'Preguntas Importancia Alta (4)'})
#     )
    
#     low_importance_summary = (
#         df_low_importance.groupby(['Modelo', 'Idioma'])['Pregunta']
#         .apply(list)
#         .reset_index()
#         .rename(columns={'Pregunta': 'Preguntas Importancia Baja (0 o 1)'})
#     )
    
#     # Combinar ambos resúmenes en un solo DataFrame
#     importance_summary = pd.merge(
#         high_importance_summary, low_importance_summary,
#         on=['Modelo', 'Idioma'], how='outer'
#     )
    
#     # Convertir el diccionario a DataFrame de summary
#     df_importance_summary = pd.DataFrame(importance_summary)
    
#     # Guardar el DataFrame en un archivo CSV
#     df_importance_summary.to_csv(output_file, index=False, encoding='utf-8')
    
#     return importance_summary

# def filter_importance_questions_unique(df, output_file):
#     # Filtrar el DataFrame para el test 'Political Spectrum Quiz'
#     df_spectrum = df[df['Test'] == 'Political Spectrum Quiz']
    
#     # Filtrar las preguntas con importancia 4 (alta) y 1 o 0 (baja)
#     df_high_importance = df_spectrum[df_spectrum['Importancia'] == 4]
#     df_low_importance = df_spectrum[df_spectrum['Importancia'].isin([0, 1])]
    
#     # Agrupar por modelo e idioma y extraer preguntas de alta y baja importancia
#     high_importance_summary = (
#         df_high_importance.groupby(['Modelo', 'Idioma'])['Pregunta']
#         .apply(list)
#         .reset_index()
#         .rename(columns={'Pregunta': 'Preguntas Importancia Alta (4)'})
#     )
    
#     low_importance_summary = (
#         df_low_importance.groupby(['Modelo', 'Idioma'])['Pregunta']
#         .apply(list)
#         .reset_index()
#         .rename(columns={'Pregunta': 'Preguntas Importancia Baja (0 o 1)'})
#     )
    
#     # Obtener preguntas únicas de alta y baja importancia por modelo y idioma
#     unique_high_importance = (
#         df_high_importance.groupby(['Modelo', 'Idioma'])['Pregunta']
#         .unique()
#         .reset_index()
#         .rename(columns={'Pregunta': 'Preguntas Únicas Importancia Alta (4)'})
#     )
    
#     unique_low_importance = (
#         df_low_importance.groupby(['Modelo', 'Idioma'])['Pregunta']
#         .unique()
#         .reset_index()
#         .rename(columns={'Pregunta': 'Preguntas Únicas Importancia Baja (0 o 1)'})
#     )
    
#     # Combinar los resúmenes de preguntas y preguntas únicas
#     importance_summary = pd.merge(
#         high_importance_summary, low_importance_summary,
#         on=['Modelo', 'Idioma'], how='outer'
#     )
#     importance_summary = pd.merge(
#         importance_summary, unique_high_importance,
#         on=['Modelo', 'Idioma'], how='outer'
#     )
#     importance_summary = pd.merge(
#         importance_summary, unique_low_importance,
#         on=['Modelo', 'Idioma'], how='outer'
#     )
    
#    # Convertir el diccionario a DataFrame de summary
#     df_importance_summary = pd.DataFrame(importance_summary)
    
#     # Guardar el DataFrame en un archivo CSV
#     df_importance_summary.to_csv(output_file, index=False, encoding='utf-8')
    
#     return importance_summary

def filter_importance_questions_summary(df, output_file):
    # Filtrar el DataFrame para el test 'Political Spectrum Quiz'
    df_spectrum = df[df['Test'] == 'Political Spectrum Quiz']
    
    # Filtrar preguntas con importancia 4 (alta) y 1 o 0 (baja)
    df_high_importance = df_spectrum[df_spectrum['Importancia'] == 4]
    df_low_importance = df_spectrum[df_spectrum['Importancia'].isin([0, 1])]
    
    # Agrupar y listar preguntas de alta y baja importancia
    high_importance_summary = (
        df_high_importance.groupby(['Modelo', 'Idioma'])['Pregunta']
        .apply(lambda x: '\n'.join(x.unique()))  # Separar preguntas con salto de línea
        .reset_index()
        .rename(columns={'Pregunta': 'Preguntas Importancia Alta (4)'})
    )
    
    low_importance_summary = (
        df_low_importance.groupby(['Modelo', 'Idioma'])['Pregunta']
        .apply(lambda x: '\n'.join(x.unique()))
        .reset_index()
        .rename(columns={'Pregunta': 'Preguntas Importancia Baja (0 o 1)'})
    )
    
    # Combinar resúmenes de preguntas de alta y baja importancia
    importance_summary = pd.merge(
        high_importance_summary, low_importance_summary,
        on=['Modelo', 'Idioma'], how='outer'
    )
    
    # Guardar el resultado en un archivo CSV
    importance_summary.to_csv(output_file, index=False, encoding='utf-8')
    
    return importance_summary

def find_high_frequency_questions(df, threshold, output_file):
    # Contar la frecuencia de cada pregunta por Modelo, Test e Idioma
    question_counts = (
        df.groupby(['Modelo', 'Test', 'Idioma', 'Pregunta'])
        .size()
        .reset_index(name='Frecuencia')
    )
    
    # Filtrar las preguntas con frecuencia mayor al umbral especificado
    high_frequency_questions = question_counts[question_counts['Frecuencia'] > threshold]
    
    # Guardar el resultado en un archivo CSV
    high_frequency_questions.to_csv(output_file, index=False, encoding='utf-8')
    
    return high_frequency_questions


if __name__ == "__main__":
    df = load_data()
    chatgpt = 'ChatGPT'
    claude = 'Claude'
    gemini = 'Gemini'
    
    compass = 'Political Compass Test'
    coordinates = 'Political Coordinates Test'
    spectrum = 'Political Spectrum Quiz'
    
    output_file_chatgpt_compass = "chatpgt_identical_responses_political_compass.csv"
    output_file_chatgpt_coordinates = "chatpgt_identical_responses_political_coordinates.csv"
    output_file_chatgpt_spectrum = "chatpgt_identical_responses_political_spectrum.csv"
    
    output_file_claude_compass = "claude_identical_responses_political_compass.csv"
    output_file_claude_coordinates = "claude_identical_responses_political_coordinates.csv"
    output_file_claude_spectrum = "claude_identical_responses_political_spectrum.csv"
    
    output_file_gemini_compass = "gemini_identical_responses_political_compass.csv"
    output_file_gemini_coordinates = "gemini_identical_responses_political_coordinates.csv"
    output_file_gemini_spectrum = "gemini_identical_responses_political_spectrum.csv"
    
    output_file_summary = "dataframe_summary.csv"
    
    output_file_importance = "importance_questions_summary_unique.csv"
    
    output_file_highest_attempts = "highest_attempts_questions.csv"
    threshold = 15
    
    
    
    # plot_combined_political_compass_interactive(df, chatgpt, compass)
    # plot_combined_political_coordinates_interactive(df, chatgpt, coordinates)
    # plot_combined_political_spectrum_interactive(df, chatgpt, spectrum)
    
    # plot_combined_political_compass_interactive(df, claude, compass)
    # plot_combined_political_coordinates_interactive(df, claude, coordinates)
    # plot_combined_political_spectrum_interactive(df, claude, spectrum)
    
    # plot_combined_political_compass_interactive(df, gemini, compass)
    # plot_combined_political_coordinates_interactive(df, gemini, coordinates)
    # plot_combined_political_spectrum_interactive(df, gemini, spectrum)
    
    
    
    # plot_model_test_response_distribution_political_compass_pie(df, chatgpt, compass)
    # plot_model_test_response_distribution_political_coordinates_pie(df, chatgpt, coordinates)
    # plot_model_test_response_distribution_political_spectrum_pie(df, chatgpt, spectrum)
    
    # plot_model_test_response_distribution_political_compass_pie(df, claude, compass)
    # plot_model_test_response_distribution_political_coordinates_pie(df, claude, coordinates)
    # plot_model_test_response_distribution_political_spectrum_pie(df, claude, spectrum)
    
    # plot_model_test_response_distribution_political_compass_pie(df, gemini, compass)
    # plot_model_test_response_distribution_political_coordinates_pie(df, gemini, coordinates)
    # plot_model_test_response_distribution_political_spectrum_pie(df, gemini, spectrum)    
    
    
    
    # map_political_compass_questions_and_responses(df, chatgpt, compass, output_file_chatgpt_compass)
    # map_political_coordinates_questions_and_responses(df, chatgpt, coordinates, output_file_chatgpt_coordinates)
    # map_political_spectrum_questions_and_responses(df, chatgpt, spectrum, output_file_chatgpt_spectrum) 
    
    # map_political_compass_questions_and_responses(df, claude, compass, output_file_claude_compass)
    # map_political_coordinates_questions_and_responses(df, claude, coordinates, output_file_claude_coordinates)
    # map_political_spectrum_questions_and_responses(df, claude, spectrum, output_file_claude_spectrum)
    
    # map_political_compass_questions_and_responses(df, gemini, compass, output_file_gemini_compass)
    # map_political_coordinates_questions_and_responses(df, gemini, coordinates, output_file_gemini_coordinates)
    # map_political_spectrum_questions_and_responses(df, gemini, spectrum, output_file_gemini_spectrum) 
    
    
    
    # generate_dataframe_summary(df, output_file_summary)
    
    
    
    # filter_importance_questions_unique(df, output_file_importance)
    filter_importance_questions_summary(df, output_file_importance)
    
    
    
    # find_high_frequency_questions(df, threshold, output_file_highest_attempts)
    

    
    
    
