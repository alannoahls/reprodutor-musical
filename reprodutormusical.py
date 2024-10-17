import pygame
import tkinter as tk
from tkinter import Listbox, Scrollbar, filedialog, messagebox
import speech_recognition as sr
import threading
import os

# Inicializar o Pygame
pygame.mixer.init()

# Inicializar a janela principal
janela = tk.Tk()
janela.title("Reprodutor de Música")
janela.geometry("400x400")
janela.configure(bg="#1e1e2f")  # Fundo roxo-escuro

musicas = []
musica_atual = None  # Variável para armazenar a música atual

def nova_musica():
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de Música", "*.mp3 *.wav")])
    if arquivo:
        lista_reproducao.insert(tk.END, os.path.basename(arquivo))  # Adiciona o nome da música à lista
        musicas.append(arquivo)  # Adiciona o caminho à lista de músicas

def nova_playlist():
    pasta = filedialog.askdirectory()
    if pasta:
        for arquivo in os.listdir(pasta):
            if arquivo.endswith(('.mp3', '.wav')):
                caminho_completo = os.path.join(pasta, arquivo)
                musicas.append(caminho_completo)
                lista_reproducao.insert(tk.END, arquivo)

def tocar_musica():
    global musica_atual
    try:
        if musicas:  # Verifica se a lista de músicas não está vazia
            if musica_atual is None:  # Se nenhuma música foi selecionada, escolhe a primeira
                musica_atual = 0
            pygame.mixer.music.load(musicas[musica_atual])
            pygame.mixer.music.play(loops=0)
            label_musica.config(text=os.path.basename(musicas[musica_atual]))
            print(f"Tocando: {musicas[musica_atual]}")  # Depuração
    except pygame.error as e:
        messagebox.showerror("Erro", f"Erro ao carregar a música: {e}")

def parar_musica():
    pygame.mixer.music.stop()
    label_musica.config(text="")

def avancar_musica():
    global musica_atual
    if musicas:
        if musica_atual is None or musica_atual >= len(musicas) - 1:
            musica_atual = 0  # Reinicia se estiver no final
        else:
            musica_atual += 1  # Avança para a próxima música
        print(f"Avançando para: {musicas[musica_atual]}")  # Depuração
        tocar_musica()

def voltar_musica():
    global musica_atual
    if musicas:
        if musica_atual is None or musica_atual <= 0:
            musica_atual = len(musicas) - 1  # Vai para a última música
        else:
            musica_atual -= 1  # Volta para a música anterior
        print(f"Voltando para: {musicas[musica_atual]}")  # Depuração
        tocar_musica()

def controlar_por_voz():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ajustando o ruído do ambiente...")
        reconhecedor.adjust_for_ambient_noise(source)
        while True:
            print("Aguardando comando...")
            audio = reconhecedor.listen(source)
            try:
                comando = reconhecedor.recognize_google(audio, language='pt-BR')
                print(f"Você disse: {comando}")  # Exibe o comando reconhecido
                if "Ariana" in comando:
                    if "tocar" in comando:
                        tocar_musica()
                    elif "parar" in comando:
                        parar_musica()
                    elif "avançar" in comando:
                        avancar_musica()
                    elif "voltar" in comando:
                        voltar_musica()
                    elif "nova música" in comando:
                        nova_musica()
                    elif "nova playlist" in comando:
                        nova_playlist()
                    else:
                        print("Comando não reconhecido.")
            except sr.UnknownValueError:
                print("Comando não entendido, aguardando novo comando...")
            except sr.RequestError as e:
                print(f"Erro ao solicitar resultados do serviço de reconhecimento de voz: {e}")

def iniciar_controle_por_voz():
    threading.Thread(target=controlar_por_voz, daemon=True).start()

# Estilo dos botões
estilo_botao = {
    "bg": "#2f2f6e",
    "fg": "white",
    "activebackground": "#40406e",
    "font": ("Arial", 12, "bold")
}

# Rótulo para exibir a música atual
label_musica = tk.Label(janela, text="", bg="#1e1e2f", fg="white", font=("Arial", 12))
label_musica.pack(pady=10)

# Criação da lista de reprodução
scrollbar = Scrollbar(janela)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista_reproducao = Listbox(janela, height=10, width=50, yscrollcommand=scrollbar.set, bg="#2f2f6e", fg="white")
lista_reproducao.pack(pady=10)

scrollbar.config(command=lista_reproducao.yview)

# Botão para Controle de Voz
botao_controle_voz = tk.Button(janela, text="Controle por Voz", command=iniciar_controle_por_voz, **estilo_botao)
botao_controle_voz.pack(pady=10)

# Botão para nova música
botao_nova_musica = tk.Button(janela, text="Nova Música", command=nova_musica, **estilo_botao)
botao_nova_musica.pack(pady=10)

# Botão para nova playlist
botao_nova_playlist = tk.Button(janela, text="Nova Playlist", command=nova_playlist, **estilo_botao)
botao_nova_playlist.pack(pady=5)

# Botão para Tocar
botao_tocar = tk.Button(janela, text="Tocar", command=tocar_musica, **estilo_botao)
botao_tocar.pack(pady=10)

# Botão para Parar
botao_stop = tk.Button(janela, text="Parar", command=parar_musica, **estilo_botao)
botao_stop.pack(pady=10)

# Botão para Avançar
botao_avancar = tk.Button(janela, text="Avançar", command=avancar_musica, **estilo_botao)
botao_avancar.pack(pady=5)

# Botão para Voltar
botao_voltar = tk.Button(janela, text="Voltar", command=voltar_musica, **estilo_botao)
botao_voltar.pack(pady=5)

# Iniciar o loop principal da interface
janela.mainloop()
