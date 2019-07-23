import cpuinfo, locale, os, platform, psutil, pygame, time, socket, string, sys, multiprocessing

pygame.init()
username = os.getlogin()#Pega o nome do usuario


#Obtém informações da CPU
info_cpu = cpuinfo.get_cpu_info()
freq = psutil.cpu_freq().max
core = psutil.cpu_count(logical=False)
logc_core = psutil.cpu_count()

#Obtém informações da Memoria
memory = psutil.virtual_memory()
memory_total = str(round(memory.total/(1024*1024*1024),1))
memory_free = str(round(memory.free/(1024*1024*1024),1))

#Obtém informações da Memoria de Paginação
memoryp = psutil.swap_memory()
memoryp_total =str(round(memoryp.total/(1024*1024*1024),1))
memoryp_free = str(round(memoryp.free/(1024*1024*1024),1))

#Obtém informações do Disco
partition = os.getcwd()
disk = psutil.disk_usage(partition)
disk_total = str(round(disk.total/(1024*1024*1024),2))
disk_used = str(round(disk.used/(1024*1024*1024),2))

#Obtém informações da internet
interface = psutil.net_if_addrs()


###Tela
menu = 2 #0 = cpu  , 1 = memoria, 2 = disco, 3 = ...
width = 640
height = 480
screen = pygame.display.set_mode((width, height))
screen.fill((255,255,255))
clock = pygame.time.Clock()
fps = 340



###Variaveis de posição da UX
##Barra lateral
side_bar_x = 50
side_bar_y = 250
side_bar_a = False
side_bar_ab = False
side_bar_open = False
side_bar_mouse = False
bar_cpu_font = pygame.font.Font('AGENCYR.ttf', 30)

###Estilo da aplicação
blue = (27,129,154)
pink = (255,38,116)


white = (255,255,255)
soft_red = (200,0,0)
soft_purple = (100,0, 200)
soft_blue = (27,100,255)
soft_green = (0,200,0)
soft1_grey = (240,240,240)
soft_grey = (180,180,180)
grey = (90,90,90)
dark_grey = (50,50,50)
black = (0,0,0)

font = pygame.font.Font(None, 25)



#Obtém as informações dos diretorios e dos arquivos
list = os.listdir()
list_file = [] # lista para guardar os arquivos
list_dir = [] # lista para guardar os diretórios
file_size = []
file_atime = []
file_mtime = []
intermediate = pygame.surface.Surface((550, 9999))
intermediate.fill(soft_grey)
scroll_y = 60
soma = 0
disk_folder_show = False
disk_folder_show1 = False

for i in list:
    if os.path.isfile(i):
        list_file.append(i)
        file_size.append(os.stat(i).st_size)
        file_atime.append(os.stat(i).st_atime)
        file_mtime.append(os.stat(i).st_mtime)
        
    else:
        list_dir.append(i)


#Verifica o idioma padrão do computador.
if 'apt_BR' in locale.getdefaultlocale():
    lang = 'Gerenciador de Tarefas'
    lang_side_bar = [('CPU', 85, 60), ('Memoria', 70, 108), ('Disco', 80, 156), ('Ethernet', 70, 205)]
    lang_usage = [('Uso da CPU:', 80, 70), ('Uso da memoria:', 80, 70), ('Uso do disco:', 80, 70)]
    lang_cpu = [('Modelo:', 120, 200, info_cpu['brand'], 190, 200 ),
                ('Arquitetura:', 120, 230, info_cpu['arch'], 225, 230),
                ('Frequencia:', 120, 260, str(freq) + ' Mhz', 225, 260),
                ('Núcleos:', 120, 290, str(core), 200, 290),
                ('Núcleo Logicos:', 120, 320, str(logc_core), 255, 320)]
    lang_memory = [('Total:', 120, 200, memory_total + ' GB', 170, 200 ),
                   ('Disponivel:', 120, 230, memory_free + ' GB', 220, 230),
                   ('Total de Paginação:', 120, 260, memoryp_total + ' GB', 290, 260),
                   ('Paginação Disponivel:', 120, 290, memoryp_free + ' GB', 310, 290)]
    lang_disk = [('Disco:', 120, 200, str(partition[0:2]), 175, 200),
                 ('Capacidade Total:', 120, 230, disk_total + ' GB' , 275, 230),
                 ('Usada:', 120, 260, disk_used + ' GB', 180, 260)]
    lang_network = [('IPv4:', 120, 200, interface['Ethernet'][1][1], 165, 200),
                    ('Mascara IPv4:', 120, 230, interface['Ethernet'][1][2], 240, 230),
                    ('IPv6:', 120, 260, interface['Ethernet'][2][1], 165, 260)]
    

