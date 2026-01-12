import tkinter as tk
import time

class ChessClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Productivity Clock")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        # Time variables (in seconds)
        self.player1_time = 5  # Productivity - counts down
        self.player2_time = 0    # Slack - counts up
        self.active_player = None
        self.running = False
        self.last_update = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="Productivity Clock", font=('Arial', 24, 'bold'),
                        bg='#2c3e50', fg='white')
        title.pack(pady=15)
        
        # Settings
        settings = tk.Frame(self.root, bg='#34495e', relief=tk.RAISED, bd=2)
        settings.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(settings, text="Time:", font=('Arial', 11),
                bg='#34495e', fg='white').pack(side=tk.LEFT, padx=10)
        
        tk.Button(settings, text="1 hour", width=8,
                 command=lambda: self.set_time(3600)).pack(side=tk.LEFT, padx=3)
        tk.Button(settings, text="2 hour", width=8,
                 command=lambda: self.set_time(7200)).pack(side=tk.LEFT, padx=3)
        
        tk.Label(settings, text="Custom (min):", font=('Arial', 11),
                bg='#34495e', fg='white').pack(side=tk.LEFT, padx=(15, 5))
        
        self.custom_entry = tk.Entry(settings, width=8, font=('Arial', 11))
        self.custom_entry.pack(side=tk.LEFT, padx=3)
        
        tk.Button(settings, text="Set", width=6,
                 command=self.set_custom).pack(side=tk.LEFT, padx=3)
        
        # Clocks
        clocks = tk.Frame(self.root, bg='#2c3e50')
        clocks.pack(pady=25, expand=True, fill=tk.BOTH)
        
        # Player 1
        self.p1_frame = tk.Frame(clocks, bg='#ecf0f1', relief=tk.RAISED, bd=4)
        self.p1_frame.pack(side=tk.LEFT, padx=15, expand=True, fill=tk.BOTH)
        
        self.p1_name = tk.Entry(self.p1_frame, font=('Arial', 16, 'bold'),
                               justify='center', bg='#ecf0f1', relief=tk.FLAT)
        self.p1_name.insert(0, "Productivity")
        self.p1_name.pack(pady=15)
        
        self.p1_time = tk.Label(self.p1_frame, text="00:10:00", 
                               font=('Arial', 56, 'bold'), bg='#ecf0f1')
        self.p1_time.pack(pady=40)
        
        self.p1_btn = tk.Button(self.p1_frame, text="CLICK", 
                               font=('Arial', 16, 'bold'), 
                               bg='#3498db', fg='white',
                               activebackground='#2980b9',
                               height=3, width=15)
        self.p1_btn.config(command=lambda: self.button_click(1))
        self.p1_btn.pack(pady=25)
        
        # Player 2
        self.p2_frame = tk.Frame(clocks, bg='#ecf0f1', relief=tk.RAISED, bd=4)
        self.p2_frame.pack(side=tk.RIGHT, padx=15, expand=True, fill=tk.BOTH)
        
        self.p2_name = tk.Entry(self.p2_frame, font=('Arial', 16, 'bold'),
                               justify='center', bg='#ecf0f1', relief=tk.FLAT)
        self.p2_name.insert(0, "Slack")
        self.p2_name.pack(pady=15)
        
        self.p2_time = tk.Label(self.p2_frame, text="00:00:00", 
                               font=('Arial', 56, 'bold'), bg='#ecf0f1')
        self.p2_time.pack(pady=40)
        
        self.p2_btn = tk.Button(self.p2_frame, text="CLICK", 
                               font=('Arial', 16, 'bold'), 
                               bg='#3498db', fg='white',
                               activebackground='#2980b9',
                               height=3, width=15)
        self.p2_btn.config(command=lambda: self.button_click(2))
        self.p2_btn.pack(pady=25)
        
        # Controls
        controls = tk.Frame(self.root, bg='#2c3e50')
        controls.pack(pady=15)
        
        self.pause_btn = tk.Button(controls, text="STOP", font=('Arial', 13, 'bold'),
                 command=self.toggle_pause, width=12, height=2,
                 bg='#e74c3c', fg='white')
        self.pause_btn.pack(side=tk.LEFT, padx=8)
        
        tk.Button(controls, text="RESET", font=('Arial', 13, 'bold'),
                 command=self.reset, width=12, height=2,
                 bg='#95a5a6', fg='white').pack(side=tk.LEFT, padx=8)
    
    def button_click(self, player):
        # Start or switch to the clicked player's clock
        if self.active_player == player and self.running:
            # Already running this clock, do nothing
            return
        
        # Switch to or start this player's clock
        self.active_player = player
        self.running = True
        self.last_update = time.time()
        self.update_buttons()
        
        if not hasattr(self, '_tick_running'):
            self._tick_running = False
        
        if not self._tick_running:
            self._tick_running = True
            self.tick()
    
    def update_buttons(self):
        if self.active_player == 1:
            self.p1_btn.config(text="ACTIVE", bg='#2ecc71')
            self.p2_btn.config(text="CLICK", bg='#3498db')
        elif self.active_player == 2:
            self.p2_btn.config(text="ACTIVE", bg='#2ecc71')
            self.p1_btn.config(text="CLICK", bg='#3498db')
        else:
            self.p1_btn.config(text="CLICK", bg='#3498db')
            self.p2_btn.config(text="CLICK", bg='#3498db')
    
    def tick(self):
        if not self.running or self.active_player is None:
            self._tick_running = False
            return
        
        now = time.time()
        elapsed = now - self.last_update
        self.last_update = now
        
        if self.active_player == 1:
            # Productivity - count down
            self.player1_time -= elapsed
            if self.player1_time <= 0:
                self.player1_time = 0
                self.end_game(2)  # Slack wins
                self._tick_running = False
                return
        else:
            # Slack - count up
            self.player2_time += elapsed
        
        self.display_times()
        self.root.after(100, self.tick)
    
    def display_times(self):
        # Format and display times with hours
        total_seconds1 = int(abs(self.player1_time))
        h1 = total_seconds1 // 3600
        m1 = (total_seconds1 % 3600) // 60
        s1 = total_seconds1 % 60
        self.p1_time.config(text=f"{h1:02d}:{m1:02d}:{s1:02d}")
        
        total_seconds2 = int(abs(self.player2_time))
        h2 = total_seconds2 // 3600
        m2 = (total_seconds2 % 3600) // 60
        s2 = total_seconds2 % 60
        self.p2_time.config(text=f"{h2:02d}:{m2:02d}:{s2:02d}")
        
        # Color warnings for Productivity (countdown)
        if self.player1_time < 60:
            self.p1_frame.config(bg='#e74c3c')
            self.p1_time.config(bg='#e74c3c', fg='white')
        elif self.player1_time < 180:
            self.p1_frame.config(bg='#f39c12')
            self.p1_time.config(bg='#f39c12', fg='white')
        else:
            self.p1_frame.config(bg='#ecf0f1')
            self.p1_time.config(bg='#ecf0f1', fg='black')
        
        # Color warnings for Slack (countup) - changes color as time increases
        if self.player2_time > 1800:  # Over 30 min
            self.p2_frame.config(bg='#e74c3c')
            self.p2_time.config(bg='#e74c3c', fg='white')
        elif self.player2_time > 600:  # Over 10 min
            self.p2_frame.config(bg='#f39c12')
            self.p2_time.config(bg='#f39c12', fg='white')
        else:
            self.p2_frame.config(bg='#ecf0f1')
            self.p2_time.config(bg='#ecf0f1', fg='black')
    
    def set_time(self, seconds):
        if not self.running:
            self.player1_time = seconds
            self.player2_time = 0  # Slack always starts at 0
            self.display_times()
    
    def set_custom(self):
        try:
            minutes = float(self.custom_entry.get())
            seconds = int(minutes * 60)
            if seconds > 0:
                self.set_time(seconds)
        except ValueError:
            pass
    
    def toggle_pause(self):
        if self.active_player is None:
            return
        
        self.running = not self.running
        
        if self.running:
            self.pause_btn.config(text="STOP", bg='#e74c3c')
            self.last_update = time.time()
            if not hasattr(self, '_tick_running'):
                self._tick_running = False
            if not self._tick_running:
                self._tick_running = True
                self.tick()
        else:
            self.pause_btn.config(text="RESUME", bg='#f39c12')
            self._tick_running = False
    
    def reset(self):
        self.running = False
        self.active_player = None
        self.player1_time = 600
        self.player2_time = 0  # Slack resets to 0
        self.pause_btn.config(text="STOP", bg='#e74c3c')
        self.update_buttons()
        self.display_times()
    
    def end_game(self, winner):
        self.running = False
        self.p1_btn.config(text="GAME OVER", bg='#7f8c8d')
        self.p2_btn.config(text="GAME OVER", bg='#7f8c8d')
        
        winner_name = self.p1_name.get() if winner == 2 else self.p2_name.get()
        
        win = tk.Toplevel(self.root)
        win.title("Game Over")
        win.geometry("350x180")
        win.configure(bg='#2c3e50')
        
        tk.Label(win, text=f"{winner_name} Wins!", 
                font=('Arial', 24, 'bold'), 
                bg='#2c3e50', fg='white').pack(pady=40)
        tk.Button(win, text="Close", command=win.destroy, 
                 font=('Arial', 14), width=10,
                 bg='#3498db', fg='white').pack()

def main():
    root = tk.Tk()
    app = ChessClock(root)
    root.mainloop()

if __name__ == "__main__":
    main()