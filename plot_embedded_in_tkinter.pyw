
from tkinter import *
from tkinter.ttk import *
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import websocket 
import threading
import queue
import json
from binance.spot import Spot 

api_key    = 'rstEylR30Mv4UrRYsG0bNGqBrcF4ZEivJrCx9nmw8pcblK7cCFZzwTPLIHAzroC0';
api_secret = '0VAJaTsim0SUn7dDn5Npqs7sX9Prz67zsFv6p4l4pYw6WA2FTjG1R2cykU6QPZpH';
symbol=f"LTCBTC&side=BUY&type=LIMIT&timeInForce=GTC&quantity=1&price=0.1&recvWindow=5000&timestamp=1499827319559"


def schedule_check(task_connect):
	"""
	Programar la ejecución de la función `check_if_done()` dentro de 
	un segundo.
	"""
	#global window
	window.after(1200, check_if_done, task_connect)
def check_if_done(task_connect):
	# Si el hilo ha finalizado, restaruar el botón y mostrar un mensaje.
	global x,y,x_iter,y_iter,widget,toolbar,frame;			
	x_iter.append(x)
	y_iter.append(float(q.get()))	

	print(x_iter,y_iter)
	# remove old widgets
	if widget:
		widget.destroy()
	if toolbar:
		toolbar.destroy()
	

	# the figure that will contain the plot
	fig = plt.Figure(figsize = (1, 1), dpi = 80)

	# list of squares
	# adding the subplot
	plot_ = fig.add_subplot(1,1,1)
	plot_.set_ylabel("USD ($)")
	plot_.set_xlabel("Segundos (s)")
	
	
	#fig.add_subplot(233, projection='polar')  # polar subplot
	#fig.add_subplot(234)  # subplot sharing x-axis with ax1
	#fig.add_subplot(235, facecolor="red")  # red subplot

	if(len(x_iter) >= 31):
		del x_iter[0];
		del y_iter[0];
		if(len(x_iter) == 30):
			plot_.set_xlim([x_iter[0],x_iter[29]])
	else:
		plot_.set_xlim([0, 30])
	#plot_.set_ylim([0.99*y_iter[0] ,1.01*y_iter[0]])
	# plotting the graph	
	plot_.plot(x_iter,y_iter, color='blue', marker='o', linestyle='solid',linewidth=2, markersize=3)
	fig.legend(['BitCoin'], loc='upper right')
	# creating the Tkinter canvas
	# containing the Matplotlib figure
	canvas = FigureCanvasTkAgg(fig,master = window)  
	canvas.draw()  
	# placing the canvas on the Tkinter window
	canvas.get_tk_widget().place(x=10, y=10, width=500, height=500)
	# creating the Matplotlib toolbar
	toolbar = NavigationToolbar2Tk(canvas, window)	
	toolbar.update()  
	x+=1;	
	# Si no, volver a chequear en unos momentos.
	schedule_check(task_connect)


def init_graphics():
	global  x_iter,y_iter,plot_,widget,toolbar,frame;
	# the figure that will contain the plot	

	fig = plt.Figure(figsize = (1, 1), dpi = 80)
	# list of squares
	# adding the subplot
	fig.legend(['single element'])
	plot_ = fig.subplots()
	#plot_ = fig.add_axes([0.1, 0.1, 0.6, 0.75])
	plot_.set_xlim([0, 30])
	plot_.set_ylabel("USD ($)")
	plot_.set_xlabel("Segundos (s)")
	
	# plotting the graph
	plot_.plot(x_iter,y_iter, color='blue', marker='o', linestyle='solid', linewidth=2, markersize=3)
	fig.legend(['BitCoin'], loc='upper right')
	# creating the Tkinter canvas
	# containing the Matplotlib figure
	canvas = FigureCanvasTkAgg(fig,master = window)  
	canvas.draw()  
	# placing the canvas on the Tkinter window
	widget = canvas.get_tk_widget().place(x=10, y=10, width=500, height=500)
	# creating the Matplotlib toolbar
	toolbar = NavigationToolbar2Tk(canvas, window)
	#toolbar.pack()
	toolbar.update() 
def BinanceConnect(q):    
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
    ws.run_forever();

def on_message(ws,message):
    global valor_
    try:        
        valor_ = message[message.index("c")+3 : message.index("h")-2]# message[141:157];
        print(json.loads(message)) 
        #print(valor_[1:11])        
        q.put(valor_[1:11])
        #caja.insert(END,valor_);     
    except Exception as e:
        raise print(e) 

def on_close(ws,message):
    pass

def on_open(ws):
    print("opened")
	

def Grafica_main(q):
	global window
	window = Tk();	
	#window.resizable(False, False)
	window.geometry('520x580');#('560x400');
	window.iconbitmap('logo_icono.ico')
	window.title("Trader - Binance");
	
	task_connect = threading.Thread(target=BinanceConnect,args=(q,)); #puertos disponibles  
	task_connect.start();
	
	init_graphics()
	schedule_check(task_connect)




	window.mainloop()



if __name__ == "__main__":
	x=0;y=0;x_iter = [];y_iter = [];
	q = queue.Queue(maxsize=0); 

	socket = f'wss://stream.binance.com:9443/ws/btcusdt@kline_1m';
	socket1 = f'wss://stream.binance.com:9443/ws'
	Grafica_main(q);
