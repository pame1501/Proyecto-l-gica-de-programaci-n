import tkinter as tk
import tkinter.messagebox as mb
import random

# COLORES Y FUENTES

COLOR_FONDO = "#0a0a0f"
COLOR_NEON_ROSA = "#ff4df0"
COLOR_NEON_CIAN = "#00fff2"
COLOR_NEON_VERDE = "#28ffbf"

FUENTE_TITULO = ("Arial", 28, "bold")
FUENTE_SUBTITULO = ("Arial", 14)
FUENTE_RESALTADA = ("Arial", 20, "bold")

# MUÑECO  (estados 6 a 0)

STICKMAN = {
    6: "  \\😃/  \n   |   \n  / \\ ",
    5: "  \\😄/  \n   |   \n  /    ",
    4: "  \\🙂/  \n   |   \n       ",
    3: "   😐   \n  /|   \n       ",
    2: "   😟   \n   |   \n       ",
    1: "   😢   \n       \n       ",
    0: "   💀   \n       \n       "
}

# CENTRAR VENTANA

def center_window(win):
    win.update_idletasks()
    w, h = win.winfo_width(), win.winfo_height()
    ws, hs = win.winfo_screenwidth(), win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f"+{x}+{y}")

# CÁLCULO DE PUNTOS 

def calcular_puntos(inicial, restantes):
    try:
        return (restantes / inicial) * 100
    except:
        return 0

# PORTADA

def mostrar_portada():
    portada = tk.Tk()
    portada.title("GANAR 😼 O MORIR 😶‍🌫️")
    portada.config(bg=COLOR_FONDO)

    tk.Label(
        portada,
        text="GANAR 😼 O MORIR 😶‍🌫️",
        fg=COLOR_NEON_ROSA,
        bg=COLOR_FONDO,
        font=FUENTE_TITULO
    ).pack(pady=40)

    tk.Button(
        portada,
        text="INICIAR",
        command=lambda: (portada.destroy(), iniciar_juego()),
        font=FUENTE_RESALTADA,
        fg=COLOR_NEON_CIAN,
        bg=COLOR_FONDO,
        bd=0
    ).pack(pady=20)

    portada.geometry("400x300")
    center_window(portada)
    portada.mainloop()

# PARPADEO ROJO

def parpadeo_rojo(target_window, flashes=4, delay=120):
    original = target_window.cget("bg")
    def efecto(i):
        if i <= 0:
            try:
                target_window.config(bg=original)
            except:
                pass
            return
        try:
            target_window.config(bg="#ff0000")
        except:
            pass
        target_window.after(delay, lambda: (
            target_window.config(bg=original),
            target_window.after(delay, lambda: efecto(i - 1))
        ))
    efecto(flashes)

# INICIAR JUEGO

def iniciar_juego():
    global ventana_juego
    ventana_juego = tk.Tk()
    ventana_juego.title("Ahorcado Neon")
    ventana_juego.config(bg=COLOR_FONDO)

    # Lista de animales
    animales = [
        "perro", "gato", "tigre", "leon", "lobo", "zorro"
    ]

    palabra = random.choice(animales)

    # Mensaje inicial
    mb.showinfo("ADVERTENCIA 🐾", "Debes adivinar el nombre de un ANIMAL 🐾")

    intentos_iniciales = 6
    state = {
        "palabra": palabra,
        "guiones": ["_" for _ in palabra],
        "errores": [],
        "intentos": intentos_iniciales,
        "puntos": 0
    }

    # UI
    
    tk.Label(
        ventana_juego, text="Ahorcado ",
        fg=COLOR_NEON_ROSA, bg=COLOR_FONDO,
        font=FUENTE_TITULO
    ).pack(pady=10)

    lbl_palabra = tk.Label(
        ventana_juego, text=" ".join(state["guiones"]),
        fg=COLOR_NEON_CIAN, bg=COLOR_FONDO,
        font=FUENTE_RESALTADA
    )
    lbl_palabra.pack(pady=10)

    lbl_intentos = tk.Label(
        ventana_juego, text=f"Intentos: {state['intentos']}",
        fg=COLOR_NEON_VERDE, bg=COLOR_FONDO,
        font=FUENTE_SUBTITULO
    )
    lbl_intentos.pack()

    stickman_label = tk.Label(
        ventana_juego, text=STICKMAN[state["intentos"]],
        fg=COLOR_NEON_ROSA, bg=COLOR_FONDO,
        font=("Courier", 20, "bold"), justify="center"
    )
    stickman_label.pack()

    errores_label = tk.Label(
        ventana_juego, text="Errores: ",
        fg="red", bg=COLOR_FONDO,
        font=FUENTE_SUBTITULO
    )
    errores_label.pack(pady=5)

    lbl_score = tk.Label(
        ventana_juego, text="Puntos: 0",
        fg=COLOR_NEON_CIAN, bg=COLOR_FONDO,
        font=FUENTE_SUBTITULO
    )
    lbl_score.pack()

    # ACTUALIZAR UI
   
    def actualizar_ui():
        lbl_palabra.config(text=" ".join(state["guiones"]))
        lbl_intentos.config(text=f"Intentos: {state['intentos']}")
        v = max(0, min(6, state["intentos"]))
        stickman_label.config(text=STICKMAN.get(v, STICKMAN[0]))
        errores_label.config(text="Errores: " + ", ".join(state["errores"]))
        try:
            state["puntos"] = (state["intentos"] / intentos_iniciales) * 100
        except:
            state["puntos"] = 0
        lbl_score.config(text=f"Puntos: {int(state['puntos'])}")

    # VERIFICAR LETRA
   
    def verificar_letra(letra):
        letra = letra.lower()

        if letra in state["guiones"] or letra in state["errores"]:
            return

        if letra in state["palabra"]:
            for i, c in enumerate(state["palabra"]):
                if c == letra:
                    state["guiones"][i] = letra
            actualizar_ui()

            if "_" not in state["guiones"]:
                mb.showinfo("GANASTE 😸", "¡Eres un ganador! 😸")
                ventana_juego.destroy()
                mostrar_portada()
        else:
            state["errores"].append(letra)
            state["intentos"] -= 1
            actualizar_ui()

            if state["intentos"] == 1:
                mb.showinfo(
                    "Última oportunidad",
                    "😝 ¿ESTÁS LISTO PARA MORIR?\n\n😼 ¿O ESTÁS LISTA PARA REMONTAR?"
                )
                parpadeo_rojo(ventana_juego, flashes=4, delay=120)

            if state["intentos"] <= 0:
                mb.showerror("DERROTA 💀", f"Lo siento, eres un perdedor 🥺\nEl animal era: {state['palabra']}")
                ventana_juego.destroy()
                mostrar_portada()

    # TECLADO
    teclado_frame = tk.Frame(ventana_juego, bg=COLOR_FONDO)
    teclado_frame.pack(pady=20)

    filas = ["ABCDEFGHIJKLM", "NOPQRSTUVWXYZ"]
    for fila in filas:
        fila_frame = tk.Frame(teclado_frame, bg=COLOR_FONDO)
        fila_frame.pack()
        for letra in fila:
            tk.Button(
                fila_frame,
                text=letra,
                command=lambda l=letra: verificar_letra(l),
                font=FUENTE_SUBTITULO,
                fg=COLOR_NEON_CIAN,
                bg=COLOR_FONDO,
                width=3
            ).pack(side="left", padx=2, pady=2)

    ventana_juego.geometry("550x550")
    center_window(ventana_juego)
    ventana_juego.mainloop()

mostrar_portada()
