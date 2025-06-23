from features.imports import *

def carga_de_puntajes():
    """Carga puntajes desde archivo (sin usar 'with')"""
    archivo = None  # Inicializamos la variable para evitar errores
    try:
        ruta = os.path.join("utilities", "puntajes.txt")
        
        # Abre el archivo
        archivo = open(ruta, "r")  # En modo de lectura (tener un tecnico en redes tiene sus ventajas xd)
        lineas = []
        for linea in archivo:
            linea = linea.strip()
            if linea:  # Ignora líneas vacías
                try:
                    nombre, puntos = linea.rsplit(",", 1)
                    lineas.append((nombre, int(puntos)))
                except ValueError:
                    continue  # Ignora líneas mal formateadas
        
        # Devuelve top 5 o datos por defecto
        return sorted(lineas, key=lambda x: x[1], reverse=True)[:5] if lineas else [("Nadie aún", 0)] * 5
    
    except FileNotFoundError:
        return [("Nadie aún", 0)] * 5  # Archivo no existe
    except Exception as e:
        print(f"Error cargando puntajes: {e}")
        return [("Error", 0)] * 5
    finally:
        if archivo:  # Siempre cierra el archivo si se abrió
            archivo.close()

def mostrar_pantalla_puntajes(ventana):
    """Muestra la pantalla de puntajes con PyGame"""
    reloj = pygame.time.Clock()
    fuente_titulo = pygame.font.SysFont("Arial", 50, bold=True)
    fuente_puntajes = pygame.font.SysFont("Arial", 36)
    fuente_boton = pygame.font.SysFont("Arial", 30)
    
    # Cargar puntajes
    puntajes = carga_de_puntajes()
    
    # Botón Volver
    boton_volver = pygame.Rect(800//2 - 100, 600 - 100, 200, 50)
    
    while True:
        ventana.fill((0, 0, 30))  # Fondo azul oscuro
        
        # Título
        titulo = fuente_titulo.render("MEJORES PUNTAJES", True, (255, 215, 0))
        ventana.blit(titulo, (800//2 - titulo.get_width()//2, 50))
        
        # Lista de puntajes
        for i, (nombre, puntos) in enumerate(puntajes):
            texto = fuente_puntajes.render(f"{i+1}. {nombre}: {puntos}", True, (255, 255, 255))
            ventana.blit(texto, (800//2 - texto.get_width()//2, 150 + i * 60))
        
        # Dibujar botón Volver
        pygame.draw.rect(ventana, (200, 50, 50), boton_volver, border_radius=10)
        texto_volver = fuente_boton.render("VOLVER", True, (255, 255, 255))
        ventana.blit(texto_volver, 
                    (boton_volver.x + boton_volver.width//2 - texto_volver.get_width()//2,
                     boton_volver.y + boton_volver.height//2 - texto_volver.get_height()//2))
        
        pygame.display.flip()
        
        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):
                    return  # Regresa al menú principal
        
        reloj.tick(60)