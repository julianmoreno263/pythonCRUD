from tkinter import *
from tkinter import messagebox
import sqlite3

#------ funciones --------------------

def conexionBd():
    miConexion=sqlite3.connect('Usuarios')
    miCursor=miConexion.cursor()
    
    try:
        miCursor.execute('''
                        create table datosusuarios(
                            id integer primary key autoincrement,
                            nombreusuario varchar(50),
                            password varchar(50),
                            apellido varchar(10),
                            direccion varchar(50),
                            comentario varchar(100)
                        )''')
        
        messagebox.showinfo('BBDD', 'BBDD creada con exito!')
    
    except:
        messagebox.showwarning('!Atencion!','La BBDD ya existe!')
        
def salirAplicacion():
    valor=messagebox.askquestion('Salir','Deseas salir de la aplicacion?')
    
    if valor=='yes':
        root.destroy()
    

def limpiarCampos():
    miId.set('')
    miNombre.set('')
    miPass.set('')
    miApellido.set('')
    miDireccion.set('')
    textoComentario.delete(1.0,END)
    
def crear():
    miConexion=sqlite3.connect('Usuarios')
    miCursor=miConexion.cursor()
    
    #creamos una consulta parametrizada para evitar sqlinyection
    datos=miNombre.get(),miPass.get(),miApellido.get(),miDireccion.get(),textoComentario.get(1.0,END)
    miCursor.execute("insert into datosusuarios values(null,?,?,?,?,?)",(datos))
    miConexion.commit()
    messagebox.showinfo('BBDD', 'Registro insertado con exito!')
    
def leer():
    miConexion=sqlite3.connect('Usuarios')
    miCursor=miConexion.cursor()
    
    #fetchall nos trae todo en un array para poder recorrerlo
    miCursor.execute("select * from datosusuarios where id=" + miId.get())
    elUsuario=miCursor.fetchall()
    for usuario in elUsuario:
        miId.set(usuario[0])
        miNombre.set(usuario[1])
        miPass.set(usuario[2])
        miApellido.set(usuario[3])
        miDireccion.set(usuario[4])
        textoComentario.insert(1.0,usuario[5])
        
    miConexion.commit()
    
def actualizar():
    miConexion=sqlite3.connect('Usuarios')
    miCursor=miConexion.cursor()
    
    #creamos una consulta parametrizada para evitar sqlinyection
    datos=miNombre.get(),miPass.get(),miApellido.get(),miDireccion.get(),textoComentario.get(1.0,END)
    miCursor.execute("update datosusuarios set nombreusuario=?,password=?,apellido=?,direccion=?,comentario=? where id=" + miId.get(),(datos))
    miConexion.commit()
    messagebox.showinfo('BBDD', 'Registro actualizado con exito!')
    
def eliminar():
    miConexion=sqlite3.connect('Usuarios')
    miCursor=miConexion.cursor()
    
    miCursor.execute("delete from datosusuarios where id=" + miId.get())
    miConexion.commit()
    messagebox.showinfo('BBDD', 'Registro eliminado con exito!')
    
def licencia():
    messagebox.showinfo('BBDD', 'Licencia GNU open source!')
    
def version():
    messagebox.showinfo('BBDD', 'App Tkinter version 0.1')
    
    
    


#---- root de tkinter --------
root=Tk()

#-------  menu ------
barraMenu=Menu(root)
root.config(menu=barraMenu,width=300,height=300)

bbddMenu=Menu(barraMenu,tearoff=0)
bbddMenu.add_command(label='Conectar',command=conexionBd)
bbddMenu.add_command(label='Salir',command=salirAplicacion)

borrarMenu=Menu(barraMenu,tearoff=0)
borrarMenu.add_command(label='Borrar campos',command=limpiarCampos)

