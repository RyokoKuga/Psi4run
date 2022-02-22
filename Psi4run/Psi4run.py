import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os, subprocess, threading

#####  関数  #####
# 入力ファイルの登録 (Add Filesボタン)
def save_input():
    # ファイル選択ダイアログ表示
    typ = [("Psi4", "*.in"), ("Psi4", "*.dat"), ("All Files","*.*")] 
    input_paths = tk.filedialog.askopenfilenames(filetypes = typ)

    if len(input_paths) != 0:
        # ファイルが選択された場合
        for input_path in input_paths:
            # パスをツリービューに登録
            table.insert("", "end", values = ("Pending", input_path))
            # ステータス更新
            statusbar["text"] = "  Let's Start!!"
    else:
        pass
        
# ボタンの一時無効化
def invalid_func():
    file_button['state'] = tk.DISABLED
    remove_button['state'] = tk.DISABLED
    run_button['state'] = tk.DISABLED
    
# ボタンの有効化
def ac_func():
    file_button['state'] = tk.NORMAL
    remove_button['state'] = tk.NORMAL
    run_button['state'] = tk.NORMAL
    
###########################################################################################
# バッチ計算の実行
def batch_calc():
    # テーブルに値がない場合、終了    
    if not table.get_children():
        return
    # ボタンの一時無効化
    invalid_func()
    try:
        # ツリービューからパス取得
        for child in table.get_children():
            path = table.item(child)["values"][1]
            # ステータスの更新
            statusbar["text"] = "  Psi4 calculation has started please wait..."
            
            # 作業ディレクトリの移動
            os.chdir(os.path.dirname(path))
            # Psi4実行
            subprocess.run(["psi4", os.path.basename(path)])
            
            # ツリービュー更新
            table.delete(child)
            table.insert("", "end", values = ("Done", path))

        # 終了後にステータス更新
        statusbar["text"] = "  Successfully terminated!!"
        # ボタンの有効化
        ac_func()
        # 終了通知
        messagebox.showinfo("Information", "Successfully terminated!!")
        
    except:
        try:
            # ステータス更新
            statusbar["text"] = "  Error!!"
            # ボタンの有効化
            ac_func()
            # エラー通知
            messagebox.showerror("Error", "Check the settings!!")
        except:
            pass

# スレッドの生成と開始 (Runボタン)
def add_thread():
    global thread
    thread = threading.Thread(target = batch_calc, daemon = True)
    thread.start()
###########################################################################################

# ツリービューの削除 (Removeボタン)
def del_vule():
    # 選択した値の取得
    slct_items = table.selection()
    # 選択された場合は削除
    if not slct_items:
        return
    for slct_item in  slct_items:
        table.delete(slct_item)
    # テーブルに値がない場合、ステータス更新    
    if not table.get_children():
        statusbar["text"] = "  No input file!!"

# 終了確認 (閉じるボタン)
def on_closing():
    try:
        # Psi4が計算中の場合
        if thread.is_alive():
            # 警告
            messagebox.showwarning("Warning", "Psi4 is calculating!!")
        else:
            # 閉じる
            root.destroy()
    except:
        root.destroy()
    
#####  GUI  #####
# ウインドウ作成
root = tk.Tk()
root.title("Psi4run Ver.1.0.0")
root.geometry("800x500")
root.minsize(width = 800, height = 500)
root.iconphoto(True, tk.PhotoImage(file = "tb_icon.png"))
root.configure(bg = "#ffffff")

# フレーム色
style = ttk.Style()
style.configure("example.TFrame", background = "#ffffff")

# フレーム作成
frame1 = ttk.Frame(root, padding = 5, style="example.TFrame")
frame1.pack(fill = tk.BOTH)
frame2 = ttk.Frame(root, padding = 5, style="example.TFrame")
frame2.pack(fill = tk.BOTH)
frame3 = ttk.Frame(root, padding = 5, style="example.TFrame")
frame3.pack(padx = 5, pady = 5, fill = tk.BOTH, expand =1)

# キャンバス作成
canvas = tk.Canvas(frame1, height = 80, bg = "#ffffff", highlightthickness = 0, relief = "flat")
canvas.pack(side = tk.LEFT, padx = 5, pady = 5)
background_img = tk.PhotoImage(file = f"background.png")
background = canvas.create_image(10, 10, image = background_img, anchor = tk.NW)

# Fileボタン作成
img2 = tk.PhotoImage(file = f"img2.png")
file_button = tk.Button(frame2, image = img2, borderwidth = 0, highlightthickness = 0, relief = "flat", command = save_input)
file_button.pack(side = tk.LEFT, padx = 5, pady = 5)
# Removeボタン作成
img1 = tk.PhotoImage(file = f"img1.png")
remove_button = tk.Button(frame2, image = img1, borderwidth = 0, highlightthickness = 0, relief = "flat", command = del_vule)
remove_button.pack(side = tk.LEFT, padx = 5, pady = 5)
# Runボタン作成
img0 = tk.PhotoImage(file = f"img0.png")
run_button = tk.Button(frame2, image = img0, borderwidth = 0, highlightthickness = 0, relief = "flat", command = add_thread)
run_button.pack(side = tk.LEFT, padx = 5, pady = 5)

# ツリービュー作成
table = ttk.Treeview(frame3)
# 列の作成
table["column"] = (1, 2)
table["show"] = "headings"
# ヘッダーテキスト
table.heading(1, anchor="w", text = "Status")
table.heading(2, anchor="w", text = "Name")
# 列幅
table.column(1, width = 80)
table.column(2, width = 500)

# スクロールバー作成
yscroll = tk.Scrollbar(frame3, orient = tk.VERTICAL, command = table.yview)
yscroll.pack(side = tk.RIGHT, fill = "y")
table["yscrollcommand"] = yscroll.set
# ツリービュー設置
table.pack(fill = tk.BOTH, expand =1)

# ステータスバー作成
statusbar = tk.Label(root, bd = 1, text =  "  No input file!!", relief = tk.SUNKEN, anchor = tk.W, bg = "#ffffff")
statusbar.pack(side = tk.BOTTOM, fill=tk.X)

# 終了確認
root.protocol("WM_DELETE_WINDOW", on_closing)

# ウインドウ状態の維持
root.mainloop()