import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import config
from ui.styles import AppStyles
from modules.sales import SalesManager
from modules.inventory import InventoryManager
from utils.logs import ActivityLogger



class DashboardWindow:
    """Main dashboard window"""
    
    def __init__(self, root, user):
        self.root = root
        self.user = user
        
        # Configure main window
        self.root.title(f"{config.APP_CONFIG['app_name']} - Dashboard")
        self.root.state('zoomed')  # Maximize window
        
        # Configure styles
        AppStyles.configure_ttk_styles()
        
        # Create UI
        self.create_menu()
        self.create_widgets()
        
        # Load initial data
        self.refresh_data()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_menu(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Refresh", command=self.refresh_data)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self.logout)
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Products menu
        products_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Products", menu=products_menu)
        products_menu.add_command(label="Manage Products", command=self.open_products)
        products_menu.add_command(label="Inventory", command=self.open_inventory)
        
        # Sales menu
        sales_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sales", menu=sales_menu)
        sales_menu.add_command(label="New Sale (POS)", command=self.open_pos)
        sales_menu.add_command(label="View Sales", command=self.view_sales)
        sales_menu.add_command(label="Reports", command=self.open_reports)
        
        # Admin menu (only for admins)
        if self.user.role == 'admin':
            admin_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Admin", menu=admin_menu)
            admin_menu.add_command(label="Manage Users", command=self.manage_users)
            admin_menu.add_command(label="Activity Logs", command=self.view_logs)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_widgets(self):
        """Create dashboard widgets"""
        # Main container with background
        main_container = tk.Frame(self.root, bg=AppStyles.BACKGROUND)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header section
        self.create_header(main_container)
        
        # Content area
        content_frame = tk.Frame(main_container, bg=AppStyles.BACKGROUND)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create three columns
        left_column = tk.Frame(content_frame, bg=AppStyles.BACKGROUND)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        middle_column = tk.Frame(content_frame, bg=AppStyles.BACKGROUND)
        middle_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        right_column = tk.Frame(content_frame, bg=AppStyles.BACKGROUND)
        right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Quick action buttons
        self.create_quick_actions(left_column)
        
        # Recent sales
        self.create_recent_sales(middle_column)
        
        # Alerts and summary
        self.create_alerts_summary(right_column)
    
    def create_header(self, parent):
        """Create dashboard header"""
        header_frame = tk.Frame(parent, bg=AppStyles.PRIMARY, height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Title and welcome
        title_label = tk.Label(
            header_frame,
            text="Dashboard",
            font=AppStyles.FONT_HEADER,
            bg=AppStyles.PRIMARY,
            fg=AppStyles.WHITE
        )
        title_label.pack(side=tk.LEFT, padx=30, pady=20)
        
        # User info
        user_frame = tk.Frame(header_frame, bg=AppStyles.PRIMARY)
        user_frame.pack(side=tk.RIGHT, padx=30)
        
        welcome_label = tk.Label(
            user_frame,
            text=f"Welcome, {self.user.full_name}",
            font=AppStyles.FONT_MEDIUM,
            bg=AppStyles.PRIMARY,
            fg=AppStyles.WHITE
        )
        welcome_label.pack()
        
        role_label = tk.Label(
            user_frame,
            text=f"Role: {self.user.role.title()}",
            font=AppStyles.FONT_SMALL,
            bg=AppStyles.PRIMARY,
            fg=AppStyles.LIGHT
        )
        role_label.pack()
    
    def create_quick_actions(self, parent):
        """Create quick action buttons"""
        card = AppStyles.create_card_frame(parent)
        card.pack(fill=tk.BOTH, expand=True)
        
        # Card header
        header = tk.Label(
            card,
            text="Quick Actions",
            font=AppStyles.FONT_LARGE,
            bg=AppStyles.WHITE,
            fg=AppStyles.PRIMARY
        )
        header.pack(pady=(20, 15), padx=20, anchor='w')
        
        # Buttons container
        btn_container = tk.Frame(card, bg=AppStyles.WHITE)
        btn_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Action buttons
        actions = [
            ("🛒 New Sale", self.open_pos, 'Success.TButton'),
            ("📦 Manage Products", self.open_products, 'Primary.TButton'),
            ("📊 View Reports", self.open_reports, 'Primary.TButton'),
            ("📋 Inventory", self.open_inventory, 'Primary.TButton'),
        ]
        
        for text, command, style in actions:
            btn = AppStyles.create_button(
                btn_container,
                text=text,
                command=command,
                style=style
            )
            btn.pack(fill=tk.X, pady=5, ipady=15)
    
    def create_recent_sales(self, parent):
        """Create recent sales table"""
        card = AppStyles.create_card_frame(parent)
        card.pack(fill=tk.BOTH, expand=True)
        
        # Card header
        header_frame = tk.Frame(card, bg=AppStyles.WHITE)
        header_frame.pack(fill=tk.X, pady=(20, 10), padx=20)
        
        header = tk.Label(
            header_frame,
            text="Recent Orders",
            font=AppStyles.FONT_LARGE,
            bg=AppStyles.WHITE,
            fg=AppStyles.PRIMARY
        )
        header.pack(side=tk.LEFT)
        
        refresh_btn = ttk.Button(
            header_frame,
            text="Refresh",
            command=self.refresh_sales,
            style='Primary.TButton'
        )
        refresh_btn.pack(side=tk.RIGHT)
        
        # Table container
        table_container = tk.Frame(card, bg=AppStyles.WHITE)
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Treeview
        columns = ('Date', 'Order No.', 'Customer', 'Total')
        self.sales_tree = ttk.Treeview(
            table_container,
            columns=columns,
            show='headings',
            height=15
        )
        
        # Column headings
        self.sales_tree.heading('Date', text='Date')
        self.sales_tree.heading('Order No.', text='Order No.')
        self.sales_tree.heading('Customer', text='Customer Name')
        self.sales_tree.heading('Total', text='Total Cost')
        
        # Column widths
        self.sales_tree.column('Date', width=150)
        self.sales_tree.column('Order No.', width=150)
        self.sales_tree.column('Customer', width=150)
        self.sales_tree.column('Total', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_container,
            orient=tk.VERTICAL,
            command=self.sales_tree.yview
        )
        self.sales_tree.configure(yscrollcommand=scrollbar.set)
        
        self.sales_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def create_alerts_summary(self, parent):
        """Create alerts and summary section"""
        # Low stock alerts
        alerts_card = AppStyles.create_card_frame(parent)
        alerts_card.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        alerts_header = tk.Label(
            alerts_card,
            text="⚠️ Low Stock Alerts",
            font=AppStyles.FONT_LARGE,
            bg=AppStyles.WHITE,
            fg=AppStyles.WARNING
        )
        alerts_header.pack(pady=(20, 10), padx=20, anchor='w')
        
        # Alerts list
        self.alerts_listbox = tk.Listbox(
            alerts_card,
            font=AppStyles.FONT_NORMAL,
            height=8,
            relief='flat',
            borderwidth=0,
            highlightthickness=0
        )
        self.alerts_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Summary card
        summary_card = AppStyles.create_card_frame(parent)
        summary_card.pack(fill=tk.BOTH, expand=True)
        
        summary_header = tk.Label(
            summary_card,
            text="Today's Summary",
            font=AppStyles.FONT_LARGE,
            bg=AppStyles.WHITE,
            fg=AppStyles.PRIMARY
        )
        summary_header.pack(pady=(20, 15), padx=20, anchor='w')
        
        # Summary labels
        self.summary_frame = tk.Frame(summary_card, bg=AppStyles.WHITE)
        self.summary_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Placeholder summary items
        self.sales_count_label = self.create_summary_item(
            self.summary_frame, "Total Orders", "0"
        )
        self.revenue_label = self.create_summary_item(
            self.summary_frame, "Total Revenue", f"{config.BUSINESS_CONFIG['currency_symbol']}0.00"
        )
    
    def create_summary_item(self, parent, label, value):
        """Create a summary item widget"""
        item_frame = tk.Frame(parent, bg=AppStyles.WHITE)
        item_frame.pack(fill=tk.X, pady=5)
        
        label_widget = tk.Label(
            item_frame,
            text=label,
            font=AppStyles.FONT_NORMAL,
            bg=AppStyles.WHITE,
            fg=AppStyles.TEXT_LIGHT
        )
        label_widget.pack(side=tk.LEFT)
        
        value_widget = tk.Label(
            item_frame,
            text=value,
            font=AppStyles.FONT_MEDIUM,
            bg=AppStyles.WHITE,
            fg=AppStyles.PRIMARY
        )
        value_widget.pack(side=tk.RIGHT)
        
        return value_widget
    
    def refresh_data(self):
        """Refresh all dashboard data"""
        self.refresh_sales()
        self.refresh_alerts()
        self.refresh_summary()
    
    def refresh_sales(self):
        """Refresh recent sales table"""
        # Clear existing items
        for item in self.sales_tree.get_children():
            self.sales_tree.delete(item)
        
        # Get recent sales
        try:
            sales = SalesManager.get_recent_sales(limit=20)
            currency = config.BUSINESS_CONFIG['currency_symbol']
            
            for sale in sales:
                date_str = sale['sale_date'].strftime("%Y-%m-%d %H:%M")
                customer = sale['customer_name'] or "Walk-in"
                total = f"{currency}{sale['total_amount']:.2f}"
                
                self.sales_tree.insert('', tk.END, values=(
                    date_str,
                    sale['sale_number'],
                    customer,
                    total
                ))
        except Exception as e:
            print(f"Error refreshing sales: {e}")
    
    def refresh_alerts(self):
        """Refresh low stock alerts"""
        self.alerts_listbox.delete(0, tk.END)
        
        try:
            low_stock = InventoryManager.get_low_stock_products()
            
            if low_stock:
                for product in low_stock[:10]:  # Show top 10
                    alert_text = f"{product['product_name']}: {product['stock_quantity']} units"
                    self.alerts_listbox.insert(tk.END, alert_text)
            else:
                self.alerts_listbox.insert(tk.END, "No low stock alerts")
        except Exception as e:
            print(f"Error refreshing alerts: {e}")
            self.alerts_listbox.insert(tk.END, "Error loading alerts")
    
    def refresh_summary(self):
        """Refresh today's summary"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            report = SalesManager.get_sales_report(start_date=today, end_date=today)
            
            currency = config.BUSINESS_CONFIG['currency_symbol']
            self.sales_count_label.config(text=str(report.get('total_orders', 0)))
            self.revenue_label.config(text=f"{currency}{report.get('total_revenue', 0):.2f}")
        except Exception as e:
            print(f"Error refreshing summary: {e}")
    
    # Navigation methods
    def open_pos(self):
        """Open POS window"""
        try:
            from ui.pos_window import open_pos_window
            open_pos_window(self.root, self.user)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open POS window:\n{e}")
    
    def open_products(self):
        """Open products management window"""
        try:
            from ui.product_window import open_product_window
            open_product_window(self.root, self.user)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Products window:\n{e}")
    
    def open_inventory(self):
        """Open inventory window"""
        try:
            from ui.inventory_window import open_inventory_window
            open_inventory_window(self.root, self.user)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Inventory window:\n{e}")
    
    def open_reports(self):
        """Open reports window"""
        try:
            from ui.reports_window import open_reports_window
            open_reports_window(self.root, self.user)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Reports window:\n{e}")
    
    def view_sales(self):
        """View sales history"""
        messagebox.showinfo("Coming Soon", "Sales history window will be implemented.")
    
    def manage_users(self):
        """Open user management (admin only)"""
        messagebox.showinfo("Coming Soon", "User management window will be implemented.")
    
    def view_logs(self):
        """View activity logs (admin only)"""
        messagebox.showinfo("Coming Soon", "Activity logs window will be implemented.")
    
    def show_about(self):
        """Show about dialog"""
        about_text = f"""
{config.APP_CONFIG['app_name']}
Version {config.APP_CONFIG['version']}

A comprehensive grocery store management system
with inventory tracking, POS, and reporting.

Developed with Python and MySQL
        """
        messagebox.showinfo("About", about_text)
    
    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            # Log logout activity
            ActivityLogger.log_logout(self.user.user_id, self.user.username)
            
            # Close dashboard
            self.root.destroy()
            
            # Show login again
            from ui.login_window import show_login
            show_login(lambda user: self.__init__(tk.Tk(), user))
    
    def on_closing(self):
        """Handle window close"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            ActivityLogger.log_logout(self.user.user_id, self.user.username)
            self.root.destroy()