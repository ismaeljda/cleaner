#!/usr/bin/env python3
import sys
import random
import time
import os
from threading import Timer

# Essaie d'importer PyQt5 ou PySide2
try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                 QHBoxLayout, QLabel, QPushButton, QFrame, QMessageBox, QDesktopWidget)
    from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QRect, QEasingCurve
    from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor
    QT_AVAILABLE = "PyQt5"
except ImportError:
    try:
        from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                                       QHBoxLayout, QLabel, QPushButton, QFrame, QMessageBox, QDesktopWidget)
        from PySide2.QtCore import Qt, QTimer, Signal as pyqtSignal, QPropertyAnimation, QRect, QEasingCurve
        from PySide2.QtGui import QPixmap, QFont, QPalette, QColor
        QT_AVAILABLE = "PySide2"
    except ImportError:
        print("❌ Ni PyQt5 ni PySide2 ne sont installés!")
        print("Installez l'un d'eux avec:")
        print("  pip install PyQt5")
        print("  ou")
        print("  pip install PySide2")
        sys.exit(1)

# Configuration
IMAGE_PATH = "image.jpg"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

class LinuxTrollWindow(QMainWindow):
    restart_signal = pyqtSignal()
    
    def __init__(self, parent_pos=None):
        super().__init__()
        self.is_running = True
        self.blink_timer = QTimer()
        self.top_timer = QTimer()
        self.shake_timer = QTimer()
        self.title_red = True
        self.original_pos = None
        self.shake_intensity = 15
        self.parent_pos = parent_pos
        
        # Liste des fenêtres enfants créées
        self.child_windows = []
        
        # Connecte le signal de redémarrage
        self.restart_signal.connect(self.restart_window)
        
        self.setup_window()
        self.create_interface()
        self.start_effects()
    
    def setup_window(self):
        """Configure la fenêtre principale"""
        self.setWindowTitle("⚠️ ALERTE SÉCURITÉ CRITIQUE ⚠️")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Position de la fenêtre
        if self.parent_pos:
            # Position décalée par rapport à la fenêtre parent
            offset_x = random.randint(-200, 200)
            offset_y = random.randint(-150, 150)
            x = max(0, min(self.parent_pos[0] + offset_x, 
                          QApplication.desktop().width() - WINDOW_WIDTH))
            y = max(0, min(self.parent_pos[1] + offset_y, 
                          QApplication.desktop().height() - WINDOW_HEIGHT))
        else:
            # Centre la première fenêtre
            screen = QApplication.desktop().screenGeometry()
            x = (screen.width() - WINDOW_WIDTH) // 2
            y = (screen.height() - WINDOW_HEIGHT) // 2
        
        self.move(x, y)
        self.original_pos = (x, y)
        
        # Style sombre
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QWidget {
                background-color: #1a1a1a;
                color: white;
            }
        """)
        
        # Garde au premier plan
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Window)
        
        # Empêche la fermeture normale
        self.setAttribute(Qt.WA_QuitOnClose, False)
    
    def create_interface(self):
        """Crée l'interface utilisateur"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Frame principal avec bordure rouge
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border: 5px solid red;
                margin: 10px;
            }
        """)
        main_layout.addWidget(main_frame)
        
        frame_layout = QVBoxLayout()
        main_frame.setLayout(frame_layout)
        
        # Titre principal
        self.title_label = QLabel("🚨 SYSTÈME COMPROMIS 🚨")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("DejaVu Sans", 28, QFont.Bold))
        self.title_label.setStyleSheet("color: #ff0000; margin: 20px;")
        frame_layout.addWidget(self.title_label)
        
        # Sous-titre
        subtitle = QLabel("ACCÈS NON AUTORISÉ DÉTECTÉ")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("DejaVu Sans", 16, QFont.Bold))
        subtitle.setStyleSheet("color: #ffff00; margin-bottom: 20px;")
        frame_layout.addWidget(subtitle)
        
        # Layout horizontal pour image et détails
        content_layout = QHBoxLayout()
        frame_layout.addLayout(content_layout)
        
        # Section image
        self.create_image_section(content_layout)
        
        # Section détails
        self.create_details_section(content_layout)
        
        # Boutons
        self.create_buttons(frame_layout)
    
    def create_image_section(self, layout):
        """Crée la section image"""
        image_widget = QWidget()
        image_layout = QVBoxLayout()
        image_widget.setLayout(image_layout)
        
        # Essaie de charger l'image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, IMAGE_PATH)
        
        if os.path.exists(image_path):
            try:
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    # Redimensionne l'image
                    scaled_pixmap = pixmap.scaled(600, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    
                    # Frame avec bordure rouge pour l'image
                    img_frame = QFrame()
                    img_frame.setStyleSheet("border: 3px solid red; background-color: black;")
                    img_frame_layout = QVBoxLayout()
                    img_frame.setLayout(img_frame_layout)
                    
                    img_label = QLabel()
                    img_label.setPixmap(scaled_pixmap)
                    img_label.setAlignment(Qt.AlignCenter)
                    img_frame_layout.addWidget(img_label)
                    
                    image_layout.addWidget(img_frame)
                    layout.addWidget(image_widget)
                    return
            except Exception as e:
                print(f"Erreur de chargement de l'image : {e}")
        
        # Image ASCII de remplacement
        ascii_art = """
    ⚠️  DANGER  ⚠️
   ╔══════════════╗
   ║   SYSTÈME   ║
   ║ COMPROMIS ! ║
   ║             ║
   ║    💀👨‍💻💀    ║
   ║             ║
   ║   HACKEUR   ║
   ║   DÉTECTÉ   ║
   ╚══════════════╝
    🚨  URGENT  🚨"""
        
        ascii_label = QLabel(ascii_art)
        ascii_label.setAlignment(Qt.AlignCenter)
        ascii_label.setFont(QFont("Courier", 12, QFont.Bold))
        ascii_label.setStyleSheet("color: red; background-color: black; padding: 20px;")
        image_layout.addWidget(ascii_label)
        
        layout.addWidget(image_widget)
    
    def create_details_section(self, layout):
        """Crée la section détails système"""
        details_frame = QFrame()
        details_frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border: 2px solid gray;
                border-radius: 5px;
            }
        """)
        details_layout = QVBoxLayout()
        details_frame.setLayout(details_layout)
        
        # Titre des détails
        details_title = QLabel("📊 RAPPORT DE SÉCURITÉ LINUX")
        details_title.setAlignment(Qt.AlignCenter)
        details_title.setFont(QFont("DejaVu Sans", 14, QFont.Bold))
        details_title.setStyleSheet("color: #00ff00; margin: 10px;")
        details_layout.addWidget(details_title)
        
        # Informations système
        try:
            username = os.getenv('USER', 'unknown')
            hostname = os.uname().nodename
            system = os.uname().sysname
        except:
            username = 'user'
            hostname = 'localhost'
            system = 'Linux'
        
        info_text = f"""🔴 STATUS: SYSTEM PWNED
🕒 TIME: {time.strftime("%H:%M:%S")}
🌐 TARGET: {username}@{hostname}
🖥️  SYSTEM: {system}
📡 IP SRC: 192.168.1.{random.randint(1, 254)}
🔑 ROOT: {random.choice(['YES', 'PENDING', 'ACQUIRED'])}
⚡ PID: {random.randint(1000, 9999)}

⚠️ COMPROMISED DATA:
• ~/.ssh/id_rsa (Private Keys)
• ~/.bash_history (Commands)  
• ~/Documents (Personal Files)
• Browser passwords & cookies
• /etc/shadow (System Hashes)

🚨 MALICIOUS ACTIVITIES:
• Reverse shell established
• Keylogger active
• Network traffic sniffed
• Privilege escalation
• Data exfiltration in progress

💀 YOU'VE BEEN PWNED! 💀
Root access: COMPROMISED"""
        
        info_label = QLabel(info_text)
        info_label.setFont(QFont("Courier", 9))
        info_label.setStyleSheet("color: white; padding: 15px; background-color: #2a2a2a;")
        info_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        details_layout.addWidget(info_label)
        
        layout.addWidget(details_frame)
    
    def create_buttons(self, layout):
        """Crée les boutons d'action"""
        button_layout = QHBoxLayout()
        
        # Bouton principal
        main_button = QPushButton("🔒 SECURE SYSTEM NOW")
        main_button.setFont(QFont("DejaVu Sans", 14, QFont.Bold))
        main_button.setStyleSheet("""
            QPushButton {
                background-color: #ff0000;
                color: white;
                padding: 10px 30px;
                border: 3px solid darkred;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #cc0000;
            }
        """)
        main_button.clicked.connect(self.fake_security_action)
        button_layout.addWidget(main_button)
        
        # Bouton secondaire
        alt_button = QPushButton("❌ IGNORE (RISKY)")
        alt_button.setFont(QFont("DejaVu Sans", 12))
        alt_button.setStyleSheet("""
            QPushButton {
                background-color: #444444;
                color: white;
                padding: 8px 20px;
                border: 2px solid #666666;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        alt_button.clicked.connect(self.fake_ignore_action)
        button_layout.addWidget(alt_button)
        
        # Bouton Linux
        linux_button = QPushButton("🐧 RUN CLEANUP")
        linux_button.setFont(QFont("DejaVu Sans", 12))
        linux_button.setStyleSheet("""
            QPushButton {
                background-color: #0066cc;
                color: white;
                padding: 8px 20px;
                border: 2px solid #0044aa;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0055bb;
            }
        """)
        linux_button.clicked.connect(self.fake_linux_action)
        button_layout.addWidget(linux_button)
        
        layout.addLayout(button_layout)
    
    def start_effects(self):
        """Démarre les effets visuels"""
        if not self.is_running:
            return
        
        # Timer pour le clignotement du titre
        self.blink_timer.timeout.connect(self.blink_title)
        self.blink_timer.start(800)
        
        # Timer pour rester au premier plan
        self.top_timer.timeout.connect(self.keep_on_top)
        self.top_timer.start(2000)
    
    def start_screen_shake(self):
        """Démarre l'effet de tremblement de l'écran"""
        if not self.is_running or not self.original_pos:
            return
        
        self.shake_timer.timeout.connect(self.shake_screen)
        self.shake_timer.start(50)  # Tremblement rapide
        
        # Arrête le tremblement après 3 secondes
        QTimer.singleShot(3000, self.stop_screen_shake)
    
    def shake_screen(self):
        """Fait trembler la fenêtre"""
        if not self.is_running or not self.original_pos:
            return
        
        # Calcule une position aléatoire autour de la position originale
        shake_x = random.randint(-self.shake_intensity, self.shake_intensity)
        shake_y = random.randint(-self.shake_intensity, self.shake_intensity)
        
        new_x = self.original_pos[0] + shake_x
        new_y = self.original_pos[1] + shake_y
        
        # S'assure que la fenêtre reste dans l'écran
        screen = QApplication.desktop().screenGeometry()
        new_x = max(0, min(new_x, screen.width() - WINDOW_WIDTH))
        new_y = max(0, min(new_y, screen.height() - WINDOW_HEIGHT))
        
        self.move(new_x, new_y)
    
    def stop_screen_shake(self):
        """Arrête l'effet de tremblement"""
        if self.shake_timer.isActive():
            self.shake_timer.stop()
        
        # Remet la fenêtre à sa position originale
        if self.original_pos:
            self.move(self.original_pos[0], self.original_pos[1])
    
    def multiply_windows(self, count=5):
        """Crée plusieurs fenêtres supplémentaires"""
        current_pos = (self.x(), self.y())
        
        for i in range(count):
            try:
                # Crée une nouvelle fenêtre avec une position décalée
                new_window = LinuxTrollWindow(parent_pos=current_pos)
                new_window.show()
                self.child_windows.append(new_window)
                
                # Ajoute un petit délai pour l'effet visuel
                QTimer.singleShot(100 * i, lambda w=new_window: w.start_screen_shake())
                
            except Exception as e:
                print(f"Erreur lors de la création d'une fenêtre: {e}")
                break
    
    def blink_title(self):
        """Fait clignoter le titre"""
        if not self.is_running:
            return
        
        color = "#ff0000" if self.title_red else "#ffff00"
        self.title_label.setStyleSheet(f"color: {color}; margin: 20px;")
        self.title_red = not self.title_red
    
    def keep_on_top(self):
        """Maintient la fenêtre au premier plan"""
        if not self.is_running:
            return
        
        self.raise_()
        self.activateWindow()
    
    def fake_security_action(self):
        """Simule une action de sécurité"""
        # Démarre le tremblement
        self.start_screen_shake()
        
        msg = QMessageBox(self)
        msg.setWindowTitle("SCANNING SYSTEM")
        msg.setText("🔄 Running security scan...\n\n"
                   "⚠️ NEW THREATS DETECTED ⚠️\n\n"
                   "Additional vulnerabilities found!\n\n"
                   "🐧 This is a harmless prank! 😄")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        
        # Multiplie les fenêtres
        self.multiply_windows(3)
        
        self.restart_popup()
    
    def fake_ignore_action(self):
        """Simule l'action d'ignorer"""
        # Démarre le tremblement intense
        self.shake_intensity = 25
        self.start_screen_shake()
        
        msg = QMessageBox(self)
        msg.setWindowTitle("CRITICAL ERROR")
        msg.setText("🚨 WARNING! 🚨\n\n"
                   "Ignoring security alerts puts your system at EXTREME RISK!\n\n"
                   "🔥 ACTIVE THREATS DETECTED 🔥\n\n"
                   "Restarting security scan...\n\n"
                   "😈 You've been TROLLED! 😈")
        msg.setIcon(QMessageBox.Critical)
        msg.exec_()
        
        # Multiplie encore plus les fenêtres
        self.multiply_windows(4)
        
        self.restart_popup()
    
    def fake_linux_action(self):
        """Action spéciale Linux"""
        # Tremblement modéré
        self.shake_intensity = 20
        self.start_screen_shake()
        
        msg = QMessageBox(self)
        msg.setWindowTitle("LINUX CLEANUP")
        msg.setText("🐧 Running Linux system cleanup...\n\n"
                   "$ sudo rm -rf /* --no-preserve-root\n"
                   "Just kidding! 😂\n\n"
                   "🎭 This is just a harmless troll!\n\n"
                   "Your Linux system is perfectly safe! 🛡️\n\n"
                   "But the popup will return anyway... 😈")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        
        # Multiplie les fenêtres
        self.multiply_windows(2)
        
        self.restart_popup()
    
    def restart_popup(self):
        """Redémarre la popup"""
        # Utilise un timer pour éviter les problèmes de threading
        QTimer.singleShot(1000, self.restart_signal.emit)
    
    def restart_window(self):
        """Redémarre la fenêtre"""
        if not self.is_running:
            return
        
        # Crée une nouvelle instance
        current_pos = (self.x(), self.y())
        new_window = LinuxTrollWindow(parent_pos=current_pos)
        new_window.show()
        
        # Ferme la fenêtre actuelle
        self.close()
    
    def closeEvent(self, event):
        """Gère les tentatives de fermeture - MULTIPLICATION DES FENÊTRES!"""
        # EFFET SPÉCIAL: Multiplie les fenêtres de manière agressive
        self.multiply_windows(random.randint(6, 10))
        
        # Tremblement intense pour toutes les nouvelles fenêtres
        for window in self.child_windows[-5:]:  # Les 5 dernières créées
            if window and hasattr(window, 'start_screen_shake'):
                QTimer.singleShot(random.randint(100, 500), window.start_screen_shake)
        
        msg = QMessageBox(self)
        msg.setWindowTitle("CANNOT CLOSE")
        msg.setText("🚨 CRITICAL ALERT ACTIVE 🚨\n\n"
                   "This window cannot be closed until\n"
                   "security issues are resolved!\n\n"
                   "🐧 Welcome to Linux trolling! 😄\n\n"
                   "💥 MULTIPLYING WINDOWS! 💥")
        msg.setIcon(QMessageBox.Warning)
        
        # Fait trembler cette fenêtre pendant que le message s'affiche
        self.shake_intensity = 30
        self.start_screen_shake()
        
        msg.exec_()
        
        event.ignore()  # Empêche la fermeture
        self.restart_popup()
    
    def stop_troll(self):
        """Arrête le troll proprement"""
        self.is_running = False
        self.blink_timer.stop()
        self.top_timer.stop()
        if hasattr(self, 'shake_timer'):
            self.shake_timer.stop()
        
        # Ferme toutes les fenêtres enfants
        for window in self.child_windows:
            if window:
                try:
                    window.stop_troll()
                    window.close()
                except:
                    pass

class LinuxTrollApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)  # Empêche la fermeture automatique
        
        # Style global sombre
        self.app.setStyle('Fusion')
        palette = self.app.palette()
        palette.setColor(QPalette.Window, QColor(26, 26, 26))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        self.app.setPalette(palette)
        
        self.window = LinuxTrollWindow()
        self.window.show()
        
        # Démarre un tremblement initial léger après 2 secondes
        QTimer.singleShot(2000, self.window.start_screen_shake)
    
    def run(self):
        """Lance l'application"""
        return self.app.exec_()

# Lancement du programme
if __name__ == "__main__":
    print(f"🐧 Linux Troll Popup starting with {QT_AVAILABLE}...")
    print("🛑 Close terminal or press Ctrl+C to stop")
    
    try:
        app = LinuxTrollApp()
        sys.exit(app.run())
    except KeyboardInterrupt:
        print("\n🛑 Troll stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)