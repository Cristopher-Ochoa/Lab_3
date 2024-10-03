# -*- coding: utf-8 -*-
"""
Created on Thu sep  29 12:41:21 2024

@author: Santiago
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from scipy.fft import fft, fftfreq  # Corregimos la importación
from scipy.stats import ttest_ind

# Parámetros
fs = 1000  # Frecuencia de muestreo en Hz
tiempo_total = 5  # Duración total de la señal en segundos
t = np.linspace(0, tiempo_total, fs * tiempo_total)  # Tiempo de muestreo
reposo = np.random.normal(0, 0.1, len(t))  # Ruido en reposo
contraccion = np.random.normal(0, 0.5, len(t))  # Ruido con contracción muscular

# Definir el periodo de contracción (entre 2 y 3 segundos)
inicio_contraccion = int(2 * fs)
fin_contraccion = int(3 * fs)

# Señal EMG sintética
emg_signal = reposo.copy()
emg_signal[inicio_contraccion:fin_contraccion] += contraccion[inicio_contraccion:fin_contraccion]

# Diseño del filtro Butterworth pasa bajas
frecuencia_corte = 50  # Frecuencia de corte en Hz
rango_normalizado = frecuencia_corte / (0.5 * fs)  # Normalización de la frecuencia de corte
orden = 4  # Orden del filtro

# Calcular coeficientes del filtro
b, a = butter(orden, rango_normalizado, btype='low', analog=False)

# Aplicar el filtro a la señal EMG
emg_filtrada = filtfilt(b, a, emg_signal)

# Aplicación de la ventana Hamming usando numpy
tamanio_ventana = len(emg_filtrada)  # Tamaño de la ventana igual a la longitud de la señal
ventana_hamming = np.hamming(tamanio_ventana)  # Usar np.hamming() para generar la ventana

# Aplicar la ventana a la señal EMG filtrada
emg_ventaneada = emg_filtrada * ventana_hamming

# Extraer la parte de la señal correspondiente a la contracción
emg_contraccion = emg_ventaneada[inicio_contraccion:fin_contraccion]
emg_reposo = emg_ventaneada[:inicio_contraccion]  # Parte en reposo

# Calcular la FFT para ambas condiciones (reposo y contracción)
n_contraccion = len(emg_contraccion)
frecuencias_contraccion = fftfreq(n_contraccion, 1/fs)  # fftfreq del módulo correcto
fft_contraccion = fft(emg_contraccion)
magnitude_fft_contraccion = np.abs(fft_contraccion)[:n_contraccion // 2]
frecuencias_positivas_contraccion = frecuencias_contraccion[:n_contraccion // 2]

n_reposo = len(emg_reposo)
frecuencias_reposo = fftfreq(n_reposo, 1/fs)  # fftfreq del módulo correcto
fft_reposo = fft(emg_reposo)
magnitude_fft_reposo = np.abs(fft_reposo)[:n_reposo // 2]
frecuencias_positivas_reposo = frecuencias_reposo[:n_reposo // 2]

# Frecuencia media de ambas condiciones
frecuencia_media_contraccion = np.sum(frecuencias_positivas_contraccion * magnitude_fft_contraccion) / np.sum(magnitude_fft_contraccion)
frecuencia_media_reposo = np.sum(frecuencias_positivas_reposo * magnitude_fft_reposo) / np.sum(magnitude_fft_reposo)

# Realizar el test de hipótesis (t-test) entre las frecuencias medias
t_stat, p_value = ttest_ind(frecuencias_positivas_reposo, frecuencias_positivas_contraccion)

# Gráficos
plt.figure(figsize=(12, 8))

# Señal EMG original y ventaneada
plt.subplot(2, 1, 1)
plt.plot(t, emg_ventaneada, label="Señal EMG ventaneada", color='blue')
plt.axvspan(2, 3, color='orange', alpha=0.3, label="Contracción muscular")
plt.title(f"Señal EMG Ventaneada del Bíceps")
plt.xlabel("Tiempo (s)")
plt.ylabel("Amplitud")
plt.legend()
plt.grid(True)

# Transformada de Fourier de ambas condiciones
plt.subplot(2, 1, 2)
plt.plot(frecuencias_positivas_reposo, magnitude_fft_reposo, label="FFT - Reposo", color='green')
plt.plot(frecuencias_positivas_contraccion, magnitude_fft_contraccion, label="FFT - Contracción", color='red')
plt.title("Transformada de Fourier (FFT) de la Señal EMG")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Amplitud")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Mostrar resultados
print(f"Frecuencia media en reposo: {frecuencia_media_reposo:.2f} Hz")
print(f"Frecuencia media durante contracción: {frecuencia_media_contraccion:.2f} Hz")
print(f"T-statistic: {t_stat:.2f}")
print(f"P-value: {p_value:.5f}")

# Interpretación del p-valor
alpha = 0.05  # Nivel de significancia
if p_value < alpha:
    print("Conclusión: Se rechaza la hipótesis nula. Existe una diferencia significativa entre las frecuencias medias en reposo y durante la contracción.")
else:
    print("Conclusión: No se rechaza la hipótesis nula. No hay evidencia suficiente para afirmar que existe una diferencia significativa entre las frecuencias medias.")
