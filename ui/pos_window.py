import tkinter as tk
from tkinter import ttk, messagebox
from modules.products import ProductManager
from modules.sales import SalesManager, CartItem
from ui.styles import AppStyles
from utils.validators import Validator
from utils.pdf_generator import PDFGenerator
import config
from datetime import datetime


class POSWindow:
    """Point of Sale window for processing sales"""
    
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.window = tk.Toplevel(parent)
        self.window.title("Point of Sale (POS)")
        self.window.geometry("1600x900")
        
        # Configure styles
        AppStyles.configure_ttk_styles()
        
        # Cart items
        self.cart_items = []  # List of CartItem objects
        
        # Create UI
        self.create_widgets()
        
        # Focus on barcode entry
        self.barcode_entry.focus()
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_container = tk.Frame(self.window, bg=AppStyles.BACKGROUND)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_container, bg=AppStyles.SUCCESS, height=70)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🛒 Point of Sale",
            font=AppStyles.FONT_HEADER,
            bg=AppStyles.SUCCESS,
            fg=AppStyles.WHITE
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        cashier_label = tk.Label(
            header_frame,
            text=f"Cashier: {self.user.full_name}",
            font=AppStyles.FONT_MEDIUM,
            bg=AppStyles.SUCCESS,
            fg=AppStyles.WHITE
        )
        cashier_label.pack(side=tk.RIGHT, padx=20)
        
        # Content area - three columns
        content_frame = tk.Frame(main_container, bg=AppStyles.BACKGROUND)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left - Product search and add
        left_frame = tk.Frame(content_frame, bg=AppStyles.BACKGROUND, width=400)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        left_frame.pack_propagate(False)
        
        # Center - Shopping cart
        center_frame = tk.Frame(content_frame, bg=AppStyles.BACKGROUND)
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Right - Totals and payment
        right_frame = tk.Frame(content_frame, bg=AppStyles.BACKGROUND, width=350)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        right_frame.pack_propagate(False)
        
        self.create_product_search(left_frame)
        self.create_shopping_cart(center_frame)
        self.create_payment_section(right_frame)
    
    def create_product_search(self, parent):
        """Create product search section"""
        # Barcode scan card
        scan_card = AppStyles.create_card_frame(parent)
        scan_card.pack(fill=tk.X, pady=(0, 10))
        
        scan_header = tk.Label(
            scan_card,
            text="Scan Barcode",
            font=AppStyles.FONT_LARGE,
            bg=AppStyles.WHITE,
            fg=AppStyles.PRIMARY
        )
        scan_header.pack(pady=(15, 10), padx=15, anchor='w')
        
        barcode_frame = tk.Frame(scan_card, bg=AppStyles.WHITE)
        barcode_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        self.barcode_var = tk.StringVar()
        self.barcode_entry = ttk.Entry(
            barcode_frame,
            textvariable=self.barcode_var,
            font=AppStyles.FONT_LARGE,
            width=20
        )
        self.barcode_entry.pack(fill=tk.X, pady=(0, 10))
        self.barcode_entry.bind('<Return>', lambda e: self.add_by_barcode())
        
        add_btn = AppStyles.create_button(
            barcode_frame,
            text="➕ Add to Cart",
            command=self.add_by_barcode,
            style='Success.TButton'
        )
        add_btn.pack(fill=tk.X)
        
        # Product search card
        search_card = AppStyles.create_card_frame(parent)
        search_card.pack(fill=tk.BOTH, expand=True)
        
        search_header = tk.Label(
            search_card,
            text="Search Products",
            font=AppStyles.FONT_LARGE,
            bg=AppStyles.WHITE,
            fg=AppStyles.PRIMARY
        )
        search_header.pack(pady=(15, 10), padx=15, anchor='w')
        
        search_frame = tk.Frame(search_card, bg=AppStyles.WHITE)
        search_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=AppStyles.FONT_NORMAL
        )
        search_entry.pack(fill=tk.X, pady=(0, 5))
        search_entry.bind('<KeyRelease>', lambda e: self.search_products())
        
        # Product list
        list_frame = tk.Frame(search_card, bg=AppStyles.WHITE)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.product_listbox = tk.Listbox(
            list_frame,
            font=AppStyles.FONT_NORMAL,
            yscrollcommand=scrollbar.set,
            height=20
        )
        self.product_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.product_listbox.yview)
        
        self.product_listbox.bind('<Double-Button-1>', lambda e: self.add_selected_product())
        
        add_selected_btn = AppStyles.create_button(
            search_card,
            text="➕ Add Selected to Cart",
            command=self.add_selected_product,
            style='Success.TButton'
        )
        add_selected_btn.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Store product data
        self.product_data = []
    
    def create_shopping_cart(self, parent):
        """Create shopping cart section"""
        cart_card = AppStyles.create_card_frame(parent)
        cart_card.pack(fill=tk.BOTH, expand=True)
        
        # Cart header
        header_frame = tk.Frame(cart_card, bg=AppStyles.WHITE)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        cart_header = tk.Label(
            header_frame,
            text="Shopping Cart",
            font=AppStyles.FONT_LARGE,
            bg=AppStyles.WHITE,
            fg=AppStyles.PRIMARY
        )
        cart_header.pack(side=tk.LEFT)
        
        clear_cart_btn = AppStyles.create_button(
            header_frame,
            text="🗑️ Clear Cart",
            command=self.clear_cart,
            style='Danger.TButton'
        )
        clear_cart_btn.pack(side=tk.RIGHT)
        
        # Cart table
        table_frame = tk.Frame(cart_card, bg=AppStyles.WHITE)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ('Product', 'Price', 'Qty', 'Subtotal')
        self.cart_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.config(command=self.cart_tree.yview)
        
        # Headings
        self.cart_tree.heading('Product', text='Product Name')
        self.cart_tree.heading('Price', text='Unit Price')
        self.cart_tree.heading('Qty', text='Quantity')
        self.cart_tree.heading('Subtotal', text='Subtotal')
        
        # Widths
        self.cart_tree.column('Product', width=300)
        self.cart_tree.column('Price', width=100)
        self.cart_tree.column('Qty', width=80)
        self.cart_tree.column('Subtotal', width=120)
        
        self.cart_tree.pack(fill=tk.BOTH, expand=True)
        
        # Cart actions
        actions_frame = tk.Frame(cart_card, bg=AppStyles.WHITE)
        actions_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        remove_btn = AppStyles.create_button(
            actions_frame,
            text="➖ Remove Selected",
            command=self.remove_from_cart,
            style='Danger.TButton'
        )
        remove_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        update_qty_btn = AppStyles.create_button(
            actions_frame,
            text="✏️ Update Quantity",
            command=self.update_quantity,
            style='Primary.TButton'
        )
        update_qty_btn.pack(side=tk.LEFT)
    
    def create_payment_section(self, parent):
        """Create payment and totals section"""
        payment_card = AppStyles.create_card_frame(parent)
        payment_card.pack(fill=tk.BOTH, expand=True)
        
        # Header
        payment_header = tk.Label(
            payment_card,
            text="Payment",
            font=AppStyles.FONT_LARGE,
            bg=AppStyles.WHITE,
            fg=AppStyles.PRIMARY
        )
        payment_header.pack(pady=(20, 15), padx=20, anchor='w')
        
        # Customer info
        info_frame = tk.Frame(payment_card, bg=AppStyles.WHITE)
        info_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        tk.Label(info_frame, text="Customer Name:", font=AppStyles.FONT_NORMAL,
                bg=AppStyles.WHITE).grid(row=0, column=0, sticky='w', pady=5)
        self.customer_name_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.customer_name_var,
                 font=AppStyles.FONT_NORMAL).grid(row=0, column=1, sticky='ew', pady=5)
        
        tk.Label(info_frame, text="Customer Phone:", font=AppStyles.FONT_NORMAL,
                bg=AppStyles.WHITE).grid(row=1, column=0, sticky='w', pady=5)
        self.customer_phone_var = tk.StringVar()
        ttk.Entry(info_frame, textvariable=self.customer_phone_var,
                 font=AppStyles.FONT_NORMAL).grid(row=1, column=1, sticky='ew', pady=5)
        
        info_frame.columnconfigure(1, weight=1)
        
        # Discount
        discount_frame = tk.Frame(payment_card, bg=AppStyles.WHITE)
        discount_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        tk.Label(discount_frame, text="Discount (%):", font=AppStyles.FONT_NORMAL,
                bg=AppStyles.WHITE).pack(side=tk.LEFT)
        self.discount_var = tk.StringVar(value="0")
        discount_entry = ttk.Entry(discount_frame, textvariable=self.discount_var,
                                   font=AppStyles.FONT_NORMAL, width=10)
        discount_entry.pack(side=tk.LEFT, padx=(10, 10))
        discount_entry.bind('<KeyRelease>', lambda e: self.calculate_totals())
        
        apply_btn = AppStyles.create_button(
            discount_frame,
            text="Apply",
            command=self.calculate_totals,
            style='Primary.TButton'
        )
        apply_btn.pack(side=tk.LEFT)
        
        # Payment method
        payment_method_frame = tk.Frame(payment_card, bg=AppStyles.WHITE)
        payment_method_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        tk.Label(payment_method_frame, text="Payment Method:",
                font=AppStyles.FONT_NORMAL, bg=AppStyles.WHITE).pack(anchor='w', pady=(0, 5))
        
        self.payment_method_var = tk.StringVar(value="cash")
        methods = [("Cash", "cash"), ("Card", "card"), ("Mobile Money", "mobile_money")]
        for text, value in methods:
            tk.Radiobutton(
                payment_method_frame,
                text=text,
                variable=self.payment_method_var,
                value=value,
                font=AppStyles.FONT_NORMAL,
                bg=AppStyles.WHITE
            ).pack(anchor='w')
        
        # Totals
        totals_frame = tk.Frame(payment_card, bg=AppStyles.LIGHT, relief=tk.SOLID, borderwidth=1)
        totals_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        currency = config.BUSINESS_CONFIG['currency_symbol']
        
        self.subtotal_label = self.create_total_row(totals_frame, "Subtotal:", f"{currency}0.00", 0)
        self.discount_label = self.create_total_row(totals_frame, "Discount:", f"{currency}0.00", 1)
        self.tax_label = self.create_total_row(totals_frame, "Tax:", f"{currency}0.00", 2)
        
        # Total (larger)
        total_frame = tk.Frame(totals_frame, bg=AppStyles.SUCCESS, height=60)
        total_frame.grid(row=3, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        total_frame.pack_propagate(False)
        
        tk.Label(total_frame, text="TOTAL:", font=AppStyles.FONT_HEADER,
                bg=AppStyles.SUCCESS, fg=AppStyles.WHITE).pack(side=tk.LEFT, padx=20)
        
        self.total_label = tk.Label(
            total_frame,
            text=f"{currency}0.00",
            font=('Segoe UI', 32, 'bold'),
            bg=AppStyles.SUCCESS,
            fg=AppStyles.WHITE
        )
        self.total_label.pack(side=tk.RIGHT, padx=20)
        
        # Complete sale button
        complete_btn = AppStyles.create_button(
            payment_card,
            text="💳 COMPLETE SALE",
            command=self.complete_sale,
            style='Success.TButton'
        )
        complete_btn.pack(fill=tk.X, padx=20, pady=(0, 20), ipady=20)
        
        totals_frame.columnconfigure(0, weight=1)
        totals_frame.columnconfigure(1, weight=1)
    
    def create_total_row(self, parent, label_text, value_text, row):
        """Create a row in totals section"""
        label = tk.Label(
            parent,
            text=label_text,
            font=AppStyles.FONT_MEDIUM,
            bg=AppStyles.LIGHT,
            anchor='w'
        )
        label.grid(row=row, column=0, sticky='w', padx=20, pady=10)
        
        value = tk.Label(
            parent,
            text=value_text,
            font=AppStyles.FONT_LARGE,
            bg=AppStyles.LIGHT,
            anchor='e'
        )
        value.grid(row=row, column=1, sticky='e', padx=20, pady=10)
        
        return value
    
    def search_products(self):
        """Search products and populate listbox"""
        search_term = self.search_var.get().strip()
        
        # Clear listbox
        self.product_listbox.delete(0, tk.END)
        self.product_data = []
        
        if not search_term:
            return
        
        try:
            products = ProductManager.search_products(search_term, active_only=True)
            currency = config.BUSINESS_CONFIG['currency_symbol']
            
            for product in products:
                if product.stock_quantity > 0:
                    display_text = f"{product.product_name} - {currency}{product.unit_price:.2f} (Stock: {product.stock_quantity})"
                    self.product_listbox.insert(tk.END, display_text)
                    self.product_data.append(product)
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search products:\n{e}")
    
    def add_by_barcode(self):
        """Add product to cart by barcode"""
        barcode = self.barcode_var.get().strip()
        
        if not barcode:
            messagebox.showwarning("Warning", "Please enter a barcode")
            return
        
        try:
            product = ProductManager.get_product_by_barcode(barcode)
            
            if not product:
                messagebox.showerror("Error", f"Product not found with barcode: {barcode}")
                self.barcode_var.set('')
                return
            
            if product.stock_quantity <= 0:
                messagebox.showerror("Error", f"Product '{product.product_name}' is out of stock")
                self.barcode_var.set('')
                return
            
            self.add_to_cart(product)
            self.barcode_var.set('')
            self.barcode_entry.focus()
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product:\n{e}")
    
    def add_selected_product(self):
        """Add selected product from search list to cart"""
        selection = self.product_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a product")
            return
        
        idx = selection[0]
        product = self.product_data[idx]
        self.add_to_cart(product)
    
    def add_to_cart(self, product):
        """Add product to cart"""
        # Check if product already in cart
        for item in self.cart_items:
            if item.product_id == product.product_id:
                # Increase quantity
                if item.quantity < product.stock_quantity:
                    item.update_quantity(item.quantity + 1)
                    self.refresh_cart()
                    self.calculate_totals()
                else:
                    messagebox.showwarning("Warning", f"Cannot add more. Only {product.stock_quantity} in stock")
                return
        
        # Add new item
        cart_item = CartItem(
            product_id=product.product_id,
            product_name=product.product_name,
            barcode=product.barcode,
            unit_price=product.unit_price,
            quantity=1
        )
        self.cart_items.append(cart_item)
        self.refresh_cart()
        self.calculate_totals()
    
    def refresh_cart(self):
        """Refresh cart display"""
        # Clear tree
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # Populate
        currency = config.BUSINESS_CONFIG['currency_symbol']
        for item in self.cart_items:
            self.cart_tree.insert('', tk.END, values=(
                item.product_name,
                f"{currency}{item.unit_price:.2f}",
                item.quantity,
                f"{currency}{item.subtotal:.2f}"
            ))
    
    def remove_from_cart(self):
        """Remove selected item from cart"""
        selection = self.cart_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item to remove")
            return
        
        idx = self.cart_tree.index(selection[0])
        del self.cart_items[idx]
        self.refresh_cart()
        self.calculate_totals()
    
    def update_quantity(self):
        """Update quantity of selected item"""
        selection = self.cart_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an item")
            return
        
        idx = self.cart_tree.index(selection[0])
        item = self.cart_items[idx]
        
        # Ask for new quantity
        new_qty = tk.simpledialog.askinteger(
            "Update Quantity",
            f"Enter new quantity for {item.product_name}:",
            initialvalue=item.quantity,
            minvalue=1
        )
        
        if new_qty:
            # Check stock
            product = ProductManager.get_product_by_id(item.product_id)
            if new_qty > product.stock_quantity:
                messagebox.showerror("Error", f"Only {product.stock_quantity} in stock")
                return
            
            item.update_quantity(new_qty)
            self.refresh_cart()
            self.calculate_totals()
    
    def calculate_totals(self):
        """Calculate and display totals"""
        if not self.cart_items:
            currency = config.BUSINESS_CONFIG['currency_symbol']
            self.subtotal_label.config(text=f"{currency}0.00")
            self.discount_label.config(text=f"{currency}0.00")
            self.tax_label.config(text=f"{currency}0.00")
            self.total_label.config(text=f"{currency}0.00")
            return
        
        # Get discount
        discount_str = self.discount_var.get()
        valid, msg, discount_percent = Validator.validate_discount(discount_str)
        if not valid:
            discount_percent = 0
        
        # Calculate
        totals = SalesManager.calculate_totals(self.cart_items, discount_percent)
        
        currency = config.BUSINESS_CONFIG['currency_symbol']
        self.subtotal_label.config(text=f"{currency}{totals['subtotal']:.2f}")
        self.discount_label.config(text=f"{currency}{totals['discount_amount']:.2f}")
        self.tax_label.config(text=f"{currency}{totals['tax_amount']:.2f}")
        self.total_label.config(text=f"{currency}{totals['total_amount']:.2f}")
    
    def complete_sale(self):
        """Complete the sale transaction"""
        if not self.cart_items:
            messagebox.showwarning("Warning", "Cart is empty")
            return
        
        # Confirm
        result = messagebox.askyesno(
            "Confirm Sale",
            "Complete this sale transaction?"
        )
        
        if not result:
            return
        
        # Get customer info
        customer_name = self.customer_name_var.get().strip() or None
        customer_phone = self.customer_phone_var.get().strip() or None
        
        # Get discount
        discount_str = self.discount_var.get()
        valid, msg, discount_percent = Validator.validate_discount(discount_str)
        if not valid:
            discount_percent = 0
        
        # Get payment method
        payment_method = self.payment_method_var.get()
        
        try:
            # Process sale
            sale_id = SalesManager.process_sale(
                cart_items=self.cart_items,
                customer_name=customer_name,
                customer_phone=customer_phone,
                discount_percent=discount_percent,
                payment_method=payment_method,
                cashier_id=self.user.user_id
            )
            
            if sale_id:
                # Get sale details
                sale = SalesManager.get_sale_by_id(sale_id)
                
                # Show success
                messagebox.showinfo(
                    "Success",
                    f"Sale completed successfully!\n\nSale Number: {sale.sale_number}\nTotal: {config.BUSINESS_CONFIG['currency_symbol']}{sale.total_amount:.2f}"
                )
                
                # Ask to print receipt
                print_receipt = messagebox.askyesno(
                    "Print Receipt",
                    "Would you like to generate a receipt?"
                )
                
                if print_receipt:
                    try:
                        # Generate PDF receipt
                        sale_data = {
                            'sale_number': sale.sale_number,
                            'sale_date': sale.sale_date,
                            'customer_name': sale.customer_name,
                            'cashier_name': self.user.full_name,
                            'items': sale.items,
                            'subtotal': sale.subtotal,
                            'tax_amount': sale.tax_amount,
                            'discount_amount': sale.discount_amount,
                            'total_amount': sale.total_amount
                        }
                        
                        filename = PDFGenerator.generate_receipt(sale_data)
                        messagebox.showinfo("Success", f"Receipt saved to:\n{filename}")
                        
                        # Open receipt (Windows)
                        import os
                        os.startfile(filename)
                    
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to generate receipt:\n{e}")
                
                # Clear cart
                self.clear_cart()
            else:
                messagebox.showerror("Error", "Failed to process sale")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to complete sale:\n{e}")
    
    def clear_cart(self):
        """Clear the shopping cart"""
        if self.cart_items:
            result = messagebox.askyesno("Confirm", "Clear entire cart?")
            if not result:
                return
        
        self.cart_items = []
        self.refresh_cart()
        self.calculate_totals()
        self.customer_name_var.set('')
        self.customer_phone_var.set('')
        self.discount_var.set('0')
        self.barcode_entry.focus()


# Function to open POS window from dashboard
def open_pos_window(parent, user):
    """Open Point of Sale window"""
    POSWindow(parent, user)