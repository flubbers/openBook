#!/usr/python
# -*- coding: utf-8 -*-

import MySQLdb
from gi.repository import Gtk, GdkPixbuf, Gdk
import sys

class DB:
    conexion = None
    micursor = None

    def __init__(self):
        """Crea la base de datos"""	
        self.conexion = MySQLdb.connect('localhost','conan','crom','DBdeConan')
        self.micursor = self.conexion.cursor(MySQLdb.cursors.DictCursor)
        query = "CREATE TABLE book (id INT NOT NULL AUTO_INCREMENT, Nombre VARCHAR(100), Autor VARCHAR(100), Editorial VARCHAR(100), Anio INT(4), Formato VARCHAR(10), Genero VARCHAR(100),PRIMARY KEY (id) );"
        self.micursor.execute(query)
        self.conexion.commit()


    def destroy(self):
        """Destruye la base de datos"""
        self.conexion.commit()
        query = "DROP TABLE book;"
        self.micursor.execute(query)
        self.micursor.close()
        self.conexion.close()

class GUI:

    builder = ''
    db = None

    def __init__(self):
        self.db = DB()
        self.builder = Gtk.Builder()
        self.builder.add_from_file("openBook.glade")

        self.handlers = {
                        "onDeleteWindow": self.destroy,
                        "onAboutClick": self.onAboutClick,
                        "onAboutClose": self.onAboutClose,
                        "onLoadDB": self.onLoadDB,
                        "onDeleteDB":self.onDeleteDB,
                        "onMessageClose":self.onMessageClose,
                        "onButtonClick": self.onButtonClick,
                        "opcionCrear" : self.opcionCrear,
                        "opcionActualizar" : self.opcionActualizar,
                        "opcionBorrar" : self.opcionBorrar,
                        "opcionObtener" : self.opcionObtener,
                        "onSelectID" : self.onSelectID,
                        }
        
        self.builder.connect_signals(self.handlers)
        self.window = self.builder.get_object("window1")
        id = self.builder.get_object("label2")
        id.set_sensitive(False)
        idText = self.builder.get_object("entry1")
        idText.set_sensitive(False)
        self.window.show_all()

    def destroy(self,window):
        if self.db:
            self.db.destroy()
        Gtk.main_quit()

    def onLoadDB(self,window):
        """Crea Base de datos """
        self.db = DB()
        windows = self.builder.get_object("messagedialog1")
        mensaje = self.builder.get_object("label1")
        mensaje.set_label("Base de datos creado correctamente ")
        windows.show_all()

    def onDeleteDB(self,window):
        """ Elimina la base de datos """
        if self.db:
            self.db.destroy()
            self.db = None
            windows = self.builder.get_object("messagedialog1")
            mensaje = self.builder.get_object("label1")
            mensaje.set_label("Base de datos eliminada correctamente ")
            windows.show_all()

    def onMessageClose(self,button):
        self.about = self.builder.get_object("messagedialog1")
        self.about.hide()

    def onAboutClick(self,button):
        windows = self.builder.get_object("aboutdialog1")     
        windows.show_all()

    def onButtonClick(self,button):
        if (button.get_label() == "Crear"):
            print "inserta datos"
            self.insert()
            print "hace commit"
            self.db.conexion.commit()
            print "limpia entry"
            self.clean()

        elif (button.get_label() == "Borrar"):
            print "Borrar datos"
            self.delete()
            print "hace commit"
            self.db.conexion.commit()
            print "limpia entry"
            self.clean()

        elif (button.get_label() == "Actualizar"):
            print "Actualizar datos"
            self.update()
            print "hace commit"
            self.db.conexion.commit()
            print "limpia entry"
            self.clean()
        
        elif (button.get_label() == "Obtener"):
            print "Obtiene datos"
            print "hace commit"
            print "limpia entry"
            self.clean()

        elif (button.get_label() == "Cancelar"):
            self.clean()

        else:
            print "Boton pulsado pero no hace nada"

    def onAboutClose(self, *args):
        self.about = self.builder.get_object("aboutdialog1")
        self.about.hide()

    def opcionCrear(self,entry):
        id = self.builder.get_object("label2")
        id.set_sensitive(False)
        idText = self.builder.get_object("entry1")
        idText.set_sensitive(False)
        boton = self.builder.get_object("button3")
        boton.set_label("Crear")

    def opcionBorrar(self,entry):
        id = self.builder.get_object("label2")
        id.set_sensitive(True)
        idText = self.builder.get_object("entry1")
        idText.set_sensitive(True)
        boton = self.builder.get_object("button3")
        boton.set_label("Borrar")

        query = "SELECT id FROM book WHERE 1;"

        self.db.micursor.execute(query)
        id = self.db.micursor.fetchall()
        idText.remove_all()
        for i in id:
            idText.insert(-1,None,str(i['id']))

    def opcionObtener(self,entry):
        id = self.builder.get_object("label2")
        id.set_sensitive(True)
        idText = self.builder.get_object("entry1")
        idText.set_sensitive(True)
        boton = self.builder.get_object("button3")
        boton.set_label("Obtener")

        query = "SELECT id FROM book WHERE 1;"

        self.db.micursor.execute(query)
        id = self.db.micursor.fetchall()
        idText.remove_all()
        for i in id:
            idText.insert(-1,None,str(i['id']))

    def opcionActualizar(self,entry):
        id = self.builder.get_object("label2")
        id.set_sensitive(True)
        idText = self.builder.get_object("entry1")
        idText.set_sensitive(True)
        boton = self.builder.get_object("button3")
        boton.set_label("Actualizar")

        query = "SELECT id FROM book WHERE 1;"

        self.db.micursor.execute(query)
        id = self.db.micursor.fetchall()
        idText.remove_all()
        for i in id:
            idText.insert(-1,None,str(i['id']))

    def onSelectID(self,entry):
        idEntrada = self.builder.get_object("entry1")
        id = idEntrada.get_active_text()

        query = "SELECT Nombre ,Autor, Editorial ,Anio, Formato, Genero FROM book WHERE id="+ str(id) +";"
        self.db.micursor.execute(query)

        registros = self.db.micursor.fetchone()
        print registros

        nombreEntrada = self.builder.get_object("entry2")
        nombre = nombreEntrada.set_text(str(registros['Nombre']))

        autorEntrada = self.builder.get_object("entry3")
        autor = autorEntrada.set_text(str(registros['Autor']))

        editorialEntrada = self.builder.get_object("entry4")
        editorial = editorialEntrada.set_text(str(registros['Editorial']))

        anioEntrada = self.builder.get_object("entry5")
        anio = anioEntrada.set_text(str(registros['Anio']))

        tipoEntrada = self.builder.get_object("comboboxtext1")
        if (str(registros['Genero']) == "pdf"):
            opcion = 0
        else:
            opcion = 1

        tipo = tipoEntrada.set_active(opcion)

        generoEntrada = self.builder.get_object("comboboxtext2")
        if (str(registros['Formato']) == "desarrollo web"):
            opcion = 0
        else:
            opcion = 1

        genero = generoEntrada.set_active(opcion)

    def clean(self):
        idEntrada = self.builder.get_object("entry1")
        id = idEntrada.set_active(-1)

        nombreEntrada = self.builder.get_object("entry2")
        nombre = nombreEntrada.set_text("")

        autorEntrada = self.builder.get_object("entry3")
        autor = autorEntrada.set_text("")

        editorialEntrada = self.builder.get_object("entry4")
        editorial = editorialEntrada.set_text("")

        anioEntrada = self.builder.get_object("entry5")
        anio = anioEntrada.set_text("")

        tipoEntrada = self.builder.get_object("comboboxtext1")
        tipo = tipoEntrada.set_active(-1)

        generoEntrada = self.builder.get_object("comboboxtext2")
        genero = generoEntrada.set_active(-1)

    def update(self):
        idEntrada = self.builder.get_object("entry1")
        id = idEntrada.get_active_text()        
        
        nombreEntrada = self.builder.get_object("entry2")
        nombre = nombreEntrada.get_text()

        autorEntrada = self.builder.get_object("entry3")
        autor = autorEntrada.get_text()

        editorialEntrada = self.builder.get_object("entry4")
        editorial = editorialEntrada.get_text()

        anioEntrada = self.builder.get_object("entry5")
        anio = anioEntrada.get_text()

        tipoEntrada = self.builder.get_object("comboboxtext1")
        tipo = tipoEntrada.get_active_text()

        generoEntrada = self.builder.get_object("comboboxtext2")
        genero = generoEntrada.get_active_text()

        if (nombre == '' or autor == '' or editorial == '' or anio == '' or tipo =='' or genero ==''):
            self.mensajeError()
        else:
            #
            query = "update book set Nombre='" + str(nombre) + "' ,Autor='" + str(autor) + "',Editorial='" + str(editorial) + "',Anio='" + str(anio) + "' ,Formato='" + str(tipo) + "',Genero='" + str(genero) + "' where id='" + str(id) + "';"
            print query
            self.db.micursor.execute(query)
            self.mensajeOK()


    def delete(self):
        idEntrada = self.builder.get_object("entry1")
        id = idEntrada.get_active_text()
        query = "DELETE FROM book WHERE id="+str(id)+";"
        self.db.micursor.execute(query)
        self.mensajeOK()

    def insert(self):
        nombreEntrada = self.builder.get_object("entry2")
        nombre = nombreEntrada.get_text()

        autorEntrada = self.builder.get_object("entry3")
        autor = autorEntrada.get_text()

        editorialEntrada = self.builder.get_object("entry4")
        editorial = editorialEntrada.get_text()

        anioEntrada = self.builder.get_object("entry5")
        anio = anioEntrada.get_text()

        tipoEntrada = self.builder.get_object("comboboxtext1")
        tipo = tipoEntrada.get_active_text()

        generoEntrada = self.builder.get_object("comboboxtext2")
        genero = generoEntrada.get_active_text()

        if (nombre == '' or autor == '' or editorial == '' or anio == '' or tipo =='' or genero ==''):
            self.mensajeError()
        else:
            query = "INSERT INTO book (Nombre ,Autor, Editorial ,Anio, Formato, Genero) VALUES (\""+str(nombre)+"\",\""+str(autor)+"\",\""+str(editorial)+"\","+str(anio)+",\""+str(genero)+"\",\""+str(tipo)+"\");"
            self.db.micursor.execute(query)
            self.mensajeOK()

    def mensajeOK(self):
            windows = self.builder.get_object("messagedialog1")
            mensaje = self.builder.get_object("label1")
            mensaje.set_label("todo correcto")
            windows.show_all()

    def mensajeError(self):
            windows = self.builder.get_object("messagedialog1")
            mensaje = self.builder.get_object("label1")
            mensaje.set_label("Error")
            windows.show_all()

def main():
    app = GUI()
    Gtk.main()

if __name__ == "__main__":
    sys.exit(main())
def main():

    app = GUI()

    Gtk.main()

    # Destruye la DB
    db.destroy()




if __name__ == "__main__":
    sys.exit(main())