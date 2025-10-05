#!/usr/bin/env python3
"""
HABICON - Space Habitat Designer
Complete Flow: Login → Dashboard → HabitatCreator → Simulation → Results
With Drag & Drop and Gamification
"""

import sys
import random
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class LoginWindow(QMainWindow):
    def __init__(self, app_controller):
        super().__init__()
        self.app = app_controller
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("🚀 HABICON - Mission Access Terminal")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                         stop:0 #0a0a0a, stop:1 #1a1a2e); }
            QLabel { color: #00d4ff; font-family: 'Consolas'; }
            QLineEdit { background: #16213e; color: #00d4ff; border: 2px solid #00d4ff; 
                       border-radius: 8px; padding: 10px; font-size: 14px; }
            QPushButton { background: #16213e; color: #00d4ff; border: 2px solid #00d4ff; 
                         border-radius: 8px; padding: 12px; font-size: 14px; font-weight: bold; }
            QPushButton:hover { background: #00d4ff; color: #0a0a0a; }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        header = QLabel("🚀 HABICON")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 36px; font-weight: bold; margin: 30px;")
        layout.addWidget(header)
        
        subtitle = QLabel("Space Habitat Designer & Controller")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; margin-bottom: 40px;")
        layout.addWidget(subtitle)
        
        form_widget = QWidget()
        form_widget.setMaximumWidth(400)
        form_layout = QVBoxLayout(form_widget)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        form_layout.addWidget(self.username_input)
        
        login_btn = QPushButton("🚀 Launch Mission")
        login_btn.clicked.connect(self.login)
        form_layout.addWidget(login_btn)
        
        layout.addWidget(form_widget, alignment=Qt.AlignCenter)
        layout.addStretch()
    
    def login(self):
        username = self.username_input.text() or "Commander"
        user_data = {'username': username, 'level': 1, 'missions': 0}
        self.app.show_dashboard(user_data)

class DashboardWindow(QMainWindow):
    def __init__(self, app_controller, user_data):
        super().__init__()
        self.app = app_controller
        self.user_data = user_data
        self.missions = self.get_nasa_missions()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("🎛️ NASA Mission Command Center")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                         stop:0 #0a0a0a, stop:1 #1a1a2e); }
            QLabel { color: #00d4ff; font-family: 'Consolas'; }
            QPushButton { background: #16213e; color: #00d4ff; border: 2px solid #00d4ff; 
                         border-radius: 8px; padding: 12px; font-size: 14px; font-weight: bold; }
            QPushButton:hover { background: #00d4ff; color: #0a0a0a; }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Header
        header = QLabel(f"🎛️ NASA Mission Command - Commander {self.user_data['username']}")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(header)
        
        # Progress info
        progress_info = QLabel(f"Level: {self.user_data.get('level', 1)} | Completed Missions: {self.user_data.get('missions_completed', 0)}")
        progress_info.setAlignment(Qt.AlignCenter)
        progress_info.setStyleSheet("font-size: 16px; margin: 10px; color: #ff6b35;")
        layout.addWidget(progress_info)
        
        # Mission grid
        missions_label = QLabel("🚀 NASA Mission Selection")
        missions_label.setAlignment(Qt.AlignCenter)
        missions_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 20px;")
        layout.addWidget(missions_label)
        
        # Create mission grid
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        grid_layout = QGridLayout(scroll_widget)
        
        for i, mission in enumerate(self.missions):
            mission_widget = self.create_mission_widget(mission, i)
            row = i // 3
            col = i % 3
            grid_layout.addWidget(mission_widget, row, col)
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        layout.addStretch()
    
    def get_nasa_missions(self):
        return [
            {
                'id': 1, 'name': 'ISS Training Module', 'level': 1, 'difficulty': 'Beginner',
                'description': 'Design a basic ISS-style module for crew training',
                'location': 'Low Earth Orbit', 'duration': '30 days', 'crew': 3,
                'requirements': ['Node (Unity)', 'Crew Quarters (COLPA)', 'Power & Thermal (ECLSS)'],
                'unlocked': True, 'completed': False
            },
            {
                'id': 2, 'name': 'Lunar Gateway Station', 'level': 2, 'difficulty': 'Intermediate',
                'description': 'Create a lunar orbit station for Moon missions',
                'location': 'Lunar Orbit', 'duration': '6 months', 'crew': 4,
                'requirements': ['Node (Unity)', 'Crew Quarters (COLPA)', 'Life Support (ECLSS)', 'Docking Port (PMA)'],
                'unlocked': self.user_data.get('missions_completed', 0) >= 1, 'completed': False
            },
            {
                'id': 3, 'name': 'Mars Transit Habitat', 'level': 3, 'difficulty': 'Advanced',
                'description': 'Design a long-duration habitat for Mars journey',
                'location': 'Deep Space', 'duration': '9 months', 'crew': 6,
                'requirements': ['Node (Unity)', 'Crew Quarters (COLPA)', 'Life Support (ECLSS)', 'Medical (Health Care)', 'Exercise (COLPA)'],
                'unlocked': self.user_data.get('missions_completed', 0) >= 2, 'completed': False
            },
            {
                'id': 4, 'name': 'Mars Surface Base', 'level': 4, 'difficulty': 'Expert',
                'description': 'Build a permanent Mars surface habitat',
                'location': 'Mars Surface', 'duration': '2 years', 'crew': 8,
                'requirements': ['Node (Unity)', 'Crew Quarters (COLPA)', 'Life Support (ECLSS)', 'Plant Production (VEG)', 'Airlock (Quest/EVA)'],
                'unlocked': self.user_data.get('missions_completed', 0) >= 3, 'completed': False
            },
            {
                'id': 5, 'name': 'Europa Research Station', 'level': 5, 'difficulty': 'Master',
                'description': 'Design a research station for Jupiter\'s moon Europa',
                'location': 'Europa Orbit', 'duration': '3 years', 'crew': 10,
                'requirements': ['Node (Unity)', 'Laboratory (Destiny)', 'Life Support (ECLSS)', 'Communications (Cupola)', 'Medical (Health Care)'],
                'unlocked': self.user_data.get('missions_completed', 0) >= 4, 'completed': False
            },
            {
                'id': 6, 'name': 'Deep Space Colony', 'level': 6, 'difficulty': 'Legendary',
                'description': 'Create a self-sustaining deep space colony',
                'location': 'Asteroid Belt', 'duration': '5 years', 'crew': 15,
                'requirements': ['All NASA modules required'],
                'unlocked': self.user_data.get('missions_completed', 0) >= 5, 'completed': False
            }
        ]
    
    def create_mission_widget(self, mission, index):
        widget = QWidget()
        widget.setFixedSize(400, 300)
        layout = QVBoxLayout(widget)
        
        # Mission status styling
        if not mission['unlocked']:
            widget.setStyleSheet("""
                QWidget { background: #2a2a2a; border: 2px solid #555; border-radius: 10px; }
                QLabel { color: #666; }
            """)
        elif mission['completed']:
            widget.setStyleSheet("""
                QWidget { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                         stop:0 #1a4a1a, stop:1 #2a6a2a); border: 2px solid #4CAF50; border-radius: 10px; }
            """)
        else:
            widget.setStyleSheet("""
                QWidget { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                         stop:0 #16213e, stop:1 #1a1a2e); border: 2px solid #00d4ff; border-radius: 10px; }
            """)
        
        # Mission header
        header_layout = QHBoxLayout()
        level_label = QLabel(f"Level {mission['level']}")
        level_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #ff6b35;")
        header_layout.addWidget(level_label)
        
        header_layout.addStretch()
        
        difficulty_label = QLabel(mission['difficulty'])
        difficulty_color = {'Beginner': '#4CAF50', 'Intermediate': '#FF9800', 'Advanced': '#FF5722', 'Expert': '#9C27B0', 'Master': '#F44336', 'Legendary': '#FFD700'}
        difficulty_label.setStyleSheet(f"font-size: 12px; font-weight: bold; color: {difficulty_color.get(mission['difficulty'], '#00d4ff')};")
        header_layout.addWidget(difficulty_label)
        
        layout.addLayout(header_layout)
        
        # Mission name
        name_label = QLabel(mission['name'])
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(name_label)
        
        # Mission details
        details = f"""
🌍 {mission['location']}
🕰️ {mission['duration']}
👥 {mission['crew']} crew
        """
        details_label = QLabel(details)
        details_label.setAlignment(Qt.AlignCenter)
        details_label.setStyleSheet("font-size: 12px; margin: 5px;")
        layout.addWidget(details_label)
        
        # Description
        desc_label = QLabel(mission['description'])
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("font-size: 11px; margin: 10px; color: #ccc;")
        layout.addWidget(desc_label)
        
        # Action button
        if not mission['unlocked']:
            btn = QPushButton("🔒 Locked")
            btn.setEnabled(False)
            btn.setStyleSheet("background: #555; color: #999; border: 1px solid #666;")
        elif mission['completed']:
            btn = QPushButton("✅ Completed")
            btn.clicked.connect(lambda: self.start_mission(mission))
            btn.setStyleSheet("background: #4CAF50; color: white; border: 1px solid #4CAF50;")
        else:
            btn = QPushButton("🚀 Start Mission")
            btn.clicked.connect(lambda: self.start_mission(mission))
            btn.setStyleSheet("background: #ff6b35; color: white; border: 1px solid #ff6b35; font-weight: bold;")
        
        layout.addWidget(btn)
        
        return widget
    
    def start_mission(self, mission):
        # Add mission data to user data
        self.user_data['current_mission'] = mission
        self.app.show_habitat_creator(self.user_data)

class DraggableModule(QLabel):
    def __init__(self, module_type, icon, parent=None):
        super().__init__(parent)
        self.module_type = module_type
        self.icon = icon
        self.setText(f"{icon} {module_type}")
        self.setFixedSize(120, 60)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            background: #ff6b35; 
            border: 2px solid #ff6b35; 
            border-radius: 10px; 
            color: white; 
            font-weight: bold;
            font-size: 10px;
        """)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()
    
    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if ((event.pos() - self.drag_start_position).manhattanLength() < 
            QApplication.startDragDistance()):
            return
        
        drag = QDrag(self)
        mimeData = QMimeData()
        mimeData.setText(f"{self.icon}|{self.module_type}")
        drag.setMimeData(mimeData)
        
        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        
        drag.exec_(Qt.MoveAction)

class DropZone(QWidget):
    moduleDropped = pyqtSignal(str, str, int, int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumSize(800, 600)
        self.modules = []
        self.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                       stop:0 #16213e, stop:1 #1a1a2e);
            border: 3px dashed #00d4ff;
            border-radius: 15px;
        """)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
            self.setStyleSheet("""
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                           stop:0 #16213e, stop:1 #1a1a2e);
                border: 3px solid #4CAF50;
                border-radius: 15px;
            """)
        else:
            event.ignore()
    
    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                       stop:0 #16213e, stop:1 #1a1a2e);
            border: 3px dashed #00d4ff;
            border-radius: 15px;
        """)
    
    def dropEvent(self, event):
        if event.mimeData().hasText():
            data = event.mimeData().text().split('|')
            if len(data) == 2:
                icon, module_type = data
                pos = event.pos()
                
                module = DraggableModule(module_type, icon, self)
                module.move(pos.x() - 60, pos.y() - 30)
                module.show()
                
                self.modules.append({
                    'type': module_type,
                    'icon': icon,
                    'x': pos.x(),
                    'y': pos.y(),
                    'widget': module
                })
                
                self.moduleDropped.emit(icon, module_type, pos.x(), pos.y())
                event.accept()
        
        self.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                       stop:0 #16213e, stop:1 #1a1a2e);
            border: 3px dashed #00d4ff;
            border-radius: 15px;
        """)
    
    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.modules:
            painter = QPainter(self)
            painter.setPen(QPen(QColor("#666666"), 2))
            painter.setFont(QFont("Consolas", 16))
            painter.drawText(self.rect(), Qt.AlignCenter, 
                           "🚀 Drag modules here to design your habitat\n\n"
                           "💡 Tip: Place related modules close together!")

class GameStats(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.score = 0
        self.level = 1
        self.xp = 0
        self.achievements = []
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        self.score_label = QLabel("🏆 Score: 0")
        self.score_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
        layout.addWidget(self.score_label)
        
        self.level_label = QLabel("⭐ Level: 1")
        self.level_label.setStyleSheet("font-size: 14px; color: #FF9800;")
        layout.addWidget(self.level_label)
        
        xp_layout = QHBoxLayout()
        xp_layout.addWidget(QLabel("XP:"))
        self.xp_bar = QProgressBar()
        self.xp_bar.setRange(0, 100)
        self.xp_bar.setValue(0)
        self.xp_bar.setStyleSheet("""
            QProgressBar { border: 2px solid #00d4ff; border-radius: 5px; }
            QProgressBar::chunk { background: #00d4ff; }
        """)
        xp_layout.addWidget(self.xp_bar)
        layout.addLayout(xp_layout)
        
        self.achievements_label = QLabel("🎖️ Achievements: 0")
        self.achievements_label.setStyleSheet("font-size: 12px; color: #00d4ff;")
        layout.addWidget(self.achievements_label)
        
        layout.addStretch()
    
    def add_score(self, points):
        self.score += points
        self.xp += points // 10
        
        if self.xp >= 100:
            self.level += 1
            self.xp = 0
            self.show_level_up()
        
        self.update_display()
    
    def add_achievement(self, achievement):
        if achievement not in self.achievements:
            self.achievements.append(achievement)
            self.show_achievement(achievement)
            self.update_display()
    
    def update_display(self):
        self.score_label.setText(f"🏆 Score: {self.score}")
        self.level_label.setText(f"⭐ Level: {self.level}")
        self.xp_bar.setValue(self.xp)
        self.achievements_label.setText(f"🎖️ Achievements: {len(self.achievements)}")
    
    def show_level_up(self):
        msg = QMessageBox()
        msg.setWindowTitle("🎉 Level Up!")
        msg.setText(f"Congratulations! You reached Level {self.level}!")
        msg.setStyleSheet("background: #1a1a2e; color: #00d4ff;")
        msg.exec_()
    
    def show_achievement(self, achievement):
        msg = QMessageBox()
        msg.setWindowTitle("🏆 Achievement Unlocked!")
        msg.setText(f"🎖️ {achievement}")
        msg.setStyleSheet("background: #1a1a2e; color: #4CAF50;")
        msg.exec_()

class HabitatCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shape = "Cylinder"
        self.modules = []
        self.setMinimumSize(800, 600)
        
    def set_shape(self, shape):
        self.shape = shape
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw habitat shape outline
        painter.setPen(QPen(QColor(0, 212, 255), 3))
        center_x, center_y = self.width()//2, self.height()//2
        
        if self.shape == "Cylinder":
            radius = min(center_x, center_y) - 80
            painter.drawEllipse(center_x - radius, center_y - radius, radius*2, radius*2)
        elif self.shape == "Torus":
            outer_radius = min(center_x, center_y) - 60
            inner_radius = outer_radius - 80
            painter.drawEllipse(center_x - outer_radius, center_y - outer_radius, outer_radius*2, outer_radius*2)
            painter.drawEllipse(center_x - inner_radius, center_y - inner_radius, inner_radius*2, inner_radius*2)
        elif self.shape == "Dome":
            radius = min(center_x, center_y) - 80
            painter.drawArc(center_x - radius, center_y - radius//2, radius*2, radius*2, 0, 180*16)
            painter.drawLine(center_x - radius, center_y + radius//2, center_x + radius, center_y + radius//2)
        elif self.shape == "Spherical":
            radius = min(center_x, center_y) - 80
            painter.drawEllipse(center_x - radius, center_y - radius, radius*2, radius*2)
            # Add sphere lines
            painter.drawLine(center_x - radius, center_y, center_x + radius, center_y)
            painter.drawLine(center_x, center_y - radius, center_x, center_y + radius)
        elif self.shape == "Modular":
            # Draw connected rectangular modules
            module_width, module_height = 120, 80
            for i in range(3):
                for j in range(2):
                    x = center_x - 180 + i * module_width
                    y = center_y - 80 + j * module_height
                    painter.drawRect(x, y, module_width, module_height)

class HabitatCreatorWindow(QMainWindow):
    def __init__(self, app_controller, user_data):
        super().__init__()
        self.app = app_controller
        self.user_data = user_data
        self.current_mission = user_data.get('current_mission', {})
        self.modules = []
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("🏗️ Habitat Creator")
        self.setGeometry(100, 100, 1600, 1000)
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                         stop:0 #0a0a0a, stop:1 #1a1a2e); }
            QLabel { color: #00d4ff; font-family: 'Consolas'; }
            QPushButton { background: #16213e; color: #00d4ff; border: 2px solid #00d4ff; 
                         border-radius: 8px; padding: 8px; font-size: 12px; }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        
        # Left panel - Module palette
        left_panel = QWidget()
        left_panel.setMaximumWidth(200)
        left_layout = QVBoxLayout(left_panel)
        
        title = QLabel("🧩 Module Palette")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #00d4ff; margin: 10px;")
        left_layout.addWidget(title)
        
        # NASA Standard Habitat Modules
        modules = [
            ("🏠", "Node (Unity)"),
            ("🛏️", "Crew Quarters (COLPA)"),
            ("🍴", "Galley (Food System)"),
            ("🚿", "Waste & Hygiene (WHC)"),
            ("🩺", "Medical (Health Care)"),
            ("🔧", "Maintenance (IVA Tools)"),
            ("💪", "Exercise (COLPA)"),
            ("🌱", "Plant Production (VEG)"),
            ("📦", "Logistics (Cargo)"),
            ("⚡", "Power & Thermal (ECLSS)"),
            ("🌬️", "Life Support (ECLSS)"),
            ("🚀", "Airlock (Quest/EVA)"),
            ("🔬", "Laboratory (Destiny)"),
            ("📡", "Communications (Cupola)"),
            ("🛰️", "Docking Port (PMA)")
        ]
        
        for icon, name in modules:
            module = DraggableModule(name, icon)
            left_layout.addWidget(module)
        
        left_layout.addStretch()
        layout.addWidget(left_panel)
        
        # Center panel - Design area
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← Dashboard")
        back_btn.clicked.connect(self.back_to_dashboard)
        header_layout.addWidget(back_btn)
        
        mission_name = self.current_mission.get('name', 'Free Design')
        header = QLabel(f"🏗️ {mission_name}")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(header)
        
        clear_btn = QPushButton("🗑️ Clear All")
        clear_btn.clicked.connect(self.clear_all)
        clear_btn.setStyleSheet("background: #F44336; border-color: #F44336;")
        header_layout.addWidget(clear_btn)
        
        center_layout.addLayout(header_layout)
        
        # Shape selector
        shape_layout = QHBoxLayout()
        shape_layout.addWidget(QLabel("Habitat Shape:"))
        self.shape_combo = QComboBox()
        self.shape_combo.addItems(["Cylinder", "Torus", "Dome", "Spherical", "Modular"])
        self.shape_combo.currentTextChanged.connect(self.change_shape)
        self.shape_combo.setStyleSheet("""
            QComboBox { background: #16213e; color: #00d4ff; border: 2px solid #00d4ff; 
                       border-radius: 5px; padding: 5px; }
        """)
        shape_layout.addWidget(self.shape_combo)
        shape_layout.addStretch()
        center_layout.addLayout(shape_layout)
        
        # Combined canvas with drop zone
        canvas_container = QWidget()
        canvas_layout = QVBoxLayout(canvas_container)
        canvas_layout.setContentsMargins(0, 0, 0, 0)
        
        self.habitat_canvas = HabitatCanvas()
        self.drop_zone = DropZone()
        self.drop_zone.moduleDropped.connect(self.on_module_dropped)
        
        # Stack the canvas and drop zone
        stacked_widget = QStackedWidget()
        
        # Create combined widget
        combined_widget = QWidget()
        combined_layout = QVBoxLayout(combined_widget)
        combined_layout.setContentsMargins(0, 0, 0, 0)
        combined_layout.addWidget(self.habitat_canvas)
        
        # Overlay drop zone on canvas
        self.drop_zone.setParent(combined_widget)
        self.drop_zone.setGeometry(0, 0, 800, 600)
        self.drop_zone.setStyleSheet("""
            background: transparent;
            border: 3px dashed #00d4ff;
            border-radius: 15px;
        """)
        
        center_layout.addWidget(combined_widget)
        
        simulate_btn = QPushButton("🚀 Run Simulation")
        simulate_btn.clicked.connect(self.run_simulation)
        simulate_btn.setStyleSheet("background: #4CAF50; border-color: #4CAF50; padding: 15px; font-size: 16px; font-weight: bold;")
        center_layout.addWidget(simulate_btn)
        
        layout.addWidget(center_panel)
        
        # Right panel - Stats and metrics
        right_panel = QWidget()
        right_panel.setMaximumWidth(300)
        right_layout = QVBoxLayout(right_panel)
        
        self.game_stats = GameStats()
        right_layout.addWidget(self.game_stats)
        
        metrics_label = QLabel("📊 Live Metrics")
        metrics_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        right_layout.addWidget(metrics_label)
        
        self.metrics_display = QLabel(self.get_metrics_text())
        self.metrics_display.setStyleSheet("background: #16213e; padding: 15px; border-radius: 10px; font-size: 11px;")
        right_layout.addWidget(self.metrics_display)
        
        # Mission requirements
        if self.current_mission:
            mission_info = QLabel("🎯 Mission Requirements")
            mission_info.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
            right_layout.addWidget(mission_info)
            
            self.mission_display = QLabel(self.get_mission_requirements())
            self.mission_display.setStyleSheet("background: #16213e; padding: 10px; border-radius: 10px; font-size: 10px;")
            right_layout.addWidget(self.mission_display)
        
        # NASA Standards info
        nasa_info = QLabel("📋 NASA Standards")
        nasa_info.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        right_layout.addWidget(nasa_info)
        
        self.nasa_display = QLabel(self.get_nasa_standards())
        self.nasa_display.setStyleSheet("background: #16213e; padding: 10px; border-radius: 10px; font-size: 10px;")
        right_layout.addWidget(self.nasa_display)
        
        validation_label = QLabel("✅ Validation")
        validation_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        right_layout.addWidget(validation_label)
        
        self.validation_display = QLabel("Add modules to see validation")
        self.validation_display.setStyleSheet("background: #16213e; padding: 15px; border-radius: 10px;")
        right_layout.addWidget(self.validation_display)
        
        layout.addWidget(right_panel)
    
    def on_module_dropped(self, icon, module_type, x, y):
        self.modules.append({
            'type': module_type,
            'icon': icon,
            'x': x,
            'y': y
        })
        
        self.game_stats.add_score(50)
        
        if len(self.modules) == 1:
            self.game_stats.add_achievement("First Module Placed!")
        elif len(self.modules) == 5:
            self.game_stats.add_achievement("Habitat Taking Shape!")
        elif len(self.modules) == 10:
            self.game_stats.add_achievement("Master Builder!")
        
        self.update_metrics()
    
    def clear_all(self):
        for module_data in self.drop_zone.modules:
            module_data['widget'].deleteLater()
        self.drop_zone.modules.clear()
        self.modules.clear()
        self.update_metrics()
    
    def update_metrics(self):
        self.metrics_display.setText(self.get_metrics_text())
        self.validation_display.setText(self.get_validation_text())
        if hasattr(self, 'mission_display') and self.current_mission:
            self.mission_display.setText(self.get_mission_requirements())
        self.nasa_display.setText(self.get_nasa_standards())
    
    def get_metrics_text(self):
        module_count = len(self.modules)
        shape_multiplier = {"Cylinder": 1.0, "Torus": 1.2, "Dome": 0.8, "Spherical": 1.1, "Modular": 0.9}
        multiplier = shape_multiplier.get(self.shape_combo.currentText(), 1.0)
        
        volume = module_count * 50 * multiplier
        power = module_count * 2.5 * multiplier
        mass = module_count * 1000 * multiplier  # kg per module
        
        return f"""
👥 Crew: 4
🏗️ Modules: {module_count}
🏠 Shape: {self.shape_combo.currentText()}
📏 Volume: {volume:.1f} m³
⚡ Power: {power:.1f} kW
⚖️ Mass: {mass:.0f} kg
💧 Water: {14.0 * multiplier:.1f} L/day
🫁 O₂: {3.36 * multiplier:.2f} kg/day
        """
    
    def get_mission_requirements(self):
        if not self.current_mission:
            return "No active mission"
        
        requirements = self.current_mission.get('requirements', [])
        req_text = f"""
🎯 {self.current_mission['name']}
🌍 {self.current_mission['location']}
🕰️ {self.current_mission['duration']}
👥 {self.current_mission['crew']} crew

📋 Required Modules:
        """
        
        for req in requirements:
            req_text += f"• {req}\n"
        
        return req_text
    
    def get_nasa_standards(self):
        return """
📐 Volume: 14m³/person min
⚡ Power: 2.5kW/person
🌡️ Temp: 18-27°C
💨 Pressure: 101.3 kPa
🫁 O₂: 21% ±2%
💧 Water: 3.5L/person/day
🍽️ Food: 1.83kg/person/day
        """
    
    def change_shape(self, shape):
        self.habitat_canvas.set_shape(shape)
        self.update_metrics()
    
    def get_validation_text(self):
        if not self.modules:
            return "❌ No modules placed"
        
        # NASA ISS-based requirements
        required = ["Node (Unity)", "Crew Quarters (COLPA)", "Waste & Hygiene (WHC)", "Power & Thermal (ECLSS)"]
        present = [m["type"] for m in self.modules]
        
        status = []
        for req in required:
            if any(req in p for p in present):
                status.append(f"✅ {req}")
            else:
                status.append(f"❌ {req}")
        
        return "\n".join(status)
    
    def run_simulation(self):
        if len(self.modules) < 4:
            QMessageBox.warning(self, "Warning", "Place at least 4 NASA modules before simulation!")
            return
        
        habitat_data = {
            'user': self.user_data,
            'modules': self.modules,
            'score': self.game_stats.score,
            'shape': self.shape_combo.currentText(),
            'mission': self.current_mission
        }
        self.app.show_validity_check(habitat_data)
    
    def back_to_dashboard(self):
        self.app.show_dashboard(self.user_data)

class ValidityCheckWindow(QMainWindow):
    def __init__(self, app_controller, habitat_data):
        super().__init__()
        self.app = app_controller
        self.habitat_data = habitat_data
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("📋 NASA Validity Check")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                         stop:0 #0a0a0a, stop:1 #1a1a2e); }
            QLabel { color: #00d4ff; font-family: 'Consolas'; }
            QPushButton { background: #16213e; color: #00d4ff; border: 2px solid #00d4ff; 
                         border-radius: 8px; padding: 8px; }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Header
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← Back to Designer")
        back_btn.clicked.connect(self.back_to_designer)
        header_layout.addWidget(back_btn)
        
        header_layout.addStretch()
        header = QLabel("📋 NASA Habitat Validity Check")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        header_layout.addWidget(header)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Validity results
        content_layout = QHBoxLayout()
        
        # Left panel - Requirements check
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        req_label = QLabel("📋 NASA Requirements Check")
        req_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        left_layout.addWidget(req_label)
        
        self.requirements_display = QLabel(self.get_requirements_check())
        self.requirements_display.setStyleSheet("background: #16213e; padding: 20px; border-radius: 10px; font-size: 12px;")
        left_layout.addWidget(self.requirements_display)
        
        content_layout.addWidget(left_panel)
        
        # Right panel - Compliance status
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        status_label = QLabel("✅ Compliance Status")
        status_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        right_layout.addWidget(status_label)
        
        self.status_display = QLabel(self.get_compliance_status())
        self.status_display.setStyleSheet("background: #16213e; padding: 20px; border-radius: 10px; font-size: 12px;")
        right_layout.addWidget(self.status_display)
        
        # Overall validity
        validity_score = self.calculate_validity_score()
        validity_color = "#4CAF50" if validity_score >= 80 else "#FF9800" if validity_score >= 60 else "#F44336"
        
        mission = self.habitat_data.get('mission', {})
        mission_name = mission.get('name', 'Free Design') if mission else 'Free Design'
        
        overall_label = QLabel(f"Mission: {mission_name}\nValidity: {validity_score}%")
        overall_label.setAlignment(Qt.AlignCenter)
        overall_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {validity_color}; margin: 20px; padding: 15px; background: #16213e; border-radius: 10px;")
        right_layout.addWidget(overall_label)
        
        content_layout.addWidget(right_panel)
        layout.addLayout(content_layout)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        mission = self.habitat_data.get('mission', {})
        min_score = 70 if mission.get('difficulty') in ['Expert', 'Master', 'Legendary'] else 60
        
        if validity_score >= min_score:
            proceed_btn = QPushButton("🚀 Proceed to Simulation")
            proceed_btn.clicked.connect(self.proceed_to_simulation)
            proceed_btn.setStyleSheet("background: #4CAF50; border-color: #4CAF50; color: white; font-weight: bold; padding: 15px; font-size: 16px;")
            button_layout.addWidget(proceed_btn)
        else:
            warning_label = QLabel(f"⚠️ Mission requires {min_score}% validity. Current: {validity_score}%")
            warning_label.setAlignment(Qt.AlignCenter)
            warning_label.setStyleSheet("color: #F44336; font-size: 16px; font-weight: bold; margin: 20px;")
            layout.addWidget(warning_label)
        
        redesign_btn = QPushButton("🏗️ Redesign Habitat")
        redesign_btn.clicked.connect(self.back_to_designer)
        button_layout.addWidget(redesign_btn)
        
        layout.addLayout(button_layout)
    
    def get_requirements_check(self):
        modules = self.habitat_data.get('modules', [])
        module_types = [m['type'] for m in modules]
        
        # Critical NASA requirements
        checks = [
            ("Structural Node (Unity)", any("Node" in m for m in module_types)),
            ("Life Support (ECLSS)", any("ECLSS" in m for m in module_types)),
            ("Crew Quarters (COLPA)", any("Crew Quarters" in m for m in module_types)),
            ("Waste & Hygiene (WHC)", any("Waste & Hygiene" in m for m in module_types)),
            ("Power System", any("Power" in m for m in module_types)),
            ("Airlock (EVA)", any("Airlock" in m for m in module_types)),
            ("Medical Bay", any("Medical" in m for m in module_types)),
            ("Food System", any("Galley" in m or "Food" in m for m in module_types)),
            ("Minimum 4 Modules", len(modules) >= 4),
            ("Maximum 15 Modules", len(modules) <= 15)
        ]
        
        result = ""
        for requirement, passed in checks:
            status = "✅" if passed else "❌"
            result += f"{status} {requirement}\n"
        
        return result
    
    def get_compliance_status(self):
        modules = self.habitat_data.get('modules', [])
        shape = self.habitat_data.get('shape', 'Unknown')
        
        # Calculate metrics
        module_count = len(modules)
        shape_multiplier = {"Cylinder": 1.0, "Torus": 1.2, "Dome": 0.8, "Spherical": 1.1, "Modular": 0.9}
        multiplier = shape_multiplier.get(shape, 1.0)
        
        volume = module_count * 50 * multiplier
        power = module_count * 2.5 * multiplier
        mass = module_count * 1000 * multiplier
        
        # NASA standards compliance
        crew_size = 4
        min_volume = crew_size * 14  # 14m³ per person
        min_power = crew_size * 2.5  # 2.5kW per person
        
        volume_ok = volume >= min_volume
        power_ok = power >= min_power
        mass_ok = mass <= 50000  # 50 ton limit
        
        return f"""
📏 Volume: {volume:.1f} m³ {'(✅ OK)' if volume_ok else '(❌ LOW)'}
   Required: {min_volume} m³ minimum

⚡ Power: {power:.1f} kW {'(✅ OK)' if power_ok else '(❌ LOW)'}
   Required: {min_power} kW minimum

⚖️ Mass: {mass:.0f} kg {'(✅ OK)' if mass_ok else '(❌ HIGH)'}
   Limit: 50,000 kg maximum

🏠 Shape: {shape}
   Efficiency: {multiplier:.1f}x

👥 Crew: {crew_size} astronauts
📋 Modules: {module_count} NASA standard
        """
    
    def calculate_validity_score(self):
        modules = self.habitat_data.get('modules', [])
        module_types = [m['type'] for m in modules]
        mission = self.habitat_data.get('mission', {})
        
        score = 0
        
        # Critical modules (60 points total)
        critical_modules = [
            ("Node", 15),
            ("ECLSS", 15),
            ("Crew Quarters", 10),
            ("Waste & Hygiene", 10),
            ("Power", 10)
        ]
        
        for module_key, points in critical_modules:
            if any(module_key in m for m in module_types):
                score += points
        
        # Mission-specific requirements (30 points)
        if mission and 'requirements' in mission:
            mission_reqs = mission['requirements']
            for req in mission_reqs:
                if req != 'All NASA modules required':  # Skip generic requirement
                    req_key = req.split('(')[0].strip()  # Extract key part
                    if any(req_key in m for m in module_types):
                        score += 30 // len(mission_reqs)  # Distribute points evenly
        
        # Module count (10 points)
        if 4 <= len(modules) <= 15:
            score += 10
        elif len(modules) > 15:
            score += 5
        
        return min(100, score)
    
    def proceed_to_simulation(self):
        self.app.show_simulation(self.habitat_data)
    
    def back_to_designer(self):
        user_data = self.habitat_data['user']
        self.app.show_habitat_creator(user_data)

class SimulationWindow(QMainWindow):
    def __init__(self, app_controller, habitat_data):
        super().__init__()
        self.app = app_controller
        self.habitat_data = habitat_data
        self.progress = 0
        self.phase = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.init_ui()
        self.start_simulation()
    
    def init_ui(self):
        self.setWindowTitle("🧪 Habitat Simulation")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                         stop:0 #0a0a0a, stop:1 #1a1a2e); }
            QLabel { color: #00d4ff; font-family: 'Consolas'; }
            QProgressBar { border: 2px solid #00d4ff; border-radius: 8px; 
                          text-align: center; background: #16213e; }
            QProgressBar::chunk { background: #00d4ff; border-radius: 6px; }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        header = QLabel("🧪 Running Habitat Simulation")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(header)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("Initializing simulation...")
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet("font-size: 16px; margin: 10px;")
        layout.addWidget(self.progress_label)
        
        self.metrics_label = QLabel("")
        self.metrics_label.setAlignment(Qt.AlignCenter)
        self.metrics_label.setStyleSheet("font-size: 14px; background: #16213e; padding: 20px; border-radius: 10px; margin: 20px;")
        layout.addWidget(self.metrics_label)
        
        layout.addStretch()
    
    def start_simulation(self):
        self.phases = [
            "Testing life support systems...",
            "Analyzing power distribution...",
            "Simulating crew activities...",
            "Evaluating safety protocols...",
            "Generating NASA report..."
        ]
        self.timer.start(1000)
    
    def update_simulation(self):
        self.progress += 20
        self.progress_bar.setValue(self.progress)
        
        if self.phase < len(self.phases):
            self.progress_label.setText(self.phases[self.phase])
            self.phase += 1
        
        oxygen = max(85, 100 - self.progress * 0.3)
        power = max(80, 100 - self.progress * 0.2)
        morale = max(75, 100 - self.progress * 0.25)
        
        self.metrics_label.setText(f"""
🫁 Oxygen Level: {oxygen:.1f}%
⚡ Power Status: {power:.1f}%
😊 Crew Morale: {morale:.1f}%
🌡️ Temperature: 22.{self.progress//10}°C
        """)
        
        if self.progress >= 100:
            self.timer.stop()
            self.progress_label.setText("Simulation complete! Generating results...")
            QTimer.singleShot(2000, self.show_results)
    
    def show_results(self):
        base_score = random.randint(70, 90)
        bonus = min(20, len(self.habitat_data['modules']) * 2)
        final_score = min(100, base_score + bonus)
        
        results_data = {
            'habitat': self.habitat_data,
            'scores': {
                'overall': final_score,
                'lifesupport': random.randint(80, 95),
                'power': random.randint(75, 90),
                'comfort': random.randint(70, 85),
                'safety': random.randint(80, 95)
            }
        }
        self.app.show_results(results_data)

class ResultsWindow(QMainWindow):
    def __init__(self, app_controller, results_data):
        super().__init__()
        self.app = app_controller
        self.results_data = results_data
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("📄 NASA Evaluation Report")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("""
            QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                         stop:0 #0a0a0a, stop:1 #1a1a2e); }
            QLabel { color: #00d4ff; font-family: 'Consolas'; }
            QPushButton { background: #16213e; color: #00d4ff; border: 2px solid #00d4ff; 
                         border-radius: 8px; padding: 8px; }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        header_layout = QHBoxLayout()
        
        back_creator_btn = QPushButton("← Redesign Habitat")
        back_creator_btn.clicked.connect(self.back_to_creator)
        back_creator_btn.setStyleSheet("background: #ff6b35; color: white; font-weight: bold;")
        header_layout.addWidget(back_creator_btn)
        
        back_dashboard_btn = QPushButton("← Dashboard")
        back_dashboard_btn.clicked.connect(self.back_to_dashboard)
        header_layout.addWidget(back_dashboard_btn)
        
        header_layout.addStretch()
        
        header = QLabel("📄 NASA Evaluation Report")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 24px; font-weight: bold;")
        header_layout.addWidget(header)
        
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        content_layout = QHBoxLayout()
        
        # Score display
        score_widget = QWidget()
        score_widget.setMaximumWidth(300)
        score_layout = QVBoxLayout(score_widget)
        
        overall_score = self.results_data['scores']['overall']
        grade = self.get_grade(overall_score)
        
        score_label = QLabel(f"Mission Grade: {grade}")
        score_label.setAlignment(Qt.AlignCenter)
        score_label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 20px;")
        score_layout.addWidget(score_label)
        
        score_value = QLabel(f"{overall_score}%")
        score_value.setAlignment(Qt.AlignCenter)
        score_value.setStyleSheet(f"font-size: 48px; font-weight: bold; color: {self.get_score_color(overall_score)};")
        score_layout.addWidget(score_value)
        
        game_score = self.results_data['habitat'].get('score', 0)
        game_score_label = QLabel(f"🎮 Game Score: {game_score}")
        game_score_label.setAlignment(Qt.AlignCenter)
        game_score_label.setStyleSheet("font-size: 16px; color: #4CAF50; margin: 10px;")
        score_layout.addWidget(game_score_label)
        
        content_layout.addWidget(score_widget)
        
        # Details
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        
        scores = self.results_data['scores']
        module_count = len(self.results_data['habitat'].get('modules', []))
        habitat_shape = self.results_data['habitat'].get('shape', 'Unknown')
        
        # NASA module analysis
        modules = self.results_data['habitat'].get('modules', [])
        nasa_modules = [m['type'] for m in modules]
        has_node = any('Node' in m for m in nasa_modules)
        has_eclss = any('ECLSS' in m for m in nasa_modules)
        has_crew_quarters = any('Crew Quarters' in m for m in nasa_modules)
        
        metrics_text = f"""
🫁 Life Support: {scores['lifesupport']}%
⚡ Power Management: {scores['power']}%
😊 Crew Comfort: {scores['comfort']}%
🚨 Safety Systems: {scores['safety']}%

🏗️ NASA Modules: {module_count}
🏠 Habitat Shape: {habitat_shape}
👥 Crew Size: 4

📋 NASA Compliance:
{'✅' if has_node else '❌'} Structural Node
{'✅' if has_eclss else '❌'} Life Support (ECLSS)
{'✅' if has_crew_quarters else '❌'} Crew Quarters

✅ Strengths:
• NASA-standard modules used
• Proper habitat configuration
• ISS-based design principles

⚠️ Recommendations:
• Add redundant life support
• Include emergency systems
        """
        
        metrics_display = QLabel(metrics_text)
        metrics_display.setStyleSheet("font-size: 14px; padding: 20px; background: #16213e; border-radius: 10px;")
        details_layout.addWidget(metrics_display)
        
        content_layout.addWidget(details_widget)
        layout.addLayout(content_layout)
    
    def get_grade(self, score):
        if score >= 95: return 'A+'
        if score >= 90: return 'A'
        if score >= 85: return 'B+'
        if score >= 80: return 'B'
        if score >= 75: return 'C+'
        if score >= 70: return 'C'
        return 'D'
    
    def get_score_color(self, score):
        if score >= 90: return '#4CAF50'
        if score >= 70: return '#FF9800'
        return '#F44336'
    
    def back_to_creator(self):
        user_data = self.results_data['habitat']['user']
        self.app.show_habitat_creator(user_data)
    
    def back_to_dashboard(self):
        user_data = self.results_data['habitat']['user']
        # Check if mission completed successfully
        overall_score = self.results_data['scores']['overall']
        if overall_score >= 75:  # Mission success threshold
            user_data['missions_completed'] = user_data.get('missions_completed', 0) + 1
            user_data['level'] = user_data.get('level', 1) + 1
        self.app.show_dashboard(user_data)

class HabiconApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.current_window = None
        self.show_login()
    
    def show_login(self):
        if self.current_window:
            self.current_window.close()
        self.current_window = LoginWindow(self)
        self.current_window.show()
    
    def show_dashboard(self, user_data):
        if self.current_window:
            self.current_window.close()
        self.current_window = DashboardWindow(self, user_data)
        self.current_window.show()
    
    def show_habitat_creator(self, user_data):
        if self.current_window:
            self.current_window.close()
        self.current_window = HabitatCreatorWindow(self, user_data)
        self.current_window.show()
    
    def show_validity_check(self, habitat_data):
        if self.current_window:
            self.current_window.close()
        self.current_window = ValidityCheckWindow(self, habitat_data)
        self.current_window.show()
    
    def show_simulation(self, habitat_data):
        if self.current_window:
            self.current_window.close()
        self.current_window = SimulationWindow(self, habitat_data)
        self.current_window.show()
    
    def show_results(self, results_data):
        if self.current_window:
            self.current_window.close()
        self.current_window = ResultsWindow(self, results_data)
        self.current_window.show()
    
    def run(self):
        return self.app.exec_()

def main():
    habicon = HabiconApp()
    return habicon.run()

if __name__ == '__main__':
    sys.exit(main())