# **Testare unitara in Python**

## Descriere
Aplicatia reprezinta un sistem de monitorizare a temperaturilor inregistrate de senzorii a 6 frigidere, determinand daca acestea sunt critice sau nu, in functie de un prag de alerta specificat. Sistemul verifica daca numarul de temperaturi este corect, daca pragul de alerta este valid si daca valorile temperaturilor sunt in intervalul permis: [-150, 0] grade.
Daca toate conditiile sunt indeplinite, se returneaza media temperaturilor si numarul de valori critice (temperaturi care depasesc pragul de alerta).


## Specificatiile programului

* aadffv
* defgbb
* hhmjmm


## Configuratie hardware

| Componenta | Descriere |
| :---: | :---: |
| CPU | Intel Core i5 (8th Gen) |
| RAM | 8 GB |
| Storage | 477 GB SSD (NVMe) |
| GPU | Intel (R) UHD Graphics 620 |
| OS | Windows 10 |



## Configuratie Software

| Componenta | Descriere |
| :---: | :---: |
| Limbaj |	Python 3.13.11 |
| IDE | Visual Studio Code |
| Unit Testing |  |
| Version Control |	Git |



## Demo


## Testare Functionala

### 1. Partitionare in clase de echivalenta


Pentru fiecare clasa, se selecteaza un caz reprezentativ, cu presupunerea ca toate valorile din aceeasi clasa vor produce acelasi tip de rezultat.

Se disting urmatoarele clase:

#### Lungimea listei de temperaturi

* **L1**: lungime valida (**exact 6 elemente**)
* **L2**: lungime prea mica (**< 6 elemente**) → mesaj de eroare
* **L3**: lungime prea mare (**> 6 elemente**) → mesaj de eroare

Clasele **L2 si L3** produc acelasi mesaj de eroare, dar sunt pastrate separat deoarece provin din **subdomenii distincte ale spatiului de intrare**.

#### Pragul de alerta

* **A1**: prag valid (**<= -50**)
* **A2**: prag invalid (**> -50**) → mesaj de eroare

#### Valorile temperaturilor

* **T1**: toate temperaturile valide (**-150 <= t <= 0**)
* **T2**: exista cel putin o temperatura prea mica (**t < -150**) → eroare senzor
* **T3**: exista cel putin o temperatura prea mare (**t > 0**) → eroare senzor

---

#### Strategia de alegere a testelor

Conform principiului partitionarii in clase de echivalenta, este suficient sa alegem:

* **cel putin un caz reprezentativ pentru fiecare clasa valida**
* **cel putin un caz reprezentativ pentru fiecare clasa invalida**

---

#### Cazuri de test derivate

| ID Test | Clase acoperite | Intrare               | Rezultat asteptat    |
| ------- | --------------- | --------------------- | -------------------- |
| TST1    | L1, A1, T1      | 6 temperaturi valide  | media + numar critic |
| TST2    | L2              | 5 temperaturi         | eroare lungime       |
| TST3    | L3              | 7 temperaturi         | eroare lungime       |
| TST4    | L1, A2          | prag invalid          | eroare prag          |
| TST5    | L1, A1, T2      | o temperatura < -150 | `Sensor failure!`    |
| TST6    | L1, A1, T3      | o temperatura > 0    | `Sensor failure!`    |
| TST7    | L1, A1, T1      | niciuna critica       | contor = 0           |
| TST8    | L1, A1, T1      | toate critice         | contor = 6           |

---

#### Implementarea testelor în Python

```python
def test_equivalence_partitioning(self):
    # L1, A1, T1 - test valid
    self.assertEqual(
        analyze_status([-80, -60, -70, -80, -90, -100], -72),
        (-80.0, 2)
    )

    # L2 - lungime prea mica
    self.assertEqual(
        analyze_status([-60] * 5, -55),
        "Exactly 6 temperature readings are required"
    )

    # L3 - lungime prea mare
    self.assertEqual(
        analyze_status([-60] * 7, -55),
        "Exactly 6 temperature readings are required"
    )

    # L1, A2 - prag invalid
    self.assertEqual(
        analyze_status([-60] * 6, -40),
        "Alert threshold must be less than or equal to -50"
    )

    # L1, A1, T2 - temperatura prea mica
    self.assertEqual(
        analyze_status([-160, -55, -70, -80, -90, -100], -55),
        "Sensor failure!"
    )

    # L1, A1, T3 - temperatura prea mare
    self.assertEqual(
        analyze_status([-60, 10, -70, -80, -90, -100], -55),
        "Sensor failure!"
    )

    # L1, A1, T1 - nicio temperatura critica
    self.assertEqual(
        analyze_status([-60] * 6, -55),
        (-60.0, 0)
    )

    # L1, A1, T1 - toate temperaturile critice
    self.assertEqual(
        analyze_status([-60] * 6, -70),
        (-60.0, 6)
    )
```

