from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile 
import time
import hashlib
import os

ws = Tk()
ws.title('PythonGuides')
ws.geometry('400x200') 


def open_file1():
    global file_path1, filepath1
    file_path1 = askopenfile(mode='r', filetypes=[('ALL files', '*.*')])
    if file_path1 is not None:
        filepath1 = os.path.abspath(file_path1.name)
        Label(ws, text='File1!', foreground='green', justify="right").grid(row=0, column=2, padx=30)
        pass

def open_file2():
    global file_path2, filepath2
    file_path2 = askopenfile(mode='r', filetypes=[('ALL files', '*.*')])
    if file_path2 is not None:
        filepath2 = os.path.abspath(file_path2.name)
        Label(ws, text='File2!', foreground='green', justify="right").grid(row=1, column=2, padx=30)
        pass


def uploadFiles():
    pb1 = Progressbar(
        ws, 
        orient=HORIZONTAL, 
        length=300, 
        mode='determinate'
        )
    pb1.grid(row=4, columnspan=3, pady=20)
    for i in range(5):
        ws.update_idletasks()
        pb1['value'] += 20
        time.sleep(1)
    pb1.destroy()
    Label(ws, text='File Uploaded Successfully!', foreground='green').grid(row=4, columnspan=3, pady=10)

    #original_sha512 = '70cd37d0c0b25d3b6038d3f8229a1d735ff50a9e94ca97861d4f1117b0810b2c421dacee603f22f52cfef3ef197abd38c759e8877230f531674a946196cde6df'
def check_hash512():
    global file_path1, file_path2
    with open(filepath1, 'rb') as f:
        data1 = f.read()
        sha512_hash = hashlib.sha3_512(data1).hexdigest()

    with open(filepath2, 'rb') as f:
        data2 = f.read()
        sha512_returned = hashlib.sha3_512(data2).hexdigest()

    if sha512_hash == sha512_returned:
        Label(ws, text='SHA3-512 verified!', foreground='green').grid(row=4, columnspan=3, pady=10)
        print("Nilai Hash File 1: ", sha512_hash)
        print("Nilai Hash File 2: ", sha512_returned)
    else:
        Label(ws, text='SHA3-512 verification failed!', foreground='green').grid(row=4, columnspan=3, pady=10)
        print("Nilai Hash File 1: ", sha512_hash)
        print("Nilai Hash File 2: ", sha512_returned)

adhar = Label(
    ws, 
    text='Upload file 1'
    )
adhar.grid(row=0, column=0, padx=30)

adharbtn = Button(
    ws, 
    text ='Choose File', 
    command = lambda:open_file1()
    ) 
adharbtn.grid(row=0, column=1)

dl = Label(
    ws, 
    text='Upload file 2'
    )
dl.grid(row=1, column=0, padx=30)

dlbtn = Button(
    ws, 
    text ='Choose File ', 
    command = lambda:open_file2()
    ) 
dlbtn.grid(row=1, column=1)

upld = Button(
    ws, 
    text='Check Hash512', 
    command=check_hash512
    )
upld.grid(row=2, columnspan=3, pady=30)



ws.mainloop()