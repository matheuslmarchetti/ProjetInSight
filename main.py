from gui import criar_tela_inicial
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestão de Projetos")
    
    # Remova a linha abaixo para não fixar tamanho
    # root.geometry("800x500") 
    
    # Em vez disso, inicie maximizado ou adaptável
    root.state('zoomed')  # Para Windows
    # root.attributes('-fullscreen', True)  # Para tela cheia real
    
    criar_tela_inicial(root)
    root.mainloop()