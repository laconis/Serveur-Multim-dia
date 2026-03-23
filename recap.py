import subprocess

def lancer_scripts_depuis_fichier(fichier, script):
    processus = []

    with open(fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne:
                continue

            # Découpe les arguments
            args = ligne.split()

            # Lance le script avec les arguments
            p = subprocess.Popen(["python", script] + args)
            processus.append((p.pid, ligne))

            print(f"Lancé : python {script} {ligne}  (PID {p.pid})")

    return processus


# Exemple d'utilisation
processus_lances = lancer_scripts_depuis_fichier("params.txt", "worker.py")
