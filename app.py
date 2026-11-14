import re
import unicodedata
import gradio as gr

# Tarea 1: Diseño de intenciones
intenciones = {
    "saludo": {
        "patrones": ["hola", "buenos dias", "buenas tardes"],
        "respuesta": "¡Hola! Bienvenido al Hotel Los Cabos. ¿En qué puedo ayudarte?"
    },
    "horarios": {
        "patrones": ["horario", "check in", "check out", "entrada", "salida"],
        "respuesta": "El check-in es a las 3:00 p.m. y el check-out a las 12:00 p.m."
    },
    "reservaciones": {
        "patrones": ["reservar", "reservacion", "reserva", "habitacion"],
        "respuesta": "Puedes realizar tu reservación directamente en la recepción del hotel."
    },
    "servicios": {
        "patrones": ["servicios", "alberca", "wifi", "restaurante"],
        "respuesta": "Contamos con alberca, wifi y restaurante."
    },
    "ubicacion": {
        "patrones": ["ubicacion", "direccion", "donde"],
        "respuesta": "Nuestro hotel se encuentra en Cabo San Lucas, Baja California Sur."
    },
    "precios": {
        "patrones": ["precio", "costo", "tarifa", "cuanto cuesta"],
        "respuesta": "Las tarifas comienzan desde $1,500 MXN por noche."
    },
    "despedida": {
        "patrones": ["adios", "gracias", "hasta luego"],
        "respuesta": "¡Gracias por contactarnos! Que tengas un excelente día."
    }
}

# Tarea 2: Procesamiento de consultas
def limpiar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        letra for letra in texto
        if unicodedata.category(letra) != "Mn"
    )
    texto = re.sub(r"[^\w\s]", " ", texto)
    return " ".join(texto.split())


def identificar_intencion(mensaje):
    mensaje = limpiar_texto(mensaje)
    for nombre, datos in intenciones.items():
        for patron in datos["patrones"]:
            patron_regex = r"\b" + re.escape(patron) + r"\b"
            if re.search(patron_regex, mensaje):
                return nombre
    return None


def responder(mensaje, ultima_intencion=None):
    texto = limpiar_texto(mensaje)
    intencion = identificar_intencion(mensaje)

    if intencion is None and texto in [
        "me lo puedes repetir", "puedes repetir", "repitelo", "y eso"
    ]:
        intencion = ultima_intencion

    if intencion is not None:
        return intenciones[intencion]["respuesta"], intencion

    return (
        "Lo siento, no entendí tu pregunta. "
        "Puedes consultarme sobre horarios, reservaciones, "
        "servicios, ubicación o precios."
    ), ultima_intencion


# Tarea 3: Interfaz e historial
def enviar_mensaje(mensaje, historial, ultima_intencion):
    if not mensaje.strip():
        return "", historial, ultima_intencion

    respuesta, ultima_intencion = responder(mensaje, ultima_intencion)
    historial = historial + [
        {"role": "user", "content": mensaje},
        {"role": "assistant", "content": respuesta}
    ]
    return "", historial, ultima_intencion


def evaluar_satisfaccion(calificacion):
    if calificacion is None:
        return "Selecciona una calificación."
    return f"Gracias por tu evaluación: {calificacion}"


with gr.Blocks() as interfaz:
    gr.Markdown("# Chatbot de Atención al Cliente")
    gr.Markdown("Hotel Los Cabos - Asistente Virtual")

    chat = gr.Chatbot(label="Conversación")
    ultima_intencion = gr.State(value=None)
    mensaje = gr.Textbox(
        label="Escribe tu pregunta",
        placeholder="Ejemplo: ¿Tienen alberca?"
    )
    boton_enviar = gr.Button("Enviar")
    boton_enviar.click(
        fn=enviar_mensaje,
        inputs=[mensaje, chat, ultima_intencion],
        outputs=[mensaje, chat, ultima_intencion]
    )

    gr.Markdown("### Evalúa la atención recibida")
    satisfaccion = gr.Radio(
        choices=[
            "1 - Muy mala", "2 - Mala", "3 - Regular",
            "4 - Buena", "5 - Excelente"
        ],
        label="¿Qué te pareció la atención?"
    )
    boton_evaluar = gr.Button("Enviar evaluación")
    resultado_evaluacion = gr.Textbox(label="Resultado")
    boton_evaluar.click(
        fn=evaluar_satisfaccion,
        inputs=satisfaccion,
        outputs=resultado_evaluacion
    )

if __name__ == "__main__":
    
import os

puerto = int(os.environ.get("PORT", 10000))
interfaz.launch(server_name="0.0.0.0", server_port=puerto)

