import gi
import shutil
gi.require_version('Notify', '0.7')
gi.require_version('Nautilus', '4.0')

from gi.repository import Nautilus, GObject, Notify 
from typing import List
from os.path import exists, join
from pathlib import Path

VALID_MIMETYPES = "application/vnd.comicbook-rar", "application/vnd.comicbook+zip", "inode/directory"


class Move2Comics(GObject.GObject, Nautilus.MenuProvider):

    def __init__(self):
        super().__init__()

    def menu_activate_cb(
         self,
         menu: Nautilus.MenuItem,
         file: Nautilus.FileInfo,
     ) -> None:
        if file.is_gone():
            return

        home = str(Path.home())       
        origen = file.get_location().get_path()
        destino = join(home, "Comics", file.get_name())
        
        Notify.init("moviendo2Comics")
        titulo = "Mover a ~/Comics"

        if not exists(destino):
            shutil.move(origen, destino)
            notificacion = Notify.Notification.new (titulo,
                                                 "%s movido" % file.get_name(),
                                                 "dialog-information")
            notificacion.set_urgency(0)
        else:
            notificacion = Notify.Notification.new (titulo,
                                                 "%s ya existe" % file.get_name(),
                                                 "dialog-error")
            notificacion.set_urgency(2)

        notificacion.show()

    def get_file_items(
        self,
        files: List[Nautilus.FileInfo],
        ) -> List[Nautilus.MenuItem]:
        if len(files) != 1:
            return []

        file = files[0]

        if not file.get_mime_type() in VALID_MIMETYPES:
            return []

        item = Nautilus.MenuItem(
            name="move2comics",
            label="Mover a Comics: %s" % file.get_name(),
            tip="Mover a Comics: %s" % file.get_name(),
        )
        item.connect("activate", self.menu_activate_cb, file)

        return [
            item,
        ]

    def get_background_items(
         self,
         current_folder: Nautilus.FileInfo,
     ) -> List[Nautilus.MenuItem]:
         return []
