import pandas as pd          
import numpy as np           
import matplotlib.pyplot as plt


archivo = "Short_Laprida_Sian_TPINTEGRADOR.xlsx"

df = pd.read_excel(archivo, sheet_name="Hoja1", header=1)

df = df.drop(columns={"Unnamed: 0", "Unnamed: 1"})

df["Horas promedio en redes sociales"] = pd.to_numeric(
    df["Horas promedio en redes sociales"], 
    errors="coerce"
)
df["Horas promedio en redes sociales"] = df["Horas promedio en redes sociales"].fillna(
    df["Horas promedio en redes sociales"].mean()
)
df["Horas promedio en redes sociales"].head(5)

df["Rendimiento academico"] = pd.to_numeric(
    df["Rendimiento academico"], 
    errors="coerce"
)
df["Rendimiento academico"] = df["Rendimiento academico"].fillna(
    df["Rendimiento academico"].mean()
)

df["Rendimiento academico"].head(5)


#Contratacion de datos
bins=[0,2,4,6,8,10,12]
labels=["0-2","2-4","4-6","6-8","8-10","10-12"] 

df['Horas_intervalo'] = pd.cut(df['Promedio diario de uso de pantalla'], bins=bins, labels=labels, right=False)

#verificacion de que se haya hecho correctamente la columna de intervalos
df["Horas_intervalo"].head()

frecuencia_abs=df["Horas_intervalo"].value_counts().sort_index()

frecuencia_rel=(frecuencia_abs/len(df))*100

frecuencia_acum=frecuencia_abs.cumsum()

frecuencia_acum_rel=frecuencia_rel.cumsum

#Tabla de frecuencias
tabla_frecuencia=pd.DataFrame({"Frecuencia absoluta":frecuencia_abs,
                            "Frecuencia relativa":frecuencia_rel,
                            "Frecuencia acumulada":frecuencia_acum,
                            "Frecuencia acumulada relativa":frecuencia_acum_rel})

print(tabla_frecuencia)


# Estadistica descrictiva
media=df["Promedio diario de uso de pantalla"].mean()
print("media:",media)
mediana=df["Promedio diario de uso de pantalla"].median()
print("mediana:",mediana)
moda=df["Promedio diario de uso de pantalla"].mode()[0]
print("moda:",moda)
varianza=df["Promedio diario de uso de pantalla"].var()
print("varianza:",varianza)
desviacion_estandar=df["Promedio diario de uso de pantalla"].std()
print("desviación estándar:",desviacion_estandar)
rango=df["Promedio diario de uso de pantalla"].max()-df["Promedio diario de uso de pantalla"].min()
print("rango:",rango)

#Hallando los valores de Q1 y Q3 para calcular el rango intercuartilico
Q1=df["Promedio diario de uso de pantalla"].quantile(0.25)
print("Q1:",Q1)
Q3=df["Promedio diario de uso de pantalla"].quantile(0.75)
print("Q3:",Q3)
IQR=Q3-Q1  
print("IQR:",IQR)
#Determinar el sesgo de la distribucion
if media>mediana:
    sesgo="positivo"
elif media<mediana:
    sesgo="negativo"
else:
    sesgo="simétrico"

print(sesgo)
#Interpretación de los resultados

print(f"la distribucion presenta un sesgo:{sesgo}")
print("la media y mediana indican que los datos estan distribuidos de manera desigual")
print("la desviacion estandar muestra que los datos se alejan de la media en promedio 2,042 unidades")
print(f"los datos se encuentran en un rango de {rango} unidades")
print(f"El {frecuencia_rel.max():.1f}% de los estudiantes se encuentra en el intervalo {tabla_frecuencia["Frecuencia relativa"].idxmax()} horas.")
print(f"El {frecuencia_acum_rel.iloc[-1]:.1f}% de los estudiantes usa entre 0 y 12 horas de redes sociales.")

# Compararacion de la medida pertinente

## para la comparacion decidi seleccionar la media aritmetica 

#media aritmetica obtenida del excel del compañero de trabajo
media_aritmetica=6.8886

