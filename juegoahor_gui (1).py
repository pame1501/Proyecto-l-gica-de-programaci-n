import tkinter as tk              
import tkinter.messagebox as mb   
import random                      

COLOR_FONDO = "#0a0a0f"       
COLOR_NEON_ROSA = "#ff4df0"   
COLOR_NEON_CIAN = "#00fff2"   
COLOR_NEON_VERDE = "#28ffbf"  

FUENTE_TITULO = ("Arial", 28, "bold")    
FUENTE_SUBTITULO = ("Arial", 14)          
FUENTE_RESALTADA = ("Arial", 20, "bold")  

STICKMAN = {
    6: "  \\😃/  \n   |   \n  / \\ ",  
    5: "  \\😄/  \n   |   \n  /    ",  
    4: "  \\🙂/  \n   |   \n       ", 
    3: "   😐   \n  /|   \n       ", 
    2: "   😟   \n   |   \n       ", 
    1: "   😢   \n       \n       ", 
    0: "   💀   \n       \n       "  
}

def calcular_puntos(inicial, restantes):
    try:
        return (restantes / inicial) * 100  
    except:
        return 0  #

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

    portada.geometry("1100x1000")                   
    portada.mainloop()                            

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

def iniciar_juego():
    global ventana_juego
    ventana_juego = tk.Tk()                       
    ventana_juego.title("Ahorcado OKP")
    ventana_juego.config(bg=COLOR_FONDO)

    animales = ["perro", "gato", "tigre", "leon", "lobo", "zorro"]

    palabra = random.choice(animales)             

    mb.showinfo("Bienvenido al juego Ahorcado OKP 🐾",                 
                "Debes adivinar el nombre de un ANIMAL 🐾")

    intentos_iniciales = 6                        

    juego = {                                     
        "palabra": palabra,                       
        "guiones": ["_" for _ in palabra],        
        "errores": [],                            
        "intentos": intentos_iniciales,          
        "puntos": 0                               
    }

    tk.Label(                                    
        ventana_juego, text="Ahorcado OKP ",
        fg=COLOR_NEON_ROSA, bg=COLOR_FONDO,
        font=FUENTE_TITULO
    ).pack(pady=10)

    lbl_palabra = tk.Label(                       
        ventana_juego, text=" ".join(juego["guiones"]),
        fg=COLOR_NEON_CIAN, bg=COLOR_FONDO,
        font=FUENTE_RESALTADA
    )
    lbl_palabra.pack(pady=10)

    lbl_intentos = tk.Label(                      
        ventana_juego, text=f"Intentos: {juego['intentos']}",
        fg=COLOR_NEON_VERDE, bg=COLOR_FONDO,
        font=FUENTE_SUBTITULO
    )
    lbl_intentos.pack()

    stickman_label = tk.Label(                    
        ventana_juego, text=STICKMAN[juego["intentos"]],
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
        ventana_juego, text="Puntos: 100",
        fg=COLOR_NEON_CIAN, bg=COLOR_FONDO,
        font=FUENTE_SUBTITULO
    )
    lbl_score.pack()

    def actualizar_ui():
        lbl_palabra.config(text=" ".join(juego["guiones"])) 
        lbl_intentos.config(text=f"Intentos: {juego['intentos']}") 

        v = max(0, min(6, juego["intentos"]))     
        stickman_label.config(text=STICKMAN[v])   

        errores_label.config(text="Errores: " + ", ".join(juego["errores"]))

        try:
            juego["puntos"] = (juego["intentos"] / intentos_iniciales) * 100 
        except:
            juego["puntos"] = 0

        lbl_score.config(text=f"Puntos: {int(juego['puntos'])}") 

    def verificar_letra(letra):
        letra = letra.lower()                     

        if letra in juego["guiones"] or letra in juego["errores"]:
            return                                

        if letra in juego["palabra"]:             
            for i, c in enumerate(juego["palabra"]):
                if c == letra:
                    juego["guiones"][i] = letra   

            actualizar_ui()                       

            if "_" not in juego["guiones"]:       
                mb.showinfo("GANASTE 😸", "¡Logras adivinar el animal felicitaciones! 😸")
                ventana_juego.destroy()
                mostrar_portada()                 

        else:                                     
            juego["errores"].append(letra)        
            juego["intentos"] -= 1                
            actualizar_ui()

            if juego["intentos"] == 1:            
                mb.showinfo(
                    "Última oportunidad",
                    "¿ESTÁS LIST@ PARA MORIR😝?\n¿O ESTÁS LIST@ PARA REMONTAR😼?"
                )
                parpadeo_rojo(ventana_juego)      

            if juego["intentos"] <= 0:            
                mb.showerror("DERROTA 💀",
                            f"Hoy no fue tu dia sigue intentandolo 🥺\n El animal selecionado era: {juego['palabra']}")
                ventana_juego.destroy()
                mostrar_portada()

    teclado_frame = tk.Frame(ventana_juego, bg=COLOR_FONDO)
    teclado_frame.pack(pady=20)

    filas = ["ABCDEFG","HIJKLM","NOPQRT","UVWXYZ"]    

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
            
    ventana_juego.geometry("1000x1000")  
    ventana_juego.mainloop()           

mostrar_portada()
