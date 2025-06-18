from PySide6.QtCore import Signal
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QTableWidget, QHeaderView, \
    QTableWidgetItem, QAbstractItemView


class ROIWidget(QWidget):
    delete_ROI = Signal(str)
    delete_all_ROI = Signal()
    modify_ROI = Signal(tuple)
    apply_changes = Signal()

    def __init__(self, width, height):
        super().__init__()

        self.width = width
        self.height = height

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create the table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "X", "Y", "Width", "Height"])
        self.table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        self.table.cellChanged.connect(self.cell_changed)

        # 1. Stretch columns to fill space
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 2. Select entire rows
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        # 3. Remove row numbers (vertical header)
        self.table.verticalHeader().setVisible(False)

        # 4. Style header (background color to light grey)
        header = self.table.horizontalHeader()
        palette = header.palette()
        palette.setColor(QPalette.Window, QColor("lightgrey"))
        header.setPalette(palette)
        header.setStyleSheet("QHeaderView::section { background-color: lightgrey; border-bottom: 1px solid #aaa; }")

        self.btn_delete_selected = QPushButton("Delete Selected ROI")
        self.btn_delete_all = QPushButton("Delete All ROIs")
        self.btn_apply = QPushButton("Apply Changes")

        layout.addWidget(QLabel("Defined ROIs:"))
        layout.addWidget(self.table)
        layout.addWidget(self.btn_delete_selected)
        layout.addWidget(self.btn_delete_all)
        layout.addWidget(self.btn_apply)

        self.setLayout(layout)

        # Connect buttons
        self.btn_delete_selected.clicked.connect(self.delete_selected_roi)
        self.btn_delete_all.clicked.connect(self.delete_all_rois)
        self.btn_apply.clicked.connect(self.on_apply_clicked)

    def delete_selected_roi(self):
        selected_rows = self.table.selectionModel().selectedRows()
        for index in selected_rows:
            roi_id_item = self.table.item(index.row(), 0)
            if roi_id_item:
                roi_id = roi_id_item.text()
                self.delete_ROI.emit(roi_id)


    def delete_all_rois(self):
        self.delete_all_ROI.emit()

    def on_apply_clicked(self):
        self.apply_changes.emit()

    def refresh_list(self, rois):
        """
        `rois` is a dictionary {id: {"x": x, "y": y, "width": w, "height": h}}
        """
        self.table.blockSignals(True)  # Block signal temporarily

        self.table.setRowCount(0)  # Clear existing rows£

        for i, (roi_id, region) in enumerate(rois.items()):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(roi_id)))
            self.table.setItem(i, 1, QTableWidgetItem(str(region["x"])))
            self.table.setItem(i, 2, QTableWidgetItem(str(region["y"])))
            self.table.setItem(i, 3, QTableWidgetItem(str(region["width"])))
            self.table.setItem(i, 4, QTableWidgetItem(str(region["height"])))

        self.table.blockSignals(False)  # Re-enable signals

    def cell_changed(self, row, column):
        print(f"cell_changed called for row={row}, column={column}")
        # Ignore changes to ID column (assumed read-only)
        if column == 0:
            return

        try:
            roi_id = self.table.item(row, 0).text()
            x = int(self.table.item(row, 1).text())
            y = int(self.table.item(row, 2).text())
            w = int(self.table.item(row, 3).text())
            h = int(self.table.item(row, 4).text())
        except Exception:
            # If any cell is empty or invalid, just ignore
            return

        if column in (3, 4):  # Width or height edited
            w = max(1, min(w, self.width - x))
            h = max(1, min(h, self.height - y))
        elif column in (1, 2):  # X or Y edited
            x = max(0, min(x, self.width - w))
            y = max(0, min(y, self.height - h))

        updated_roi = {"x": x, "y": y, "width": w, "height": h}
        self.modify_ROI.emit((roi_id, updated_roi))  # Emit a tuple