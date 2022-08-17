import tkinter as tk
from tkinter import messagebox
from tkinter.messagebox import showinfo
from tkinter import *
from tkinter.ttk import Treeview
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
        Button(self.frame, text='Kolye Ekle', command=self.add_necklace_page).grid(row=1, column=0, sticky='w')
        
        self.bottom_frame = Frame(master)
        self.bottom_frame.pack(fill='x', expand=False)
        Button(self.frame, text='Boncuklari Göster', command=self.show_beads).grid(row=2, column=0, sticky='w')
        Button(self.frame, text='Kolyeleri Göster', command=self.show_necklace).grid(row=2, column=1, sticky='w')
        self.tree = Treeview(self.bottom_frame)
        
        
    def add_bead_page(self):
        self.new = Toplevel(self.frame)
        self.new.geometry("400x450")
        self.new.title("New Window")
        
        Label(self.new, text='Boncuk Adi: ').grid(row=1, column=0, sticky='e')
        Label(self.new, text='Boncuk Adeti: ').grid(row=2, column=0, sticky='e')
        Label(self.new, text='Fiyat: ').grid(row=3, column=0, sticky='e')
        
        self.new_bead_name = Entry(self.new)
        self.new_bead_name.grid(row=1, column=1)
        self.new_bead_piece = Entry(self.new)
        self.new_bead_piece.grid(row=2, column=1)
        self.new_bead_price = Entry(self.new)
        self.new_bead_price.grid(row=3, column=1)
        Button(self.new, text='Ekle', command=self.add_bead_operations).grid(row=4, column=1)
        
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
            Label(self.new, text=item_name).grid(row=row_c, column=0, sticky='e')
            piece = Entry(self.new)
            piece.grid(row=row_c, column=1, pady=2)
            unit_price = Label(self.new, text=bead_list[item_name]['Unit_Price'])
            unit_price.grid(row=row_c, column=2, sticky='w')
            row_c +=1
            self.piece_entries.append({'name': item_name,
                                       'entry': piece})
        

        Label(self.new, text='Komisyon: ').grid(row=row_c+1, column=0)
        self.komisyon_text = Entry(self.new)
        self.komisyon_text.grid(row=row_c+1, column=1)
        self.komisyon_text.insert(0, '5.5')
        
        Label(self.new, text='Paketleme: ').grid(row=row_c+2, column=0)
        self.paketleme_text = Entry(self.new)
        self.paketleme_text.insert(0, '14')
        self.paketleme_text.grid(row=row_c+2, column=1)
        
        Label(self.new, text='Satış Fiyatı:').grid(row= row_c+3, column=0)
        self.urun_fiyat = Entry(self.new)
        self.urun_fiyat.grid(row=row_c+3, column=1)
        
        row_c +=4
        Button(self.new, text='Maliyet Hesapla', command=self.maliyet_hesapla).grid(row=row_c, column=0, columnspan=2, sticky='w')
        row_c +=1
        
        self.maliyet_label = Label(self.new, text='Boncukların Maliyeti: ')
        self.maliyet_label.grid(row=row_c, column=0, columnspan=2, sticky='w')
        row_c +=1
        self.toplam_maliyet = Label(self.new, text='Toplam Maliyet: ')
        self.toplam_maliyet.grid(row=row_c, column=0, columnspan=2, sticky='w')
        
        self.kazanc_label = Label(self.new, text='Kazanç: ')
        self.kazanc_label.grid(row=row_c, column=2, sticky='w')
        
        row_c +=1
        Label(self.new, text='Kolye Adı: ').grid(row=row_c, column=0)
        self.kolye_adi_text = Entry(self.new, text='')
        self.kolye_adi_text.grid(row=row_c, column=1)
        
        Button(self.new, text='Urun Ekle', command=self.add_necklace_operation).grid(row=row_c+2, column=2, sticky='w')
    
    def add_necklace_operation(self):
        if self.kolye_adi_text == '':
            messagebox.showinfo(title='Hata', message='Kolye adı boş, Lütfen gerekli alanları doldurunuz.', parent=self.new)
        item_list = dict()
        for each in self.piece_entries:
            piece = each['entry'].get()
            if piece != '':
                
                item_list[each['name']] = float(piece)

        try:
            boncuklarin_maliyeti = self.maliyet_label['text'].split(': ')[1]
            toplam_maliyet = self.toplam_maliyet['text'].split(': ')[1]
            kazanc = self.kazanc_label['text'].split(': ')[1]
            satis_fiyat = float(self.urun_fiyat.get())
            print(boncuklarin_maliyeti, toplam_maliyet, kazanc, satis_fiyat)
            self.items.add_new_necklace(item_list, self.kolye_adi_text.get(), satis_fiyat, boncuklarin_maliyeti, toplam_maliyet, kazanc)
            self.status_message['text'] = 'Kolye Kaydedildi'
            self.new.destroy()
        except:
            messagebox.showinfo(title='Hata', message='Kolye Eklenemedi.', parent=self.new)
    
    def maliyet_hesapla(self):
        item_amount = 0

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
        
        boncuklarin_maliyeti = item_amount
        paketleme = float(self.paketleme_text.get())
        satis_fiyati = float(self.urun_fiyat.get())
        komisyon = float(self.komisyon_text.get())
        komisyon_miktari = ((satis_fiyati*komisyon) / 100)
        
        kazanc = satis_fiyati - komisyon_miktari - paketleme - item_amount
        kazanc = "{:.2f}".format(kazanc)
        item_amount = "{:.2f}".format(item_amount)
        toplam_maliyet = boncuklarin_maliyeti + komisyon_miktari + paketleme
        boncuklarin_maliyeti = "{:.2f}".format(boncuklarin_maliyeti)
        toplam_maliyet = "{:.2f}".format(toplam_maliyet)
        self.maliyet_label['text'] = f'Boncukların Maliyeti: {boncuklarin_maliyeti}'
        self.toplam_maliyet['text'] = f'Toplam Maliyet: {toplam_maliyet}'
        self.kazanc_label['text'] = f'Kazanç: {kazanc}'

    def show_beads(self):
        self.remove_tree_view()
        column_list = ["boncuk_adi", "birim_fiyat"]
        self.tree = Treeview(self.bottom_frame, columns=column_list, show='headings')
        self.tree.heading('boncuk_adi', text='Boncuk Adı')
        self.tree.heading('birim_fiyat', text='Birim Fiyatı')
        self.tree.grid(row=0, column=0)
        
        beads = self.items.product['beads']
        
        for item in beads.values():
            contact = (item['Item_Name'], item['Unit_Price'])
            self.tree.insert('', tk.END, values=contact)
            
    def show_necklace(self):
        self.remove_tree_view()
        self.show_info_button = Button(self.bottom_frame, text='Ürün Detaylarını Gör', command=self.necklace_info)
        self.show_info_button.grid(row=1, column=0, sticky='NW')
        column_list = ["kolye_adi", "boncuk_maliyet_fiyati", "toplam_maliyet", 'satis_fiyati']
        self.tree = Treeview(self.bottom_frame, columns=column_list, show='headings')
        self.tree.heading('kolye_adi', text='Kolye Adı')
        self.tree.heading('boncuk_maliyet_fiyati', text='Boncuk Fiyatı')
        self.tree.heading('toplam_maliyet', text='Toplam Maliyet')
        self.tree.heading('satis_fiyati', text='Satış Fiyatı')
        self.tree.grid(row=0, column=0)

        necklaces = self.items.product['products']
        
        for item in necklaces.values():

            contact = (item['Item_Name'], item['Boncuk_Maliyeti'], item['Toplam_Maliyet'], item['Satis_Fiyati'])
            self.tree.insert('', tk.END, values=contact)

    def remove_tree_view(self):
        self.tree.grid_remove()
        try:
            self.show_info_button.grid_remove()
        except:
            pass
        try:
            self.detaylar_tree.grid_remove()
        except:
            pass
    def necklace_info(self):
        column_list = ['boncuk_adi', 'boncuk_adet']
        self.detaylar_tree = Treeview(self.bottom_frame, columns=column_list, show='headings') 
        self.detaylar_tree.heading('boncuk_adi', text='Boncuk')
        self.detaylar_tree.heading('boncuk_adet', text='Kullanılan Adet')
        self.detaylar_tree.grid(row=1, column=0, sticky='e')
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            itemname, _, _,_ = item['values']        # get values from the table
            item_info = self.items.product['products'][itemname]['Beads']
            for name, piece in item_info.items():
                self.detaylar_tree.insert('', tk.END, values=(name, piece))
        
         
    
if __name__ == "__main__":
    
    root = tk.Tk()
    root.title('Maliyet Hesaplama')
    root.geometry('1100x550+200+100')
    obj = app(root)
    root.mainloop()