import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime
import time

# ===============================
# CEB CONFIGURATION (PROFESSIONAL EDITION)
# ===============================
CEB_HOST = "127.0.0.1"
CEB_PORT = 5001

# ===============================
# CEB PROFESSIONAL COLORS
# ===============================
CEB_NAVY_BLUE = "#1e3a5f"
CEB_LIGHT_GRAY = "#f5f7fa"
CEB_WHITE = "#ffffff"
CEB_ACCENT_BLUE = "#0066cc"
CEB_DARK_GRAY = "#2c3e50"
CEB_BORDER_GRAY = "#d1d5db"
CEB_SUCCESS_GREEN = "#10b981"
CEB_WARNING_AMBER = "#f59e0b"
CEB_TEXT_DARK = "#374151"
CEB_TEXT_LIGHT = "#6b7280"
CEB_SIDEBAR = "#f9fafb"
CEB_HOVER_BLUE = "#0052a3"

class CEBProfessional:
    def __init__(self):
        self.ceb_window = tk.Tk()
        self.ceb_window.title("CEB Enterprise Messenger")
        self.ceb_window.geometry("1100x750")
        self.ceb_window.configure(bg=CEB_WHITE)
        self.ceb_window.resizable(False, False)
        
        self.ceb_user_name = ""
        self.ceb_socket_conn = None
        self.ceb_hosting = False
        self.ceb_active_session = True
        self.ceb_dark_mode = False
        self.ceb_typing = False
        self.ceb_last_typing_time = 0
        self.ceb_connected_users = []
        self.ceb_user_status = {}
        self.ceb_other_user_typing = False
        
        self.ceb_display_login()
        
    def ceb_display_login(self):
        """CEB Professional login interface"""
        for widget in self.ceb_window.winfo_children():
            widget.destroy()
        
        colors = self.ceb_get_login_colors()
        self.ceb_window.configure(bg=colors['bg'])
        
        # CEB Left panel (branding)
        ceb_left_panel = tk.Frame(self.ceb_window, bg=colors['panel_bg'], width=450)
        ceb_left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        ceb_left_panel.pack_propagate(False)
        
        # CEB Company branding
        ceb_brand_frame = tk.Frame(ceb_left_panel, bg=colors['panel_bg'])
        ceb_brand_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(
            ceb_brand_frame,
            text="CEB",
            font=("Segoe UI", 52, "bold"),
            bg=colors['panel_bg'],
            fg=colors['brand_text']
        ).pack()
        
        tk.Label(
            ceb_brand_frame,
            text="ENTERPRISE MESSENGER",
            font=("Segoe UI", 12),
            bg=colors['panel_bg'],
            fg=colors['subtitle']
        ).pack(pady=5)
        
        tk.Label(
            ceb_brand_frame,
            text="━━━━━━━━━━━━━━━━━━━",
            font=("Segoe UI", 10),
            bg=colors['panel_bg'],
            fg=CEB_ACCENT_BLUE
        ).pack(pady=15)
        
        tk.Label(
            ceb_brand_frame,
            text="Secure • Professional • Reliable",
            font=("Segoe UI", 10),
            bg=colors['panel_bg'],
            fg=colors['subtitle']
        ).pack()
        
        # CEB Dark mode toggle on left panel
        ceb_theme_btn = tk.Button(
            ceb_left_panel,
            text="🌙 Dark Mode" if not self.ceb_dark_mode else "☀️ Light Mode",
            font=("Segoe UI", 9),
            bg=colors['panel_bg'],
            fg=colors['subtitle'],
            activebackground=colors['panel_bg'],
            relief=tk.FLAT,
            cursor="hand2",
            command=self.ceb_toggle_login_theme
        )
        ceb_theme_btn.place(relx=0.5, rely=0.9, anchor="center")
        
        # CEB Right panel (login form)
        ceb_right_panel = tk.Frame(self.ceb_window, bg=colors['bg'])
        ceb_right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # CEB Login container
        ceb_login_container = tk.Frame(ceb_right_panel, bg=colors['bg'])
        ceb_login_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # CEB Welcome header
        tk.Label(
            ceb_login_container,
            text="Welcome",
            font=("Segoe UI", 28, "bold"),
            bg=colors['bg'],
            fg=colors['text']
        ).pack(pady=(0, 5))
        
        tk.Label(
            ceb_login_container,
            text="Sign in to continue to CEB Messenger",
            font=("Segoe UI", 11),
            bg=colors['bg'],
            fg=colors['text_light']
        ).pack(pady=(0, 40))
        
        # CEB Username field
        tk.Label(
            ceb_login_container,
            text="Display Name",
            font=("Segoe UI", 10, "bold"),
            bg=colors['bg'],
            fg=colors['text'],
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 5))
        
        ceb_entry_frame = tk.Frame(ceb_login_container, bg=colors['input_bg'], relief=tk.SOLID, bd=1, highlightbackground=colors['border'], highlightthickness=1)
        ceb_entry_frame.pack(fill=tk.X, pady=(0, 30))
        
        self.ceb_name_field = tk.Entry(
            ceb_entry_frame,
            font=("Segoe UI", 12),
            bg=colors['input_bg'],
            fg=colors['text'],
            insertbackground=CEB_ACCENT_BLUE,
            relief=tk.FLAT,
            bd=0
        )
        self.ceb_name_field.pack(fill=tk.X, padx=12, pady=12)
        
        # CEB Connection type label
        tk.Label(
            ceb_login_container,
            text="Connection Type",
            font=("Segoe UI", 10, "bold"),
            bg=colors['bg'],
            fg=colors['text'],
            anchor="w"
        ).pack(fill=tk.X, pady=(0, 10))
        
        # CEB Button container
        ceb_buttons_frame = tk.Frame(ceb_login_container, bg=colors['bg'])
        ceb_buttons_frame.pack(fill=tk.X)
        
        # CEB Host button
        ceb_host_button = tk.Button(
            ceb_buttons_frame,
            text="Host Session",
            font=("Segoe UI", 11, "bold"),
            bg=CEB_ACCENT_BLUE,
            fg=CEB_WHITE,
            activebackground=CEB_HOVER_BLUE,
            activeforeground=CEB_WHITE,
            relief=tk.FLAT,
            bd=0,
            padx=30,
            pady=12,
            cursor="hand2",
            command=lambda: self.ceb_initialize_connection(True)
        )
        ceb_host_button.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        # CEB Join button
        ceb_join_button = tk.Button(
            ceb_buttons_frame,
            text="Join Session",
            font=("Segoe UI", 11),
            bg=colors['bg'],
            fg=CEB_ACCENT_BLUE,
            activebackground=colors['hover'],
            activeforeground=CEB_ACCENT_BLUE,
            relief=tk.SOLID,
            bd=2,
            padx=30,
            pady=12,
            cursor="hand2",
            command=lambda: self.ceb_initialize_connection(False)
        )
        ceb_join_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # CEB Footer
        tk.Label(
            ceb_right_panel,
            text="© 2025 CEB Corporation. All rights reserved.",
            font=("Segoe UI", 8),
            bg=colors['bg'],
            fg=colors['text_light']
        ).pack(side=tk.BOTTOM, pady=20)
    
    def ceb_get_login_colors(self):
        """CEB Get colors for login screen"""
        if self.ceb_dark_mode:
            return {
                'bg': CEB_DARK_GRAY,
                'panel_bg': CEB_NAVY_BLUE,
                'text': CEB_WHITE,
                'text_light': CEB_LIGHT_GRAY,
                'input_bg': '#1a1a2e',
                'border': '#404040',
                'brand_text': CEB_WHITE,
                'subtitle': CEB_LIGHT_GRAY,
                'hover': '#1a1a2e'
            }
        else:
            return {
                'bg': CEB_WHITE,
                'panel_bg': CEB_NAVY_BLUE,
                'text': CEB_TEXT_DARK,
                'text_light': CEB_TEXT_LIGHT,
                'input_bg': CEB_WHITE,
                'border': CEB_BORDER_GRAY,
                'brand_text': CEB_WHITE,
                'subtitle': CEB_LIGHT_GRAY,
                'hover': CEB_LIGHT_GRAY
            }
    
    def ceb_toggle_login_theme(self):
        """CEB Toggle theme from login screen"""
        self.ceb_dark_mode = not self.ceb_dark_mode
        self.ceb_display_login()
        
    def ceb_toggle_dark_mode(self):
        """CEB Toggle between dark and light mode"""
        self.ceb_dark_mode = not self.ceb_dark_mode
        
        # Check if we're in the chat screen
        if hasattr(self, 'ceb_messages_display'):
            self.ceb_apply_theme()
    
    def ceb_get_colors(self):
        """CEB Get current theme colors"""
        if self.ceb_dark_mode:
            return {
                'bg': CEB_DARK_GRAY,
                'panel_bg': CEB_NAVY_BLUE,
                'text': CEB_WHITE,
                'text_secondary': CEB_LIGHT_GRAY,
                'input_bg': '#1a1a2e',
                'border': '#404040'
            }
        else:
            return {
                'bg': CEB_WHITE,
                'panel_bg': CEB_WHITE,
                'text': CEB_TEXT_DARK,
                'text_secondary': CEB_TEXT_LIGHT,
                'input_bg': CEB_WHITE,
                'border': CEB_BORDER_GRAY
            }
    
    def ceb_apply_theme(self):
        """CEB Apply current theme to chat interface"""
        colors = self.ceb_get_colors()
        
        # Update main window
        self.ceb_window.configure(bg=colors['bg'])
        
        # Update all frames and widgets
        for widget in self.ceb_window.winfo_children():
            self.ceb_update_widget_colors(widget, colors)
        
        # Update message display tags
        if self.ceb_dark_mode:
            self.ceb_messages_display.tag_config("ceb_system", foreground=CEB_LIGHT_GRAY)
            self.ceb_messages_display.tag_config("ceb_own_name", foreground=CEB_ACCENT_BLUE)
            self.ceb_messages_display.tag_config("ceb_own_msg", foreground=CEB_WHITE)
            self.ceb_messages_display.tag_config("ceb_other_name", foreground=CEB_SUCCESS_GREEN)
            self.ceb_messages_display.tag_config("ceb_other_msg", foreground=CEB_WHITE)
            self.ceb_messages_display.tag_config("ceb_status", foreground=CEB_WARNING_AMBER)
            self.ceb_messages_display.tag_config("ceb_timestamp", foreground="#808080")
        else:
            self.ceb_messages_display.tag_config("ceb_system", foreground=CEB_TEXT_LIGHT)
            self.ceb_messages_display.tag_config("ceb_own_name", foreground=CEB_ACCENT_BLUE)
            self.ceb_messages_display.tag_config("ceb_own_msg", foreground=CEB_TEXT_DARK)
            self.ceb_messages_display.tag_config("ceb_other_name", foreground=CEB_SUCCESS_GREEN)
            self.ceb_messages_display.tag_config("ceb_other_msg", foreground=CEB_TEXT_DARK)
            self.ceb_messages_display.tag_config("ceb_status", foreground=CEB_WARNING_AMBER)
            self.ceb_messages_display.tag_config("ceb_timestamp", foreground=CEB_TEXT_LIGHT)
    
    def ceb_update_widget_colors(self, widget, colors):
        """CEB Recursively update widget colors"""
        widget_type = widget.winfo_class()
        
        try:
            # Skip buttons with specific colors (like Send button)
            if widget_type == 'Button':
                if widget.cget('bg') not in [CEB_ACCENT_BLUE, CEB_SUCCESS_GREEN]:
                    widget.config(bg=colors['panel_bg'], fg=colors['text'])
            elif widget_type == 'Frame':
                current_bg = widget.cget('bg')
                # Only update frames with standard backgrounds
                if current_bg in [CEB_WHITE, CEB_LIGHT_GRAY, CEB_SIDEBAR, CEB_DARK_GRAY, CEB_NAVY_BLUE]:
                    if current_bg == CEB_LIGHT_GRAY:
                        widget.config(bg=colors['bg'] if not self.ceb_dark_mode else '#2a2a3e')
                    else:
                        widget.config(bg=colors['panel_bg'])
            elif widget_type == 'Label':
                current_bg = widget.cget('bg')
                current_fg = widget.cget('fg')
                # Update labels but preserve special colors
                if current_bg in [CEB_WHITE, CEB_LIGHT_GRAY, CEB_SIDEBAR, CEB_DARK_GRAY, CEB_NAVY_BLUE]:
                    widget.config(bg=colors['panel_bg'])
                if current_fg in [CEB_TEXT_DARK, CEB_TEXT_LIGHT, CEB_WHITE]:
                    widget.config(fg=colors['text'])
            elif widget_type in ['Entry', 'Text']:
                widget.config(bg=colors['input_bg'], fg=colors['text'], insertbackground=CEB_ACCENT_BLUE)
        except:
            pass
        
        # Recursively update children
        for child in widget.winfo_children():
            self.ceb_update_widget_colors(child, colors)
    
    def ceb_show_credits(self):
        """CEB Show project creators"""
        ceb_credits_window = tk.Toplevel(self.ceb_window)
        ceb_credits_window.title("Project Credits")
        ceb_credits_window.geometry("400x300")
        ceb_credits_window.resizable(False, False)
        ceb_credits_window.configure(bg=CEB_WHITE)
        
        # Title
        tk.Label(
            ceb_credits_window,
            text="CEB Messenger",
            font=("Segoe UI", 22, "bold"),
            bg=CEB_WHITE,
            fg=CEB_NAVY_BLUE
        ).pack(pady=(30, 10))
        
        tk.Label(
            ceb_credits_window,
            text="━━━━━━━━━━━━━━━━━━",
            font=("Segoe UI", 10),
            bg=CEB_WHITE,
            fg=CEB_ACCENT_BLUE
        ).pack()
        
        # Creators section
        tk.Label(
            ceb_credits_window,
            text="Created By:",
            font=("Segoe UI", 14, "bold"),
            bg=CEB_WHITE,
            fg=CEB_TEXT_DARK
        ).pack(pady=(20, 15))
        
        creators = ["Chase Dishongh", "Ethan Espenshade", "Brandon Sharp"]
        
        for creator in creators:
            tk.Label(
                ceb_credits_window,
                text=f"👤 {creator}",
                font=("Segoe UI", 12),
                bg=CEB_WHITE,
                fg=CEB_TEXT_DARK
            ).pack(pady=5)
        
        # Footer
        tk.Label(
            ceb_credits_window,
            text="© 2025 CEB Corporation",
            font=("Segoe UI", 9),
            bg=CEB_WHITE,
            fg=CEB_TEXT_LIGHT
        ).pack(side=tk.BOTTOM, pady=20)
    
    def ceb_toggle_afk(self):
        """CEB Toggle AFK status"""
        if self.ceb_socket_conn:
            ceb_data = self.ceb_format_message("STATUS", self.ceb_user_name, "Away")
            ceb_time = datetime.now().strftime("%I:%M %p")
            self.ceb_add_message(ceb_time, "ceb_timestamp")
            self.ceb_add_message(f"{self.ceb_user_name} is now away", "ceb_status")
            try:
                self.ceb_socket_conn.send(ceb_data)
            except:
                self.ceb_add_message("Failed to send status update.", "ceb_system")
    
    def ceb_quit_session(self):
        """CEB Quit session with confirmation"""
        if messagebox.askyesno("Quit Session", "Are you sure you want to end this session?"):
            self.ceb_add_message("Ending session...", "ceb_system")
            self.ceb_active_session = False
            if self.ceb_socket_conn:
                try:
                    self.ceb_socket_conn.close()
                except:
                    pass
            self.ceb_window.after(1000, self.ceb_display_login)
    
    def ceb_return_to_login(self):
        """CEB Return to main login screen"""
        if messagebox.askyesno("Confirm", "Are you sure you want to return to login? This will end your current session."):
            self.ceb_active_session = False
            if self.ceb_socket_conn:
                try:
                    self.ceb_socket_conn.close()
                except:
                    pass
            self.ceb_display_login()
    
    def ceb_show_emoji_picker(self):
        """CEB Show emoji picker window"""
        ceb_emoji_window = tk.Toplevel(self.ceb_window)
        ceb_emoji_window.title("Emoji Picker")
        ceb_emoji_window.geometry("400x300")
        ceb_emoji_window.resizable(False, False)
        
        tk.Label(
            ceb_emoji_window,
            text="Select an Emoji",
            font=("Segoe UI", 14, "bold"),
            pady=10
        ).pack()
        
        ceb_emojis = [
            "😀", "😃", "😄", "😁", "😅", "😂", "🤣", "😊",
            "😇", "🙂", "😉", "😌", "😍", "🥰", "😘", "😗",
            "😙", "😚", "🤗", "🤩", "🤔", "🤨", "😐", "😑",
            "😶", "🙄", "😏", "😣", "😥", "😮", "🤐", "😯",
            "😪", "😫", "😴", "😌", "😛", "😜", "😝", "🤤",
            "👍", "👎", "👌", "✌️", "🤞", "🤟", "🤘", "👏",
            "🙌", "👐", "🤲", "🤝", "🙏", "✍️", "💪", "🦾",
            "❤️", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤",
            "🤍", "💔", "❣️", "💕", "💞", "💓", "💗", "💖",
            "💘", "💝", "🔥", "✨", "💫", "⭐", "🌟", "💯"
        ]
        
        ceb_emoji_frame = tk.Frame(ceb_emoji_window)
        ceb_emoji_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        row, col = 0, 0
        for emoji in ceb_emojis:
            btn = tk.Button(
                ceb_emoji_frame,
                text=emoji,
                font=("Segoe UI", 20),
                width=2,
                height=1,
                command=lambda e=emoji: self.ceb_insert_emoji(e, ceb_emoji_window)
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 7:
                col = 0
                row += 1
    
    def ceb_insert_emoji(self, emoji, window):
        """CEB Insert emoji into message field"""
        current_text = self.ceb_message_field.get()
        self.ceb_message_field.delete(0, tk.END)
        self.ceb_message_field.insert(0, current_text + emoji)
        window.destroy()
        self.ceb_message_field.focus()
    
    def ceb_update_users_list(self):
        """CEB Update the users list display"""
        self.ceb_users_display.config(state=tk.NORMAL)
        self.ceb_users_display.delete(1.0, tk.END)
        
        # Add current user
        self.ceb_users_display.insert(tk.END, f"🟢 {self.ceb_user_name} (You)\n", "ceb_user_active")
        
        # Add connected users
        for user in self.ceb_connected_users:
            status = self.ceb_user_status.get(user, "online")
            if status == "typing":
                self.ceb_users_display.insert(tk.END, f"✍️ {user} (typing...)\n", "ceb_user_typing")
            elif status == "afk":
                self.ceb_users_display.insert(tk.END, f"💤 {user} (Away)\n", "ceb_user_afk")
            else:
                self.ceb_users_display.insert(tk.END, f"🟢 {user}\n", "ceb_user_active")
        
        self.ceb_users_display.config(state=tk.DISABLED)
    
    def ceb_on_typing(self, event=None):
        """CEB Handle typing event"""
        current_time = time.time()
        if not self.ceb_typing or (current_time - self.ceb_last_typing_time) > 2:
            self.ceb_typing = True
            self.ceb_last_typing_time = current_time
            try:
                if self.ceb_socket_conn:
                    self.ceb_socket_conn.send(self.ceb_format_message("TYPING", self.ceb_user_name, "start"))
            except:
                pass
            
            # Auto-stop typing after 3 seconds
            self.ceb_window.after(3000, self.ceb_stop_typing_indicator)
    
    def ceb_stop_typing_indicator(self):
        """CEB Stop typing indicator"""
        if self.ceb_typing:
            self.ceb_typing = False
            try:
                if self.ceb_socket_conn:
                    self.ceb_socket_conn.send(self.ceb_format_message("TYPING", self.ceb_user_name, "stop"))
            except:
                pass
    
    def ceb_initialize_connection(self, host_mode):
        """CEB Initialize connection"""
        ceb_display_name = self.ceb_name_field.get().strip()
        if not ceb_display_name:
            messagebox.showwarning("Input Required", "Please enter your display name to continue.")
            return
            
        self.ceb_user_name = ceb_display_name
        self.ceb_hosting = host_mode
        
        self.ceb_create_messenger()
        
        if host_mode:
            threading.Thread(target=self.ceb_host_session, daemon=True).start()
        else:
            threading.Thread(target=self.ceb_join_session, daemon=True).start()
    
    def ceb_create_messenger(self):
        """CEB Main messenger interface"""
        for widget in self.ceb_window.winfo_children():
            widget.destroy()
        
        # CEB Menu Bar
        ceb_menubar = tk.Menu(self.ceb_window, bg=CEB_WHITE, fg=CEB_TEXT_DARK, relief=tk.FLAT)
        self.ceb_window.config(menu=ceb_menubar)
        
        # CEB File Menu
        ceb_file_menu = tk.Menu(ceb_menubar, tearoff=0, bg=CEB_WHITE, fg=CEB_TEXT_DARK)
        ceb_menubar.add_cascade(label="File", menu=ceb_file_menu)
        ceb_file_menu.add_command(label="Return to Login", command=self.ceb_return_to_login)
        ceb_file_menu.add_separator()
        ceb_file_menu.add_command(label="Exit", command=self.ceb_window.quit)
        
        # CEB View Menu
        ceb_view_menu = tk.Menu(ceb_menubar, tearoff=0, bg=CEB_WHITE, fg=CEB_TEXT_DARK)
        ceb_menubar.add_cascade(label="View", menu=ceb_view_menu)
        ceb_view_menu.add_command(label="Toggle Dark Mode", command=self.ceb_toggle_dark_mode)
        
        # CEB Credits Menu
        ceb_credits_menu = tk.Menu(ceb_menubar, tearoff=0, bg=CEB_WHITE, fg=CEB_TEXT_DARK)
        ceb_menubar.add_cascade(label="Credits", menu=ceb_credits_menu)
        ceb_credits_menu.add_command(label="Project Creators", command=self.ceb_show_credits)
        
        # CEB Help Menu
        ceb_help_menu = tk.Menu(ceb_menubar, tearoff=0, bg=CEB_WHITE, fg=CEB_TEXT_DARK)
        ceb_menubar.add_cascade(label="Help", menu=ceb_help_menu)
        ceb_help_menu.add_command(label="About CEB", command=lambda: messagebox.showinfo("About", "CEB Enterprise Messenger v1.0\n\nSecure communication platform"))
        
        # CEB Top navigation bar
        ceb_navbar = tk.Frame(self.ceb_window, bg=CEB_WHITE, height=70, relief=tk.FLAT, bd=1)
        ceb_navbar.pack(fill=tk.X)
        ceb_navbar.pack_propagate(False)
        
        # Add subtle bottom border
        tk.Frame(ceb_navbar, bg=CEB_BORDER_GRAY, height=1).pack(side=tk.BOTTOM, fill=tk.X)
        
        # CEB Logo/Title section
        ceb_title_section = tk.Frame(ceb_navbar, bg=CEB_WHITE)
        ceb_title_section.pack(side=tk.LEFT, padx=30, pady=15)
        
        tk.Label(
            ceb_title_section,
            text="CEB",
            font=("Segoe UI", 18, "bold"),
            bg=CEB_WHITE,
            fg=CEB_NAVY_BLUE
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Frame(ceb_title_section, bg=CEB_BORDER_GRAY, width=2, height=30).pack(side=tk.LEFT, padx=(0, 15))
        
        tk.Label(
            ceb_title_section,
            text="Enterprise Messenger",
            font=("Segoe UI", 11),
            bg=CEB_WHITE,
            fg=CEB_TEXT_LIGHT
        ).pack(side=tk.LEFT)
        
        # CEB User info section
        ceb_user_section = tk.Frame(ceb_navbar, bg=CEB_WHITE)
        ceb_user_section.pack(side=tk.RIGHT, padx=30, pady=15)
        
        tk.Label(
            ceb_user_section,
            text=self.ceb_user_name,
            font=("Segoe UI", 11, "bold"),
            bg=CEB_WHITE,
            fg=CEB_TEXT_DARK
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # CEB Status indicator
        ceb_status_container = tk.Frame(ceb_user_section, bg=CEB_SIDEBAR, relief=tk.FLAT, bd=1)
        ceb_status_container.pack(side=tk.LEFT)
        
        ceb_mode_label = "Hosting" if self.ceb_hosting else "Connecting"
        self.ceb_status_indicator = tk.Label(
            ceb_status_container,
            text=f"● {ceb_mode_label}",
            font=("Segoe UI", 9),
            bg=CEB_SIDEBAR,
            fg=CEB_WARNING_AMBER,
            padx=12,
            pady=6
        )
        self.ceb_status_indicator.pack()
        
        # CEB Main content area with sidebar
        ceb_main_content = tk.Frame(self.ceb_window, bg=CEB_LIGHT_GRAY)
        ceb_main_content.pack(fill=tk.BOTH, expand=True)
        
        # CEB Users sidebar
        ceb_sidebar = tk.Frame(ceb_main_content, bg=CEB_WHITE, width=200, relief=tk.FLAT, bd=1)
        ceb_sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20), pady=20)
        ceb_sidebar.pack_propagate(False)
        
        tk.Label(
            ceb_sidebar,
            text="👥 Users",
            font=("Segoe UI", 12, "bold"),
            bg=CEB_WHITE,
            fg=CEB_TEXT_DARK
        ).pack(pady=10)
        
        tk.Frame(ceb_sidebar, bg=CEB_BORDER_GRAY, height=1).pack(fill=tk.X)
        
        self.ceb_users_display = scrolledtext.ScrolledText(
            ceb_sidebar,
            wrap=tk.WORD,
            font=("Segoe UI", 9),
            bg=CEB_WHITE,
            fg=CEB_TEXT_DARK,
            relief=tk.FLAT,
            bd=0,
            state=tk.DISABLED,
            padx=10,
            pady=10,
            width=20
        )
        self.ceb_users_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # CEB Users display tags
        self.ceb_users_display.tag_config("ceb_user_active", foreground=CEB_SUCCESS_GREEN, font=("Segoe UI", 9, "bold"))
        self.ceb_users_display.tag_config("ceb_user_typing", foreground=CEB_ACCENT_BLUE, font=("Segoe UI", 9, "italic"))
        self.ceb_users_display.tag_config("ceb_user_afk", foreground=CEB_WARNING_AMBER, font=("Segoe UI", 9))
        
        # Initialize users list
        self.ceb_update_users_list()
        
        # CEB Chat panel
        ceb_chat_panel = tk.Frame(ceb_main_content, bg=CEB_WHITE, relief=tk.FLAT, bd=1)
        ceb_chat_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(40, 10), pady=30)
        
        # Add border
        tk.Frame(ceb_chat_panel, bg=CEB_BORDER_GRAY, height=1).pack(fill=tk.X)
        
        # CEB Chat header
        ceb_chat_header = tk.Frame(ceb_chat_panel, bg=CEB_WHITE, height=50)
        ceb_chat_header.pack(fill=tk.X)
        ceb_chat_header.pack_propagate(False)
        
        tk.Label(
            ceb_chat_header,
            text="Messages",
            font=("Segoe UI", 13, "bold"),
            bg=CEB_WHITE,
            fg=CEB_TEXT_DARK
        ).pack(side=tk.LEFT, padx=20, pady=15)
        
        # CEB Typing indicator
        self.ceb_typing_label = tk.Label(
            ceb_chat_header,
            text="",
            font=("Segoe UI", 9, "italic"),
            bg=CEB_WHITE,
            fg=CEB_TEXT_LIGHT
        )
        self.ceb_typing_label.pack(side=tk.LEFT, padx=10)
        
        tk.Frame(ceb_chat_panel, bg=CEB_BORDER_GRAY, height=1).pack(fill=tk.X)
        
        # CEB Messages display area
        ceb_messages_frame = tk.Frame(ceb_chat_panel, bg=CEB_WHITE)
        ceb_messages_frame.pack(fill=tk.BOTH, expand=True)
        
        self.ceb_messages_display = scrolledtext.ScrolledText(
            ceb_messages_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg=CEB_WHITE,
            fg=CEB_TEXT_DARK,
            relief=tk.FLAT,
            bd=0,
            state=tk.DISABLED,
            padx=20,
            pady=20
        )
        self.ceb_messages_display.pack(fill=tk.BOTH, expand=True)
        
        # CEB Message styling tags
        self.ceb_messages_display.tag_config("ceb_system", foreground=CEB_TEXT_LIGHT, font=("Segoe UI", 9, "italic"))
        self.ceb_messages_display.tag_config("ceb_own_name", foreground=CEB_ACCENT_BLUE, font=("Segoe UI", 10, "bold"))
        self.ceb_messages_display.tag_config("ceb_own_msg", foreground=CEB_TEXT_DARK, font=("Segoe UI", 10))
        self.ceb_messages_display.tag_config("ceb_other_name", foreground=CEB_SUCCESS_GREEN, font=("Segoe UI", 10, "bold"))
        self.ceb_messages_display.tag_config("ceb_other_msg", foreground=CEB_TEXT_DARK, font=("Segoe UI", 10))
        self.ceb_messages_display.tag_config("ceb_status", foreground=CEB_WARNING_AMBER, font=("Segoe UI", 9, "italic"))
        self.ceb_messages_display.tag_config("ceb_timestamp", foreground=CEB_TEXT_LIGHT, font=("Segoe UI", 8))
        
        tk.Frame(ceb_chat_panel, bg=CEB_BORDER_GRAY, height=1).pack(fill=tk.X)
        
        # CEB Input area
        ceb_input_section = tk.Frame(ceb_chat_panel, bg=CEB_WHITE, height=90)
        ceb_input_section.pack(fill=tk.X)
        ceb_input_section.pack_propagate(False)
        
        # CEB Commands hint
        tk.Label(
            ceb_input_section,
            text="Commands: /afk (mark as away) • /quit (end session)",
            font=("Segoe UI", 8),
            bg=CEB_WHITE,
            fg=CEB_TEXT_LIGHT
        ).pack(anchor=tk.W, padx=20, pady=(10, 5))
        
        # CEB Input field container
        ceb_input_container = tk.Frame(ceb_input_section, bg=CEB_WHITE)
        ceb_input_container.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # CEB Emoji button
        ceb_emoji_btn = tk.Button(
            ceb_input_container,
            text="😀",
            font=("Segoe UI", 14),
            bg=CEB_WHITE,
            fg=CEB_TEXT_DARK,
            activebackground=CEB_LIGHT_GRAY,
            relief=tk.FLAT,
            bd=0,
            width=3,
            cursor="hand2",
            command=self.ceb_show_emoji_picker
        )
        ceb_emoji_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        ceb_input_border = tk.Frame(ceb_input_container, bg=CEB_WHITE, relief=tk.SOLID, bd=1, highlightbackground=CEB_BORDER_GRAY, highlightthickness=1)
        ceb_input_border.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.ceb_message_field = tk.Entry(
            ceb_input_border,
            font=("Segoe UI", 11),
            bg=CEB_WHITE,
            fg=CEB_TEXT_DARK,
            insertbackground=CEB_ACCENT_BLUE,
            relief=tk.FLAT,
            bd=0
        )
        self.ceb_message_field.pack(fill=tk.BOTH, padx=15, pady=12)
        self.ceb_message_field.bind("<Return>", lambda e: self.ceb_send_message())
        self.ceb_message_field.bind("<KeyPress>", self.ceb_on_typing)
        
        # CEB Send button
        ceb_send_btn = tk.Button(
            ceb_input_container,
            text="Send",
            font=("Segoe UI", 11, "bold"),
            bg=CEB_ACCENT_BLUE,
            fg=CEB_WHITE,
            activebackground=CEB_HOVER_BLUE,
            activeforeground=CEB_WHITE,
            relief=tk.FLAT,
            bd=0,
            width=12,
            cursor="hand2",
            command=self.ceb_send_message
        )
        ceb_send_btn.pack(side=tk.LEFT, ipady=8)
        
    def ceb_add_message(self, text, tag="ceb_system"):
        """CEB Add message to display"""
        self.ceb_messages_display.config(state=tk.NORMAL)
        self.ceb_messages_display.insert(tk.END, text + "\n", tag)
        self.ceb_messages_display.see(tk.END)
        self.ceb_messages_display.config(state=tk.DISABLED)
        
    def ceb_send_message(self):
        """CEB Send message handler"""
        ceb_text = self.ceb_message_field.get().strip()
        if not ceb_text or not self.ceb_socket_conn:
            return
            
        self.ceb_message_field.delete(0, tk.END)
        self.ceb_stop_typing_indicator()
        
        if ceb_text.lower() == "/quit":
            self.ceb_add_message("Ending session...", "ceb_system")
            self.ceb_active_session = False
            if self.ceb_socket_conn:
                self.ceb_socket_conn.close()
            self.ceb_window.after(1000, self.ceb_display_login)
            return
            
        elif ceb_text.lower() == "/afk":
            ceb_data = self.ceb_format_message("STATUS", self.ceb_user_name, "Away")
            ceb_time = datetime.now().strftime("%I:%M %p")
            self.ceb_add_message(ceb_time, "ceb_timestamp")
            self.ceb_add_message(f"{self.ceb_user_name} is now away", "ceb_status")
        else:
            ceb_data = self.ceb_format_message("TEXT", self.ceb_user_name, ceb_text)
            ceb_time = datetime.now().strftime("%I:%M %p")
            self.ceb_add_message(ceb_time, "ceb_timestamp")
            self.ceb_add_message(self.ceb_user_name, "ceb_own_name")
            self.ceb_add_message(ceb_text, "ceb_own_msg")
        
        try:
            self.ceb_socket_conn.send(ceb_data)
        except:
            self.ceb_add_message("Failed to send message. Connection error.", "ceb_system")
    
    def ceb_format_message(self, msg_type, sender, body):
        """CEB Format message for transmission"""
        return f"{msg_type}|{sender}|{body}".encode()
    
    def ceb_parse_message(self, data):
        """CEB Parse received message"""
        try:
            decoded = data.decode()
            msg_type, sender, body = decoded.split("|", 2)
            return msg_type, sender, body
        except:
            return None, None, None
    
    def ceb_host_session(self):
        """CEB Host server session"""
        try:
            ceb_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ceb_server.bind((CEB_HOST, CEB_PORT))
            ceb_server.listen(1)
            
            self.ceb_add_message(f"Session hosted on {CEB_HOST}:{CEB_PORT}", "ceb_system")
            self.ceb_add_message("Waiting for participants to join...", "ceb_system")
            
            ceb_conn, ceb_addr = ceb_server.accept()
            self.ceb_socket_conn = ceb_conn
            
            self.ceb_add_message(f"Participant connected from {ceb_addr[0]}", "ceb_system")
            self.ceb_status_indicator.config(text="● Connected", fg=CEB_SUCCESS_GREEN)
            
            # Send username to other user
            self.ceb_socket_conn.send(self.ceb_format_message("USERNAME", self.ceb_user_name, ""))
            
            self.ceb_receive_messages()
            
        except Exception as e:
            self.ceb_add_message(f"Server error: {str(e)}", "ceb_system")
    
    def ceb_join_session(self):
        """CEB Join client session"""
        try:
            ceb_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ceb_client.connect((CEB_HOST, CEB_PORT))
            self.ceb_socket_conn = ceb_client
            
            self.ceb_add_message(f"Connected to session at {CEB_HOST}:{CEB_PORT}", "ceb_system")
            self.ceb_status_indicator.config(text="● Connected", fg=CEB_SUCCESS_GREEN)
            
            # Send username to other user
            self.ceb_socket_conn.send(self.ceb_format_message("USERNAME", self.ceb_user_name, ""))
            
            self.ceb_receive_messages()
            
        except Exception as e:
            self.ceb_add_message(f"Connection failed: {str(e)}", "ceb_system")
            self.ceb_add_message("Please ensure the host session is active.", "ceb_system")
    
    def ceb_receive_messages(self):
        """CEB Receive messages loop"""
        while self.ceb_active_session:
            try:
                ceb_data = self.ceb_socket_conn.recv(1024)
                if not ceb_data:
                    self.ceb_add_message("Connection closed by remote participant.", "ceb_system")
                    break
                    
                ceb_type, ceb_sender, ceb_body = self.ceb_parse_message(ceb_data)
                
                if ceb_type == "USERNAME":
                    # Add user to connected users list
                    if ceb_sender not in self.ceb_connected_users:
                        self.ceb_connected_users.append(ceb_sender)
                        self.ceb_user_status[ceb_sender] = "online"
                        self.ceb_update_users_list()
                        self.ceb_add_message(f"{ceb_sender} joined the session", "ceb_system")
                
                elif ceb_type == "TYPING":
                    if ceb_body == "start":
                        self.ceb_user_status[ceb_sender] = "typing"
                        self.ceb_typing_label.config(text=f"{ceb_sender} is typing...")
                        self.ceb_update_users_list()
                    else:
                        self.ceb_user_status[ceb_sender] = "online"
                        self.ceb_typing_label.config(text="")
                        self.ceb_update_users_list()
                
                elif ceb_type == "TEXT":
                    ceb_time = datetime.now().strftime("%I:%M %p")
                    self.ceb_add_message(ceb_time, "ceb_timestamp")
                    self.ceb_add_message(ceb_sender, "ceb_other_name")
                    self.ceb_add_message(ceb_body, "ceb_other_msg")
                    self.ceb_typing_label.config(text="")
                    self.ceb_user_status[ceb_sender] = "online"
                    self.ceb_update_users_list()
                    
                elif ceb_type == "STATUS":
                    ceb_time = datetime.now().strftime("%I:%M %p")
                    self.ceb_add_message(ceb_time, "ceb_timestamp")
                    self.ceb_add_message(f"{ceb_sender} is now {ceb_body.lower()}", "ceb_status")
                    self.ceb_user_status[ceb_sender] = "afk"
                    self.ceb_update_users_list()
                    
            except:
                break
    
    def ceb_start(self):
        """CEB Start application"""
        self.ceb_window.mainloop()

# ===============================
# CEB PROFESSIONAL EDITION LAUNCH
# ===============================
if __name__ == "__main__":
    ceb_professional_app = CEBProfessional()
    ceb_professional_app.ceb_start()