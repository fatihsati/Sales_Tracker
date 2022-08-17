from audioop import add
from cgitb import text
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import Treeview
from turtle import onclick
from ProductOperations import Product

class app:
    def __init__(self, master):
        self.items = Product()
        self.frame = Frame(master)
        self.frame.pack(fill='x', expand=False)
        self.status_message = Label(self.frame, text='')
        self.status_message.grid(row=0, column=1, sticky='e')
        self.add_bead_button = Button(self.frame, text='Boncuk Ekle', command=self.add_bead_page)
        self.add_bead_button.grid(row=0, column=0, sticky='w')
        add_necklace_button = Button(self.frame, text='Kolye Ekle', command=self.add_necklace_page).grid(row=1, column=0, sticky='w')
        
        self.bottom_frame = Frame(master)
        self.bottom_frame.pack(fill='x', expand=False)
        show_beads_button = Button(self.frame, text='Boncuklari Göster', command=self.show_beads).grid(row=2, column=0, sticky='w')
        show_necklace_button = Button(self.frame, text='Kolyeleri Göster', command=self.show_necklace).grid(row=2, column=1, sticky='w')
        
        
    def add_bead_page(self):
        self.new = Toplevel(self.frame)
        self.new.geometry("400x450")
        self.new.title("New Window")
        
        bead_name = Label(self.new, text='Boncuk Adi: ').grid(row=1, column=0)
        piece_label = Label(self.new, text='Boncuk Adeti: ').grid(row=2, column=0)
        fiyat_label = Label(self.new, text='Fiyat: ').grid(row=3, column=0)
        
        self.new_bead_name = Entry(self.new)
        self.new_bead_name.grid(row=1, column=1)
        self.new_bead_piece = Entry(self.new)
        self.new_bead_piece.grid(row=2, column=1)
        self.new_bead_price = Entry(self.new)
        self.new_bead_price.grid(row=3, column=1)
        add_button = Button(self.new, text='Ekle', command=self.add_bead_operations).grid(row=4, column=1)
        
    def add_bead_operations(self):
        
        if self.new_bead_name.get() == '':
            messagebox.showinfo(title='Hata', message='Boncuk Adi Boş Olamaz!', parent=self.new)
            return
        if self.new_bead_piece.get() == '':
            messagebox.showinfo(title='Hata', message='Boncuk Adeti Boş Olamaz!', parent=self.new)
            return
        if self.new_bead_price.get() == '':
            messagebox.showinfo(title='Hata', message='Fiyat Boş Olamaz!', parent=self.new)
        
        piece = float(self.new_bead_piece.get())
        price = float(self.new_bead_price.get())
        name = self.new_bead_name.get()

        try:
            self.items.add_new_bead(piece, price, name)
            self.status_message['text'] = 'Boncuk Kaydedildi'
            self.new.destroy()
        except:
            messagebox.showinfo(title='Hata', message='Ürün Eklenirken bir hata oluştu', parent=self.new)
 
    def add_necklace_page(self):
        self.new = Toplevel(self.frame)
        self.new.geometry("400x450")
        self.new.title("New Window")
        
        bead_list = self.items.product['beads']
        if len(bead_list) == 0:
            messagebox.showinfo(title='Hata', message='Kolye eklemek için kayıtlı boncuk olması gerekiyor.', parent=self.new)
        row_c = 0
        self.piece_entries = []
        for item_name in bead_list.keys():
            item = Label(self.new, text=item_name).grid(row=row_c, column=0)
            piece = Entry(self.new)
            piece.grid(row=row_c, column=1, padx=10)
            unit_price = Label(self.new, text=bead_list[item_name]['Unit_Price'])
            unit_price.grid(row=row_c, column=2)
            row_c +=1
            self.piece_entries.append({'name': item_name,
                                       'entry': piece})
        

        komisyon_label = Label(self.new, text='Komisyon: ').grid(row=row_c+1, column=0)
        self.komisyon_text = Entry(self.new)
        self.komisyon_text.grid(row=row_c+1, column=1)
        self.komisyon_text.insert(0, '5.5')
        paketleme_label = Label(self.new, text='Paketleme: ').grid(row=row_c+2, column=0)
        self.paketleme_text = Entry(self.new)
        self.paketleme_text.insert(0, '14')
        self.paketleme_text.grid(row=row_c+2, column=1)
        urun_fiyat_label = Label(self.new, text='Satış Fiyatı:').grid(row= row_c+3, column=0)
        self.urun_fiyat = Entry(self.new)
        self.urun_fiyat.grid(row=row_c+3, column=1)
        
        row_c +=4
        maliyet_hesapla_button = Button(self.new, text='Maliyet Hesapla', command=self.maliyet_hesapla).grid(row=row_c, column=0)
        self.maliyet_label = Label(self.new, text='Toplam Maliyet: ')
        self.maliyet_label.grid(row=row_c, column=1)
        self.kazanc_label = Label(self.new, text='Kazanç: ')
        self.kazanc_label.grid(row=row_c, column=2)
        row_c +=1
        kolye_adi = Label(self.new, text='Kolye Adı: ').grid(row=row_c, column=0)
        self.kolye_adi_text = Entry(self.new, text='')
        self.kolye_adi_text.grid(row=row_c, column=1)
        add_button = Button(self.new, text='Urun Ekle', command=self.add_necklace_operation).grid(row=row_c+2, column=2)
    
    def add_necklace_operation(self):
        if self.kolye_adi_text == '':
            messagebox.showinfo(title='Hata', message='Kolye adı boş, Lütfen gerekli alanları doldurunuz.', parent=self.new)
        item_list = dict()
        for each in self.piece_entries:
            piece = each['entry'].get()
            if piece != '':
                
                item_list[each['name']] = float(piece)

        try:
            self.items.add_new_necklace(item_list, self.kolye_adi_text.get(), float(self.urun_fiyat.get()))
            self.status_message['text'] = 'Kolye Kaydedildi'
            self.new.destroy()
        except:
            messagebox.showinfo(title='Hata', message='Kolye Eklenemedi.', parent=self.new)
    
    def maliyet_hesapla(self):
        item_amount = 0
        # add komisyon paketleme ucreti vs
        #
        for each in self.piece_entries:
            piece = each['entry'].get()
            name = each['name']
            if piece == '':
                piece = 0
            piece = int(piece)
            unit_price = float(self.items.product['beads'][name]['Unit_Price'])
            item_amount += piece * unit_price
            
        if self.paketleme_text.get() == '' or self.urun_fiyat.get() == '' or self.komisyon_text.get() =='':
            messagebox.showinfo(title='Hata', message='Bazı alanlar boş, Lütfen gerekli alanları doldurunuz.', parent=self.new)
        item_amount += float(self.paketleme_text.get())
        # satis fiyati yazilacak, altta kar kismi olucak hesaplaya basildigi zaman kar hesaplayacak, ekle derse ekleyecek.
        satis_fiyati = float(self.urun_fiyat.get())
        komisyon = float(self.komisyon_text.get())

        kazanc = satis_fiyati - ((satis_fiyati*komisyon) / 100) - item_amount
        kazanc = "{:.2f}".format(kazanc)
        item_amount = "{:.2f}".format(item_amount)
        self.maliyet_label['text'] = f'Toplam Maliyet: {item_amount}'
        self.kazanc_label['text'] = f'Kazanç: {kazanc}'

    def show_beads(self):
        # create treeview for bead list.
        column_list = ["boncuk_adi", "birim_fiyat"]
        tree = Treeview(self.bottom_frame, columns=column_list, show='headings')
        tree.heading('boncuk_adi', text='Boncuk Adı')
        tree.heading('birim_fiyat', text='Birim Fiyatı')
        
        tree.grid(row=1, column=0)
            
    def show_necklace(self):
        pass

if __name__ == "__main__":
    
    root = tk.Tk()
    root.title('Maliyet Hesaplama')
    root.geometry('400x450')
    obj = app(root)
    root.mainloop()