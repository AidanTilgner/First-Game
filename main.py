import sys, pygame

# initialize pygame
pygame.init()

# Make window appear
screenWidth = 500
screenHeight = 480
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Change display name
pygame.display.set_caption("First Game")

# Player animation variables
walkRight = [
    pygame.image.load('./images/R1.png'),
    pygame.image.load('./images/R2.png'),
    pygame.image.load('./images/R3.png'),
    pygame.image.load('./images/R4.png'),
    pygame.image.load('./images/R5.png'),
    pygame.image.load('./images/R6.png'),
    pygame.image.load('./images/R7.png'),
    pygame.image.load('./images/R8.png'),
    pygame.image.load('./images/R9.png'),
]

walkLeft = [
    pygame.image.load('./images/L1.png'),
    pygame.image.load('./images/L2.png'),
    pygame.image.load('./images/L3.png'),
    pygame.image.load('./images/L4.png'),
    pygame.image.load('./images/L5.png'),
    pygame.image.load('./images/L6.png'),
    pygame.image.load('./images/L7.png'),
    pygame.image.load('./images/L8.png'),
    pygame.image.load('./images/L9.png'),
]

background = pygame.image.load('./images/bg.jpg')

character = pygame.image.load('./images/standing.png')

# Music
music = pygame.mixer.music.load('./sound/music.mp3')
pygame.mixer.music.play(-1)

# Timing
clock = pygame.time.Clock()

# Scorekeeping
score = 0

# Player object
class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        
    def draw(self, screen):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        
        if not(self.standing):
            if self.left:
                screen.blit(walkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))
        
        # we need to change the hitbox
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        
        # Draw hitbox
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
    
    def hit(self):
        self.x = 60
        self.y = 410
        self.walkCount = 0
        warningBanner = pygame.font.SysFont('monospace', 100)
        text = warningBanner.render('-5', 1, (255, 0, 0))
        screen.blit(text, ((screenWidth//2) - (text.get_width()//2), screenHeight//2))
        pygame.display.update()
        i = 0 
        while i < 100:
            pygame.time.delay(30)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.velocity = 8 * facing
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class Enemy(object):
    walkRight = [
        pygame.image.load('./images/R1E.png'),
        pygame.image.load('./images/R2E.png'),
        pygame.image.load('./images/R3E.png'),
        pygame.image.load('./images/R4E.png'),
        pygame.image.load('./images/R5E.png'),
        pygame.image.load('./images/R6E.png'),
        pygame.image.load('./images/R7E.png'),
        pygame.image.load('./images/R8E.png'),
        pygame.image.load('./images/R9E.png'),
        pygame.image.load('./images/R10E.png'),
        pygame.image.load('./images/R11E.png'),
    ]
    
    walkLeft = [
        pygame.image.load('./images/L1E.png'),
        pygame.image.load('./images/L2E.png'),
        pygame.image.load('./images/L3E.png'),
        pygame.image.load('./images/L4E.png'),
        pygame.image.load('./images/L5E.png'),
        pygame.image.load('./images/L6E.png'),
        pygame.image.load('./images/L7E.png'),
        pygame.image.load('./images/L8E.png'),
        pygame.image.load('./images/L9E.png'),
        pygame.image.load('./images/L10E.png'),
        pygame.image.load('./images/L11E.png'),
    ]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.velocity = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True
        
    def draw(self, screen):
        self.move()
        
        if self.visible:
            if self.walkCount >= 33:
                self.walkCount = 0
            
            if self.velocity > 0:
                screen.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            else:
                screen.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount += 1
            
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)    
            
            # Healthbar
            pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(screen, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50/10) * (10 - self.health)), 10))
            
            # Draw hitbox        
            # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

        
    def move(self):
        # if moving right
        if self.velocity > 0:
            # and still within the boundaries
            if self.x + self.velocity < self.path[1]:
                # move right
                self.x += self.velocity
            #or else change directions
            else:
                self.velocity = self.velocity * -1
                self.walkCount = 0
        # if not moving right
        else:
            # and within boundaries
            if self.x - self.velocity > self.path[0]:
                # move left
                self.x += self.velocity
            # or else change directions
            else:
                self.velocity = self.velocity * -1
                self.walkCount = 0
    
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else: 
            self.visible = False
        print('hit')

# draw stuff to the screen
def redrawGameWindow():
    screen.blit(background, (0,0))
    
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    screen.blit(text, (50, 10))
    
    man.draw(screen)
    
    for bullet in bullets:
        bullet.draw(screen)
        
    goblin.draw(screen)
    
    pygame.display.update()


# Player instance
man = Player(300, 410, 64, 64)
goblin = Enemy(100, 410, 64, 64, 450)

# Stores bullets in game
bullets = []

# to fix multiple bullets shooting at once
shootLoop = 0

# Text
font = pygame.font.SysFont('monospace', 30, True)

# game loop
run = True
while run:
    # Sets FPS
    clock.tick(27)
    
    # Setting player hit event
    if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5
    
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3: 
        shootLoop = 0
    
    # When the user presses exit button, exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # Controls bullets
    for bullet in bullets:
        # check for collision
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
        
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.velocity
        else:
            bullets.pop(bullets.index(bullet))
    
    # Basic movement
    keys = pygame.key.get_pressed()
    
    # Shoot bullet
    if keys[pygame.K_SPACE] and shootLoop == 0:
        if man.left:
            facing = -1
        else:
            facing = 1
            
        if len(bullets) < 5:
            # Add new bullet to the bullets list
            bullets.append(Projectile(
                round(man.x + man.width//2), 
                round(man.y + man.height//2),
                6, (0, 0, 0), facing
            ))
        
        shootLoop = 1
    
    # move left
    if keys[pygame.K_LEFT] and man.x > man.velocity:
        man.x -= man.velocity
        man.left = True
        man.right = False
        man.standing = False
    # move right
    elif keys[pygame.K_RIGHT] and man.x < screenWidth - man.width - man.velocity:
        man.x += man.velocity
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.walkCount = 0
        man.standing = True
    
    # Make sure none of this is triggered when the jump is happening
    if not(man.isJump):
        # jump
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
    
    else:
        # some jump logic using quadratics to 
        if man.jumpCount >= -10:
            # if jumpCount is a positive number, then move up, otherwise, move down
            neg = .5
            if man.jumpCount < 0:
                neg = -.5
            man.y -= (man.jumpCount ** 2) * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
            
    redrawGameWindow()
            
pygame.quit()