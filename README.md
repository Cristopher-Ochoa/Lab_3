Informe de Análisis de Señal EMG
Este informe presenta el análisis de una señal EMG (Electromiografía) simulada, que incluye:

Generación de la señal con contracción muscular en el brazo.
Aplicación de un filtro pasa-bajas para eliminar el ruido de alta frecuencia.
Aplicación de una ventana de Hamming para mejorar el análisis en el dominio de la frecuencia.
Transformada de Fourier para observar las frecuencias dominantes.
Análisis estadístico utilizando un test t para comparar la media de las frecuencias entre reposo y contracción muscular.
Tabla de contenido
Descripción del problema
Generación de la señal EMG
Filtro y ventana
Transformada de Fourier
Análisis estadístico
Conclusiones
Anexos
Descripción del problema
Se requiere simular una señal EMG para un músculo del brazo, en este caso el bíceps, que presente una contracción entre los segundos 2 y 3. A partir de la señal, se aplica un análisis que incluye:

Filtrado de la señal.
Aplicación de una ventana de Hamming.
Análisis en el dominio de la frecuencia mediante Transformada de Fourier (FFT).
Análisis estadístico para determinar si existe una diferencia significativa en las frecuencias medias entre la señal en reposo y durante la contracción.
Generación de la señal EMG
La señal EMG simulada tiene las siguientes características:

Frecuencia de muestreo: 1000 Hz.
Duración: 5 segundos.
Periodo de contracción: entre 2 y 3 segundos.
Se utiliza una señal aleatoria para simular el ruido en reposo y se aumenta la amplitud durante la contracción para simular la activación muscular.

El código para generar la señal EMG es el siguiente:

python
Copiar código
import numpy as np

fs = 1000  # Frecuencia de muestreo en Hz
tiempo_total = 5  # Duración total de la señal en segundos
t = np.linspace(0, tiempo_total, fs * tiempo_total)  # Tiempo de muestreo
reposo = np.random.normal(0, 0.1, len(t))  # Ruido en reposo
contraccion = np.random.normal(0, 0.5, len(t))  # Ruido con contracción muscular

inicio_contraccion = int(2 * fs)
fin_contraccion = int(3 * fs)

# Señal EMG sintética
emg_signal = reposo.copy()
emg_signal[inicio_contraccion:fin_contraccion] += contraccion[inicio_contraccion:fin_contraccion]
Filtro y ventana
Filtro Butterworth
Se aplica un filtro pasa-bajas de tipo Butterworth para eliminar frecuencias superiores a 50 Hz y reducir el ruido de alta frecuencia.

python
Copiar código
from scipy.signal import butter, filtfilt

frecuencia_corte = 50
rango_normalizado = frecuencia_corte / (0.5 * fs)
orden = 4

# Filtro Butterworth
b, a = butter(orden, rango_normalizado, btype='low')
emg_filtrada = filtfilt(b, a, emg_signal)
Ventana de Hamming
Aplicamos una ventana de Hamming para suavizar los efectos de borde y reducir el leakage en la Transformada de Fourier.

python
Copiar código
ventana_hamming = np.hamming(len(emg_filtrada))
emg_ventaneada = emg_filtrada * ventana_hamming
Transformada de Fourier
A continuación, se realiza la Transformada de Fourier (FFT) de las señales en reposo y durante la contracción para observar las componentes de frecuencia dominantes.

python
Copiar código
from scipy.fft import fft, fftfreq

# FFT para ambas señales
fft_contraccion = fft(emg_ventaneada[inicio_contraccion:fin_contraccion])
fft_reposo = fft(emg_ventaneada[:inicio_contraccion])

frecuencias_contraccion = fftfreq(len(fft_contraccion), 1/fs)
frecuencias_reposo = fftfreq(len(fft_reposo), 1/fs)
Las frecuencias dominantes y sus características serán evaluadas en la siguiente sección.

Análisis estadístico
Se aplica un test de hipótesis t-student para comparar las medias de las frecuencias dominantes entre la señal en reposo y durante la contracción.

Hipótesis
H₀: No existe diferencia significativa entre las medias de las frecuencias.
H₁: Existe una diferencia significativa en las medias de las frecuencias.
python
Copiar código
from scipy.stats import ttest_ind

# Test t entre las frecuencias de reposo y contracción
t_stat, p_value = ttest_ind(frecuencias_reposo, frecuencias_contraccion)

# Resultados del test
print(f"T-statistic: {t_stat}")
print(f"P-value: {p_value}")
Conclusiones
El análisis estadístico arrojó un p-valor de X, lo que indica que [explicar resultados según los valores obtenidos]. Con base en esto, podemos concluir que:

[Conclusión sobre el cambio en la frecuencia dominante durante la contracción].
[Cualquier observación adicional sobre la señal EMG y su comportamiento].
Anexos
Este repositorio incluye los siguientes archivos que permiten reproducir el análisis completo:

lab_3.py: Código completo que incluye la generación, filtrado, ventana, transformada de Fourier y análisis estadístico.
señales.pdf: Documento con una explicación adicional sobre los fundamentos teóricos usados.
plots/: Carpeta que contiene gráficos generados durante el análisis.
Instrucciones para reproducir el trabajo
Clona este repositorio:

bash
Copiar código
git clone https://github.com/tu-usuario/nombre-del-repositorio.git
Asegúrate de tener instaladas las dependencias:

bash
Copiar código
pip install -r requirements.txt
Ejecuta el archivo lab_3.py para generar los gráficos y obtener los resultados del análisis:

bash
Copiar código
python lab_3.py
Nota: El código es autocontenido, lo que significa que todas las bibliotecas y funciones necesarias están incluidas en los archivos del repositorio.

Instrucciones para subir el proyecto a GitHub
Crea un nuevo repositorio en GitHub.

En tu máquina local, navega a la carpeta donde tienes el proyecto y ejecuta los siguientes comandos:

bash
Copiar código
git init
git add .
git commit -m "Subir informe y código EMG"
git remote add origin https://github.com/tu-usuario/nombre-del-repositorio.git
git push -u origin master
Esto te permitirá tener un informe autocontenido, con todo el código, gráficos y análisis estadístico, disponible en GitHub para que otros puedan reproducirlo.

¿Te gustaría que te ayude con algún detalle específico del código o con los pasos para configurar el repositorio en GitHub?






