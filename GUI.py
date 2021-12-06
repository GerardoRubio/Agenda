from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class Ventana1(Tk):
    def __init__(self):
        super().__init__()
        self.title('Login')
        self.geometry('200x90')
        self.resizable(0,0)
        self.columnconfigure(0,weight=20)
        self.componentes()
        self.inicio()
        
    def componentes(self):
        self.clave=StringVar()
        self.usuario=StringVar()
        
        Label(self, text='Usuario', padx=2, pady=2).grid(column=0, row=0)
        Label(self, text='Clave', padx=2, pady=2).grid(column=0, row=1)
        
        Entry(self, textvariable=self.usuario).grid(column=1, row=0, sticky='nswe') #entrada usuario
        Entry(self, textvariable=self.clave, show='*').grid(column=1, row=1, sticky='nswe') #entrada clave
        
        Button(self, text='OK', command=lambda:self.abre()).grid(column=0, row=2, sticky='nswe')
        Button(self, text='Salir', command=lambda:self.destroy()).grid(column=1, row=2, sticky='nswe')
        
    def abre(self):
        if(self.clave.get() == 'admin' and self.usuario.get() == 'admin'):
            self.destroy()
            v2=Ventana2()
        if(self.Validar()):
            self.destroy()
            v3=Ventana3()
        else:
            print('Datos incorrectos')
    
    def Validar(self):
        if(len(self.usuario.get()) !=0 and len(self.clave.get()) !=0):
            a=self.clave.get()
            conexion=sqlite3.connect("Agenda.db")
            try:
                cursor=conexion.cursor()
                cursor.execute("SELECT  User  FROM Usuarios WHERE Password=?", (a,))
                dato=cursor.fetchone()
                
                cursor.execute("SELECT  idContacto  FROM Usuarios WHERE Password=?", (a,))
                datoId=cursor.fetchone()
                
                datoId=datoId[0]
                listaId.append(datoId)
                
                if(dato[0] == self.clave.get()):
                   conexion.close()
                   return True
            except Exception as e:
                print(e)
                return False
            finally:
                conexion.close()
        else:
            return False

    def inicio(self):
        self.mainloop()
#-*-*-*-*-Fin de clase Ventana1

class Ventana2(Tk):
    def __init__(self):
        super().__init__()
        self.title('Administracion')
        self.geometry('220x140')
        self.resizable(0,0)
        self.componentes()
        self.inicio()
        
    def inicio(self):
        self.mainloop()
        
    def componentes(self):
        self.clave=StringVar()
        self.clave2=StringVar()
        self.usuario=StringVar()
        self.nombre=StringVar()
        
        Label(self, text='Usuario', padx=2, pady=2).grid(column=0, row=0)
        Label(self, text='Clave', padx=2, pady=2).grid(column=0, row=1)
        Label(self, text='Confirmar Clave', padx=2, pady=2).grid(column=0, row=2)
        Label(self, text='Nombre', padx=2, pady=2).grid(column=0, row=3)
        self.mensaje=Label(self, text='', fg= 'red').grid(column=0, row=4) #error
        
        Entry(self, textvariable=self.usuario).grid(column=1, row=0) #entrada usuario
        Entry(self, textvariable=self.clave, show='*').grid(column=1, row=1) #entrada clave
        Entry(self, textvariable=self.clave2, show='*').grid(column=1, row=2) #entrada clave confirmar
        Entry(self, textvariable=self.nombre).grid(column=1, row=3) #entrada nombre
        
        Button(self, text='OK', command=lambda:self.Guardar()).grid(column=0, row=4, sticky='nswe')
        Button(self, text='Salir', command=lambda:self.Salir()).grid(column=1, row=4, sticky='nswe')
    
    def Guardar(self):
        passw=self.clave.get()
        passw2=self.clave2.get()
        user=self.usuario.get()
        nom=self.nombre.get()
        
        if(passw == passw2): #Se revisa si ambas contraseñas son iguales
            if(self.Validacion()):
                conexion=sqlite3.connect("Agenda.db")
                try:
                    cursor=conexion.cursor()
                    sql="insert into Usuarios(User,Password,Nombre) values (?,?,?)"
                    datos=(user,passw,nom)
                    cursor.execute(sql,datos)
                    conexion.commit()
                    conexion.close()
                    #limpiamos los entrys
                    self.nombre.set('')
                    self.clave.set('')
                    self.clave2.set('')
                    self.usuario.set('')
                except:
                    print('ERROR EN LA MATRIX, LLAMA A MORPHEO!!!')
                finally:
                    conexion.close()
            else:
                print('Contraseña distinta / elegir otra contraseña')
        
    def Validacion(self):
        # Aqui se valida que los campos no esten vacios
        return len(self.nombre.get()) !=0 and len(self.clave.get()) !=0 and len(self.usuario.get()) !=0 and self.clave.get() != 'admin'
        
    def Salir(self):
        self.destroy()
        v1=Ventana1()
#-*-*-*-*-Fin de clase Ventana2

