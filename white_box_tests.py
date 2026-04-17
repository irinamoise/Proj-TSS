import unittest
from function import analyze_status

#TESTARE STRUCTURALA (WHITE BOX TESTING)

class TestWhiteBox(unittest.TestCase):

    #acoperire la nivel de instructiune

    def test_statement_coverage(self):

        # instruct 1, 2 <-- lungime lista invalida
        self.assertEqual(analyze_status([-60]*5, -55), "Exactly 6 temperature readings are required")
        
        # (1), 3, 4 <-- prag de alerta invalid
        self.assertEqual(analyze_status([-60]*6, -40), "Alert threshold must be less than or equal to -50")

        # (1, 3), 5, 6, 7, 8, 9, 10, 11, 14, 15, 16 <-- returneaza media si numarul de valori critice
        self.assertEqual(analyze_status([-60]*6, -70), (-60.0, 6))
        
        # (1, 3, 5, 6, 7, 8), 12, 13 <-- temperatura invalida
        self.assertEqual(analyze_status([-160, -55, -70, -80, -90, -100], -55), "Sensor failure!")
        
    # acoperire la nivel de ramura (decizie)

    """

    decizii:

        1. if len(temperatures) != 6                                
        2. if alert_threshold > -50         
        3. for t in temperatures                                     
        4. if t >= -150 and t <= 0                                                                
        5. if t > alert_threshold        
    
    """   
                             

    def test_branch_coverage(self):

        # decizia 1 adevarata:  1 --> 2
        self.assertEqual(analyze_status([-60]*5, -55) , "Exactly 6 temperature readings are required")

        # decizia 1 falsa, decizia 2 adevarata: ramura 1 --> 3 --> 4
        self.assertEqual(analyze_status([-60]*6, -40), "Alert threshold must be less than or equal to -50")
        
        # decizia 1 falsa, decizia 2 falsa, decizia 3 adevarata de 6 ori, apoi falsa, decizia 4 adevarata, 
        # decizia 5 adevarata prima oara, apoi falsa: ramura 1 -- 3 --> 5--> 6 --> 7 --> 8--> 9 --> 10 --> 11 --> 14 --> 15 --> 16
        self.assertEqual(analyze_status([-59, -61, -60, -60, -60, -60], -60), (-60.0, 1))

        # decizia 1 falsa, decizia 2 falsa, decizia 3 adevarata o data, decizia 4 falsa: ramura 1 -- 3 -- 5 -- 6 -- 7 -- 8 --> 12 --> 13
        self.assertEqual(analyze_status([-160, -100, -70, -80, -90, -100], -55), "Sensor failure!")



    #acoperire la nivel de conditie

    """

                decizii                                     conditii            
    
        1. if len(temperatures) != 6                    1. len(temperatures) != 6        
        2. if alert_threshold > -50                     2. alert_threshold > -50
        3. for t in temperatures                        3. t in temperatures (indicele lui t < 6)
        4. if t >= -150 and t <= 0                      4. t >= -150           5. t <= 0                      
        5. if t > alert_threshold                       6. t > alert_threshold
    
    """   

    def test_condition_coverage(self):

        # conditia 1 adevarata 
        self.assertEqual(analyze_status([-60]*5, -55) , "Exactly 6 temperature readings are required")

        # conditia 1 falsa, conditia 2 adevarata
        self.assertEqual(analyze_status([-60]*6, -40), "Alert threshold must be less than or equal to -50")

        # _ , _ , conditia 3 adevarata de 6 ori, apoi falsa, conditia 4 adevarata, coditia 5 adevarata, 
        # conditia 6 adevarata prima oara, apoi falsa 
        self.assertEqual(analyze_status([-59, -61, -60, -60, -60, -60], -60), (-60.0, 1))

        # _, _, conditia 3 adevarata o data, conditia 4 falsa 
        self.assertEqual(analyze_status([-160, -61, -60, -60, -60, -60], -60), "Sensor failure!")

        # _, _, conditia 3 adevarata o data, conditia 4 adevarata, conditia 5 falsa
        self.assertEqual(analyze_status([10, -61, -60, -60, -60, -60], -60), "Sensor failure!")


    # circuite independente

    """
    identifica setul de bază de căi liniar independente

    conform grafului control flow, la care adaugam muchii de la
    nodurile finale (2), (4), (12, 13), (16) la nodul de start (1) pentru a obtine 
    un graf complet conectat, avem:
    n= 13 noduri
    e = 18 muchii

    V(G) = e - n + 1 =  18 - 13 + 1 = 6
    deci avem 6 circuite independente:
        1 (eroare lungime): 1 --> 2 --> 1
        2 (eroare prag alerta): 1 --> 3 --> 4 --> 1
        3 (iteratie in for - temperatura <= prag alerta): 7 --> 8 --> 9 --> 10 --> 7
        4 (iteratie in for - temperatura > prag alerta): 7 --> 8 --> 9 --> 10 --> 11 --> 7
        5 (returneaza valori valide): 1 --> 3 --> 5,6 --> 7 --> 14, 15 --> 16 --> 1
        6 (eroare senzor): 1 --> 3 --> 5,6 --> 7 --> 8 --> 12,13 --> 1
        
    """


    def test_independent_paths(self):

        # Calea 1 (Eroare Lungime): 1 --> 2 --> EXIT
        self.assertEqual(analyze_status([-60]*5, -55) , "Exactly 6 temperature readings are required")

        # Calea 2 (Eroare Prag): 1 --> 3 --> 4 --> EXIT
        self.assertEqual(analyze_status([-60]*6, -40), "Alert threshold must be less than or equal to -50")

        # Calea 3 (iteratie in for - temperatura <= prag alerta): 7 --> 8 --> 9 --> 10 --> 7
        self.assertEqual(analyze_status([-61, -60, -60, -60, -60, -60], -60), (-60.17, 0))

        # Calea 4(iteratie in for - temperatura > prag alerta): 7 --> 8 --> 9 --> 10 --> 11 --> 7
        self.assertEqual(analyze_status([-30]*6, -60), (-30.0, 6))

        # Calea 5 (returneaza valori valide): 1 --> 3 --> 5,6 --> 7 --> 14, 15 --> 16 --> EXIT
        self.assertEqual(analyze_status([-59, -61, -60, -60, -60, -60], -60), (-60.0, 1))

         # Calea 6 (Eroare Senzor): 1 --> 3 --> 5,6 --> 7 --> 8 --> 12,13 --> EXIT
        self.assertEqual(analyze_status([-160, -61, -60, -60, -60, -60], -60), "Sensor failure!")






        
if __name__ == "__main__":
    unittest.main()