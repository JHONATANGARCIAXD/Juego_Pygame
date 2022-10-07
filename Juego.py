import time
import pygame 
import sys


ANCHO = 640
ALTO = 480
AZUL = (0, 0 ,64)
BLANCO =  (255, 255, 255)   


pygame.init()



class Bolita(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/bolita.png")
        self.rect = self.image.get_rect()
        # Posicion inicial centrada en la pantalla
        self.rect.centerx = ANCHO / 2
        self.rect.centery = ALTO / 2
        # Velocidad inicial
        self.speed = [3, 3]

    def update(self):
         # Evitar que salga por debajo.
        if  self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        # Evitar que se salga por los lados
        elif self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.speed[0] = -self.speed[0]
        # Mover en base a posicion actual y velocidad.
        self.rect.move_ip(self.speed)
    
class Paleta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/paleta.png")
        self.rect = self.image.get_rect()
        # Posicion inicial centrada en la pantalla en X.
        self.rect.midbottom = (ANCHO / 2, ALTO - 20)
        # Velocidad inicial
        self.speed = [0, 0]
    
    def update(self,evento):
    # Buscar si se presiono flecha izquierda.
        if evento.key == pygame.K_LEFT  and self.rect.left > 0:
            self.speed = [-20,0]
    # Buscar si se presiono flecha derecha.
        elif evento.key == pygame.K_RIGHT and self.rect.right < ANCHO:
            self.speed = [20,0]
        else:
            self.speed = [0,0]
    # Mover en base a posicion actual y velocidad.
        self.rect.move_ip(self.speed)


class Ladrillo(pygame.sprite.Sprite):
    def __init__(self, posicion):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/ladrillo.png")
        self.rect = self.image.get_rect()
        # Posicion inicial, provista externamente.
        self.rect.topleft = posicion


class Muro(pygame.sprite.Group):
    def __init__(self, cantidadladrillos):
        pygame.sprite.Group.__init__(self)
        pos_x = 0
        pos_y = 20

        # Crear los ladrillos
        for i in range(cantidadladrillos):
            
            ladrillo = Ladrillo((pos_x , pos_y))
            self.add(ladrillo)
            pos_x += ladrillo.rect.width
            if pos_x >= ANCHO:
                pos_x = 0
                pos_y += ladrillo.rect.height
     


# Funcion llamada tras dejar ir la bolita. 

def juego_terminado():
    fuente = pygame.font.SysFont('Arial', 70)
    texto = fuente.render("GAME OVER", True, (BLANCO))
    texto_rect = texto.get_rect()
    texto_rect.center = [ANCHO / 2, ALTO / 2]
    pantalla.blit(texto, texto_rect)
    pygame.display.flip()
    # Esperar 3 segundos antes de terminar.
    time.sleep(3)
    # Salir
    sys.exit()

def Mostrar_Puntacion():
    fuente = pygame.font.SysFont('Cosolas', 30)
    texto = fuente.render(str(puntos).zfill(5), True, (BLANCO))
    texto_rect = texto.get_rect()
    texto_rect.topleft = [0,0]
    pantalla.blit(texto, texto_rect)

def Mostrar_vidas():
    fuente = pygame.font.SysFont('Cosolas', 30)
    cadena = "Vidas: " + str(vidas).zfill(2)
    texto = fuente.render(cadena, True, (BLANCO))
    texto_rect = texto.get_rect()
    texto_rect.topright = [ANCHO,0]
    pantalla.blit(texto, texto_rect)



# Inicializando pantalla

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Ladrillos")
# Crear reloj para controlar FPS
reloj = pygame.time.Clock()
# Ajustar repetición de evento de tecla presionada.
pygame.key.set_repeat(30)



bolita = Bolita()
jugador = Paleta()
muro  = Muro(70)
puntos = 0
vidas = 3

while True:
    # Establecer FPS
    reloj.tick(100)

    # Revisar todos los eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            sys.exit()
        # Buscar eventos del teclado.
        elif evento.type == pygame.KEYDOWN:
            jugador.update(evento)  


    # Actualizar posicion de la bolita
    bolita.update() 

    # Colosiones entre bolita y jugador.
    if pygame.sprite.collide_rect(bolita, jugador):
        bolita.speed[1] = -bolita.speed[1]
    
    # Colision entre bolita y muro.
    lista = pygame.sprite.spritecollide(bolita, muro, False)
    if lista:
        ladrillo = lista[0]
        cx = bolita.rect.centerx
        if cx < ladrillo.rect.left or cx > ladrillo.rect.right:
            bolita.speed[0] = -bolita.speed[0]
        else:
            bolita.speed[1] = -bolita.speed[1]
        muro.remove(ladrillo)
        puntos += 10


    # Revisar si la bolita se sale de la pantalla.
    if bolita.rect.top > ALTO:
       vidas -=1
       bolita.rect.top -= ALTO / 2
   


    # Rellenar la pantalla
    pantalla.fill(AZUL)
    # Dibujar el puntaje en la pantalla
    Mostrar_Puntacion()
    # Dibujar las vidas en la pantalla
    Mostrar_vidas()
    #  Dibujar bolita en la pantalla
    pantalla.blit(bolita.image, bolita.rect)
    #  Dibujar el Jugador en la pantalla
    pantalla.blit(jugador.image, jugador.rect)
    #  Dibujar el muro en la pantalla
    muro.draw(pantalla)

    if vidas <=0:
        juego_terminado()





    # Actualizar pantalla
    pygame.display.flip() 
