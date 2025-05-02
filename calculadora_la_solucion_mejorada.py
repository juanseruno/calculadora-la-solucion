import streamlit as st
import sympy as sp
import speech_recognition as sr
import pyttsx3

# Inicialización
voz = pyttsx3.init()
x = sp.symbols('x')

# Función para hablar texto
def hablar(texto):
    voz.say(texto)
    voz.runAndWait()

# Título de la app
st.title("Calculadora La Solución")
st.subheader("Resolución paso a paso para Cálculo I")

# Entrada de función
expresion = st.text_input("Ingresa una expresión en x (ej: x**2 + 3*x):")
operacion = st.selectbox("Selecciona la operación", ["Evaluar", "Derivada", "Integral", "Límite"])

if st.button("Resolver"):
    try:
        funcion = sp.sympify(expresion)
        if operacion == "Evaluar":
            valor = st.number_input("Valor de x para evaluar:", value=1.0)
            resultado = funcion.evalf(subs={x: valor})
            pasos = f"Sustituimos x = {valor} en la expresión y obtenemos el resultado: {resultado}"
        
        elif operacion == "Derivada":
            derivada = sp.diff(funcion, x)
            resultado = derivada
            pasos = f"Se aplica la regla de derivación:
La derivada de {funcion} es: {derivada}"
        
        elif operacion == "Integral":
            integral = sp.integrate(funcion, x)
            resultado = integral
            pasos = f"Se calcula la integral indefinida:
La integral de {funcion} es: {integral} + C"
        
        elif operacion == "Límite":
            punto = st.number_input("Límite cuando x tiende a:", value=0.0)
            limite = sp.limit(funcion, x, punto)
            resultado = limite
            pasos = f"Se evalúa el límite de {funcion} cuando x → {punto}:
Resultado: {limite}"
        
        st.success(f"Resultado: {resultado}")
        st.markdown("**Pasos:**")
        st.text(pasos)
        hablar(f"El resultado es {resultado}")

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")

# Sección de entrada por voz
st.markdown("### ¿Prefieres dictar tu operación?")
if st.button("Dictar operación"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Habla ahora...")
        audio = r.listen(source)
        try:
            texto = r.recognize_google(audio, language="es-ES")
            st.write(f"Texto reconocido: {texto}")
            funcion = sp.sympify(texto)
            resultado = funcion.simplify()
            st.success(f"Resultado simbólico: {resultado}")
            hablar(f"Resultado simbólico: {resultado}")
        except Exception as e:
            st.error(f"No se pudo procesar el audio: {e}")

# Opción para impresión
st.markdown("Puedes imprimir esta página desde el navegador con Ctrl+P o menú de impresión.")