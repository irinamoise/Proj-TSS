# Raport_AI

Analiza testelor generate cu **Gemini** versus testele mele din proiect.

##  Prompt initial si rezultate din terminal

### Promptul initial catre Gemini

```text
am un fisier numit function.py cu niste cod pt care trebuie sa creez alte fisiere cu teste unitare white box si black box: partitionare in clase de echivalenta, analiza valorilor de frontiera, acoperire la nivel de instructiune, decizie, conditie, circuite independente, analiza raport creat de generatorul de mutanti, teste suplimentare pentru a omori 2 dintre mutantii neechivalenti ramasi in viata
```
I-am atasat si fisierele cu materia de la curs "Functonal Testing" si "Structural Testing", alaturi de fisierul cu functia "function.py".

###  Cod generat de Gemini pentru AI_black_box.py

```python
import unittest
from function import analyze_status


class TestBlackBox(unittest.TestCase):

   def test_ep_valid_case(self):
      res = analyze_status([-100, -90, -80, -70, -64, -51], -55)
      self.assertEqual(res, (-75.83, 1))

   def test_ep_invalid_length(self):
      res = analyze_status([-60, -70, -80], -50)
      self.assertEqual(res, "Exactly 6 temperature readings are required")

   def test_ep_invalid_threshold(self):
      res = analyze_status([-60, -60, -60, -60, -60, -60], -40)
      self.assertEqual(res, "Alert threshold must be less than or equal to -50")

   def test_ep_invalid_temperature(self):
      res = analyze_status([-60, -60, 20, -60, -60, -60], -50)
      self.assertEqual(res, "Sensor failure!")

   def test_bva_length_boundaries(self):
      self.assertEqual(
         analyze_status([-60] * 5, -50),
         "Exactly 6 temperature readings are required",
      )
      self.assertEqual(
         analyze_status([-60] * 7, -50),
         "Exactly 6 temperature readings are required",
      )

   def test_bva_threshold_boundaries(self):
      self.assertEqual(analyze_status([-60] * 6, -50), (-60.0, 0))
      self.assertEqual(analyze_status([-60] * 6, -51), (-60.0, 0))
      self.assertEqual(
         analyze_status([-60] * 6, -49),
         "Alert threshold must be less than or equal to -50",
      )

   def test_bva_temperature_boundaries(self):
      self.assertEqual(
         analyze_status([-150, 0, -60, -60, -60, -60], -50),
         (-80.0, 1),
      )
      self.assertEqual(
         analyze_status([-151, -60, -60, -60, -60, -60], -50),
         "Sensor failure!",
      )
      self.assertEqual(
         analyze_status([-60, -60, -60, 1, -60, -60], -50),
         "Sensor failure!",
      )


if __name__ == "__main__":
   unittest.main()
```

### Cod generat de Gemini pentru AI_white_box.py

```python
import unittest
from function import analyze_status


class TestWhiteBox(unittest.TestCase):

   def test_statement_coverage(self):
      self.assertEqual(
         analyze_status([], -50), "Exactly 6 temperature readings are required"
      )
      self.assertEqual(
         analyze_status([-60] * 6, -40),
         "Alert threshold must be less than or equal to -50",
      )
      self.assertEqual(
         analyze_status([-60, 10, -60, -60, -60, -60], -50), "Sensor failure!"
      )
      self.assertEqual(
         analyze_status([-65, -60, -58, -40, -70, -90], -55),
         (-63.83, 4),
      )

   def test_decision_coverage(self):
      self.assertEqual(
         analyze_status([0], -50), "Exactly 6 temperature readings are required"
      )
      self.assertEqual(
         analyze_status([-60] * 6, -10),
         "Alert threshold must be less than or equal to -50",
      )
      self.assertEqual(
         analyze_status([-200, -60, -60, -60, -60, -60], -50), "Sensor failure!"
      )
      self.assertEqual(
         analyze_status([-60, -60, -45, -45, -60, -60], -50),
         (-55.0, 2),
      )

   def test_condition_coverage(self):
      analyze_status([-200, -60, -60, -60, -60, -60], -50)
      analyze_status([5, -60, -60, -60, -60, -60], -50)
      self.assertEqual(analyze_status([-60] * 6, -55), (-60.0, 6))

   def test_circuit_1_len_invalid(self):
      self.assertEqual(
         analyze_status([], -50), "Exactly 6 temperature readings are required"
      )

   def test_circuit_2_threshold_invalid(self):
      self.assertEqual(
         analyze_status([-60] * 6, 0),
         "Alert threshold must be less than or equal to -50",
      )

   def test_circuit_3_sensor_failure_low(self):
      self.assertEqual(
         analyze_status([-160, -60, -60, -60, -60, -60], -50), "Sensor failure!"
      )

   def test_circuit_4_sensor_failure_high(self):
      self.assertEqual(
         analyze_status([10, -60, -60, -60, -60, -60], -50), "Sensor failure!"
      )

   def test_circuit_5_no_critical_temperatures(self):
      self.assertEqual(
         analyze_status([-60, -70, -80, -90, -100, -110], -50),
         (-85.0, 0),
      )

   def test_circuit_6_with_critical_temperatures(self):
      self.assertEqual(
         analyze_status([-55, -51, -60, -70, -80, -90], -55),
         (-67.67, 1),
      )


if __name__ == "__main__":
   unittest.main()
```