---

### 2. Analiza valorilor de frontiera

Analiza valorilor de frontiera este o tehnica de testare care se concentreaza pe testarea valorilor limita ale domeniului de intrare. Aceasta este importanta deoarece erorile sunt adesea gasite la limitele intervalelor.

Se identifica urmatoarele frontiere:

#### Lungimea listei de temperaturi
- Frontiera inferioara: 5 elemente (invalid)
- Valoarea valida: 6 elemente
- Frontiera superioara: 7 elemente (invalid)

#### Pragul de alerta
- Frontiera inferioara: -51 (valid)
- Valoarea limita: -50 (valid)
- Frontiera superioara: -49 (invalid)

#### Valorile temperaturilor
- Frontiera inferioara a intervalului: -151 (invalid), -150 (valid), -149 (valid)
- Frontiera superioara a intervalului: -1 (valid), 0 (valid), 1 (invalid)

---

#### Cazuri de test pentru analiza valorilor de frontiera

| ID Test | Frontiera testata | Intrare | Rezultat asteptat |
| ------- | ----------------- | ------- | ----------------- |
| BVA1    | Lungime < 6      | 5 temperaturi | eroare lungime |
| BVA2    | Lungime = 6      | 6 temperaturi | media + numar critic |
| BVA3    | Lungime > 6      | 7 temperaturi | eroare lungime |
| BVA4    | Prag = -51       | prag -51 | valid |
| BVA5    | Prag = -50       | prag -50 | valid |
| BVA6    | Prag = -49       | prag -49 | eroare prag |
| BVA7    | Temp = -151      | o temp -151 | eroare senzor |
| BVA8    | Temp = -150      | o temp -150 | valid |
| BVA9    | Temp = -149      | o temp -149 | valid |
| BVA10   | Temp = -1        | o temp -1 | valid |
| BVA11   | Temp = 0         | o temp 0 | valid |
| BVA12   | Temp = 1         | o temp 1 | eroare senzor |

---

#### Implementarea testelor pentru analiza valorilor de frontiera în Python

```python
def test_boundary_values(self):
    # Frontiere lungimea listei
    # Lungime la frontiera inferioara (5 elem)
    self.assertEqual(
        analyze_status([-60] * 5, -55),
        "Exactly 6 temperature readings are required"
    )
    # Lungime la frontiera valida (6 elem)
    self.assertEqual(
        analyze_status([-60] * 6, -55),
        (-60.0, 0)
    )
    # Lungime la frontiera superioara (7 elem)
    self.assertEqual(
        analyze_status([-60] * 7, -55),
        "Exactly 6 temperature readings are required"
    )

    # Frontiere prag de alerta
    # Prag la frontiera inferioara (-51)
    self.assertEqual(
        analyze_status([-60] * 6, -51),
        (-60.0, 0)
    )
    # Prag la frontiera valida (-50)
    self.assertEqual(
        analyze_status([-60] * 6, -50),
        (-60.0, 0)
    )
    # Prag la frontiera superioara (-49)
    self.assertEqual(
        analyze_status([-60] * 6, -49),
        "Alert threshold must be less than or equal to -50"
    )

    # Frontiere valori temperaturi
    # Inceputul intervalului - temp la frontiera inferioara (-151)
    self.assertEqual(
        analyze_status([-151, -60, -70, -80, -90, -100], -55),
        "Sensor failure!"
    )
    # Inceputul intervalului - temp la frontiera valida (-150)
    self.assertEqual(
        analyze_status([-150, -60, -70, -80, -90, -100], -55),
        (-91.67, 0)
    )
    # Inceputul intervalului - temp la frontiera superioara (-149)
    self.assertEqual(
        analyze_status([-149, -60, -70, -80, -90, -100], -55),
        (-91.5, 0)
    )
    # Sfarsitul intervalului - temp la frontiera inferioara (-1)
    self.assertEqual(
        analyze_status([-1, -60, -70, -80, -90, -100], -55),
        (-66.83, 1)
    )
    # Sfarsitul intervalului - temp la frontiera valida (0)
    self.assertEqual(
        analyze_status([0, -60, -70, -80, -90, -100], -55),
        (-66.67, 1)
    )
    # Sfarsitul intervalului - temp la frontiera superioara (1)
    self.assertEqual(
        analyze_status([1, -60, -70, -80, -90, -100], -55),
        "Sensor failure!"
    )
```

