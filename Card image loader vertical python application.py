import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Просмотрщик изображений")
        self.root.geometry("1200x800")
        
        # Список загруженных изображений
        self.images = []  # Список объектов Image
        self.image_paths = []  # Список путей к файлам
        self.thumbnails = []  # Список ImageTk для миниатюр
        
        # Создаем интерфейс
        self.create_widgets()
        
    def create_widgets(self):
        # Верхняя панель управления
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Кнопка загрузки изображений
        load_btn = tk.Button(top_frame, text="Загрузить изображения", 
                            command=self.load_images, width=20)
        load_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Кнопка очистки галереи
        clear_btn = tk.Button(top_frame, text="Очистить галерею", 
                             command=self.clear_gallery, width=20)
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Кнопка сохранения информации
        save_btn = tk.Button(top_frame, text="Сохранить список", 
                            command=self.save_image_list, width=20)
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Метка с информацией о загруженных изображениях
        self.info_label = tk.Label(top_frame, text="Изображений: 0")
        self.info_label.pack(side=tk.RIGHT)
        
        # Фрейм для галереи изображений с горизонтальной прокруткой
        gallery_frame = tk.Frame(self.root)
        gallery_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Создаем Canvas для горизонтальной галереи
        self.canvas = tk.Canvas(gallery_frame, bg="white")
        
        # Добавляем горизонтальную прокрутку
        h_scrollbar = tk.Scrollbar(gallery_frame, orient=tk.HORIZONTAL, 
                                  command=self.canvas.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Добавляем вертикальную прокрутку (на всякий случай)
        v_scrollbar = tk.Scrollbar(gallery_frame, orient=tk.VERTICAL, 
                                  command=self.canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(xscrollcommand=h_scrollbar.set, 
                             yscrollcommand=v_scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Фрейм внутри Canvas для размещения изображений
        self.image_container = tk.Frame(self.canvas, bg="white")
        self.canvas_window = self.canvas.create_window((0, 0), 
                                                      window=self.image_container, 
                                                      anchor="nw")
        
        # Привязка событий для изменения размера
        self.image_container.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Область предпросмотра выбранного изображения
        preview_frame = tk.Frame(self.root)
        preview_frame.pack(fill=tk.X, padx=10, pady=10)
        
        preview_label = tk.Label(preview_frame, text="Предпросмотр выбранного изображения:")
        preview_label.pack(anchor="w")
        
        # Фрейм для предпросмотра
        self.preview_frame = tk.Frame(preview_frame, bg="lightgray", 
                                     height=200, relief=tk.SUNKEN)
        self.preview_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Метка для предпросмотра
        self.preview_label = tk.Label(self.preview_frame, text="Выберите изображение для предпросмотра")
        self.preview_label.pack(expand=True, fill=tk.BOTH)
        
        # Статусная строка
        status_frame = tk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.status_label = tk.Label(status_frame, text="Готов к загрузке изображений", anchor="w")
        self.status_label.pack(side=tk.LEFT)
        
        help_label = tk.Label(status_frame, 
                             text="Поддерживаемые форматы: JPG, PNG, GIF, BMP", 
                             anchor="e")
        help_label.pack(side=tk.RIGHT)
    
    def load_images(self):
        """Загружает несколько изображений"""
        filetypes = [
            ("Изображения", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff"),
            ("Все файлы", "*.*")
        ]
        
        paths = filedialog.askopenfilenames(
            title="Выберите изображения",
            filetypes=filetypes
        )
        
        if not paths:
            return
        
        new_images_count = 0
        for path in paths:
            if path not in self.image_paths:  # Проверяем, не загружено ли уже
                try:
                    # Открываем изображение с помощью PIL
                    img = Image.open(path)
                    self.images.append(img)
                    self.image_paths.append(path)
                    new_images_count += 1
                    
                except Exception as e:
                    messagebox.showerror("Ошибка", 
                                       f"Не удалось загрузить {os.path.basename(path)}: {e}")
        
        if new_images_count > 0:
            self.update_gallery()
            self.update_info()
            self.status_label.config(text=f"Загружено {new_images_count} новых изображений")
    
    def create_thumbnail_widget(self, image, index):
        """Создает виджет миниатюры для галереи"""
        # Создаем фрейм для миниатюры
        frame = tk.Frame(self.image_container, relief=tk.RAISED, borderwidth=2)
        
        # Создаем миниатюру
        thumbnail_size = (150, 150)
        img_copy = image.copy()
        img_copy.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
        
        # Создаем ImageTk для отображения
        photo = ImageTk.PhotoImage(img_copy)
        
        # Сохраняем ссылку на фото
        self.thumbnails.append(photo)
        
        # Создаем метку с изображением
        label = tk.Label(frame, image=photo)
        label.pack(padx=5, pady=5)
        
        # Добавляем имя файла
        filename = tk.Label(frame, text=os.path.basename(self.image_paths[index]), 
                           wraplength=140)
        filename.pack(padx=5, pady=(0, 5))
        
        # Добавляем номер изображения
        number_label = tk.Label(frame, text=f"#{index+1}", 
                               bg="yellow", font=("Arial", 10, "bold"))
        number_label.place(x=5, y=5)
        
        # Привязываем событие клика для предпросмотра
        label.bind("<Button-1>", lambda e, idx=index: self.show_preview(idx))
        filename.bind("<Button-1>", lambda e, idx=index: self.show_preview(idx))
        number_label.bind("<Button-1>", lambda e, idx=index: self.show_preview(idx))
        
        return frame
    
    def update_gallery(self):
        """Обновляет галерею изображений"""
        # Очищаем контейнер
        for widget in self.image_container.winfo_children():
            widget.destroy()
        
        # Очищаем список миниатюр
        self.thumbnails.clear()
        
        # Создаем новые миниатюры
        for i, img in enumerate(self.images):
            thumbnail_frame = self.create_thumbnail_widget(img, i)
            thumbnail_frame.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
    
    def show_preview(self, index):
        """Показывает предпросмотр выбранного изображения"""
        if 0 <= index < len(self.images):
            try:
                # Очищаем область предпросмотра
                for widget in self.preview_frame.winfo_children():
                    widget.destroy()
                
                # Создаем увеличенную версию для предпросмотра
                preview_size = (400, 300)
                img_copy = self.images[index].copy()
                img_copy.thumbnail(preview_size, Image.Resampling.LANCZOS)
                
                # Создаем ImageTk
                photo = ImageTk.PhotoImage(img_copy)
                
                # Создаем метку с изображением
                preview_label = tk.Label(self.preview_frame, image=photo)
                preview_label.photo = photo  # Сохраняем ссылку
                preview_label.pack(expand=True, fill=tk.BOTH)
                
                # Добавляем информацию об изображении
                info_text = f"{os.path.basename(self.image_paths[index])}\n"
                info_text += f"Размер: {self.images[index].size[0]}x{self.images[index].size[1]}\n"
                info_text += f"Формат: {self.images[index].format}"
                
                info_label = tk.Label(self.preview_frame, text=info_text, 
                                     bg="lightgray", justify=tk.LEFT)
                info_label.pack(fill=tk.X)
                
                self.status_label.config(text=f"Выбрано изображение #{index+1}: {os.path.basename(self.image_paths[index])}")
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось показать предпросмотр: {e}")
    
    def clear_gallery(self):
        """Очищает галерею изображений"""
        if self.images:
            if messagebox.askyesno("Подтверждение", 
                                  "Вы уверены, что хотите очистить галерею?"):
                self.images.clear()
                self.image_paths.clear()
                self.thumbnails.clear()
                
                # Очищаем контейнер
                for widget in self.image_container.winfo_children():
                    widget.destroy()
                
                # Очищаем предпросмотр
                for widget in self.preview_frame.winfo_children():
                    widget.destroy()
                
                self.preview_label = tk.Label(self.preview_frame, 
                                             text="Выберите изображение для предпросмотра")
                self.preview_label.pack(expand=True, fill=tk.BOTH)
                
                self.update_info()
                self.status_label.config(text="Галерея очищена")
    
    def save_image_list(self):
        """Сохраняет список загруженных изображений в текстовый файл"""
        if not self.image_paths:
            messagebox.showwarning("Пустой список", "Нет изображений для сохранения")
            return
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="image_list.txt"
        )
        
        if not save_path:
            return
        
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write("Список загруженных изображений:\n")
                f.write("=" * 50 + "\n\n")
                
                for i, path in enumerate(self.image_paths, 1):
                    f.write(f"{i}. {os.path.basename(path)}\n")
                    f.write(f"   Путь: {path}\n")
                    
                    if i - 1 < len(self.images):
                        img = self.images[i-1]
                        f.write(f"   Размер: {img.size[0]}x{img.size[1]}\n")
                        f.write(f"   Формат: {img.format}\n")
                    
                    f.write("\n")
                
                f.write(f"\nВсего изображений: {len(self.image_paths)}\n")
            
            messagebox.showinfo("Успех", f"Список сохранен в:\n{save_path}")
            self.status_label.config(text=f"Список сохранен: {os.path.basename(save_path)}")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")
    
    def update_info(self):
        """Обновляет информацию о загруженных изображениях"""
        count = len(self.images)
        self.info_label.config(text=f"Изображений: {count}")
    
    def on_frame_configure(self, event=None):
        """Обновляет область прокрутки при изменении размера фрейма"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """Изменяет размер окна внутри Canvas"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)

def main():
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
