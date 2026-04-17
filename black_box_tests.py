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

        #prag la frontiera inferioara(-50.0001)
        self.assertEqual(analyze_status([-60]*6, -50.0001), (-60.0, 0))
        #prag la frontiera valida(-50.0)
        self.assertEqual(analyze_status([-60]*6, -50.0), (-60.0, 0))
        #prag la frontiera superioara(-49.9999)
        self.assertEqual(analyze_status([-60]*6, -49.9999), "Alert threshold must be less than or equal to -50")

        # frontiere valori temperaturi

        #inceputul intervalului - temp la frontiera inferioara(-150.0001)
        self.assertEqual(analyze_status([-150.0001, -60, -70, -80, -90, -100], -55), "Sensor failure!")
        #inceputul intervalului - temp la frontiera valida(-150.0)
        self.assertEqual(analyze_status([-150.0, -60, -70, -80, -90, -100], -55), (-91.67, 0))
        #inceputul intervalului - temp la frontiera superioara(-149.9999)
        self.assertEqual(analyze_status([-149.9999, -60, -70, -80, -90, -100], -55), (-91.67, 0))
        #sfarsitul intervalului - temp la frontiera inferioara(-0.0001)
        self.assertEqual(analyze_status([-0.0001, -60, -70, -80, -90, -100], -55), (-66.67, 1))
        #sfarsitul intervalului - temp la frontiera valida(0.0)
        self.assertEqual(analyze_status([0.0, -60, -70, -80, -90, -100], -55), (-66.67, 1))
        #sfarsitul intervalului - temp la frontiera superioara(0.0001)
        self.assertEqual(analyze_status([0.0001, -60, -70, -80, -90, -100], -55), "Sensor failure!")


if __name__ == "__main__":
    unittest.main()