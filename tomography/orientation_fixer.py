import os
import sys
import time
from collections import OrderedDict
from enum import Enum
import numpy as np
from skimage import io, transform
import skimage
from PIL import Image
import cv2
from PyQt5 import QtCore, QtWidgets, QtGui, QtChart

import tomo_data
import cutout_photos


# compile the main window QtDesigner ui file into a python file
# I do this so the IDE understands where the Ui_MainWindow class comes from and is able to provide hints
os.system("pyuic5 orientationGui.ui > orientationGui.py")
# if the external compilation doesn't work, the following line loads the python class directly from the ui-file
# but you get no type hints in the IDE
# from PyQt5.uic import loadUiType
# Ui_MainWindow, QMainWindow = loadUiType('mainWindow.ui')

from orientationGui import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow

# This extension of the standard QWidget UI-element is used to display the preview and spot images.
# You can provide it with an image using the update_image() method. Cropping and repositioning the image is also done
# by the widget itself if you provide the 'center' and 'zoom' arguments to the update_image() method
#
# In addition it provides a 'clicked'-event that can be subscribed to, which is used by the program to reposition the
# spot previews.
class PreviewWidget(QtWidgets.QWidget):
    """
    Image preview display widget.
    Extension of the standard QWidget UI element that is used to display the preview and spot images in this program

    You can provide it with an image using the update_image() method. Cropping and repositioning the image is also done
    by the widget itself if you provide the 'center' and 'zoom' arguments to the update_image() method

    In addition it provides a 'clicked'-event that can be subscribed to, which is used by the program to reposition the
    spot previews.
    """

    clicked = QtCore.pyqtSignal(QtGui.QMouseEvent, name='clicked')
    """
    Click signal (in the sense of the pyqt framework)
    """


    def __init__(self, parent=None, size=np.array([450, 300]), full_size=np.array([450, 300])):
        """
        Initialize the PreviewWidget

        Args:
            parent:     parent widget in which this widget is to be displayed
            size:       the size of *this* preview widget
            full_size:  the size of the *overview* preview widget. Used to determine the scale of this image so that it
                        corresponds to the scale of the overview image
        """
        super().__init__()
        self.size = size
        self.full_size = full_size
        self.setParent(parent)
        self.upperleft_ipx = None
        self.lowerright_ipx = None
        self.image = None
        self.img_size = None

    def mouseReleaseEvent(self, event):
        if self.isEnabled():
            self.clicked.emit(event)

    def paintEvent(self, event):
        """
        Override of the paint event method which is called by the Qt framework in every UI draw cycle.
        Here we put in the image rendering code.
        """
        if self.image:
            qp = QtGui.QPainter(self)
            target = QtCore.QRectF(0.0, 0.0, self.size[0], self.size[1])
            q_upperleft = QtCore.QPointF(self.upperleft_ipx[0], self.upperleft_ipx[1])
            q_lowerright = QtCore.QPointF(self.lowerright_ipx[0], self.lowerright_ipx[1])
            source = QtCore.QRectF(q_upperleft, q_lowerright)

            qp.drawImage(target, self.image, source)


    def compute_initial_figure(self):
        pass

    def update_image(self, imgdata, center=None, zoom=1.0):
        """
        Update the image to be displayed

        Args:
            imgdata:    RGB-array containing the new image to be displayed
            cpopt:      specification of the color processing method to be used
            center:     position to center the image on (in image-pixels)
            zoom:       zoom factor of the image (with respect to the *overview* preview)

        Returns:
            None
        """
        self.img_size = np.array(imgdata.shape[1::-1]) # invert the x and y-axis, images are saved in the opposite column/row-order

        # converted_imgdata = ImageConversion.apply_color_processing(imgdata, cpopt)

        self.image = QtGui.QImage(imgdata, self.img_size[0], self.img_size[1], self.img_size[0] * 3,
                                  QtGui.QImage.Format_RGB888)

        # if we have no center given, take the midpoint of the image
        if center is None:
            center = self.img_size / 2

        display_pix_per_image_pix = self.full_size / self.img_size
        scale_factor = np.min(display_pix_per_image_pix)

        crop_ipx_size = self.size / (scale_factor * zoom)
        self.upperleft_ipx = center - (crop_ipx_size / 2.0)
        self.lowerright_ipx = center + (crop_ipx_size / 2.0)

        self.update()

    def dpx_to_ipx(self, dpx):
        """
        Convert position in display pixels to position in image pixels

        Args:
            dpx:    [x,y]-position array in display pixels to be converted

        Returns:
            [x,y]-position array in image pixels
        """
        rel_pos = dpx / self.size
        ipx = self.upperleft_ipx + (self.lowerright_ipx - self.upperleft_ipx) * rel_pos
        return ipx

    def get_image_rect(self):
        """
        Return the current crop rectangle of the displayed image in image pixels, taking into account the selected
        center and zoom factor.

        Returns:
            (x1, y1, x2, y2) crop rectangle (in integer image pixel coordinates)

        """
        return (int(self.upperleft_ipx[0]), int(self.upperleft_ipx[1]), int(self.lowerright_ipx[0]), int(self.lowerright_ipx[1]))


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.overlay_color = np.array([255, 0, 0], dtype=np.uint8).reshape(1, 1, 3)
        self.bg_color = np.array([255, 255, 255], dtype=np.uint8).reshape(1, 1, 3)

        self.ph_num = 0
        # self.ph_id = (3, 'v', 1)

        self.overviewImage = PreviewWidget(
            self.overviewWidget,
            size=np.array([300, 300]),
            full_size=np.array([300, 300])
        )

        self.zoomImage = PreviewWidget(
            self.zoomWidget,
            size=np.array([300, 300]),
            full_size=np.array([300, 300])
        )

        self.markerImage = PreviewWidget(
            self.markerWidget,
            size=np.array([300, 300]),
            full_size=np.array([300, 300])
        )

        self.rotatedImage = PreviewWidget(
            self.rotatedWidget,
            size=np.array([300, 300]),
            full_size=np.array([300, 300])
        )

        self.processedImage = PreviewWidget(
            self.processedWidget,
            size=np.array([300, 300]),
            full_size=np.array([300, 300])
        )

        self.overviewImage.clicked.connect(self.overview_click)
        self.zoomImage.clicked.connect(self.zoom_click)
        self.resetButton.clicked.connect(self.reset_marker)
        self.imageTable.cellDoubleClicked.connect(self.list_click)
        self.saveButton.clicked.connect(self.save_click)
        self.skipButton.clicked.connect(self.skip_click)

        self.image_list = []
        self.image_status = []
        self.load_image_list()

        self.load_image()

        self.marker_center_pt = None
        self.marker_radius = None
        self.zoom_center_pt = None

    def load_image_list(self):
        self.image_list = cutout_photos.get_valid_photo_ids(tomo_data.cutout_selected_fn_format)
        self.image_status = [""] * len(self.image_list)

        self.imageTable.setColumnCount(2)
        self.imageTable.setRowCount(len(self.image_list))
        self.imageTable.horizontalHeader().hide()
        self.imageTable.verticalHeader().hide()

        for i in range(len(self.image_list)):
            labelItem = QtWidgets.QTableWidgetItem("plak %03d, %s %d" % self.image_list[i])
            valueItem = QtWidgets.QTableWidgetItem(self.image_status[i])

            self.imageTable.setItem(i, 0, labelItem)
            self.imageTable.setItem(i, 1, valueItem)

        self.imageTable.resizeRowsToContents()
        self.imageTable.setColumnWidth(0, self.markerTable.width() // 2 - 1)
        self.imageTable.setColumnWidth(1, self.markerTable.width() // 2 - 1)

    def list_click(self, i, j):
        self.ph_num = i
        self.load_image()
        # self.statusbar.showMessage("List clicked, row %d, id %s" % (i, str(self.image_list[i])))

    def load_image(self):
        ph_id = self.image_list[self.ph_num]
        valueItem = QtWidgets.QTableWidgetItem("current")
        self.imageTable.setItem(self.ph_num, 1, valueItem)

        self.cutout_img = io.imread(tomo_data.cutout_selected_fn_format % ph_id)
        self.cutout_overlay = np.zeros_like(self.cutout_img[:,:,0])
        self.rotated_preview_img = np.copy(self.cutout_img)
        self.processed_img = np.copy(self.cutout_img)

        self.marker_center_pt = None
        self.marker_radius = None
        self.zoom_center_pt = None

        self.update_images()
        self.update_marker()

        self.statusbar.showMessage("Image %s loaded" % str(ph_id))

    def overview_click(self, event):
        dpx = np.array([event.x(), event.y()])
        if self.overviewImage.image is not None:
            ipx = self.overviewImage.dpx_to_ipx(dpx)
            self.zoom_center_pt = ipx

            self.update_images()

            # self.statusbar.showMessage("Clicked on overview, location %f, %f" % tuple(ipx))

    def zoom_click(self, event):
        dpx = np.array([event.x(), event.y()])
        if self.zoomImage.image is not None:
            ipx = self.zoomImage.dpx_to_ipx(dpx).astype(np.int)

            if event.button() == QtCore.Qt.LeftButton:
                self.update_marker(center=ipx)
            elif event.button() == QtCore.Qt.RightButton:
                self.update_marker(radial=ipx)

            # self.statusbar.showMessage("Clicked on zoom, location %f, %f" % tuple(ipx))
            self.update_marker()

    def update_images(self):
        self.generate_overlay()
        self.cutout_combined = (
            (1-self.cutout_overlay[:,:,np.newaxis])*self.cutout_img
            + self.cutout_overlay[:,:,np.newaxis]*self.overlay_color
        )
        line_d = 5
        pimg_width = self.rotated_preview_img.shape[1]
        line_cols = np.arange(pimg_width // 2 - line_d, pimg_width // 2 + line_d + 1)

        self.redline_rotprev_img = np.copy(self.rotated_preview_img)
        self.redline_rotprev_img[:, line_cols, :] = self.overlay_color

        self.overviewImage.update_image(self.cutout_img)
        self.zoomImage.update_image(self.cutout_img, center=self.zoom_center_pt, zoom=10.0)
        self.markerImage.update_image(self.cutout_combined, center=self.zoom_center_pt, zoom=5.0)
        self.rotatedImage.update_image(self.redline_rotprev_img)
        self.processedImage.update_image(self.processed_img)

    def update_marker(self, center=None, radial=None):
        if center is not None:
            self.marker_center_pt = center
            self.generate_rotated_preview()
            if self.marker_radius is not None:
                self.generate_processed_image()
        if radial is not None and self.marker_center_pt is not None:
            self.marker_radius = float(np.linalg.norm(radial - self.marker_center_pt))
            self.generate_processed_image()

        self.show_marker_parameters()
        self.update_images()

    def generate_overlay(self):
        if self.marker_center_pt is not None and self.marker_radius is not None:
            img_size = self.cutout_img.shape
            ring_d = 5
            xs, ys = np.meshgrid(
                np.arange(img_size[1]) - self.marker_center_pt[0],
                np.arange(img_size[0]) - self.marker_center_pt[1]
            )
            rs = xs ** 2 + ys ** 2

            marker_r = self.marker_radius

            ring_overlay = np.array((rs > (marker_r - ring_d)**2) & (rs < (marker_r + ring_d)**2), dtype=np.uint8)
            self.cutout_overlay = ring_overlay
        else:
            self.cutout_overlay = np.zeros_like(self.cutout_img[:,:,0])

    def reset_marker(self):
        self.marker_center_pt = None
        self.marker_radius = None
        self.update_marker()

    def show_marker_parameters(self):
        marker_params = OrderedDict()
        marker_params["x"] = "none"
        marker_params["y"] = "none"
        marker_params["r"] = "none"
        marker_params["angle"] = "none"

        if self.marker_center_pt is not None:
            marker_params["x"] = str(self.marker_center_pt[0])
            marker_params["y"] = str(self.marker_center_pt[1])
            marker_params["angle"] = "%.1f" % np.rad2deg(self.calculate_marker_angle())

            if self.marker_radius is not None:
                r = self.marker_radius
                marker_params["r"] = "%.1f" % r

        self.markerTable.setColumnCount(2)
        self.markerTable.setRowCount(len(marker_params))
        self.markerTable.horizontalHeader().hide()
        self.markerTable.verticalHeader().hide()

        for i, (l, v) in enumerate(marker_params.items()):
            labelItem = QtWidgets.QTableWidgetItem(l)
            valueItem = QtWidgets.QTableWidgetItem(v)

            self.markerTable.setItem(i, 0, labelItem)
            self.markerTable.setItem(i, 1, valueItem)

        self.markerTable.resizeRowsToContents()
        self.markerTable.setColumnWidth(0, self.markerTable.width() // 2 - 1)
        self.markerTable.setColumnWidth(1, self.markerTable.width() // 2 - 1)

    def calculate_marker_angle(self):
        img_size = np.array(self.cutout_img[:,:,0].shape)[::-1]
        img_center = img_size / 2.0
        marker_pos = self.marker_center_pt - img_center

        r_angle = np.arctan2(*marker_pos[::-1]) + np.pi/2
        return r_angle

    def generate_rotated_preview(self):
        self.statusbar.showMessage("Starting rotation...")
        start_time = time.clock()
        # let's rotate the image
        r_angle = self.calculate_marker_angle()

        # using PIL for rotations seems to be very much faster
        # rotated_img = transform.rotate(self.cutout_img, np.rad2deg(r_angle), resize=True, cval=1.0)
        # https://stackoverflow.com/questions/5252170/specify-image-filling-color-when-rotating-in-python-with-pil-and-setting-expand
        pil_img = Image.fromarray(self.cutout_img)
        pil_imga = pil_img.convert("RGBA")
        pil_rot_imga = pil_imga.rotate(np.rad2deg(r_angle), resample=Image.BILINEAR, expand=True)
        pil_white_imga = Image.new("RGBA", pil_rot_imga.size, (255,)*4)
        pil_out_imga = Image.composite(pil_rot_imga, pil_white_imga, pil_rot_imga)
        pil_out_img = pil_out_imga.convert(pil_img.mode)
        rotated_img = np.array(pil_out_img)

        duration = time.clock() - start_time
        self.rotated_preview_img = skimage.img_as_ubyte(rotated_img)
        self.statusbar.showMessage("Finished rotating after %.3f s" % duration)

    def generate_processed_image(self):
        # first remove the marker
        img_size = self.cutout_img.shape
        xs, ys = np.meshgrid(
            np.arange(img_size[1]) - self.marker_center_pt[0],
            np.arange(img_size[0]) - self.marker_center_pt[1]
        )
        rs = xs ** 2 + ys ** 2

        marker_r = self.marker_radius

        marker_mask = np.array(rs < marker_r**2, dtype=np.uint8)
        demarkered_img = (
            (1-marker_mask[:,:,np.newaxis])*self.cutout_img
            + marker_mask[:,:,np.newaxis]*self.bg_color
        )
        r_angle = self.calculate_marker_angle()
        # rd_img = transform.rotate(demarkered_img, np.rad2deg(r_angle), resize=True, cval=1.0)

        # https://stackoverflow.com/questions/5252170/specify-image-filling-color-when-rotating-in-python-with-pil-and-setting-expand
        pil_img = Image.fromarray(demarkered_img)
        pil_imga = pil_img.convert("RGBA")
        pil_rot_imga = pil_imga.rotate(np.rad2deg(r_angle), resample=Image.NEAREST, expand=True)
        pil_white_imga = Image.new("RGBA", pil_rot_imga.size, (255,) * 4)
        pil_out_imga = Image.composite(pil_rot_imga, pil_white_imga, pil_rot_imga)
        pil_out_img = pil_out_imga.convert(pil_img.mode)
        rd_img = skimage.img_as_ubyte(np.array(pil_out_img))

        layer_sum = np.sum(rd_img, axis=-1)
        bin_img = (layer_sum < (3*255)).astype(np.uint8)
        # bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, cutout_photos.get_circular_kernel(200))
        bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, cutout_photos.get_circular_kernel(400))

        self.processed_img = rd_img * bin_img[:,:,np.newaxis] + (1-bin_img[:,:,np.newaxis])*self.bg_color

    def save_click(self):
        bin_img = (np.sum(self.processed_img, axis=-1) < (3 * 255)).astype(np.uint8)

        sum_over_cols = np.sum(bin_img, axis=0)
        sum_over_rows = np.sum(bin_img, axis=1)

        min_row = np.argmax(sum_over_rows > 0)
        max_row = len(sum_over_rows) - np.argmax(sum_over_rows[::-1] > 0)

        min_col = np.argmax(sum_over_cols > 0)
        max_col = len(sum_over_cols) - np.argmax(sum_over_cols[::-1] > 0)

        cropped_img = self.processed_img[min_row:max_row, min_col:max_col]

        ph_id = self.image_list[self.ph_num]
        io.imsave(tomo_data.rotated_fn_format % ph_id, cropped_img, quality=100)
        self.statusbar.showMessage("Image saved")

        valueItem = QtWidgets.QTableWidgetItem("saved")
        self.imageTable.setItem(self.ph_num, 1, valueItem)

        if self.ph_num + 1 < len(self.image_list):
            self.ph_num += 1
            self.load_image()

    def skip_click(self):
        valueItem = QtWidgets.QTableWidgetItem("skipped")
        self.imageTable.setItem(self.ph_num, 1, valueItem)
        if self.ph_num + 1 < len(self.image_list):
            self.ph_num += 1
            self.load_image()


if __name__ == '__main__':
    # run the application!
    app = QtWidgets.QApplication(sys.argv)
    main = Main()

    main.show()
    sys.exit(app.exec())