else:
    lang = 'Task Manager'
    lang_side_bar = [('CPU', 85, 60), ('Memory', 70, 108), ('Disk', 80, 156), ('Ethernet', 70, 205)]
    lang_usage = [('CPU usage:', 80, 70), ('Memory usage:', 80, 70), ('Disk usage:', 80, 70)]
    lang_cpu = [('Model:', 120, 200, info_cpu['brand'], 180, 200 ), ('Architecture:', 120, 230, info_cpu['arch'], 235, 230),
                ('Frequency:', 120, 260, str(freq) + ' Mhz', 215, 260), ('Cores:', 120, 290, str(core), 180, 290),
                ('Logical processors:', 120, 320, str(logc_core), 285, 320)]
    lang_memory = [('Total:', 120, 200, memory_total + ' GB', 170, 200),
                   ('Available:', 120, 230, memory_free + ' GB', 205, 230),
                   ('Paged pool:', 120, 260, memoryp_total + ' GB', 220, 260),
                   ('Non-Paged pool:', 120, 290, memoryp_free + ' GB', 260, 290)]
    lang_disk = [('Disk:', 120, 200, str(partition[0:2]), 165, 200 ),
                 ('Total capacity:', 120, 230, disk_total + ' GB', 245, 230),
                 ('Usaged:', 120, 260, disk_used + ' GB', 190, 260)]
    lang_network = [('IPv4:', 120, 200, interface['Ethernet'][1][1], 165, 200),
                    ('Mask IPv4:', 120, 230, interface['Ethernet'][1][2], 215, 230),
                    ('IPv6:', 120, 260, interface['Ethernet'][2][1], 165, 260)]
    
    
    
    
pygame.display.set_caption(lang)

def side_bar(menu):
    pygame.draw.rect(screen,soft1_grey,(0,0,side_bar_x + 2,250))
    pygame.draw.rect(screen,soft_grey,(0,0,side_bar_x, side_bar_y))
    if menu == 0:
        pygame.draw.rect(screen,soft_red,(0,0,side_bar_x,100))
    if menu == 1:
        pygame.draw.rect(screen,soft_purple,(0,100,side_bar_x,50))
    if menu == 2:
        pygame.draw.rect(screen,soft_blue,(0,150,side_bar_x,50))
    if menu == 3:
        pygame.draw.rect(screen,soft_green,(0,200,side_bar_x,50))
    if menu == 4:
        pygame.draw.rect(screen,soft_green,(0,200,side_bar_x,50))


def grapher(menu):
    pygame.draw.rect(screen, dark_grey, (80, 90, width1, 50))
    pygame.draw.rect(screen, menu, (80, 90, width2, 50))


def cpu_show():
    global width1
    global width2
    capacity = psutil.cpu_percent(interval=0)
    #largura total em pixel
    width1 = width - 2*60
    width2 = width * capacity/100
    
def cpu_spec_show():
    for i in range(0, len(lang_cpu)):
        cpu_spec_text = font.render(lang_cpu[i][0],1, dark_grey)
        screen.blit(cpu_spec_text,(lang_cpu[i][1],lang_cpu[i][2]))
        cpu_spec_text = font.render(lang_cpu[i][3], 1, soft_red)
        screen.blit(cpu_spec_text,(lang_cpu[i][4],lang_cpu[i][5]))
       
       