---

#### Codul complet al fisierului black_box_tests.py

```python
import unittest
from function import analyze_status

# TESTARE FUNCTIONALA (BLACK BOX TESTING)

class TestBlackBox(unittest.TestCase):

    # partitionare in clase de echivalenta

    """
    1. Lungimea listei de temperaturi
    L1: lungime valida (6 elemente)
    L2: lungime prea mica (<6 elem; returneaza mesaj de eroare)
    L3: lungime prea mare (>6 elem; returneaza mesaj de eroare)

    2. Valoarea pragului de alerta
    A1: prag valid (<= -50)
    A2: prag invalid (> -50; returneaza mesaj de eroare)

    3. Valorile temperaturilor
    T1: toate valorile sunt valide (-150 <= t <= 0)
    T2: cel putin o valoare prea mica (t < -150  returneaza mesaj de eroare)
    T3: cel putin o valoare prea mare (t > 0  returneaza mesaj de eroare)
    
    """

    def test_equivalence_partitioning(self):
        # L1, A1, T1 - test valid
        self.assertEqual(analyze_status([-80, -60, -70, -80, -90, -100], -72), (-80.0, 2))
        
        # L2
        self.assertEqual(analyze_status([-60]*5, -55), "Exactly 6 temperature readings are required")
        # L3
        self.assertEqual(analyze_status([-60]*7, -55), "Exactly 6 temperature readings are required")
        # L1, A2
        self.assertEqual(analyze_status([-60]*6, -40), "Alert threshold must be less than or equal to -50")
        # L1, A1, T2
        self.assertEqual(analyze_status([-160, -55, -70, -80, -90, -100], -55), "Sensor failure!")
        # L1, A1, T3
        self.assertEqual(analyze_status([-60, 10, -70, -80, -90, -100], -55), "Sensor failure!")

        # L1, A1, T1 - nicio temperatura critica
        self.assertEqual(analyze_status([-60]*6, -55), (-60.0, 0))
        # L1, A1, T1 - toate temperaturile sunt critice
        self.assertEqual(analyze_status([-60]*6, -70), (-60.0, 6))

    #analiza valorilor de frontiera

    """
    frontiere lungimea listei: 5, 6, 7
    frontiere prag de alerta: -51, -50, -49
    frontiere valori temperaturi: -151, -150, -149, -1, 0, 1
    
    """

    def test_boundary_values(self):
        # frontiere lungimea listei

        #lungime la frontiera inferioara(5 elem)
        self.assertEqual(analyze_status([-60]*5, -55), "Exactly 6 temperature readings are required")
        #lungime la frontiera valida(6 elem)
        self.assertEqual(analyze_status([-60]*6, -55), (-60.0, 0))
        #lungime la frontiera superioara(7 elem)
        self.assertEqual(analyze_status([-60]*7, -55), "Exactly 6 temperature readings are required")

        # frontiere prag de alerta

        #prag la frontiera inferioara(-51)
        self.assertEqual(analyze_status([-60]*6, -51), (-60.0, 0))
        #prag la frontiera valida(-50)
        self.assertEqual(analyze_status([-60]*6, -50), (-60.0, 0))
        #prag la frontiera superioara(-49)
        self.assertEqual(analyze_status([-60]*6, -49), "Alert threshold must be less than or equal to -50")

        # frontiere valori temperaturi

        #inceputul intervalului - temp la frontiera inferioara(-151)
        self.assertEqual(analyze_status([-151, -60, -70, -80, -90, -100], -55), "Sensor failure!")
        #inceputul intervalului - temp la frontiera inferioara(-150)
        self.assertEqual(analyze_status([-150, -60, -70, -80, -90, -100], -55), (-91.67, 0))
        #inceputul intervalului - temp la frontiera superioara(-149)
        self.assertEqual(analyze_status([-149, -60, -70, -80, -90, -100], -55), (-91.5, 0))
        #sfarsitul intervalului - temp la frontiera inferioara(-1)
        self.assertEqual(analyze_status([-1, -60, -70, -80, -90, -100], -55), (-66.83, 1))
        #sfarsitul intervalului - temp la frontiera superioara(0)
        self.assertEqual(analyze_status([0, -60, -70, -80, -90, -100], -55), (-66.67, 1))
        #sfarsitul intervalului - temp la frontiera superioara(1)
        self.assertEqual(analyze_status([1, -60, -70, -80, -90, -100], -55), "Sensor failure!")


if __name__ == "__main__":
    unittest.main()
```








