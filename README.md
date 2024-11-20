# Tesina

# Tesis: Orientación Política en Modelos de Lenguaje  
**Un enfoque comparativo en español e inglés**  

Este proyecto explora las tendencias de orientación política en modelos de lenguaje (ChatGPT[gpt-4o-mini], Claude[claude-3-haiku-20240307]
 y Gemini[gemini-1.5-flash]) mediante el análisis de sus respuestas a tres pruebas de orientación política, en inglés y español.  


## Instalación  

### Clona este repositorio:  
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd Tesina
   ```

## Instalación de dependencias
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

### Pruebas automatizadas
   ```bash
   python main.py
   ```

### Generar/actualizar el dataframe
   ```bash
   cd .\analysis\
   python process_tests.py
   ```

### Generar gráficas
   ```bash
   cd .\analysis\
   python analyze_data.py
   ```