def memory_show():
    global width1
    global width2
    global capacity
    memory = psutil.virtual_memory()
    capacity = round(100 * float(memory.used) /float(memory.total))
    #largura total em pixel
    width1 = width - 2*60
    width2 = width * capacity/100


def memory_spec_show():
    for i in range(0, len(lang_memory)):
        memory_spec_text = font.render(lang_memory[i][0],1, dark_grey)
        screen.blit(memory_spec_text,(lang_memory[i][1],lang_memory[i][2]))
        memory_spec_text = font.render(lang_memory[i][3], 1, soft_purple)
        screen.blit(memory_spec_text,(lang_memory[i][4],lang_memory[i][5]))
        
        
def disk_show():
    global width1
    global width2
    global capacity
    partition = os.getcwd()
    partition = str(partition[0:2])
    disk = psutil.disk_usage(partition)
    capacity = round(100 * float(disk.used) /float(disk.total))
    width1 = width - 2*60
    width2 = width * capacity/100


def disk_spec_show():
    for i in range(0, len(lang_disk)):
        disk_spec_text = font.render(lang_disk[i][0],1, dark_grey)
        screen.blit(disk_spec_text,(lang_disk[i][1],lang_disk[i][2]))
        disk_spec_text = font.render(lang_disk[i][3], 1, soft_blue)
        screen.blit(disk_spec_text,(lang_disk[i][4],lang_disk[i][5]))
        
def disk_fd_show():
    y = 0
    global soma
    soma = 0
    for i in range (0, len(list_file)):
        intermediate.blit(font.render('Nome: ' + list_file[i], 1, dark_grey), (10, y))
        kb = (file_size[i]/1000)
        intermediate.blit(font.render('Tamanho: ' + str(kb) + 'KB', 1, grey), (10, y + 20))
        intermediate.blit(font.render('Tempo de criação: ' + time.ctime(file_atime[i]), 1, grey), (10, y + 40))
        intermediate.blit(font.render('Tempo de modificação: ' + time.ctime(file_mtime[i]), 1, grey), (10, y + 60))
        y += 90
        soma += 90

def network_spec_show():
    for i in range(0, len(lang_network)):
        network_spec_text = font.render(lang_network[i][0],1, dark_grey)
        screen.blit(network_spec_text,(lang_network[i][1],lang_network[i][2]))
        network_spec_text = font.render(lang_network[i][3], 1, soft_green)
        screen.blit(network_spec_text,(lang_network[i][4],lang_network[i][5]))


def image_loading():
    global cpu_icon
    global ram_icon
    global disk_icon
    global network_icon
    cpu_icon = pygame.image.load("cpu_icon-30x30.png")
    ram_icon = pygame.image.load("ram_icon-30x30.png")
    disk_icon = pygame.image.load("disk_icon-30x30.png")
    network_icon = pygame.image.load("network_icon-30x30.png")
    
image_loading()


