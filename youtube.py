import sys
from PyQt5.QtCore import QUrl, QIODevice, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class YouTubeMusicApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PYQT5 YouTube Music")
        self.setGeometry(100, 100, 1024, 768)

        layout = QVBoxLayout()

        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl("https://music.youtube.com/"))
        layout.addWidget(self.web_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Set the application icon from the website's icon
        self.set_website_icon()

    def set_website_icon(self):
        url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Youtube_Music_icon.svg/512px-Youtube_Music_icon.svg.png"
        
        # Download the icon image from the URL
        manager = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(url))
        reply = manager.get(request)

        reply.finished.connect(self.icon_download_finished)

    def icon_download_finished(self):
        reply = self.sender()
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            
            # Set the window icon using the downloaded pixmap
            self.setWindowIcon(QIcon(pixmap))
        
        reply.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    youtube_music_app = YouTubeMusicApp()
    youtube_music_app.show()
    sys.exit(app.exec_())