class Ventana3(Tk):
    def __init__(self):
        super().__init__()
        self.title('Agenda')
        self.geometry('500x420')
        self.resizable(0,0)
        self.componentes()
        self.cargarDatos()
        self.inicio()
        
    def componentes(self):
        self.nombre=StringVar()
        self.telefono=StringVar()
        self.email=StringVar()
        self.direccion=StringVar()
        self.idUsuario=StringVar()
        self.infoSaludo=StringVar()
        
        self.idUsuario=int(listaId.pop(0))
        a=self.idUsuario
        conexion=sqlite3.connect("Agenda.db")
        cursor=conexion.cursor()
        cursor.execute("select Nombre from Usuarios where idContacto=?", (a, ))
        
        nombre=cursor.fetchone()
        self.infoSaludo='Hola ',nombre[0]
        
        Label(self, text=self.infoSaludo).grid(column=2, row=0)
        Label(self, text='Nombre',padx=5,pady=5,anchor='w').grid(column=0,row=0,sticky='ew')
        Label(self, text='Telefono',padx=5,pady=5,anchor='w').grid(column=0,row=1,sticky='ew')
        Label(self, text='Direccion',padx=5,pady=5,anchor='w').grid(column=0,row=2,sticky='ew')
        Label(self, text='Email',padx=5,pady=5,anchor='w').grid(column=0,row=3,sticky='ew')

        Entry(self, textvariable=self.nombre).grid(column=1,row=0)
        Entry(self, textvariable=self.telefono).grid(column=1,row=1)
        Entry(self, textvariable=self.direccion).grid(column=1,row=2)
        Entry(self, textvariable=self.email).grid(column=1,row=3)

        Button(self, text='Guardar',command=lambda:self.guardar()).grid(column=2,row=6,sticky='ew')
        Button(self, text='Eliminar',command=lambda:self.eliminar()).grid(column=1,row=8)
        Button(self, text='Salir',command=lambda:self.salir()).grid(column=3,row=8)

        self.listado=ttk.Treeview(self,show='headings')
        self.listado['columns']=('Nombre','Telefono','Direccion','Email')
        self.listado.grid(column=0,row=7,columnspan=5,sticky='ew',padx=5,pady=5)
        self.listado.column("Nombre",width=60)
        self.listado.column("Telefono",width=40)
        self.listado.column("Direccion",width=100)
        self.listado.column("Email",width=50)

        self.listado.heading("Nombre",text='Nombre', anchor=CENTER)
        self.listado.heading("Telefono",text='Telefono', anchor=CENTER)
        self.listado.heading("Direccion",text='Direccion', anchor=CENTER)
        self.listado.heading("Email",text='Email', anchor=CENTER)

    def cargarDatos(self):
        conexion=sqlite3.connect("Agenda.db")
        try:
            for i in self.listado.get_children():
                self.listado.delete(i)
            
            a=self.idUsuario
            cursor=conexion.cursor()
            cursor.execute("select * from Contactos where idUsuario = ? order by Nombre ASC", (a, ))
            filas=cursor.fetchall()
            
            for fila in filas:
                datos=(fila[2],fila[3],fila[4],fila[5])
                self.listado.insert('','end',iid=fila[0],values=datos)
        except Exception as e:
            print(e)
        finally:
            conexion.close()
    
    def guardar(self):
        nombre=self.nombre.get()
        telefono=self.telefono.get()
        email=self.email.get()
        direccion=self.direccion.get()
        aidi=IntVar()
        aidi=int(self.idUsuario)
        
        conexion=sqlite3.connect("Agenda.db")
        try:
            cursor=conexion.cursor()
            sql="insert into Contactos(idUsuario,Nombre,Telefono,Direccion,Email) values (?,?,?,?,?)"
            datos=(aidi,nombre,telefono,direccion,email)
            cursor.execute(sql,datos)
            conexion.commit()
            conexion.close()
            for i in self.listado.get_children():
                self.listado.delete(i)
            
            self.nombre.set('')
            self.telefono.set('')
            self.email.set('')
            self.direccion.set('')
            self.cargarDatos()
        except:
            print('Ya reprobaste we :C')
        finally:
            conexion.close()
    
    def eliminar(self):
        try:
            registro=self.listado.selection()[0]
            print(registro)
            Respuesta=messagebox.askretrycancel(message='¿Deseas eliminarlo?',title='CUIDADO!!!')
            if(Respuesta):
               conexion=sqlite3.connect("Agenda.db")
               cursor=conexion.cursor()
               sql="delete from Contactos where idContacto = ?"
               cursor.execute(sql,registro)
               conexion.commit()
               conexion.close()
               for i in self.listado.get_children():
                self.listado.delete(i)
               self.cargarDatos()
            else:
                print('No se elimino el contacto')
        except IndexError:
            messagebox.showinfo(message='Debes seleccionar un contacto',title='CUIDADO!!!')
    
    def salir(self):
        self.destroy()
        v1=Ventana1()
    
    def inicio(self):
        self.mainloop()
#-*-*-*-*-Fin de clase Ventana3

class crearBD():
        conexion=sqlite3.connect("Agenda.db")
        try:
            conexion.execute("""
                                create table Contactos (
                                    idContacto integer primary key autoincrement,
                                    idUsuario integer,
                                    Nombre text,
                                    Telefono text,
                                    Direccion text,
                                    Email text
                                )""")
            conexion.execute("""
                                create table Usuarios (
                                    idContacto integer primary key autoincrement,
                                    User text,
                                    Password text,
                                    Nombre text
                                )""")
            print('Se ha creado la BD agenda.db')
        except sqlite3.OperationalError:
            print('La tabla ya ha sido creada')
        finally:
            conexion.close()
#-*-*-*-*-Fin de clase base de datos

if(__name__=='__main__'):
    #db=crearBD()
    listaId=[] #aqui guardamos el indice
    ube=Ventana1()