import sys
import subprocess
import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QMenuBar, QAction, QFileDialog, QDialog, QDialogButtonBox, QHBoxLayout, QVBoxLayout
import pyttsx3
from PyQt5.QtCore import Qt

nltk.download('punkt')
nltk.download('stopwords')

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurar Chaves de API")

        self.api_key_weather = QLineEdit()
        self.api_key_traffic = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Chave de API para Previsão do Tempo:"))
        layout.addWidget(self.api_key_weather)
        layout.addWidget(QLabel("Chave de API para Tráfego:"))
        layout.addWidget(self.api_key_traffic)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def get_api_keys(self):
        return {
            'weather': self.api_key_weather.text(),
            'traffic': self.api_key_traffic.text()
        }

class AssistantGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ava - Assistente Pessoal")
        self.setGeometry(200, 200, 400, 200)

        self.stop_words = set(stopwords.words('portuguese'))

        # Criação de widgets
        self.label = QLabel("Faça uma pergunta:")
        self.question_input = QLineEdit()
        self.answer_label = QLabel()
        self.answer_label.setWordWrap(True)
        self.answer_label.setAlignment(Qt.AlignTop)
        self.answer_label.setFixedHeight(100)
        self.answer_label.setStyleSheet("QLabel { background-color : #f0f0f0; padding: 5px; }")
        self.answer_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.answer_button = QPushButton("Obter Resposta")
        self.answer_button.clicked.connect(self.get_answer)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.question_input)
        layout.addWidget(self.answer_button)
        layout.addWidget(self.answer_label)

        # Widget principal
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Configuração do menu
        self.create_menu()

        # Chaves de API
        self.api_keys = {
            'weather': '',
            'traffic': ''
        }

        # Dicionário de aprendizado
        self.learning_dict = {}

        # Inicialização do engine de síntese de voz
        self.engine = pyttsx3.init()

    def get_answer(self):
        question = self.question_input.text()
        answer = self.search_answer(question)
        self.answer_label.setText(answer)
        self.speak_answer(answer)

    def search_answer(self, question):
        question = self.preprocess_question(question)

        if question in self.learning_dict:
            return self.learning_dict[question]
        elif 'previsão do tempo' in question:
            return self.get_weather_forecast()
        elif 'trânsito' in question:
            return self.get_traffic_info()
        else:
            return 'Desculpe, não entendi sua pergunta.'

    def preprocess_question(self, question):
        # Tokenização e remoção de stopwords
        tokens = word_tokenize(question.lower())
        filtered_tokens = [token for token in tokens if token not in self.stop_words]
        preprocessed_question = ' '.join(filtered_tokens)
        return preprocessed_question

    def get_weather_forecast(self):
        if not self.api_keys['weather']:
            return 'Chave de API para Previsão do Tempo não configurada.'

        # Adicione aqui a lógica para buscar a previsão do tempo na internet usando a chave de API
        return "Aqui está a previsão do tempo."

    def get_traffic_info(self):
        if not self.api_keys['traffic']:
            return 'Chave de API para Tráfego não configurada.'

        # Adicione aqui a lógica para buscar informações de trânsito na internet usando a chave de API
        return "Aqui estão as informações de trânsito."

    def open_browser(self):
        # Adicione aqui a lógica para abrir o navegador
        return "Abrindo o navegador..."

    def shutdown_computer(self):
        # Adicione aqui a lógica para desligar o computador
        return "Desligando o computador..."

    def create_menu(self):
        # Criação da barra de menu
        menu_bar = self.menuBar()

        # Menu Configurar
        config_menu = menu_bar.addMenu("Configurar")

        configure_browser_action = QAction("Configurar Navegador", self)
        configure_browser_action.triggered.connect(self.configure_browser)
        config_menu.addAction(configure_browser_action)

        configure_api_keys_action = QAction("Configurar Chaves de API", self)
        configure_api_keys_action.triggered.connect(self.configure_api_keys)
        config_menu.addAction(configure_api_keys_action)

    def configure_browser(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Executáveis (*.exe)")
        file_dialog.setWindowTitle("Selecionar Navegador")

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            browser_path = selected_files[0]

            # Salva o caminho do navegador no arquivo de configuração
            with open('config.txt', 'w') as f:
                f.write(browser_path)

    def configure_api_keys(self):
        dialog = ConfigDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.api_keys = dialog.get_api_keys()

    def speak_answer(self, answer):
        self.engine.say(answer)
        self.engine.runAndWait()

    def learn_from_user(self, question, answer):
        self.learning_dict[question] = answer

def check_dependencies():
    try:
        import nltk
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
        import pyttsx3
        import requests
        import PyQt5
    except ImportError as e:
        return str(e)

def install_dependencies():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'nltk', 'pyttsx3', 'requests', 'PyQt5'])
        return True
    except subprocess.CalledProcessError:
        return False

if __name__ == '__main__':
    # Verificar se as dependências estão instaladas
    missing_dependencies = check_dependencies()
    if missing_dependencies:
        print(f"Falha ao importar as seguintes dependências: {missing_dependencies}")
        print("Instalando dependências...")
        if install_dependencies():
            print("Dependências instaladas com sucesso.")
        else:
            print("Falha ao instalar dependências. Certifique-se de ter o pip instalado.")
            sys.exit(1)

    app = QApplication(sys.argv)
    window = AssistantGUI()
    window.show()
    sys.exit(app.exec_())