### Rezultate din terminal la rularea scripturilor generate

#### Rulare AI_black_box.py

```text
FAIL: test_bva_temperature_boundaries (__main__.TestBlackBox.test_bva_temperature_boundaries)
Frontiere valori temperaturi: -151 (inv), -150 (val), 0 (val), 1 (inv).
----------------------------------------------------------------------
Traceback (most recent call last):
   File "C:\Users\IRINA\proiect TSS\AI_black_box.py", line 68, in test_bva_temperature_boundaries
      self.assertEqual(analyze_status([-150, 0, -60, -60, -60, -60], -50), (-80.0, 1))
AssertionError: Tuples differ: (-65.0, 1) != (-80.0, 1)

First differing element 0:
-65.0
-80.0

----------------------------------------------------------------------
Ran 7 tests in 0.003s

FAILED (failures=1)
```

#### Rulare AI_white_box.py

```text
FAIL: test_condition_coverage (__main__.TestWhiteBox.test_condition_coverage)
Fiecare conditie elementara din deciziile compuse trebuie sa fie True si False.
----------------------------------------------------------------------
Traceback (most recent call last):
   File "C:\Users\IRINA\proiect TSS\AI_white_box.py", line 68, in test_condition_coverage
      self.assertEqual(analyze_status([-60]*6, -55), (-60.0, 6))
AssertionError: Tuples differ: (-60.0, 0) != (-60.0, 6)

======================================================================
FAIL: test_statement_coverage (__main__.TestWhiteBox.test_statement_coverage)
Trebuie sa executam fiecare linie de cod cel putin o data.
----------------------------------------------------------------------
Traceback (most recent call last):
   File "C:\Users\IRINA\proiect TSS\AI_white_box.py", line 23, in test_statement_coverage
      self.assertEqual(analyze_status([-65, -60, -58, -40, -70, -90], -55), (-63.83, 4))
AssertionError: Tuples differ: (-63.83, 1) != (-63.83, 4)

----------------------------------------------------------------------
Ran 9 tests in 0.006s

FAILED (failures=2)
```



1. In `AI_black_box.py`, cazul cu `[-150, 0, -60, -60, -60, -60]` asteapta media `-80.0`, dar calculul corect este `-65.0`.
2. In `AI_white_box.py`, pentru `[-60] * 6` si prag `-55`, testul asteapta `6` valori critice, dar functia foloseste conditia stricta `t > alert_threshold`, deci rezultatul corect este `0`.
3. In `AI_white_box.py`, testul de statement coverage asteapta `critical_count = 4`, dar doar `-40 > -55` este adevarat, deci corect este `1`.

## 1. Introducere

Testele din `cod_AI.txt` au fost generate cu ajutorul Gemini (Google AI). Acest raport compara testele generate automat cu testele din `black_box_tests.py` si `white_box_tests.py`, urmarind diferente de acoperire, logica si valori asteptate.

## 2. Comparatie pe categorii de teste (Gemini vs testele mele)

### 2.1 Equivalence Partitioning

| Aspect | Teste AI (Gemini) | Testele mele (`black_box_tests.py`) | Diferenta |
|--------|-------------------|--------------------------------------|-----------|
| Caz valid | include caz valid | include caz valid (`[-80,-60,-70,-80,-90,-100], -72 -> (-80.0, 2)`) | Ambele au clasa valida, cu date diferite |
| Lungime invalida | da | da (lungime 5 si 7) | Compatibil |
| Prag invalid | da | da | Compatibil |
| Temperatura invalida | da | da (sub -150 si peste 0) | Compatibil |
| Outputuri O1/O2/O3 | partial | explicit O1 si O3 in acelasi test | Testele mele documenteaza mai clar clasele de output |

