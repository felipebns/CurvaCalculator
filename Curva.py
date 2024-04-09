import matplotlib
import math
import scipy

#Fazer genérico para qualquer curva!!!

class Curva():
    def __init__(self, list_t: list, funcX, funcY) -> None:
        self.list_t = list_t
        self.funcX = funcX
        self.funcY = funcY

        self.__x_t = {}
        self.__y_t = {}
        self.__lista_x = []
        self.__lista_y = []
        self.__lista_xl = []
        self.__lista_yl = []
        self.__lista_xl_t = {}
        self.__lista_yl_t = {}
        self.__pxs = []
        self.__pys = []
        self.__horTg = {
            'X':[],
            'Y':[]
        }
        self.__vertTg = {
            'X':[],
            'Y':[]
        }
        self.__intersec = {}

    def printaIntersec(self) -> None:
        print(self.__intersec)

    def printaHorTg(self) -> None:
        print('Pontos em que o vetor Tg é horizontal')
        for i in range(len(self.__horTg['X'])):  
            print(f'X: {self.__horTg["X"][i]} Y: {self.__horTg["Y"][i]}')  

    def printaVertTg(self) -> None:
        print('Pontos em que o vetor Tg é vertical')
        for i in range(len(self.__vertTg['X'])):  
            print(f'X: {self.__vertTg["X"][i]} Y: {self.__vertTg["Y"][i]}')   

    def derivaX(self, funcX, t: float) -> float:     
        return (scipy.misc.derivative(funcX, t, dx=1e-6))

    def derivaY(self, funcY, t: float) -> float:     
        return (scipy.misc.derivative(funcY, t, dx=1e-6))
        
    def verificaTg(self) -> None:
        for i in (range(len(self.list_t)-1)):
            x1 = self.__lista_xl[i]
            x2 = self.__lista_xl[i+1]
            y1 = self.__lista_yl[i]
            y2 = self.__lista_yl[i+1]
            if i == 0:
                primeiro = True
            self.metodoBissecX(i, y1, y2, primeiro)
            self.metodoBissecY(i, x1, x2, primeiro)

    def metodoBissecX(self, i, y1, y2, primeiro) -> None:
        if primeiro:
                y3 = self.__lista_yl[i-1]
                if y1*y3 < 0 or y1*y2 < 0:
                    self.__horTg['X'].append(self.__x_t[self.list_t[i]]) 
                    self.__horTg['Y'].append(self.__y_t[self.list_t[i]])
        elif y1*y2 < 0:
            self.__horTg['X'].append(self.__x_t[self.list_t[i]]) 
            self.__horTg['Y'].append(self.__y_t[self.list_t[i]])

    def metodoBissecY(self, i, x1, x2, primeiro) -> None:
        if primeiro:
                x3 = self.__lista_yl[i-1]
                if x1*x3 < 0 or x1*x2 < 0:
                    self.__vertTg['X'].append(self.__x_t[self.list_t[i]])
                    self.__vertTg['Y'].append(self.__y_t[self.list_t[i]])
        elif x1*x2 < 0:
            self.__vertTg['X'].append(self.__x_t[self.list_t[i]])
            self.__vertTg['Y'].append(self.__y_t[self.list_t[i]])

    def verificaIntersec(self, x1,x2,x3,x4,y1,y2,y3,y4) -> tuple:
        m1 = (y2-y1)/(x2-x1)
        m2 = (y4-y3)/(x4-x3)

        px = (m1*x1 - m2*x3 + y3-y1)/(m1-m2)
        py = m1*(px-x1) + y1

        if ((px >= min(x1,x2) and px <= max(x1,x2)) and
            (px >= min(x3,x4) and px <= max(x3,x4))):
            return px, py

    def determinaIntersec(self) -> None:    
        dict_aux = {}
        for i in (range(len(self.__lista_x)-1)):
            for j in range(i-1):
                #cria xs_ys e verifica se é diferente de 0
                if xs_ys := self.verificaIntersec(self.__lista_x[i],self.__lista_x[i+1],self.__lista_x[j],self.__lista_x[j+1],self.__lista_y[i],self.__lista_y[i+1],self.__lista_y[j],self.__lista_y[j+1]):
                    self.__pxs.append(xs_ys[0])
                    self.__pys.append(xs_ys[1])
                    dict_aux[f'X: {xs_ys[0]}'] = f'Y: {xs_ys[1]}'
                    self.__intersec[f't: {self.list_t[i]}'] = dict_aux
        
    def fazPontos(self) -> None:
        for t in (self.list_t):
            self.__lista_x.append(self.funcX(t=t))
            self.__lista_y.append(self.funcY(t=t))

            self.__lista_xl.append(self.derivaX(funcX=self.funcX, t=t))
            self.__lista_yl.append(self.derivaY(funcY=self.funcY, t=t))

            self.__x_t[t] = self.funcX(t=t)
            self.__y_t[t] = self.funcY(t=t)

            self.__lista_xl_t[t] = self.derivaX(funcX=self.funcX, t=t)
            self.__lista_yl_t[t] = self.derivaY(funcY=self.funcY, t=t)
    
    def plotTgs(self):
        for eixo,tg_list in self.__horTg.items():
            if eixo == 'Y':
                for tg in tg_list:
                    matplotlib.pyplot.axhline(y=tg, color='orange', alpha=1, linestyle='-.')

        for eixo,tg_list in self.__vertTg.items():
            if eixo == 'X':
                for tg in tg_list:
                    matplotlib.pyplot.axvline(x=tg, color='green', alpha=1, linestyle='-.')

    def plotCurva(self) -> None: 
        fig = matplotlib.pyplot.figure(facecolor='azure', figsize=(7,5))

        matplotlib.pyplot.plot(self.__lista_x, self.__lista_y)
        #plotar derivada
        # matplotlib.pyplot.plot(self.__lista_xl, self.__lista_yl, color='green')

        matplotlib.pyplot.scatter(self.__pxs, self.__pys, color='r', alpha=1, label='AutoIntersec')
        matplotlib.pyplot.scatter(self.__horTg['X'], self.__horTg['Y'], color='orange', label='Tg Horizontal')
        matplotlib.pyplot.scatter(self.__vertTg['X'], self.__vertTg['Y'], color='green', label='Tg Vertical')

        self.plotTgs()

        matplotlib.pyplot.title('Curva')
        matplotlib.pyplot.ylabel('Y')
        matplotlib.pyplot.xlabel('X')

        matplotlib.pyplot.xlim(min(self.__lista_x)-1, max(self.__lista_x)+1)
        matplotlib.pyplot.ylim(min(self.__lista_y)-1, max(self.__lista_y)+1)

        matplotlib.pyplot.grid(color='white')
        matplotlib.pyplot.axvspan(min(self.__lista_x)-1, max(self.__lista_x)+1, color='powderblue', alpha=0.6)
        matplotlib.pyplot.legend()
        matplotlib.pyplot.show()

        matplotlib.pyplot.savefig('static\curva_plot.png')  # Save the plot as a PNG file in the static directory

        # Clear the plot to release resources
        matplotlib.pyplot.close()

    def run(self) -> None:
        self.fazPontos()
        self.determinaIntersec()
        self.verificaTg()
        self.printaIntersec()
        self.printaHorTg()
        self.printaVertTg()
        self.plotCurva()
        
    