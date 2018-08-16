import os
from niconvert.fndtk.tkmodules import tk, ttk, tku

class IoFrame(ttk.LabelFrame):

    def __init__(self, parent):
        ttk.LabelFrame.__init__(self, parent, text='输入输出', padding=2)
        self.pack(fill=tk.BOTH)
        self.grid_columnconfigure(1, weight=1)
        self.init_widgets()

    def init_widgets(self):
        self.init_input_filename_widgets()
        self.init_output_filename_widgets()
        self.init_convert_widgets()
        tku.add_border_space(self, 1, 1)

    def init_input_filename_widgets(self):
        strvar = tk.StringVar()
        label = ttk.Label(self, text='弹幕文件：')
        entry = ttk.Entry(self, textvariable=strvar)
        button = ttk.Button(self, text='浏览', width=6)

        label.grid(row=0, column=0, sticky=tk.E)
        entry.grid(row=0, column=1, sticky=tk.EW)
        button.grid(row=0, column=2, sticky=tk.W)

        strvar.set(os.getcwd() + '/')
        button['command'] = self.on_input_filename_button_clicked

        self.input_filename_strvar = strvar

    def init_output_filename_widgets(self):
        strvar = tk.StringVar()
        label = ttk.Label(self, text='输出文件：')
        entry = ttk.Entry(self, textvariable=strvar)
        button = ttk.Button(self, text='浏览', width=6)

        label.grid(row=1, column=0, sticky=tk.E)
        entry.grid(row=1, column=1, sticky=tk.EW)
        button.grid(row=1, column=2, sticky=tk.W)

        strvar.set(os.getcwd() + '/')
        button['command'] = self.on_output_filename_button_clicked
        self.output_filename_strvar = strvar

    def init_convert_widgets(self):
        button = ttk.Button(self, text='转换', width=6)

        button.grid(row=3, column=2, sticky=tk.W)

        button['command'] = self.on_convert_button_clicked
        self.convert_button = button

    def on_input_filename_button_clicked(self):
        current_path = self.input_filename_strvar.get().strip()
        if current_path == '':
            foldername, filename = os.getcwd(), ''
        else:
            foldername, filename = os.path.split(current_path)

        selected_path = tk.filedialog.askopenfilename(
            parent=self,
            title='打开文件',
            initialdir=foldername,
            initialfile=filename
        )

        if selected_path is None or len(selected_path) == 0:
            return

        self.input_filename_strvar.set(selected_path)
        output_filename = self.output_filename_strvar.get().strip()
        if not output_filename.endswith('.ass'):
            path = selected_path.replace('.json', '.ass')
            self.output_filename_strvar.set(path)

    def on_output_filename_button_clicked(self):
        current_path = self.output_filename_strvar.get().strip()
        if current_path == '':
            foldername, filename = os.getcwd(), ''
        elif os.path.isdir(current_path):
            foldername, filename = current_path, ''
        else:
            foldername, filename = os.path.split(current_path)

        selected_path = tk.filedialog.asksaveasfilename(
            parent=self,
            title='保存文件',
            initialdir=foldername,
            initialfile=filename
        )

        if selected_path is None or len(selected_path) == 0:
            return

        if selected_path == '':
            selected_path = os.getcwd()
        self.output_filename_strvar.set(selected_path)

    def on_convert_button_clicked(self):
        self.event_generate('<<ConvertButtonClicked>>')

    def values(self):
        return dict(
            input_filename=self.input_filename_strvar.get().strip(),
            output_filename=self.output_filename_strvar.get().strip(),
        )

    def enable_convert_button(self):
        self.convert_button['state'] = tk.NORMAL

    def disable_convert_button(self):
        self.convert_button['state'] = tk.DISABLED