### 2.2 Boundary Value Analysis (BVA)

| Aspect | Teste AI (Gemini) | Testele mele (`black_box_tests.py`) | Diferenta |
|--------|-------------------|--------------------------------------|-----------|
| Frontiera lungime 5/6/7 | da | da | Compatibil |
| Frontiera prag | -51, -50, -49 | -50.0001, -50.0, -49.9999 | Testele mele verifica mai fin frontiera numerica |
| Frontiera temperatura | -151, -150, 0, 1 | -150.0001, -150.0, -149.9999, -0.0001, 0.0, 0.0001 | Testele mele au granularitate mai buna |
| Asteptare numerica cheie | `(-80.0, 1)` pentru `[-150,0,-60,-60,-60,-60]` | nu folosesc acel caz; valorile mele sunt coerente (`(-91.67,0)`, `(-66.67,1)`) | AI are eroare de calcul in acest punct |

### 2.3 Statement Coverage

| Aspect | Teste AI (Gemini) | Testele mele (`white_box_tests.py`) | Diferenta |
|--------|-------------------|--------------------------------------|-----------|
| Lungime invalida | da | da | Compatibil |
| Prag invalid | da | da | Compatibil |
| Sensor failure | da | da | Compatibil |
| Caz valid cu increment critic | asteapta `(-63.83, 4)` | folosesc `[-60]*6, -70 -> (-60.0, 6)` | AI are asteptare gresita la `critical_count` |

### 2.4 Branch Coverage

| Aspect | Teste AI (Gemini) | Testele mele (`white_box_tests.py`) | Diferenta |
|--------|-------------------|--------------------------------------|-----------|
| Decizia len != 6 (T/F) | da | da | Compatibil |
| Decizia prag > -50 (T/F) | da | da | Compatibil |
| Ramura interval temperatura valid/invalida | da | da | Compatibil |
| Ramura `t > alert_threshold` (T/F) | da | da (exemplu `[-59,-61,-60,-60,-60,-60], -60 -> (-60.0, 1)`) | La AI, explicatiile duc uneori la interpretare gresita a comparatiei strict `>` |

### 2.5 Condition Coverage

| Aspect | Teste AI (Gemini) | Testele mele (`white_box_tests.py`) | Diferenta |
|--------|-------------------|--------------------------------------|-----------|
| C1: len != 6 | acoperita | acoperita | Compatibil |
| C2: prag > -50 | acoperita | acoperita | Compatibil |
| C4/C5: `t >= -150` si `t <= 0` | acoperite | acoperite | Compatibil |
| C6: `t > alert_threshold` | asteapta `(-60.0, 6)` pentru `[-60]*6, -55` | valideaza prin cazuri cu 1 critic sau 0 critici reale | AI confunda `>` cu `>=` |

### 2.6 Circuit Coverage / Independent Paths

| Aspect | Teste AI (Gemini) | Testele mele (`white_box_tests.py`) | Diferenta |
|--------|-------------------|--------------------------------------|-----------|
| Numar cai independente | 6 | 6 | Compatibil |
| Calea eroare lungime | da | da | Compatibil |
| Calea eroare prag | da | da | Compatibil |
| Calea iteratie for fara critic | da | da (`[-61,-60,-60,-60,-60,-60], -60 -> (-60.17, 0)`) | Compatibil |
| Calea iteratie for cu critic | da | da (`[-30]*6, -60 -> (-30.0, 6)`) | Compatibil |
| Calea senzor invalid | da | da | Compatibil |



## 3. Rezumat diferente AI vs testele mele

1. Structura de acoperire este in mare parte similara: AI si testele mele acopera EP, BVA, statement, branch, condition si cai independente.
2. Testele mele sunt mai precise la frontiere numerice (ex: -50.0001 / -49.9999, -150.0001 / -149.9999 / -0.0001 / 0.0001).
3. Principalele erori in testele AI sunt in valorile asteptate (aritmetica si interpretarea lui `t > alert_threshold`), in timp ce testele mele au asteptari consistente cu executia.


---

## 4. Constatari finale

Per total, testele AI au acoperire buna ca intentie, dar testele mele sunt mai riguroase pe frontiere si mai corecte pe valorile asteptate.


