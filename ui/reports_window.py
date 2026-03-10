"""
Reports Window - Sales and Analytics
ui/reports_window.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from modules.sales import SalesManager
from ui.styles import AppStyles
import config


class ReportsWindow:
    """Reports window for sales analytics and reports"""
    
    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.window = tk.Toplevel(parent)
        self.window.title("Sales Reports")
        self.window.geometry("1200x800")
        
        AppStyles.configure_ttk_styles()
        self.create_widgets()
    
    def create_widgets(self):
        """Create UI widgets"""
        main_container = tk.Frame(self.window, bg=AppStyles.BACKGROUND)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_container, bg=AppStyles.INFO, height=60)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="📊 Sales Reports",
            font=AppStyles.FONT_HEADER,
            bg=AppStyles.INFO,
            fg=AppStyles.WHITE
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        # Content
        content_frame = tk.Frame(main_container, bg=AppStyles.BACKGROUND)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left - Report settings
        left_frame = tk.Frame(content_frame, bg=AppStyles.BACKGROUND, width=350)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # Right - Report display
        right_frame = tk.Frame(content_frame, bg=AppStyles.BACKGROUND)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.create_settings_panel(left_frame)
        self.create_display_panel(right_frame)
    
    def create_settings_panel(self, parent):
        """Create report settings"""
        settings_card = AppStyles.create_card_frame(parent)
        settings_card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            settings_card,
            text="Report Settings",
            font=AppStyles.FONT_LARGE,
            bg=AppStyles.WHITE,
            fg=AppStyles.PRIMARY
        ).pack(pady=(20, 15), padx=20, anchor='w')
        
        form_frame = tk.Frame(settings_card, bg=AppStyles.WHITE)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Date range
        tk.Label(form_frame, text="Date Range:", font=AppStyles.FONT_MEDIUM, bg=AppStyles.WHITE).pack(anchor='w', pady=(0, 5))
        
        date_frame = tk.Frame(form_frame, bg=AppStyles.WHITE)
        date_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(date_frame, text="From:", bg=AppStyles.WHITE).grid(row=0, column=0, sticky='w', pady=5)
        self.start_date = tk.StringVar(value=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        ttk.Entry(date_frame, textvariable=self.start_date, width=15).grid(row=0, column=1, sticky='ew', pady=5, padx=(5, 0))
        
        tk.Label(date_frame, text="To:", bg=AppStyles.WHITE).grid(row=1, column=0, sticky='w', pady=5)
        self.end_date = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(date_frame, textvariable=self.end_date, width=15).grid(row=1, column=1, sticky='ew', pady=5, padx=(5, 0))
        
        date_frame.columnconfigure(1, weight=1)
        
        # Quick date buttons
        quick_frame = tk.Frame(form_frame, bg=AppStyles.WHITE)
        quick_frame.pack(fill=tk.X, pady=(0, 20))
        
        AppStyles.create_button(quick_frame, "Today", lambda: self.set_date_range(0)).pack(fill=tk.X, pady=2)
        AppStyles.create_button(quick_frame, "Last 7 Days", lambda: self.set_date_range(7)).pack(fill=tk.X, pady=2)
        AppStyles.create_button(quick_frame, "Last 30 Days", lambda: self.set_date_range(30)).pack(fill=tk.X, pady=2)
        
        # Report type
        tk.Label(form_frame, text="Report Type:", font=AppStyles.FONT_MEDIUM, bg=AppStyles.WHITE).pack(anchor='w', pady=(10, 5))
        
        self.report_type = tk.StringVar(value="sales_summary")
        reports = [
            ("Sales Summary", "sales_summary"),
            ("Top Selling Products", "top_products"),
            ("Daily Sales", "daily_sales")
        ]
        
        for text, value in reports:
            tk.Radiobutton(
                form_frame,
                text=text,
                variable=self.report_type,
                value=value,
                font=AppStyles.FONT_NORMAL,
                bg=AppStyles.WHITE
            ).pack(anchor='w', pady=2)
        
        # Generate button
        AppStyles.create_button(
            form_frame,
            "📊 Generate Report",
            self.generate_report,
            'Success.TButton'
        ).pack(fill=tk.X, pady=(20, 10), ipady=10)
        
        AppStyles.create_button(
            form_frame,
            "📄 Export to PDF",
            self.export_pdf,
            'Primary.TButton'
        ).pack(fill=tk.X, pady=(0, 10))
    
    def create_display_panel(self, parent):
        """Create report display area"""
        display_card = AppStyles.create_card_frame(parent)
        display_card.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            display_card,
            text="Report Results",
            font=AppStyles.FONT_LARGE,
            bg=AppStyles.WHITE,
            fg=AppStyles.PRIMARY
        ).pack(pady=(20, 10), padx=20, anchor='w')
        
        # Text display
        text_frame = tk.Frame(display_card, bg=AppStyles.WHITE)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.report_text = tk.Text(
            text_frame,
            font=AppStyles.FONT_NORMAL,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set
        )
        self.report_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.report_text.yview)
    
    def set_date_range(self, days):
        """Set date range"""
        end = datetime.now()
        start = end - timedelta(days=days)
        
        self.start_date.set(start.strftime("%Y-%m-%d"))
        self.end_date.set(end.strftime("%Y-%m-%d"))
    
    def generate_report(self):
        """Generate selected report"""
        self.report_text.delete('1.0', tk.END)
        
        report_type = self.report_type.get()
        start = self.start_date.get()
        end = self.end_date.get()
        
        try:
            if report_type == "sales_summary":
                self.generate_sales_summary(start, end)
            elif report_type == "top_products":
                self.generate_top_products(start, end)
            elif report_type == "daily_sales":
                self.generate_daily_sales(start, end)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report:\n{e}")
    
    def generate_sales_summary(self, start, end):
        """Generate sales summary report"""
        report = SalesManager.get_sales_report(start, end)
        currency = config.BUSINESS_CONFIG['currency_symbol']
        
        text = f"""
