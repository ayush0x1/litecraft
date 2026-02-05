import gi
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk, WebKit2
import subprocess
from os import system

class Welcome:
    def __init__(self):
        self.win = Gtk.Window(title="Welcome to LiteCraft")
        self.win.set_default_size(800, 500)
        self.win.connect("destroy", Gtk.main_quit)

        # Create manager FIRST
        manager = WebKit2.UserContentManager()
        manager.register_script_message_handler("installer")
        manager.connect("script-message-received::installer", self.on_message)

        # Create WebView with manager
        self.web = WebKit2.WebView.new_with_user_content_manager(manager)

        # Enable JS
        settings = self.web.get_settings()
        settings.set_property("enable-javascript", True)
        settings.set_property("allow-file-access-from-file-urls", True)
        settings.set_property("allow-universal-access-from-file-urls", True)

        self.win.add(self.web)
        self.web.load_uri("file:///usr/share/litecraft-welcome/index.html")

        self.win.show_all()

    def on_message(self, manager, message):
        #print("JS MESSAGE RECEIVED:", message.get_js_value().to_string())
        if message.get_js_value().to_string() == "start":
            self.launch_calamares()

    def launch_calamares(self):
        print("Launching Calamares")
        system("pkexec calamares")
        Gtk.main_quit()
#"pkexec", 
Welcome()
Gtk.main()
