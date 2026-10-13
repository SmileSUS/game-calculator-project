from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox,
    QComboBox, QSpinBox, QTextEdit,
    QListWidget, QSplitter
)
from PyQt6.QtCore import Qt

from services.app_service import AppService


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.service = AppService()
        self.setWindowTitle("Hellring Calculator")
        self.resize(1100, 700)
        self.init_ui()
        self.auto_load()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # --- Основная область: splitter с тремя частями ---
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Левая: список провинций + управление
        left = QWidget()
        left_layout = QVBoxLayout(left)

        left_layout.addWidget(QLabel("Провинции"))

        self.input_province = QLineEdit()
        self.input_province.setPlaceholderText("Имя новой провинции")
        left_layout.addWidget(self.input_province)

        province_buttons = QHBoxLayout()
        self.btn_create_province = QPushButton("Создать")
        self.btn_create_province.clicked.connect(self.on_create_province)
        self.btn_remove_province = QPushButton("Удалить")
        self.btn_remove_province.clicked.connect(self.on_remove_province)
        province_buttons.addWidget(self.btn_create_province)
        province_buttons.addWidget(self.btn_remove_province)
        left_layout.addLayout(province_buttons)

        self.lbl_province_count = QLabel("Провинций: 0")
        left_layout.addWidget(self.lbl_province_count)

        self.list_provinces = QListWidget()
        self.list_provinces.itemClicked.connect(self.on_province_selected)
        left_layout.addWidget(self.list_provinces)

        splitter.addWidget(left)

        # Центр: сводка провинции + список городов
        center = QWidget()
        center_layout = QVBoxLayout(center)

        self.lbl_province_summary = QLabel("Провинция не выбрана")
        center_layout.addWidget(self.lbl_province_summary)

        self.input_settlement = QLineEdit()
        self.input_settlement.setPlaceholderText("Имя города")
        center_layout.addWidget(self.input_settlement)

        city_row = QHBoxLayout()
        self.spin_population = QSpinBox()
        self.spin_population.setRange(0, 1000000)
        self.spin_population.setValue(0)

        self.btn_create_settlement = QPushButton("Создать город")
        self.btn_create_settlement.clicked.connect(self.on_create_settlement)

        self.btn_remove_settlement = QPushButton("Удалить город")
        self.btn_remove_settlement.clicked.connect(self.on_remove_settlement)

        city_row.addWidget(QLabel("Жителей:"))
        city_row.addWidget(self.spin_population)
        city_row.addWidget(self.btn_create_settlement)
        city_row.addWidget(self.btn_remove_settlement)
        center_layout.addLayout(city_row)

        center_layout.addWidget(QLabel("Города провинции"))
        self.list_settlements = QListWidget()
        self.list_settlements.itemClicked.connect(self.on_settlement_selected)
        center_layout.addWidget(self.list_settlements)

        splitter.addWidget(center)

        # Правая: данные города
        right = QWidget()
        right_layout = QVBoxLayout(right)

        self.lbl_settlement = QLabel("Город не выбран")
        right_layout.addWidget(self.lbl_settlement)

        job_input_layout = QHBoxLayout()
        self.combo_job = QComboBox()
        self.combo_job.setEditable(True)
        self.combo_job.addItems([
            "Логист", "Фермер", "Повар", "Учёный", "Шахтёр",
            "Кузнец", "Металлург", "Строитель", "Духовник",
            "Рабочий", "Другое"
        ])

        self.spin_workers = QSpinBox()
        self.spin_workers.setRange(0, 1000000)
        self.spin_workers.setValue(1)

        self.btn_assign = QPushButton("Назначить")
        self.btn_assign.clicked.connect(self.on_assign_job)

        self.btn_remove_job = QPushButton("Убрать работу")
        self.btn_remove_job.clicked.connect(self.on_remove_job)

        job_input_layout.addWidget(self.combo_job)
        job_input_layout.addWidget(self.spin_workers)
        job_input_layout.addWidget(self.btn_assign)
        job_input_layout.addWidget(self.btn_remove_job)
        right_layout.addLayout(job_input_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Тип работы", "Занято"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        right_layout.addWidget(self.table)

        splitter.addWidget(right)
        splitter.setSizes([250, 350, 500])
        main_layout.addWidget(splitter)

        # --- Нижняя панель: кнопки и лог ---
        buttons_layout = QHBoxLayout()
        self.btn_save = QPushButton("Сохранить игру")
        self.btn_save.clicked.connect(self.on_save_game)

        self.btn_new = QPushButton("Новая игра")
        self.btn_new.clicked.connect(self.on_new_game)

        buttons_layout.addWidget(self.btn_save)
        buttons_layout.addWidget(self.btn_new)
        buttons_layout.addStretch()
        main_layout.addLayout(buttons_layout)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(120)
        main_layout.addWidget(self.log)

    # ---------- Обработчики провинций ----------

    def on_create_province(self):
        name = self.input_province.text().strip()
        try:
            self.service.create_province(name)
            self.input_province.clear()
            self.log.append("Создана провинция " + name)
            self.refresh_provinces()
        except ValueError as error:
            QMessageBox.critical(self, "Ошибка", str(error))

    def on_remove_province(self):
        item = self.list_provinces.currentItem()
        if item is None:
            QMessageBox.warning(self, "Ошибка", "Выберите провинцию в списке")
            return

        name = item.text()
        try:
            self.service.remove_province(name)
            self.log.append("Удалена провинция " + name)
            self.refresh_provinces()
            self.clear_settlement_panel()
        except ValueError as error:
            QMessageBox.critical(self, "Ошибка", str(error))

    def on_province_selected(self, item):
        self.refresh_settlements(item.text())

    # ---------- Обработчики городов ----------

    def on_create_settlement(self):
        province = self.current_province()
        if province is None:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите провинцию")
            return

        name = self.input_settlement.text().strip()
        population = self.spin_population.value()

        try:
            self.service.create_settlement(province, name, population)
            self.input_settlement.clear()
            self.log.append("Создан город " + name)
            self.refresh_settlements(province)
        except ValueError as error:
            QMessageBox.critical(self, "Ошибка", str(error))

    def on_remove_settlement(self):
        province = self.current_province()
        item = self.list_settlements.currentItem()
        if province is None or item is None:
            QMessageBox.warning(self, "Ошибка", "Выберите город в списке")
            return

        name = item.text()
        try:
            self.service.remove_settlement(province, name)
            self.log.append("Удалён город " + name)
            self.refresh_settlements(province)
            self.clear_settlement_panel()
        except ValueError as error:
            QMessageBox.critical(self, "Ошибка", str(error))

    def on_settlement_selected(self, item):
        self.refresh_jobs(item.text())

    # ---------- Обработчики работ ----------

    def on_assign_job(self):
        province = self.current_province()
        settlement = self.current_settlement()
        if province is None or settlement is None:
            QMessageBox.warning(self, "Ошибка", "Выберите город")
            return

        job_type = self.combo_job.currentText().strip()
        workers = self.spin_workers.value()

        try:
            self.service.assign_job(province, settlement, job_type, workers)
            self.log.append("Назначен " + job_type + " x" + str(workers) + " в " + settlement)
            self.refresh_jobs(settlement)
        except ValueError as error:
            QMessageBox.critical(self, "Ошибка", str(error))

    def on_remove_job(self):
        province = self.current_province()
        settlement = self.current_settlement()
        if province is None or settlement is None:
            QMessageBox.warning(self, "Ошибка", "Выберите город")
            return

        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите строку в таблице")
            return

        job_type = self.table.item(row, 0).text()
        self.service.remove_job(province, settlement, job_type)
        self.log.append("Убран " + job_type + " в " + settlement)
        self.refresh_jobs(settlement)

    # ---------- Сохранение / загрузка ----------

    def on_save_game(self):
        try:
            self.service.save_game()
            self.log.append("Игра сохранена: save.txt")
            QMessageBox.information(self, "Успех", "Игра сохранена!")
        except OSError as error:
            QMessageBox.critical(self, "Ошибка", "Не удалось сохранить: " + str(error))

    def on_new_game(self):
        box = QMessageBox(self)
        box.setWindowTitle("Новая игра")
        box.setText("Вы уверены, что хотите всё удалить?")
        box.setIcon(QMessageBox.Icon.Warning)
        box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        box.setButtonText(QMessageBox.StandardButton.Yes, "Да")
        box.setButtonText(QMessageBox.StandardButton.No, "Нет")

        if box.exec() != QMessageBox.StandardButton.Yes:
            return

        self.service.new_game()
        self.log.append("Начата новая игра")
        self.refresh_provinces()
        self.clear_settlement_panel()

    def auto_load(self):
        try:
            if self.service.load_game():
                self.log.append("Игра загружена из save.txt")
            self.refresh_provinces()
        except (OSError, KeyError) as error:
            self.log.append("Не удалось загрузить сохранение: " + str(error))

    # ---------- Обновление интерфейса ----------

    def current_province(self):
        item = self.list_provinces.currentItem()
        if item is None:
            return None
        return item.text()

    def current_settlement(self):
        item = self.list_settlements.currentItem()
        if item is None:
            return None
        return item.text()

    def refresh_provinces(self):
        self.list_provinces.clear()
        for province in self.service.get_provinces():
            self.list_provinces.addItem(province.get_name())
        self.lbl_province_count.setText(
            "Провинций: " + str(self.service.count_provinces())
        )

    def refresh_settlements(self, province_name):
        self.list_settlements.clear()
        for settlement in self.service.get_settlements(province_name):
            self.list_settlements.addItem(settlement.get_name())

        summary = self.service.get_province_summary(province_name)
        if summary is None:
            self.lbl_province_summary.setText("Провинция не выбрана")
            return

        self.lbl_province_summary.setText(
            "Провинция «" + summary.get("name") + "»: " +
            str(summary.get("settlements")) + " городов | " +
            "Жителей: " + str(summary.get("population")) + " | " +
            "Занято: " + str(summary.get("employed"))
        )

    def refresh_jobs(self, settlement_name):
        province = self.current_province()
        if province is None:
            return

        settlement = self.service.find_settlement(province, settlement_name)
        if settlement is None:
            return

        self.lbl_settlement.setText(
            "Город " + settlement.get_name() + ": " +
            "всего " + str(settlement.get_total_population()) +
            " | занято " + str(settlement.get_employed()) +
            " | свободно " + str(settlement.get_free())
        )

        self.table.setRowCount(0)
        jobs = self.service.get_jobs(province, settlement_name)
        for row in range(len(jobs)):
            job = jobs[row]
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(job.get_job_type()))
            self.table.setItem(row, 1, QTableWidgetItem(str(job.get_workers())))

    def clear_settlement_panel(self):
        self.list_settlements.clear()
        self.lbl_province_summary.setText("Провинция не выбрана")
        self.lbl_settlement.setText("Город не выбран")
        self.table.setRowCount(0)

    # ---------- Закрытие ----------

    def closeEvent(self, event):
        try:
            self.service.save_game()
            self.service.write_report()
            self.log.append("Автосохранение выполнено")
        except OSError as error:
            self.log.append("Автосохранение не удалось: " + str(error))
        event.accept()