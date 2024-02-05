import sys
from PyQt5.QtCore import QUrl, QIODevice, Qt, QObject, pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineSettings
from PyQt5.QtWebChannel import QWebChannel

class YouTubeMusicApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PYQT5 YouTube Music")
        self.setGeometry(100, 100, 1024, 768)

        # Set up the main layout with zero margin
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Initialize the web view with the YouTube Music URL
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        # Create a container widget to hold the layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Set the application icon by downloading it from the provided URL
        self.set_website_icon()

        # Enable the WebEngine settings to allow running JavaScript
        settings = QWebEngineSettings.globalSettings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        # Create a custom web page with WebChannel
        web_page = CustomWebPage(self.web_view)
        channel = QWebChannel(self.web_view.page())
        self.web_view.page().setWebChannel(channel)
        channel.registerObject("app", web_page)

        # Load the YouTube Music URL
        self.web_view.setUrl(QUrl("https://music.youtube.com/"))

    def set_website_icon(self):
        url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Youtube_Music_icon.svg/512px-Youtube_Music_icon.svg.png"
        
        # Download the icon image from the URL using QNetworkAccessManager
        manager = QNetworkAccessManager(self)
        request = QNetworkRequest(QUrl(url))
        reply = manager.get(request)

        # Connect the download finished signal to the appropriate slot
        reply.finished.connect(self.icon_download_finished)

    def icon_download_finished(self):
        reply = self.sender()
        
        if reply.error() == QNetworkReply.NoError:
            # Read the downloaded data and create a QPixmap from it
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)

            # Set the window icon using the downloaded pixmap
            self.setWindowIcon(QIcon(pixmap))

        # Clean up the reply object
        reply.deleteLater()

class CustomWebPage(QWebEnginePage):
    def __init__(self, view):
        super().__init__(view)
        self.loadFinished.connect(self.onLoadFinished)

    @pyqtSlot(bool)
    def onLoadFinished(self, ok):
        if ok:
            # Inject JavaScript to load uBlock Origin
            with open('ublock_origin.js', 'r') as file:
                script = file.read()
                self.runJavaScript(script)

if __name__ == "__main__":
    # Create the application instance
    app = QApplication(sys.argv)

    # Create and show the YouTubeMusicApp instance
    youtube_music_app = YouTubeMusicApp()
    youtube_music_app.show()

    # Start the application event loop
    sys.exit(app.exec_())
