"""Convertisseur de nombres en toutes lettres (français) - application PyQt5."""

import sys

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QLineEdit, QTextEdit, QPushButton, QCheckBox)
from PyQt5.QtGui import QFont

# ---------------------------------------------------------------------------
# Conversion nombre -> lettres
# ---------------------------------------------------------------------------

UNITES = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept",
          "huit", "neuf", "dix", "onze", "douze", "treize", "quatorze",
          "quinze", "seize"]
DIZAINES = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante", 6: "soixante"}


def moins_de_100(n, final=True):
    if n < 17:
        return UNITES[n]
    if n < 20:
        return "dix-" + UNITES[n - 10]
    if n < 70:
        d, u = divmod(n, 10)
        if u == 0:
            return DIZAINES[d]
        if u == 1:
            return DIZAINES[d] + " et un"
        return DIZAINES[d] + "-" + UNITES[u]
    if n < 80:                       # 70 à 79
        if n == 71:
            return "soixante et onze"
        return "soixante-" + moins_de_100(n - 60)
    if n == 80:                      # 80 à 99
        return "quatre-vingts" if final else "quatre-vingt"
    return "quatre-vingt-" + moins_de_100(n - 80)


def moins_de_1000(n, final=True):
    c, r = divmod(n, 100)
    if c == 0:
        return moins_de_100(r, final)
    texte = "cent" if c == 1 else UNITES[c] + " cent"
    if r == 0:
        return texte + ("s" if c > 1 and final else "")
    return texte + " " + moins_de_100(r, final)


def entier_en_lettres(n):
    if n == 0:
        return "zéro"
    if n < 0:
        return "moins " + entier_en_lettres(-n)
    if n >= 10**12:
        raise ValueError("Nombre trop grand (maximum : 999 999 999 999)")

    parties = []
    for valeur, nom in ((10**9, "milliard"), (10**6, "million")):
        q, n = divmod(n, valeur)
        if q:
            parties.append(moins_de_1000(q) + " " + nom + ("s" if q > 1 else ""))
    q, n = divmod(n, 1000)
    if q:
        parties.append("mille" if q == 1 else moins_de_1000(q, final=False) + " mille")
    if n:
        parties.append(moins_de_1000(n))
    return " ".join(parties)


def convertir(nombre):
    """Accepte un int, un float ou une chaîne ('12', '3,14', '-7')."""
    s = str(nombre).strip().replace(",", ".")
    signe = ""
    if s.startswith("-"):
        signe, s = "moins ", s[1:]
    entier, _, dec = s.partition(".")
    texte = signe + entier_en_lettres(int(entier or 0))
    if dec:
        zeros = len(dec) - len(dec.lstrip("0"))
        morceaux = ["zéro"] * zeros
        if dec.strip("0"):
            morceaux.append(entier_en_lettres(int(dec)))
        texte += " virgule " + " ".join(morceaux)
    return texte


# ---------------------------------------------------------------------------
# Interface graphique
# ---------------------------------------------------------------------------

class Fenetre(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nombre en lettres")
        self.resize(520, 340)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Entrez un nombre :"))
        self.champ = QLineEdit()
        self.champ.setFont(QFont("Arial", 16))
        self.champ.setPlaceholderText("ex : 1250 ou 3,14")
        self.champ.textChanged.connect(self.mettre_a_jour)
        layout.addWidget(self.champ)

        self.majuscule = QCheckBox("Première lettre en majuscule")
        self.majuscule.stateChanged.connect(self.mettre_a_jour)
        layout.addWidget(self.majuscule)

        layout.addWidget(QLabel("En toutes lettres :"))
        self.resultat = QTextEdit()
        self.resultat.setReadOnly(True)
        self.resultat.setFont(QFont("Arial", 14))
        layout.addWidget(self.resultat)

        self.bouton = QPushButton("Copier le résultat")
        self.bouton.clicked.connect(self.copier)
        layout.addWidget(self.bouton)

    def mettre_a_jour(self):
        saisie = self.champ.text().replace(" ", "")
        if not saisie:
            self.resultat.clear()
            return
        try:
            texte = convertir(saisie)
            if self.majuscule.isChecked():
                texte = texte[0].upper() + texte[1:]
            self.resultat.setPlainText(texte)
        except ValueError:
            self.resultat.setPlainText("⚠ Nombre invalide ou trop grand")

    def copier(self):
        QApplication.clipboard().setText(self.resultat.toPlainText())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = Fenetre()
    fenetre.show()
    sys.exit(app.exec_())