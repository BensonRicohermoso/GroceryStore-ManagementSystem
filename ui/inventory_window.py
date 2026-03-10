"""
Inventory Management Window - Complete Implementation
ui/inventory_window.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from modules.inventory import InventoryManager
from modules.products import ProductManager
from ui.styles import AppStyles
import config


class InventoryWindow:
    """Inventory management window"""
    
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.window = tk.Toplevel(parent)
        self.window.title("Inventory Management")
        self.window.geometry("1400x800")
        
        AppStyles.configure_ttk_styles()
        self.create_widgets()
        self.load_data()
    
    def create_widgets(self):
        """Create UI widgets"""
        main_container = tk.Frame(self.window, bg=AppStyles.BACKGROUND)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_container, bg=AppStyles.WARNING, height=60)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="📋 Inventory Management",
            font=AppStyles.FONT_HEADER,
            bg=AppStyles.WARNING,
            fg=AppStyles.WHITE
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        # Content
        content_frame = tk.Frame(main_container, bg=AppStyles.BACKGROUND)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left - Stock levels
        left_frame = tk.Frame(content_frame, bg=AppStyles.BACKGROUND)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Right - Low stock & actions
        right_frame = tk.Frame(content_frame, bg=AppStyles.BACKGROUND, width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_frame.pack_propagate(False)
        
        self.create_stock_table(left_frame)
        self.create_low_stock_section(right_frame)
    
    def create_stock_table(self, parent):
        """Create current stock table"""
        stock_card = AppStyles.create_card_frame(parent)
        stock_card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            stock_card,
            text="Current Stock Levels",
            font=AppStyles.FONT_LARGE,
            bg=AppStyles.WHITE,
            fg=AppStyles.PRIMARY
        ).pack(pady=(20, 10), padx=20, anchor='w')
        
        # Search
        search_frame = tk.Frame(stock_card, bg=AppStyles.WHITE)
        search_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        AppStyles.create_button(search_frame, "Search", lambda: self.load_data()).pack(side=tk.LEFT)
        
        # Table
        table_frame = tk.Frame(stock_card, bg=AppStyles.WHITE)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('Product', 'Barcode', 'Stock', 'Reorder', 'Status')
        self.stock_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.stock_tree.yview)
        
        for col in columns:
            self.stock_tree.heading(col, text=col)
        
        self.stock_tree.column('Product', width=250)
        self.stock_tree.column('Barcode', width=120)
        self.stock_tree.column('Stock', width=80)
        self.stock_tree.column('Reorder', width=80)
        self.stock_tree.column('Status', width=100)
        
        self.stock_tree.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        btn_frame = tk.Frame(stock_card, bg=AppStyles.WHITE)
        btn_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        AppStyles.create_button(btn_frame, "📦 Restock Selected", self.restock_product, 'Success.TButton').pack(side=tk.LEFT, padx=(0, 10))
        AppStyles.create_button(btn_frame, "✏️ Adjust Stock", self.adjust_stock, 'Primary.TButton').pack(side=tk.LEFT)
    
    def create_low_stock_section(self, parent):
        """Create low stock alerts"""
        alert_card = AppStyles.create_card_frame(parent)
        alert_card.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        tk.Label(
            alert_card,
            text="⚠️ Low Stock Alerts",
            font=AppStyles.FONT_LARGE,
            bg=AppStyles.WHITE,
            fg=AppStyles.DANGER
        ).pack(pady=(20, 10), padx=20, anchor='w')
        
        list_frame = tk.Frame(alert_card, bg=AppStyles.WHITE)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.alert_listbox = tk.Listbox(
            list_frame,
            font=AppStyles.FONT_NORMAL,
            yscrollcommand=scrollbar.set
        )
        self.alert_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.alert_listbox.yview)
        
        # Summary card
        summary_card = AppStyles.create_card_frame(parent)
        summary_card.pack(fill=tk.BOTH)
        
        tk.Label(
            summary_card,
            text="Inventory Summary",
            font=AppStyles.FONT_LARGE,
            bg=AppStyles.WHITE,
            fg=AppStyles.PRIMARY
        ).pack(pady=(20, 10), padx=20, anchor='w')
        
        self.summary_frame = tk.Frame(summary_card, bg=AppStyles.WHITE)
        self.summary_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
    
    def load_data(self):
        """Load all inventory data"""
        # Load stock table
        search_term = self.search_var.get().strip()
        
        for item in self.stock_tree.get_children():
            self.stock_tree.delete(item)
        
        try:
            if search_term:
                products = ProductManager.search_products(search_term)
            else:
                products = ProductManager.get_all_products()
            
            for product in products:
                if product.stock_quantity <= product.reorder_level:
                    status = "LOW"
                    tags = ('low_stock',)
                else:
                    status = "OK"
                    tags = ()
                
                self.stock_tree.insert('', tk.END, values=(
                    product.product_name,
                    product.barcode,
                    product.stock_quantity,
                    product.reorder_level,
                    status
                ), tags=tags)
            
            self.stock_tree.tag_configure('low_stock', background='#ffe6e6')
            
            # Load low stock alerts
            self.alert_listbox.delete(0, tk.END)
            low_stock = InventoryManager.get_low_stock_products()
            
            for item in low_stock:
                self.alert_listbox.insert(tk.END, f"{item['product_name']}: {item['stock_quantity']} units")
            
            # Load summary
            summary = InventoryManager.get_inventory_summary()
            for widget in self.summary_frame.winfo_children():
                widget.destroy()
            
            currency = config.BUSINESS_CONFIG['currency_symbol']
            items = [
                ("Total Products:", str(summary.get('total_products', 0))),
                ("Total Units:", str(summary.get('total_stock_units', 0))),
                ("Stock Value:", f"{currency}{summary.get('total_stock_value', 0):.2f}"),
                ("Low Stock Items:", str(summary.get('low_stock_count', 0))),
                ("Out of Stock:", str(summary.get('out_of_stock_count', 0)))
            ]
            
            for label, value in items:
                frame = tk.Frame(self.summary_frame, bg=AppStyles.WHITE)
                frame.pack(fill=tk.X, pady=5)
                tk.Label(frame, text=label, font=AppStyles.FONT_NORMAL, bg=AppStyles.WHITE).pack(side=tk.LEFT)
                tk.Label(frame, text=value, font=AppStyles.FONT_MEDIUM, bg=AppStyles.WHITE, fg=AppStyles.PRIMARY).pack(side=tk.RIGHT)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load inventory:\n{e}")
    
    def restock_product(self):
        """Restock selected product"""
        selection = self.stock_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a product")
            return
        
        values = self.stock_tree.item(selection[0])['values']
        product_name = values[0]
        barcode = values[1]
        
        product = ProductManager.get_product_by_barcode(barcode)
        if not product:
            messagebox.showerror("Error", "Product not found")
            return
        
        quantity = simpledialog.askinteger(
            "Restock Product",
            f"How many units of '{product_name}' to add?",
            minvalue=1
        )
        
        if quantity:
            notes = simpledialog.askstring("Notes", "Notes (optional):")
            
            success = InventoryManager.restock_product(
                product.product_id,
                quantity,
                self.user.user_id,
                notes
            )
            
            if success:
                messagebox.showinfo("Success", f"Added {quantity} units to inventory")
                self.load_data()
            else:
                messagebox.showerror("Error", "Failed to restock")
    
    def adjust_stock(self):
        """Adjust stock to specific quantity"""
        selection = self.stock_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a product")
            return
        
        values = self.stock_tree.item(selection[0])['values']
        product_name = values[0]
        barcode = values[1]
        current_stock = values[2]
        
        product = ProductManager.get_product_by_barcode(barcode)
        if not product:
            return
        
        new_qty = simpledialog.askinteger(
            "Adjust Stock",
            f"Set new quantity for '{product_name}':\n\nCurrent: {current_stock}",
            initialvalue=current_stock,
            minvalue=0
        )
        
        if new_qty is not None:
            reason = simpledialog.askstring("Reason", "Reason for adjustment (required):")
            
            if not reason:
                messagebox.showwarning("Warning", "Reason is required")
                return
            
            success = InventoryManager.adjust_stock(
                product.product_id,
                new_qty,
                self.user.user_id,
                reason
            )
            
            if success:
                messagebox.showinfo("Success", "Stock adjusted successfully")
                self.load_data()
            else:
                messagebox.showerror("Error", "Failed to adjust stock")


def open_inventory_window(parent, user):
    """Open inventory window"""
    InventoryWindow(parent, user)
