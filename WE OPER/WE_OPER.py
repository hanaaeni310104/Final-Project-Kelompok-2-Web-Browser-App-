import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QLabel, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineDownloadItem

class DownloadDialog(QDialog):
    def __init__(self, parent=None):
        super(DownloadDialog, self).__init__(parent)
        self.setWindowTitle("Download Progress")
        
        self.progress_bar = QProgressBar(self)
        self.progress_label = QLabel(self)
        self.close_button = QPushButton("Close", self)
        self.close_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.close_button)
        self.setLayout(layout)

    def set_progress(self, bytes_received, total_bytes):
        if total_bytes > 0:
            progress = int((bytes_received / total_bytes) * 100)
            self.progress_bar.setValue(progress)
            self.progress_label.setText(f"Progres Unduhan: {progress}%")
        else:
            self.progress_label.setText("Progres Unduhan: Calculating...")

    def download_finished(self, download_item):
        self.accept()


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowIcon(QIcon(os.path.join('assets', 'Logo.png')))

        self.web_engine_profile = QWebEngineProfile.defaultProfile()

        settings = self.web_engine_profile.settings()
        settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)

        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join('assets', 'Back.png')), "Back", self)
        back_btn.setStatusTip("Back to the previous page")
        navtb.addAction(back_btn)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())

        next_btn = QAction(QIcon(os.path.join('assets', 'Forward.png')), "Forward", self)
        next_btn.setStatusTip("Forward to the next page")
        navtb.addAction(next_btn)
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())

        reload_btn = QAction(QIcon(os.path.join('assets', 'Reload.png')), "Reload", self)
        reload_btn.setStatusTip("Reload the page")
        navtb.addAction(reload_btn)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())

        home_btn = QAction(QIcon(os.path.join('assets', 'Home.png')), "Home", self)
        home_btn.setStatusTip("Go home")
        navtb.addAction(home_btn)
        home_btn.triggered.connect(self.navigate_home)

        self.search_engine_combo = QComboBox(self)
        self.search_engine_combo.addItems(['Google', 'Bing', 'DuckDuckGo', 'Yahoo', 'AOL', 'Baidu', 'Looksmart', 'ASK', 'Ecosia'])

        icon_path = os.path.join('assets')
        icons = {
            'Google': 'Google.png',
            'Bing': 'Bing.png',
            'DuckDuckGo': 'DD go.png',
            'Yahoo': 'Yahoo.png',
            'AOL' : 'Aol.png',
            'Baidu' : 'Baidu.png',
            'Looksmart' : 'Looksmart.png',
            'ASK' : 'Ask.png',
            'Ecosia' : 'Ecosia.png',
        }

        for engine, icon_file in icons.items():
            icon = QIcon(os.path.join(icon_path, icon_file))
            self.search_engine_combo.setItemIcon(self.search_engine_combo.findText(engine), icon)
            radius = 5 
            self.search_engine_combo.setStyleSheet(f"QComboBox {{ border: 1px solid rgb(0, 0, 0); border-radius: {radius}px; min-width: 70px; min-height: 20px;}}")

        navtb.addWidget(self.search_engine_combo)
        self.search_engine_combo.currentIndexChanged.connect(self.go_to_selected_engine)

        social_tb = QToolBar("Social Media")
        social_tb.setIconSize(QSize(16, 16))
        self.addToolBar(social_tb)


        gmail_btn = QToolButton(self)
        gmail_btn.setIcon(QIcon(os.path.join('assets', 'Gmail.png')))
        gmail_btn.setText("Gmail")
        gmail_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        social_tb.addWidget(gmail_btn)
        gmail_btn.clicked.connect(lambda: self.open_social_media("https://mail.google.com/"))

        tiktok_btn = QToolButton(self)
        tiktok_btn.setIcon(QIcon(os.path.join('assets', 'TikTok.png')))
        tiktok_btn.setText("TikTok")
        tiktok_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        social_tb.addWidget(tiktok_btn)
        tiktok_btn.clicked.connect(lambda: self.open_social_media("https://www.tiktok.com/"))

        youtube_btn = QToolButton(self)
        youtube_btn.setIcon(QIcon(os.path.join('assets', 'YouTube.png')))
        youtube_btn.setText("YouTube")
        youtube_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        social_tb.addWidget(youtube_btn)
        youtube_btn.clicked.connect(lambda: self.open_social_media("https://www.youtube.com/"))

        instagram_btn = QToolButton(self)
        instagram_btn.setIcon(QIcon(os.path.join('assets', 'Instagram.png')))
        instagram_btn.setText("Instagram")
        instagram_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon) 
        social_tb.addWidget(instagram_btn)
        instagram_btn.clicked.connect(lambda: self.open_social_media("https://www.instagram.com/"))

        facebook_btn = QToolButton(self)
        facebook_btn.setIcon(QIcon(os.path.join('assets', 'Facebook.png')))
        facebook_btn.setText("Facebook")
        facebook_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon) 
        social_tb.addWidget(facebook_btn)
        facebook_btn.clicked.connect(lambda: self.open_social_media("https://www.facebook.com/"))

        WhatsApp_btn = QToolButton(self)
        WhatsApp_btn.setIcon(QIcon(os.path.join('assets', 'WhatsApp.png')))
        WhatsApp_btn.setText("WhatsApp")
        WhatsApp_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        social_tb.addWidget(WhatsApp_btn)
        WhatsApp_btn.clicked.connect(lambda: self.open_social_media("https://www.whatsapp.com/"))
        
        twitter_btn = QToolButton(self)
        twitter_btn.setIcon(QIcon(os.path.join('assets', 'Twitter.png')))
        twitter_btn.setText("Twitter")
        twitter_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon) 
        social_tb.addWidget(twitter_btn)
        twitter_btn.clicked.connect(lambda: self.open_social_media("https://www.twitter.com/"))


        navtb.addSeparator()
        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join('assets', 'Unlock.png')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        navtb.addWidget(self.urlbar)
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        file_menu = self.menuBar().addMenu("&Tabs")
        new_tab_action = QAction(QIcon(os.path.join('assets', 'New_Tab.png')), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        file_menu.addAction(new_tab_action)
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())

        self.bookmarks_menu = self.menuBar().addMenu("&Menu") 

        add_bookmark_action = QAction(QIcon(os.path.join('assets', 'Add Bookmark.png')), "Add Bookmark", self)
        add_bookmark_action.setStatusTip("Bookmark current page")
        self.bookmarks_menu.addAction(add_bookmark_action)
        add_bookmark_action.triggered.connect(self.add_bookmark)

        remove_bookmark_action = QAction(QIcon(os.path.join('assets', 'Delete Bookmark.png')), "Delete Bookmark", self)
        remove_bookmark_action.setStatusTip("Remove bookmark")
        self.bookmarks_menu.addAction(remove_bookmark_action)
        remove_bookmark_action.triggered.connect(self.remove_bookmark)

        self.bookmarks_menu = self.menuBar().addMenu("&Bookmarks")

        help_menu = self.menuBar().addMenu("&Help")
        exit_action = QAction(QIcon(os.path.join('assets', 'Exit.png')), "Exit", self)
        exit_action.setStatusTip("Exit the application")
        help_menu.addAction(exit_action)
        exit_action.triggered.connect(self.close_application)


        self.setStyleSheet("""
            QWidget{
                background-color: rgb(255, 255, 255);
                color: rgb(0, 0, 0);
            }

            QTabWidget::pane {
                border-top: 2px solid rgb(0, 0, 0);
                position: absolute;
                top: -0.5em;
                color: rgb(255, 255, 255);
                padding: 5px;
            }

            QTabWidget::tab-bar {
                alignment: left;
            }

            QLabel, QToolButton, QTabBar::tab {
                background: rgb(255, 255, 255);
                border: 1px solid rgb(255, 255, 255);
                border-radius: 10px;
                min-width: 8ex;
                padding: 5px;
                margin-right: 2px;
                color: rgb(74, 74, 74); 
            }

            QLabel:hover, QToolButton::hover, QTabBar::tab:selected, QTabBar::tab:hover {
                background: rgb(245, 245, 245); 
                border: 2px solid rgb(200, 200, 200); 
            }

            QLineEdit {
                border: 2px solid rgb(200, 200, 200); 
                border-radius: 10px;
                padding: 5px;
                background-color: rgb(255, 255, 255);
                color: rgb(74, 74, 74);
            }

            QLineEdit:hover {
                border: 2px solid rgb(150, 150, 150); 
            }

            QLineEdit:focus {
                border: 2px solid rgb(66, 133, 244); 
                color: rgb(66, 133, 244); 
            }

            QPushButton {
                background: rgb(245, 245, 245);
                border: 2px solid rgb(200, 200, 200);
                padding: 5px;
                border-radius: 10px;
                color: rgb(74, 74, 74);
            }

            QPushButton:hover {
                background: rgb(235, 235, 235); 
                border: 2px solid rgb(150, 150, 150); 
            }
            """)

        self.current_search_engine = '' 

        self.add_new_tab(QUrl('http://www.google.com'), 'Google', engine='Google')
        self.show()


    def navigate_to_url(self):
        url_text = self.urlbar.text()
        if not any(url_text.startswith(scheme) for scheme in ["http", "https", "ftp"]):
            search_url = QUrl(self.get_search_url(url_text))
            self.tabs.currentWidget().setUrl(search_url)
        else:
            q = QUrl(url_text)
            self.tabs.currentWidget().setUrl(q)

    def get_search_url(self, query, engine=None):
        search_engines = {
            'Google': 'http://www.google.com/search?q={}',
            'Bing': 'http://www.bing.com/search?q={}',
            'DuckDuckGo': 'http://duckduckgo.com/?q={}',
            'Yahoo': 'http://search.yahoo.com/search?p={}',
            'AOL' : 'https://search.aol.com/aol/search?q={}',
            'Baidu' : 'https://www.baidu.com/s?ie={}',
            'Looksmart' : 'https://results.looksmart.com/serp?q={}',
            'ASK' : 'https://www.ask.com/web?q={}',
            'Ecosia' : 'https://www.ecosia.org/search?method=index&q={}',
        }
        selected_engine = engine if engine else self.current_search_engine
        return search_engines.get(selected_engine, 'http://www.google.com').format(query.replace(" ", "+"))
    
    def download_requested(self, download_item):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        download_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "All Files (*);;Text Files (*.txt)", options=options)

        if download_path:
            download_item.setPath(download_path)
            download_item.accept()
            self.handle_download(download_item)
        else:
            download_item.cancel()


    def handle_download(self, download_item):
        download_item.finished.connect(lambda: self.download_finished(download_item))
        download_item.downloadProgress.connect(lambda bytes_received, total_bytes: self.show_download_progress(bytes_received, total_bytes, download_item))

    def show_download_progress(self, bytes_received, total_bytes, download_item):
        current_tab = self.tabs.currentWidget()
        if hasattr(current_tab, 'download_dialog'):
            current_tab.download_dialog.set_progress(bytes_received, total_bytes)

    def download_finished(self, download_item):
        download_dialog = DownloadDialog(self)
        download_dialog.set_progress(download_item.totalBytes(), download_item.totalBytes())
        download_dialog.exec_()



    def add_new_tab(self, qurl=None, label="", engine=None):
        if qurl is None:
            qurl = QUrl(self.get_search_url(label, engine))

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(
            lambda qurl, browser=browser: self.update_urlbar(qurl, browser)
        )
        browser.loadFinished.connect(
            lambda _, i=i, browser=browser: self.tabs.setTabText(
                i, browser.page().title()
            )
        )

        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(self.download_requested)
        browser.page().profile().downloadRequested.connect(self.handle_download)

        return browser



    def go_to_selected_engine(self):
        selected_search_engine = self.search_engine_combo.currentText()
        self.current_search_engine = selected_search_engine

        if selected_search_engine == 'Google':
            self.tabs.currentWidget().setUrl(QUrl('http://www.google.com'))
        elif selected_search_engine == 'Bing':
            self.tabs.currentWidget().setUrl(QUrl('http://www.bing.com'))
        elif selected_search_engine == 'DuckDuckGo':
            self.tabs.currentWidget().setUrl(QUrl('http://duckduckgo.com'))
        elif selected_search_engine == 'Yahoo':
            self.tabs.currentWidget().setUrl(QUrl('https://id.yahoo.com/'))
        elif selected_search_engine == 'AOL':
            self.tabs.currentWidget().setUrl(QUrl('https://www.aol.com/'))
        elif selected_search_engine == 'Baidu':
            self.tabs.currentWidget().setUrl(QUrl('https://www.baidu.com/'))
        elif selected_search_engine == 'Looksmart':
            self.tabs.currentWidget().setUrl(QUrl('https://www.looksmart.com/'))
        elif selected_search_engine == 'ASK':
            self.tabs.currentWidget().setUrl(QUrl('https://www.ask.com/'))
        elif selected_search_engine == 'Ecosia':
            self.tabs.currentWidget().setUrl(QUrl('https://www.ecosia.org/'))


    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        if q.scheme() == 'https':
            self.httpsicon.setPixmap(QPixmap(os.path.join('assets', 'Lock.png')))
        else:
            self.httpsicon.setPixmap(QPixmap(os.path.join('assets', 'Unlock.png')))
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(title)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def close_application(self):
        self.close()

    def add_bookmark(self):
        current_tab = self.tabs.currentWidget()
        current_url = current_tab.url().toString()

        bookmark_name, ok = QInputDialog.getText(self, 'Add Bookmark', 'Masukkan url bookmark:')
        if ok and bookmark_name:
            bookmark_action = QAction(bookmark_name, self)
            bookmark_action.setStatusTip("Open bookmarked page")
            bookmark_action.triggered.connect(lambda _, url=current_url: self.open_bookmarked_page(url))

            self.bookmarks_menu.addAction(bookmark_action)

    def open_bookmarked_page(self, url):
        self.add_new_tab(QUrl(url), 'Bookmark')

    def remove_bookmark(self):
        if not hasattr(self, 'bookmarks_menu'):
            return

        bookmark_items = [action.text() for action in self.bookmarks_menu.actions()]

        if not bookmark_items:
            return

        bookmark_name, ok = QInputDialog.getItem(self, 'Delete Bookmark', 'Pilih Bookmark:', bookmark_items)

        if ok and bookmark_name:
            for action in self.bookmarks_menu.actions():
                if action.text() == bookmark_name:
                    self.bookmarks_menu.removeAction(action)
                    break 


        if ok and bookmark_name:
            for action in self.bookmarks_menu.actions():
                if action.text() == bookmark_name:
                    self.bookmarks_menu.removeAction(action)
                    break

    def open_social_media(self, url):
        self.add_new_tab(QUrl(url), label='Social Media', engine=self.current_search_engine)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("WE OPER")

    window = MainWindow()
    sys.exit(app.exec_())