crudMenu=Menu(barraMenu,tearoff=0)
crudMenu.add_command(label='Crear',command=crear)
crudMenu.add_command(label='Leer',command=leer)
crudMenu.add_command(label='Actualizar',command=actualizar)
crudMenu.add_command(label='Borrar',command=eliminar)

ayudaMenu=Menu(barraMenu,tearoff=0)
ayudaMenu.add_command(label='Licencia',command=licencia)
ayudaMenu.add_command(label='Acerca de...',command=version)

barraMenu.add_cascade(label='BBDD',menu=bbddMenu)
barraMenu.add_cascade(label='BORRAR',menu=borrarMenu)
barraMenu.add_cascade(label='CRUD',menu=crudMenu)
barraMenu.add_cascade(label='AYUDA',menu=ayudaMenu)

# ----- frame principal de 6 filas y dos columnas para el formulario ------

miFrame=Frame(root)
miFrame.pack()

#-- variables de tipo stringvar para poder capturar lo que este en cada campo tipo Entry
miId=StringVar()
miNombre=StringVar()
miPass=StringVar()
miApellido=StringVar()
miDireccion=StringVar()


idLabel=Label(miFrame,text='Id:')
idLabel.grid(row=0,column=0,sticky='e',padx=10,pady=10)
cuadroId=Entry(miFrame,textvariable=miId)
cuadroId.grid(row=0,column=1,padx=10,pady=10)

nombreLabel=Label(miFrame,text='Nombre:')
nombreLabel.grid(row=1,column=0,sticky='e',padx=10,pady=10)
cuadroNombre=Entry(miFrame,textvariable=miNombre)
cuadroNombre.grid(row=1,column=1,padx=10,pady=10)
cuadroNombre.config(fg='red',justify='right')

passLabel=Label(miFrame,text='Password:')
passLabel.grid(row=2,column=0,sticky='e',padx=10,pady=10)
cuadroPass=Entry(miFrame,textvariable=miPass)
cuadroPass.grid(row=2,column=1,padx=10,pady=10)
cuadroPass.config(show='*')

apellidoLabel=Label(miFrame,text='Apellido:')
apellidoLabel.grid(row=3,column=0,sticky='e',padx=10,pady=10)
cuadroApellido=Entry(miFrame,textvariable=miApellido)
cuadroApellido.grid(row=3,column=1,padx=10,pady=10)

direccionLabel=Label(miFrame,text='Direccion:')
direccionLabel.grid(row=4,column=0,sticky='e',padx=10,pady=10)
cuadroDireccion=Entry(miFrame,textvariable=miDireccion)
cuadroDireccion.grid(row=4,column=1,padx=10,pady=10)

comentariosLabel=Label(miFrame,text='Comentarios:')
comentariosLabel.grid(row=5,column=0,sticky='e',padx=10,pady=10)
textoComentario=Text(miFrame,width=16,height=5)
textoComentario.grid(row=5,column=1,padx=10,pady=10)
scrollVert=Scrollbar(miFrame,command=textoComentario.yview)
scrollVert.grid(row=5,column=2,sticky='nsew')
textoComentario.config(yscrollcommand=scrollVert.set)

#--- segundo frame para los botones inferiores ---------------

miFrame2=Frame(root)
miFrame2.pack()

botonCrear=Button(miFrame2,text='Create',cursor='hand2',command=crear)
botonCrear.grid(row=1,column=0,sticky='e',padx=10,pady=10)

botonLeer=Button(miFrame2,text='Read',cursor='hand2',command=leer)
botonLeer.grid(row=1,column=1,sticky='e',padx=10,pady=10)

botonActualizar=Button(miFrame2,text='Update',cursor='hand2',command=actualizar)
botonActualizar.grid(row=1,column=2,sticky='e',padx=10,pady=10)

botonBorrar=Button(miFrame2,text='Delete',cursor='hand2',command=eliminar)
botonBorrar.grid(row=1,column=3,sticky='e',padx=10,pady=10)









root.mainloop()