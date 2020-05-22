"""
Author : Ashutosh Kumar
Version : 1.0
Description : Connect UI with Python
Email : ashutoshkumardbms@gmail.com
"""
import urllib.request

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os
import sys

from PyQt5.uic import loadUiType

# pafy module to download youtube videos
import pafy

# Humainze Module
import humanize

# loading our UI into Python
ui, _ = loadUiType('main.ui')


# This class will inherit from 2 things
class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        # calling parent class
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)

        # setup UI
        self.setupUi(self)

        # Calling methods
        self.InitUI()

        # Calling in Constructor so that it attaches listener to each of them
        self.Handel_Buttons()

    def InitUI(self):
        # contain all the UI changes in loading
        self.tabWidget.tabBar().setVisible(False)

        # Adding Animation
        self.Move_Box_1()
        self.Move_Box_2()
        self.Move_Box_3()
        self.Move_Box_4()

    def Handel_Buttons(self):
        # Handle all buttons in the Application

        # Calling Download Method when Button is clicked
        self.pushButton.clicked.connect(self.Download)

        # Calling Browse Button
        self.pushButton_2.clicked.connect(self.Handel_Browse)

        # Single Youtube Video
        self.pushButton_8.clicked.connect(self.Get_Video_Data)

        # Single Youtube Download Video
        self.pushButton_6.clicked.connect(self.Download_Video)

        # Single Youtube Browse Button
        self.pushButton_5.clicked.connect(self.Save_Browse)

        # Playlist Youtube Download Button
        self.pushButton_9.clicked.connect(self.Playlist_Download)

        # Playlist Youtube Browse Button
        self.pushButton_7.clicked.connect(self.Playlist_Save_Browse)

        # Menu Buttons
        # Open Menu
        self.pushButton_3.clicked.connect(self.Open_Home)

        # Open Download
        self.pushButton_4.clicked.connect(self.Open_Download)

        # Open Youtube
        self.pushButton_10.clicked.connect(self.Open_Youtube)

        # Open Settings
        self.pushButton_11.clicked.connect(self.Open_Settings)

        # Themes
        # Theme Buttons - Orange
        self.pushButton_12.clicked.connect(self.Apply_Orange_Theme)

        # Theme Buttons - Blue
        self.pushButton_13.clicked.connect(self.Apply_Dark_Theme)

        # Theme Buttons - Grey
        self.pushButton_14.clicked.connect(self.Apply_Grey_Theme)

        # Theme Buttons - Reset
        self.pushButton_15.clicked.connect(self.Apply_Reset_Theme)

    ''' Single File Download'''

    def Handel_Progress(self, blocknum, blocksize, totalsize):
        # Calculate Progress

        # totalsize = total size which is to be downloaded
        # blocksize = size of each block
        # blocknum = no of blocks downloaded

        readed_data = blocknum * blocksize
        if totalsize > 0:
            # Calculating the total progress made and showing it on the progress Bar
            download_percentage = (readed_data * 100) / totalsize

            # Showing that on the Progress Bar
            self.progressBar.setValue(download_percentage)

            # To Prevent our Application from Freezing
            QApplication.processEvents()

    def Handel_Browse(self):
        # enable browsing for save location
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")

        self.lineEdit_2.setText(str(save_location[0]))

    # Download Method
    def Download(self):
        # For downloading https://download.sublimetext.com/Sublime%20Text%20Build%203176.dmg
        print("Starting Downloading ")

        # Getting Download URL
        download_url = self.lineEdit.text()

        # Getting Save location
        save_location = self.lineEdit_2.text()

        if download_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a Valid URL or Save Location")
        else:
            # Downloading file
            try:
                urllib.request.urlretrieve(download_url, save_location, self.Handel_Progress)

            except Exception:
                # In case any URL invalid or any save location error it will show an Error !
                QMessageBox.warning(self, "Download Error", "Provide a Valid URL or Save Location")
                return

        # When download completes
        QMessageBox.information(self, "Download Completed", "The Download is Completed Successfully")

        # Resetting the values
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)

    ''' Single File Download'''

    ''' Download Youtube Single Video '''

    def Save_Browse(self):
        # Save location in the line edit
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        self.lineEdit_6.setText(str(save_location[0]))

    # Youtube Videos
    def Get_Video_Data(self):

        # getting URL
        video_url = self.lineEdit_5.text()

        # Verifying URL
        if video_url == '':
            QMessageBox.warning(self, "Data Error", "Provide a Valid URL")
        else:
            # Getting video from Youtube Video
            video = pafy.new(video_url)

            # print video details
            print(video.duration)

            # Getting different Streams
            video_streams = video.videostreams

            for stream in video_streams:
                # Converting size into Human readable form
                size = humanize.naturalsize(stream.get_filesize())

                # Adding data into Combobox by formatting the data
                data = "{} {} {} {}".format(stream.mediatype, stream.extension, stream.quality, size)

                self.comboBox.addItem(data)

    def Download_Video(self):
        video_url = self.lineEdit_5.text()
        save_location = self.lineEdit_6.text()

        if video_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a Valid URL or Save Location")
        else:
            # Downloading file
            # Getting Youtube Video
            try:
                video = pafy.new(video_url)

                # Getting Video Stream
                video_streams = video.streams

                # Getting Quality Selected
                video_quality = self.comboBox.currentIndex()

                # Downloading Video
                # Callback gives us Video Progress
                download = video_streams[video_quality].download(filepath=save_location, callback=self.Video_Progress)
            except Exception:
                QMessageBox.warning(self, "Download Error", "Provide a Valid URL or Save Location")
                return

    # parameters of the video
    # rate is the speed
    def Video_Progress(self, total, recieved, ratio, rate, time):
        readed_data = recieved
        # Calculating % of download
        if total > 0:
            download_percentage = readed_data * 100 / total

            # Setting % in Progres Bar
            self.progressBar_3.setValue(download_percentage)

            # Converting time into minute
            remaining_time = round(time / 60, 2)

            # Providing into Label about Minute
            self.label_5.setText(str('{} Minutes Remaining'.format(remaining_time)))

            # Preventing Freezing of Application
            QApplication.processEvents()

    '''Single Video Download Ends Here '''

    ''' Download Youtube Playlist  '''

    def Playlist_Download(self):
        playlist_url = self.lineEdit_7.text()
        save_location = self.lineEdit_8.text()

        # Validation
        if playlist_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a Valid Playlist URL or Save Location")
        else:
            # getting playlist
            playlist = pafy.get_playlist(playlist_url)

            # getting list of videos
            playlist_videos = playlist['items']

            # Displaying No of Videos
            self.lcdNumber_2.display(len(playlist_videos))

            # Changing location to current directory
            os.chdir(save_location)

            # If there exists a directory with the name of the playlist already we move to that directory
            if os.path.exists(str(playlist['title'])):
                os.chdir(str(playlist['title']))
            else:
                # Else we will create a Folder with the name of the playlist then move to that directory
                os.mkdir(str(playlist['title']))

                # Moviing into that directory
                os.chdir(str(playlist['title']))

            current_video_in_download = 1

            # Getting video Quality
            quality = self.comboBox_2.currentIndex()

            # displaying current video download
            self.lcdNumber.display(current_video_in_download)
            QApplication.processEvents()

            # loop tp download every video in the playlist
            for video in playlist_videos:
                # current video
                current_video = video['pafy']

                # getting it's stream
                current_video_stream = current_video.streams
                if len(current_video_stream) < quality:
                    quality = 0

                try:
                    # Downloading Video
                    download = current_video_stream[quality].download(callback=self.Playlist_Progress)

                except Exception:
                    QMessageBox.warning(self, "Download Error", "Provide a Valid URL or Save Location")
                    return

                quality = self.comboBox_2.currentIndex()

                # Preventing Freezing of Application
                QApplication.processEvents()

                # Incrementing Counter
                current_video_in_download = current_video_in_download + 1

                # Current Video Number
                self.lcdNumber.display(current_video_in_download)

    def Playlist_Progress(self, total, recieved, ratio, rate, time):
        readed_data = recieved
        # Calculating % of download
        if total > 0:
            download_percentage = readed_data * 100 / total

            # Setting % in Progres Bar
            self.progressBar_4.setValue(download_percentage)

            # Converting time into minute
            remaining_time = round(time / 60, 2)

            # Providing into Label about Minute
            self.label_6.setText(str('{} Minutes Remaining'.format(remaining_time)))

            # Preventing Freezing of Application
            QApplication.processEvents()

    def Playlist_Save_Browse(self):
        # getting Playlist Save location
        playlist_save_location = QFileDialog.getExistingDirectory(self, "Select Download Directory")

        # Adding to the UI
        self.lineEdit_8.setText(playlist_save_location)

    ''' Download Youtube Playlist  '''

    '''UI Changes Method'''

    def Open_Home(self):
        # Opening Tab Based on the Click Tab 0
        self.tabWidget.setCurrentIndex(0)

    def Open_Download(self):
        # Opening Tab Based on the Click Tab 1
        self.tabWidget.setCurrentIndex(1)

    def Open_Youtube(self):
        # Opening Tab Based on the Click Tab 2
        self.tabWidget.setCurrentIndex(2)

    def Open_Settings(self):
        # Opening Tab Based on the Click Tab 3
        self.tabWidget.setCurrentIndex(3)

    ''' Themes Selection '''

    def Apply_Dark_Theme(self):
        # Opening Stylesheet
        style = open('themes/qdarkblue.qss', 'r')

        # Reading file
        style = style.read()

        # Setting Style
        self.setStyleSheet(style)

    def Apply_Grey_Theme(self):
        # Opening Stylesheet
        style = open('themes/qgrey.qss', 'r')

        # Reading file
        style = style.read()

        # Setting Style
        self.setStyleSheet(style)

    def Apply_Orange_Theme(self):
        # Opening Stylesheet
        style = open('themes/qorange.qss', 'r')

        # Reading file
        style = style.read()

        # Setting Style
        self.setStyleSheet(style)

    def Apply_Reset_Theme(self):
        # Opening Stylesheet
        style = open('themes/qwhite.qss', 'r')

        # Reading file
        style = style.read()

        # Setting Style
        self.setStyleSheet(style)

    ''' Adding Animation '''

    def Move_Box_1(self):
        # Creating Animation
        box_animation = QPropertyAnimation(self.groupBox, b"geometry")

        # Time Duration in miliseconds
        box_animation.setDuration(1000)

        # Starting value
        box_animation.setStartValue(QRect(0, 0, 0, 0))

        # Ending value
        box_animation.setEndValue(QRect(40, 20, 311, 161))

        # Start Animation
        box_animation.start()
        self.box_animation = box_animation

    def Move_Box_2(self):
        # Creating Animation
        box_animation2 = QPropertyAnimation(self.groupBox_2, b"geometry")

        # Time Duration in miliseconds
        box_animation2.setDuration(1200)

        # Starting value
        box_animation2.setStartValue(QRect(0, 0, 0, 0))

        # Ending value
        box_animation2.setEndValue(QRect(390, 20, 301, 161))

        # Start Animation
        box_animation2.start()
        self.box_animation2 = box_animation2

    def Move_Box_3(self):
        # Creating Animation
        box_animation3 = QPropertyAnimation(self.groupBox_3, b"geometry")

        # Time Duration in miliseconds
        box_animation3.setDuration(1800)

        # Starting value
        box_animation3.setStartValue(QRect(0, 0, 0, 0))

        # Ending value
        box_animation3.setEndValue(QRect(390, 210, 311, 171))

        # Start Animation
        box_animation3.start()
        self.box_animation3 = box_animation3

    def Move_Box_4(self):
        # Creating Animation
        box_animation4 = QPropertyAnimation(self.groupBox_4, b"geometry")

        # Time Duration in miliseconds
        box_animation4.setDuration(1500)

        # Starting value
        box_animation4.setStartValue(QRect(0, 0, 0, 0))

        # Ending value
        box_animation4.setEndValue(QRect(40, 210, 311, 171))

        # Start Animation
        box_animation4.start()
        self.box_animation4 = box_animation4

    ''' Adding Animation '''


def main():
    app = QApplication(sys.argv)
    # takes system arguments

    window = MainApp()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