#media de las horas promedio de las redes sociales
media_redes_sociales=df["Horas promedio en redes sociales"].mean()
print(media_aritmetica)

print(media_redes_sociales)

#diferencias entre ambas medias

diferencia={abs(media_redes_sociales-media_aritmetica)}
print(diferencia)

print(f"la diferencia que hay entre las medias es de {diferencia} esto quieres decir que en la base de datos de mi compañero pasa,en \n promedio {diferencia}  mas en redes sociales que los estudiantes de mi muestra")

# Regresion lineal Y correlacion
#Definiendo la variable independiente y dependiente
horas_promedio_redes=df["Horas promedio en redes sociales"]
print("Variable independiente:",horas_promedio_redes)
rendimiento_academico=df["Rendimiento academico"]
print("Variable dependiente:",rendimiento_academico)
#Creando un nuevo dataframe para almacenar las variables que necesita la regresion lineal
df_2=pd.DataFrame({"X":horas_promedio_redes,"y":rendimiento_academico})
#definiendo y añadiendo nuevas columnas 
df_2["x*y"]=df_2["X"]*df_2["y"]
df_2["x^2"]=df_2["X"]**2
df_2["y^2"]=df_2["y"]**2
# Calculando las sumatorias
print("\n Sumatoria")

xSum =df_2["X"].sum()
print("Suma X:", xSum)
ySum =df_2["y"].sum()
print("Suma Y:", ySum)
xySum=df_2["x*y"].sum()
print("Suma XY:", xySum)
x2Sum=df_2["x^2"].sum()
print("Suma X^2:", x2Sum)
y2Sum=df_2["y^2"].sum()
print("Suma Y^2:", y2Sum)
n=len(df_2)
# Recta de regresion
# Calculo de coeficientes de regresion lineal
b=((n * xySum) - (xSum * ySum)) / ((n * x2Sum) - (xSum ** 2))

a = ((ySum * x2Sum) - (xySum * xSum)) / ((n * x2Sum) - (xSum ** 2))
print("\nRecta de regresion")
print(f" y= {a:.2f} + {b:.2f}x")
#Calculo de correlacion
r = ((n * xySum) - (xSum * ySum)) / np.sqrt(((n * x2Sum) - (xSum ** 2)) * ((n * y2Sum) - (ySum ** 2)))
print("\n Correlacion")
print(f"r ={r:.4f}")
r2=r**2
print(f"r^2= {r2:.4f}")
# Interpretacion de la correlacion
if r>0:
    print("\n La correlacion es positiva")
elif r<0:
    print("\n La correlacion es negativa")
else:
    print("\n No existe una correlacion")

print(f"El modelo explica aproximadamente el {r2*100:.2f}% de la variabilidad.")
# Interpretacion de la fuerza de la correlacion
if abs(r) >= 0.8:
    fuerza = "muy fuerte"
elif abs(r) >= 0.5:
    fuerza = "moderada"
elif abs(r) >= 0.3:
    fuerza = "débil"
else:
    fuerza = "muy débil o nula"
print(f"La fuerza de la correlación es {fuerza}.")
# Diagrama de dispercion con recta de regresion
#Se variable para la recta de regresion lineal
x_line=np.linspace(horas_promedio_redes.min(),horas_promedio_redes.max(),100)
y_line=a+b*x_line
#Creacion del grafico de dispersion
plt.figure(figsize=(10, 6))
plt.scatter(horas_promedio_redes,rendimiento_academico,alpha=0.6,color="blue",label="Datos reales")
plt.plot(x_line, y_line, color='red', linewidth=2, label='Recta de regresión')

# Título y etiquetas
plt.title("Regresión Lineal: Horas de redes sociales vs Rendimiento académico", fontsize=14)
plt.xlabel("Horas promedio en redes sociales", fontsize=12)
plt.ylabel("Rendimiento académico", fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend()

plt.text(0.95, 0.95, 
        f'y = {a:.4f} + {b:.4f}x\nr = {r:.4f}\nR² = {r2:.4f}', 
        transform=plt.gca().transAxes, 
        fontsize=12,
        verticalalignment='top',
        horizontalalignment='right',
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.9))
