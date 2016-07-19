from tkinter import *
from tkinter import ttk

class Application():
    def __init__(self):
        self.raiz = Tk()
        self.raiz.geometry('300x200')
        
        # Impide que los bordes puedan desplazarse para
        # ampliar o reducir el tamaño de la ventana 'self.raiz':
         
        self.raiz.resizable(width=False,height=False)
        self.raiz.title('Resercher Analizer')
         
        
         
        # Define el widget Button 'self.binfo' que llamará 
        # al metodo 'self.verinfo' cuando sea presionado
         
        #self.binfo = ttk.Button(self.raiz, text='Info', command=self.showInfo())
         
        # Coloca el botón 'self.binfo' debajo y a la izquierda
        # del widget anterior
        
        #self.binfo.pack(side=LEFT)
         
        
         
        # El foco de la aplicación se sitúa en el botón
        # 'self.binfo' resaltando su borde. Si se presiona
        # la barra espaciadora el botón que tiene el foco
        # será pulsado. El foco puede cambiar de un widget
        # a otro con la tecla tabulador [tab]
         
        #self.binfo.focus_set()
        #self.raiz.mainloop()
        
        menu1 = Menu(self.raiz)
        self.raiz.config(menu=menu1)
        menu1_1 = Menu(menu1, tearoff=0)
        menu1.add_cascade(label="Info", menu=menu1_1)
        menu1_1.add_command(label="Acerca de", command=self.showInfo())
    
        
        
        self.raiz.mainloop()
    
    def showInfo(self):
        self.infoWindow = Toplevel()
        # Define el widget Text 'self.tinfo ' en el que se
        # pueden introducir varias líneas de texto:
        self.infoWindow.resizable(width=False,height=False)
        self.infoWindow.title('About')
        self.tinfo = Text(self.infoWindow, width=40, height=10)
         
        # Sitúa la caja de texto 'self.tinfo' en la parte
        # superior de la ventana 'self.raiz':
         
        self.tinfo.pack(side=TOP)
        
        textInfo="Autor: Jose Angel Gonzalez Mejias\n"
        textInfo+="Directora: Cristina Tirnauca\n"
        textInfo+="Codirector: Domingo Gomez\n"
        textInfo+="Propiedad de los anteriores y la Universidad de Cantabria"
        self.tinfo.insert("1.0",textInfo)
        # Define el botón 'self.bsalir'. En este caso
        # cuando sea presionado, el método destruirá o
        # terminará la aplicación-ventana 'self.raíz' con 
        # 'self.raiz.destroy'
         
        self.bsalir = ttk.Button(self.infoWindow, text='Salir', 
                                 command=self.infoWindow.destroy)
                                  
        # Coloca el botón 'self.bsalir' a la derecha del 
        # objeto anterior.
                                  
        self.bsalir.pack(side=RIGHT)
        #self.infoWindow.mainloop()

def main():    
    mi_app = Application()
    return 0
    
if __name__ == '__main__':
    main()
