Informe de Análisis de Señal EMG Real
Este informe presenta el análisis de una señal EMG adquirida durante un experimento en el cual se midió la actividad muscular del bíceps durante un periodo de contracción. El análisis incluye:

Descripción del experimento y adquisición de la señal EMG.
Procesamiento de la señal mediante filtrado pasa-bajas.
Aplicación de una ventana de Hamming para análisis espectral.
Transformada de Fourier (FFT) para análisis en el dominio de la frecuencia.
Análisis estadístico usando un test de hipótesis para evaluar la diferencia en la frecuencia media entre los periodos de reposo y contracción muscular.
Tabla de contenido
Descripción del experimento
Preprocesamiento de la señal
Filtro y ventana
Transformada de Fourier
Análisis estadístico
Conclusiones
Anexos
Descripción del experimento
El experimento se llevó a cabo para medir la actividad electromiográfica (EMG) del bíceps braquial de un sujeto mientras realizaba una contracción muscular. El proceso consistió en:

Adquisición de la señal: Se utilizó un dispositivo EMG que registró la señal a una frecuencia de muestreo de 1000 Hz. La duración total de la medición fue de 5 segundos.
Condiciones del experimento:
Reposo: Durante los primeros 2 segundos, el sujeto mantuvo el brazo relajado.
Contracción muscular: Entre los segundos 2 y 3, el sujeto realizó una contracción máxima del bíceps.
Reposo: A partir del segundo 3, el sujeto relajó nuevamente el músculo.
La señal fue guardada en un archivo de datos para su posterior análisis.

Preprocesamiento de la señal
La señal EMG adquirida contiene ruido debido a interferencias externas y artefactos biológicos. Por lo tanto, se aplicó un preprocesamiento para mejorar la calidad de la señal antes del análisis espectral y estadístico.

Lectura de los datos: Los datos EMG fueron leídos desde un archivo CSV.
python
Copiar código
import numpy as np
import pandas as pd

# Cargar los datos EMG desde un archivo CSV
data = pd.read_csv("emg_data.csv")
t = data['Tiempo']  # Tiempo en segundos
emg_signal = data['EMG']  # Señal EMG registrada
Filtro y ventana
Filtro Butterworth
Dado que la señal EMG tiene componentes de alta frecuencia no deseadas, se aplicó un filtro pasa-bajas Butterworth con una frecuencia de corte de 50 Hz para eliminar el ruido de alta frecuencia.

python
Copiar código
from scipy.signal import butter, filtfilt

# Diseño del filtro pasa-bajas
frecuencia_corte = 50
rango_normalizado = frecuencia_corte / (0.5 * fs)
orden = 4

# Filtro Butterworth
b, a = butter(orden, rango_normalizado, btype='low')
emg_filtrada = filtfilt(b, a, emg_signal)
Ventana de Hamming
Para realizar la Transformada de Fourier y mejorar la resolución en el dominio de la frecuencia, se aplicó una ventana de Hamming a la señal filtrada.

python
Copiar código
ventana_hamming = np.hamming(len(emg_filtrada))
emg_ventaneada = emg_filtrada * ventana_hamming
Transformada de Fourier
Se utilizó la Transformada de Fourier (FFT) para observar las componentes de frecuencia dominantes en la señal tanto en reposo como durante la contracción muscular. La FFT nos permitió identificar las frecuencias más relevantes en ambos estados del músculo.

Transformada de Fourier:
Se extrajo la parte de la señal correspondiente al reposo y a la contracción.
Se calcularon las frecuencias y las amplitudes de las componentes espectrales.
python
Copiar código
from scipy.fft import fft, fftfreq

# FFT durante la contracción
inicio_contraccion = int(2 * fs)
fin_contraccion = int(3 * fs)

emg_contraccion = emg_ventaneada[inicio_contraccion:fin_contraccion]
emg_reposo = emg_ventaneada[:inicio_contraccion]

# Transformada de Fourier
fft_contraccion = fft(emg_contraccion)
fft_reposo = fft(emg_reposo)

frecuencias_contraccion = fftfreq(len(fft_contraccion), 1/fs)
frecuencias_reposo = fftfreq(len(fft_reposo), 1/fs)
Análisis estadístico
El análisis estadístico se realizó con el objetivo de determinar si existe una diferencia significativa entre las frecuencias medias de la señal EMG en reposo y durante la contracción muscular.

Hipótesis
H₀ (Hipótesis nula): No hay diferencia significativa entre las medias de las frecuencias en reposo y durante la contracción.
H₁ (Hipótesis alternativa): Existe una diferencia significativa en las medias de las frecuencias entre reposo y contracción.
Se realizó un test t-student para comparar las medias de las frecuencias en ambas condiciones.

python
Copiar código
from scipy.stats import ttest_ind

# Comparar las frecuencias de reposo y contracción
t_stat, p_value = ttest_ind(frecuencias_reposo, frecuencias_contraccion)

# Resultados del test t
print(f"T-statistic: {t_stat}")
print(f"P-value: {p_value}")
Si el valor p es menor que 0.05, se concluye que existe una diferencia significativa en las frecuencias medias.

Conclusiones
Del análisis de la señal EMG, se puede concluir que:

[Explicar si se encontró o no una diferencia significativa en las frecuencias medias].
La frecuencia dominante durante la contracción muscular fue de [indicar frecuencia], lo que es consistente con la activación del músculo bajo carga.
El análisis estadístico arrojó un p-valor de [p_value], lo que indica que [explicar conclusiones en función del resultado del test t].
Este estudio sugiere que la señal EMG cambia significativamente durante la contracción muscular, lo cual es consistente con la literatura sobre la actividad muscular medida mediante electromiografía






