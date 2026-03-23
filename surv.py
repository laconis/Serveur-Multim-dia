import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import signal
import platform
import argparse
import time

# ---------------------------------------------------------
#  ARGUMENTS DU SCRIPT
# ---------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--user", type=str, required=False, help="Nom utilisateur à filtrer")
args = parser.parse_args()
user_filter = args.user.lower() if args.user else None


# ---------------------------------------------------------
#  FORMATAGE DUREE HH:MM:SS
# ---------------------------------------------------------
def format_duree(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"


# ---------------------------------------------------------
#  RECUPERATION DES PROCESSUS PYTHON
# ---------------------------------------------------------
def get_python_processes():
    result = []
    for p in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent',
                                  'cmdline', 'create_time']):
        try:
            if "python" not in p.info['name'].lower():
                continue

            cmd = " ".join(p.info['cmdline']) if p.info['cmdline'] else ""

            # Filtrage par user si demandé
            if user_filter and user_filter not in cmd.lower():
                continue

            mem = p.info['memory_info'].rss / 1024 / 1024
            cpu = p.cpu_percent(interval=None)
            duree_sec = int(time.time() - p.info['create_time'])
            duree_fmt = format_duree(duree_sec)

            result.append((p.info['pid'], f"{cpu:.1f}%", f"{mem:.1f} Mo", duree_fmt, cmd))

        except:
            pass

    return result


# ---------------------------------------------------------
#  TRI AVEC FLÈCHES + MULTI-COLONNES
# ---------------------------------------------------------
def trier_colonne(tree, col, ordre, colonnes_secondaires=None):
    lignes = [(tree.set(k, col), k) for k in tree.get_children('')]

    def convertir(val):
        try:
            return float(val.replace("%", "").replace(" Mo", ""))
        except:
            return val.lower()

    lignes.sort(key=lambda t: convertir(t[0]), reverse=ordre)

    if colonnes_secondaires:
        for col2 in reversed(colonnes_secondaires):
            lignes.sort(
                key=lambda t: convertir(tree.set(t[1], col2)),
                reverse=ordre
            )

    for index, (val, k) in enumerate(lignes):
        tree.move(k, '', index)

    for c in tree["columns"]:
        texte = c
        if c == col:
            texte += " ▲" if not ordre else " ▼"
        tree.heading(c, text=texte,
                     command=lambda c=c: trier_colonne(tree, c, not ordre, colonnes_secondaires))


# ---------------------------------------------------------
#  ENVOYER CTRL+C
# ---------------------------------------------------------
def envoyer_ctrl_c():
    selected = table.selection()
    if not selected:
        messagebox.showerror("Erreur", "Aucun processus sélectionné.")
        return

    pid = table.item(selected[0])["values"][0]

    try:
        p = psutil.Process(pid)

        if platform.system() in ("Linux", "Darwin"):
            p.send_signal(signal.SIGINT)
        elif platform.system() == "Windows":
            p.send_signal(signal.CTRL_BREAK_EVENT)

        messagebox.showinfo("OK", f"Ctrl+C envoyé au PID {pid}")

    except psutil.NoSuchProcess:
        messagebox.showerror("Erreur", "Le processus n'existe plus.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'envoyer Ctrl+C : {e}")


# ---------------------------------------------------------
#  TUER LE PROCESSUS (SIGKILL)
# ---------------------------------------------------------
def tuer_processus():
    selected = table.selection()
    if not selected:
        messagebox.showerror("Erreur", "Aucun processus sélectionné.")
        return

    pid = table.item(selected[0])["values"][0]

    try:
        p = psutil.Process(pid)
        p.kill()
        messagebox.showinfo("OK", f"Processus {pid} tué.")
    except psutil.NoSuchProcess:
        messagebox.showerror("Erreur", "Le processus n'existe plus.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de tuer le processus : {e}")


# ---------------------------------------------------------
#  RAFRAICHISSEMENT AUTOMATIQUE
# ---------------------------------------------------------
def refresh_table():
    for row in table.get_children():
        table.delete(row)

    for proc in get_python_processes():
        table.insert("", tk.END, values=proc)

    fen.after(1500, refresh_table)


# ---------------------------------------------------------
#  INTERFACE TKINTER
# ---------------------------------------------------------
fen = tk.Tk()
fen.title("Gestionnaire de scripts Python")

if user_filter:
    tk.Label(fen, text=f"Filtre utilisateur : {user_filter}", fg="blue").pack(pady=5)

colonnes = ("PID", "CPU", "Mémoire", "Durée", "Commande")
table = ttk.Treeview(fen, columns=colonnes, show="headings")

for col in colonnes:
    table.heading(col, text=col,
                  command=lambda c=col: trier_colonne(table, c, False, ["PID"]))
    table.column(col, width=200)

table.pack(fill="both", expand=True)

frame_btn = tk.Frame(fen)
frame_btn.pack(pady=10)

btn_ctrlc = tk.Button(frame_btn, text="Envoyer Ctrl+C", command=envoyer_ctrl_c)
btn_ctrlc.grid(row=0, column=0, padx=10)

btn_kill = tk.Button(frame_btn, text="Tuer le processus", command=tuer_processus, bg="#ff5555")
btn_kill.grid(row=0, column=1, padx=10)

refresh_table()
fen.mainloop()