running = True
while running:
    
    #Pega a posição do mouse na janela do pygame
    mouseX = pygame.mouse.get_pos()[0] #Posição X
    mouseY = pygame.mouse.get_pos()[1] #Posição Y
    
    if menu == 0:
        #Fazer a atualização a cada segundo: 
        if fps >= 340:
            cpu_show()
            fps = 0
             
        #Barra de atualização da CPU  
        usage_text = font.render(lang_usage[0][0], 1, dark_grey)
        screen.blit(usage_text, (lang_usage[0][1], lang_usage[0][2]))
        grapher(soft_red)
        pygame.draw.rect(screen, soft_grey,(70,165,540,1))
        cpu_spec_show()
        side_bar(menu)
        
    if menu == 1:
        #Barra de atualização da memoria
        memory_show()
        memory_spec_show()
        usage_text = font.render(lang_usage[1][0], 1, dark_grey)
        screen.blit(usage_text, (lang_usage[1][1], lang_usage[1][2]))
        grapher(soft_purple)
        pygame.draw.rect(screen, soft_grey,(70,165,540,1))
       
        side_bar(menu)
        percent_text = font.render(str(capacity) + '%', 1, soft_purple)
        screen.blit(percent_text, (570, 70))
        
    if menu == 2:
        disk_show()
        if disk_folder_show == True:
            disk_fd_show()
        else:
            usage_text = font.render(lang_usage[2][0], 1, dark_grey)
            screen.blit(usage_text, (lang_usage[2][1], lang_usage[2][2]))
            disk_spec_show()
            grapher(soft_blue)
            pygame.draw.rect(screen, soft_grey,(70,165,540,1))
            percent_text = font.render(str(capacity) + '%', 1, soft_blue)
            screen.blit(percent_text, (570, 70))

        side_bar(menu)

        
    if menu == 3:
        pygame.draw.rect(screen, soft_grey,(70,165,540,1))
        network_spec_show()
        side_bar(menu)

        
    if side_bar_x <= 180 and mouseX <= side_bar_x and  mouseY >= 50 and mouseY <= side_bar_y:
        side_bar_x = side_bar_x + 1.5
        side_bar_mouse = True
        
    if side_bar_x >= 53 and mouseX >= side_bar_x or side_bar_x >= 53 and mouseY >= side_bar_y or side_bar_x >= 53 and mouseY < 50:
        side_bar_x = side_bar_x - 2.5
        side_bar_mouse = False
        

    if  pygame.mouse.get_pressed()[0] and side_bar_mouse == True and mouseY >= 50 and mouseY <= 100:
        menu = 0
        disk_folder_show = False
    if  pygame.mouse.get_pressed()[0] and side_bar_mouse == True and mouseY >= 100 and mouseY <= 150:
        menu = 1
        disk_folder_show = False
    if  pygame.mouse.get_pressed()[0] and side_bar_mouse == True and mouseY >= 150 and mouseY <= 200:
        menu = 2
    if  pygame.mouse.get_pressed()[0] and side_bar_mouse == True and mouseY >= 200 and mouseY <= 250:
        menu = 3
        disk_folder_show = False

        
    #Icones com os nomes
    screen.blit(cpu_icon, (10,62))
    screen.blit(ram_icon, (10,110))
    screen.blit(disk_icon, (10,160))
    screen.blit(network_icon, (10,210))
    
    if side_bar_mouse == True:
        for i in range (0, len(lang_side_bar)):
            cpu_text = bar_cpu_font.render(lang_side_bar[i][0], 1, white)
            screen.blit(cpu_text, (lang_side_bar[i][1], lang_side_bar[i][2]))
    
    ###Barra superior
    ##Desenha as barras superiores
    pygame.draw.rect(screen, grey,(0,0,640,53))
    pygame.draw.rect(screen, dark_grey,(0,0,640,50))
    ##Desenha o nome do usuario
    username_text = bar_cpu_font.render(username, 1, white)
    screen.blit(username_text, (480, 5))
    
    

    ###Para o botão de fechar a aplicação funcionar
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if menu == 2 and mouseY > 50 and mouseY < 165 and mouseX > 80 and mouseX < 600 :
                    disk_folder_show = True
                
            if event.button == 4: scroll_y = min(scroll_y + 35, 60)
            if event.button == 5: scroll_y = max(scroll_y - 35,  -soma + 80 * 6)
            
        if event.type == pygame.QUIT:
            running = False
            sys.exit(0)
            pygame.quit()
            
    ####Atualização da aplicação        
    fps += 1
    pygame.display.flip()
    screen.fill(soft1_grey)
    if disk_folder_show == True:
        screen.blit(intermediate, (70, scroll_y))
    
pygame.display.quit()
pygame.quit()