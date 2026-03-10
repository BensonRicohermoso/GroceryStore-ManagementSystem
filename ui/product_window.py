import tkinter as tk
from tkinter import ttk, messagebox
from modules.products import ProductManager
from ui.styles import AppStyles
from utils.validators import Validator
import config


class ProductWindow:
    """Product management window with full CRUD operations"""
    
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.window = tk.Toplevel(parent)
        self.window.title("Product Management")
        self.window.geometry("1400x800")
        
        # Configure styles
        AppStyles.configure_ttk_styles()
        
        # Variables
        self.selected_product_id = None
        self.categories = []
        
        # Create UI
        self.create_widgets()
        
        # Load initial data
        self.load_categories()
        self.load_products()
        
        # Focus on search
        self.search_entry.focus()
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_container = tk.Frame(self.window, bg=AppStyles.BACKGROUND)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_container, bg=AppStyles.PRIMARY, height=60)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="📦 Product Management",
            font=AppStyles.FONT_HEADER,
            bg=AppStyles.PRIMARY,
            fg=AppStyles.WHITE
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Content area - two columns
        content_frame = tk.Frame(main_container, bg=AppStyles.BACKGROUND)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Product list
        left_frame = tk.Frame(content_frame, bg=AppStyles.BACKGROUND)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Right side - Form
        right_frame = tk.Frame(content_frame, bg=AppStyles.BACKGROUND)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        
        self.create_product_list(left_frame)
        self.create_product_form(right_frame)
    
    def create_product_list(self, parent):
        """Create product list with search"""
        # Card for list
        list_card = AppStyles.create_card_frame(parent)
        list_card.pack(fill=tk.BOTH, expand=True)
        
        # Search section
        search_frame = tk.Frame(list_card, bg=AppStyles.WHITE)
        search_frame.pack(fill=tk.X, padx=20, pady=20)
        
        search_label = tk.Label(
            search_frame,
            text="Search Products:",
            font=AppStyles.FONT_MEDIUM,
            bg=AppStyles.WHITE
        )
        search_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_entry = ttk.Entry(search_frame, font=AppStyles.FONT_NORMAL, width=30)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', lambda e: self.search_products())
        
        search_btn = AppStyles.create_button(
            search_frame,
            text="Search",
            command=self.search_products,
            style='Primary.TButton'
        )
        search_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        refresh_btn = AppStyles.create_button(
            search_frame,
            text="Refresh",
            command=self.load_products,
            style='Primary.TButton'
        )
        refresh_btn.pack(side=tk.LEFT)
        
        # Products table
        table_frame = tk.Frame(list_card, bg=AppStyles.WHITE)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Scrollbars
        y_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        x_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        columns = ('ID', 'Barcode', 'Product Name', 'Category', 'Price', 'Stock', 'Status')
        self.product_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )
        
        # Configure scrollbars
        y_scrollbar.config(command=self.product_tree.yview)
        x_scrollbar.config(command=self.product_tree.xview)
        
        # Column headings
        self.product_tree.heading('ID', text='ID')
        self.product_tree.heading('Barcode', text='Barcode')
        self.product_tree.heading('Product Name', text='Product Name')
        self.product_tree.heading('Category', text='Category')
        self.product_tree.heading('Price', text='Price')
        self.product_tree.heading('Stock', text='Stock')
        self.product_tree.heading('Status', text='Status')
        
        # Column widths
        self.product_tree.column('ID', width=50)
        self.product_tree.column('Barcode', width=120)
        self.product_tree.column('Product Name', width=250)
        self.product_tree.column('Category', width=150)
        self.product_tree.column('Price', width=100)
        self.product_tree.column('Stock', width=80)
        self.product_tree.column('Status', width=80)
        
        self.product_tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind selection event
        self.product_tree.bind('<<TreeviewSelect>>', self.on_product_select)
        
        # Action buttons
        button_frame = tk.Frame(list_card, bg=AppStyles.WHITE)
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.edit_btn = AppStyles.create_button(
            button_frame,
            text="✏️ Edit Selected",
            command=self.edit_product,
            style='Primary.TButton'
        )
        self.edit_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.edit_btn.config(state='disabled')
        
        self.delete_btn = AppStyles.create_button(
            button_frame,
            text="🗑️ Delete Selected",
            command=self.delete_product,
            style='Danger.TButton'
        )
        self.delete_btn.pack(side=tk.LEFT)
        self.delete_btn.config(state='disabled')
    
    def create_product_form(self, parent):
        """Create product add/edit form"""
        # Card for form
        form_card = AppStyles.create_card_frame(parent)
        form_card.pack(fill=tk.BOTH, expand=True)
        
        # Form header
        form_header = tk.Label(
            form_card,
            text="Add New Product",
            font=AppStyles.FONT_LARGE,
            bg=AppStyles.WHITE,
            fg=AppStyles.PRIMARY
        )
        form_header.pack(pady=(20, 15), padx=20, anchor='w')
        
        # Form container with scrollbar
        canvas = tk.Canvas(form_card, bg=AppStyles.WHITE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_card, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=AppStyles.WHITE)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Form fields
        form_inner = tk.Frame(scrollable_frame, bg=AppStyles.WHITE)
        form_inner.pack(fill=tk.BOTH, expand=True)
        
        # Barcode
        self.create_form_field(form_inner, "Barcode *", 0)
        self.barcode_var = tk.StringVar()
        self.barcode_entry = ttk.Entry(
            form_inner,
            textvariable=self.barcode_var,
            font=AppStyles.FONT_NORMAL,
            width=30
        )
        self.barcode_entry.grid(row=1, column=0, sticky='ew', padx=20, pady=(0, 15))
        
        # Product Name
        self.create_form_field(form_inner, "Product Name *", 2)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(
            form_inner,
            textvariable=self.name_var,
            font=AppStyles.FONT_NORMAL,
            width=30
        )
        self.name_entry.grid(row=3, column=0, sticky='ew', padx=20, pady=(0, 15))
        
        # Category
        self.create_form_field(form_inner, "Category *", 4)
        self.category_var = tk.IntVar()
        self.category_combo = ttk.Combobox(
            form_inner,
            textvariable=self.category_var,
            font=AppStyles.FONT_NORMAL,
            state='readonly',
            width=28
        )
        self.category_combo.grid(row=5, column=0, sticky='ew', padx=20, pady=(0, 15))
        
        # Unit Price
        self.create_form_field(form_inner, "Unit Price *", 6)
        self.price_var = tk.StringVar()
        self.price_entry = ttk.Entry(
            form_inner,
            textvariable=self.price_var,
            font=AppStyles.FONT_NORMAL,
            width=30
        )
        self.price_entry.grid(row=7, column=0, sticky='ew', padx=20, pady=(0, 15))
        
        # Cost Price
        self.create_form_field(form_inner, "Cost Price (Optional)", 8)
        self.cost_var = tk.StringVar()
        self.cost_entry = ttk.Entry(
            form_inner,
            textvariable=self.cost_var,
            font=AppStyles.FONT_NORMAL,
            width=30
        )
        self.cost_entry.grid(row=9, column=0, sticky='ew', padx=20, pady=(0, 15))
        
        # Stock Quantity
        self.create_form_field(form_inner, "Initial Stock Quantity", 10)
        self.stock_var = tk.StringVar(value="0")
        self.stock_entry = ttk.Entry(
            form_inner,
            textvariable=self.stock_var,
            font=AppStyles.FONT_NORMAL,
            width=30
        )
        self.stock_entry.grid(row=11, column=0, sticky='ew', padx=20, pady=(0, 15))
        
        # Reorder Level
        self.create_form_field(form_inner, "Reorder Level", 12)
        self.reorder_var = tk.StringVar(value="10")
        self.reorder_entry = ttk.Entry(
            form_inner,
            textvariable=self.reorder_var,
            font=AppStyles.FONT_NORMAL,
            width=30
        )
        self.reorder_entry.grid(row=13, column=0, sticky='ew', padx=20, pady=(0, 15))
        
        # Description
        self.create_form_field(form_inner, "Description (Optional)", 14)
        self.description_text = tk.Text(
            form_inner,
            font=AppStyles.FONT_NORMAL,
            width=30,
            height=4,
            wrap=tk.WORD
        )
        self.description_text.grid(row=15, column=0, sticky='ew', padx=20, pady=(0, 20))
        
        # Button frame
        button_frame = tk.Frame(form_inner, bg=AppStyles.WHITE)
        button_frame.grid(row=16, column=0, sticky='ew', padx=20, pady=(0, 20))
        
        self.save_btn = AppStyles.create_button(
            button_frame,
            text="💾 Save Product",
            command=self.save_product,
            style='Success.TButton'
        )
        self.save_btn.pack(fill=tk.X, pady=(0, 10))
        
        self.clear_btn = AppStyles.create_button(
            button_frame,
            text="🔄 Clear Form",
            command=self.clear_form,
            style='Primary.TButton'
        )
        self.clear_btn.pack(fill=tk.X)
        
        # Configure grid
        form_inner.columnconfigure(0, weight=1)
    
    def create_form_field(self, parent, label_text, row):
        """Create a form field label"""
        label = tk.Label(
            parent,
            text=label_text,
            font=AppStyles.FONT_MEDIUM,
            bg=AppStyles.WHITE,
            fg=AppStyles.TEXT,
            anchor='w'
        )
        label.grid(row=row, column=0, sticky='w', padx=20, pady=(0, 5))
    
    def load_categories(self):
        """Load categories into dropdown"""
        try:
            self.categories = ProductManager.get_categories()
            category_names = [f"{cat[1]}" for cat in self.categories]
            self.category_combo['values'] = category_names
            if category_names:
                self.category_combo.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load categories:\n{e}")
    
    def load_products(self):
        """Load all products into table"""
        # Clear existing
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        try:
            products = ProductManager.get_all_products(active_only=False)
            currency = config.BUSINESS_CONFIG['currency_symbol']
            
            for product in products:
                status = "Active" if product.is_active else "Inactive"
                self.product_tree.insert('', tk.END, values=(
                    product.product_id,
                    product.barcode,
                    product.product_name,
                    product.category_name or 'N/A',
                    f"{currency}{product.unit_price:.2f}",
                    product.stock_quantity,
                    status
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load products:\n{e}")
    
    def search_products(self):
        """Search products"""
        search_term = self.search_entry.get().strip()
        
        # Clear existing
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        try:
            if search_term:
                products = ProductManager.search_products(search_term, active_only=False)
            else:
                products = ProductManager.get_all_products(active_only=False)
            
            currency = config.BUSINESS_CONFIG['currency_symbol']
            
            for product in products:
                status = "Active" if product.is_active else "Inactive"
                self.product_tree.insert('', tk.END, values=(
                    product.product_id,
                    product.barcode,
                    product.product_name,
                    product.category_name or 'N/A',
                    f"{currency}{product.unit_price:.2f}",
                    product.stock_quantity,
                    status
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search products:\n{e}")
    
    def on_product_select(self, event):
        """Handle product selection"""
        selection = self.product_tree.selection()
        if selection:
            self.selected_product_id = self.product_tree.item(selection[0])['values'][0]
            self.edit_btn.config(state='normal')
            self.delete_btn.config(state='normal')
        else:
            self.selected_product_id = None
            self.edit_btn.config(state='disabled')
            self.delete_btn.config(state='disabled')
    
    def edit_product(self):
        """Load selected product into form for editing"""
        if not self.selected_product_id:
            return
        
        try:
            product = ProductManager.get_product_by_id(self.selected_product_id)
            if not product:
                messagebox.showerror("Error", "Product not found")
                return
            
            # Populate form
            self.barcode_var.set(product.barcode)
            self.name_var.set(product.product_name)
            
            # Set category
            for idx, cat in enumerate(self.categories):
                if cat[0] == product.category_id:
                    self.category_combo.current(idx)
                    break
            
            self.price_var.set(str(product.unit_price))
            self.cost_var.set(str(product.cost_price) if product.cost_price else "")
            self.stock_var.set(str(product.stock_quantity))
            self.reorder_var.set(str(product.reorder_level))
            
            self.description_text.delete('1.0', tk.END)
            if product.description:
                self.description_text.insert('1.0', product.description)
            
            # Change button text
            self.save_btn.config(text="💾 Update Product")
            
            # Scroll to top
            self.barcode_entry.focus()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load product:\n{e}")
    
    def save_product(self):
        """Save or update product"""
        # Get values
        barcode = self.barcode_var.get().strip()
        name = self.name_var.get().strip()
        price_str = self.price_var.get().strip()
        cost_str = self.cost_var.get().strip()
        stock_str = self.stock_var.get().strip()
        reorder_str = self.reorder_var.get().strip()
        description = self.description_text.get('1.0', tk.END).strip()
        
        # Get category ID
        category_idx = self.category_combo.current()
        if category_idx < 0:
            messagebox.showerror("Error", "Please select a category")
            return
        category_id = self.categories[category_idx][0]
        
        # Validate
        valid, msg = Validator.validate_barcode(barcode)
        if not valid:
            messagebox.showerror("Validation Error", msg)
            self.barcode_entry.focus()
            return
        
        valid, msg = Validator.validate_name(name, "Product Name")
        if not valid:
            messagebox.showerror("Validation Error", msg)
            self.name_entry.focus()
            return
        
        valid, msg, price = Validator.validate_price(price_str)
        if not valid:
            messagebox.showerror("Validation Error", msg)
            self.price_entry.focus()
            return
        
        cost = None
        if cost_str:
            valid, msg, cost = Validator.validate_price(cost_str, allow_zero=True)
            if not valid:
                messagebox.showerror("Validation Error", msg)
                self.cost_entry.focus()
                return
        
        valid, msg, stock = Validator.validate_quantity(stock_str, allow_zero=True)
        if not valid:
            messagebox.showerror("Validation Error", msg)
            self.stock_entry.focus()
            return
        
        valid, msg, reorder = Validator.validate_quantity(reorder_str, allow_zero=True)
        if not valid:
            messagebox.showerror("Validation Error", msg)
            self.reorder_entry.focus()
            return
        
        try:
            if self.selected_product_id:
                # Update existing product
                success = ProductManager.update_product(
                    self.selected_product_id,
                    barcode=barcode,
                    product_name=name,
                    category_id=category_id,
                    unit_price=price,
                    cost_price=cost,
                    reorder_level=reorder,
                    description=description
                )
                
                if success:
                    messagebox.showinfo("Success", "Product updated successfully!")
                    self.clear_form()
                    self.load_products()
                else:
                    messagebox.showerror("Error", "Failed to update product")
            else:
                # Create new product
                product_id = ProductManager.create_product(
                    barcode=barcode,
                    product_name=name,
                    category_id=category_id,
                    unit_price=price,
                    cost_price=cost,
                    stock_quantity=stock,
                    reorder_level=reorder,
                    description=description
                )
                
                if product_id:
                    messagebox.showinfo("Success", f"Product added successfully!\nProduct ID: {product_id}")
                    self.clear_form()
                    self.load_products()
                else:
                    messagebox.showerror("Error", "Failed to add product")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save product:\n{e}")
    
    def delete_product(self):
        """Delete selected product"""
        if not self.selected_product_id:
            return
        
        # Get product details
        selection = self.product_tree.selection()
        if not selection:
            return
        
        values = self.product_tree.item(selection[0])['values']
        product_name = values[2]
        
        # Confirm
        result = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete this product?\n\n{product_name}\n\nThis action cannot be undone."
        )
        
        if result:
            try:
                success = ProductManager.delete_product(self.selected_product_id)
                if success:
                    messagebox.showinfo("Success", "Product deleted successfully!")
                    self.clear_form()
                    self.load_products()
                else:
                    messagebox.showerror("Error", "Failed to delete product")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete product:\n{e}")
    
    def clear_form(self):
        """Clear all form fields"""
        self.selected_product_id = None
        self.barcode_var.set('')
        self.name_var.set('')
        self.price_var.set('')
        self.cost_var.set('')
        self.stock_var.set('0')
        self.reorder_var.set('10')
        self.description_text.delete('1.0', tk.END)
        
        if self.categories:
            self.category_combo.current(0)
        
        self.save_btn.config(text="💾 Save Product")
        self.edit_btn.config(state='disabled')
        self.delete_btn.config(state='disabled')
        
        # Clear selection
        self.product_tree.selection_remove(self.product_tree.selection())


# Function to open product window from dashboard
def open_product_window(parent, user):
    """Open product management window"""
    ProductWindow(parent, user)