SALES SUMMARY REPORT
Period: {start} to {end}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

{"=" * 60}

Total Orders:           {report.get('total_orders', 0)}
Total Revenue:          {currency}{report.get('total_revenue', 0):,.2f}
Average Order Value:    {currency}{report.get('average_order_value', 0):,.2f}

Subtotal (Before Tax):  {currency}{report.get('total_subtotal', 0):,.2f}
Tax Collected:          {currency}{report.get('total_tax', 0):,.2f}
Discounts Given:        {currency}{report.get('total_discounts', 0):,.2f}

Highest Sale:           {currency}{report.get('highest_sale', 0):,.2f}
Lowest Sale:            {currency}{report.get('lowest_sale', 0):,.2f}

{"=" * 60}
"""
        self.report_text.insert('1.0', text)
    
    def generate_top_products(self, start, end):
        """Generate top selling products"""
        days = (datetime.strptime(end, "%Y-%m-%d") - datetime.strptime(start, "%Y-%m-%d")).days
        products = SalesManager.get_top_selling_products(limit=10, days=max(days, 1))
        currency = config.BUSINESS_CONFIG['currency_symbol']
        
        text = f"""
TOP SELLING PRODUCTS
Period: {start} to {end}
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

{"=" * 60}

"""
        if products:
            for idx, product in enumerate(products, 1):
                text += f"""
{idx}. {product['product_name']}
   Quantity Sold:  {product['total_quantity_sold']}
   Revenue:        {currency}{float(product['total_revenue']):,.2f}
   Times Sold:     {product['times_sold']}
   Avg Price:      {currency}{float(product['average_price']):,.2f}

"""
        else:
            text += "\nNo sales data found for this period.\n"
        
        self.report_text.insert('1.0', text)
    
    def generate_daily_sales(self, start, end):
        """Generate daily sales breakdown"""
        # This is a placeholder - can be expanded
        self.report_text.insert('1.0', f"""
DAILY SALES REPORT
Period: {start} to {end}

This feature is coming soon!
""")
    
    def export_pdf(self):
        """Export report to PDF"""
        messagebox.showinfo("Export", "PDF export feature coming soon!")


def open_reports_window(parent, user):
    """Open reports window"""
    ReportsWindow(parent, user)
