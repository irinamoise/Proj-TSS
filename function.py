import unittest

"""
    Functia analizeaza temperaturile inregistrate de senzorii a 6 frigidere si determina daca acestea sunt critice sau nu, 
    in functie de un prag de alerta specificat. Functia verifica daca numarul de temperaturi este corect,
    daca pragul de alerta este valid si daca valorile temperaturilor sunt in intervalul permis (-150, 0 grade).
    Daca toate conditiile sunt indeplinite, functia calculeaza media temperaturilor si 
    numarul de valori critice (temperaturi care depasesc pragul de alerta) si le returneaza.

    Parametri:
    - temperatures: o lista de 6 valori de temperatura inregistrate de senzorii frigiderelor
    - alert_threshold: un prag de alerta specificat pentru a determina daca o temperatura este critica sau nu

    Returneaza:
    - average: media temperaturilor inregistrate
    - critical_count: numarul de valori critice (temperaturi care depasesc pragul de alerta)
    - mesaje de eroare in cazul in care conditiile nu sunt indeplinite (numar incorect de temperaturi, 
    prag de alerta invalid, valori de temperatura invalide)
  
 
"""

def analyze_status(temperatures, alert_threshold):

    if len(temperatures) != 6:                                      #1
        return "Exactly 6 temperature readings are required"        #2

    # conditie compusa
    if alert_threshold > -50:                                       #3
        return "Alert threshold must be less than or equal to -50"  #4

    sum = 0                                                         #5
    critical_count = 0                                              #6

    # instructiune repetitiva( for)
    for t in temperatures:                                          #7

        # conditionala cu else
        #verificam daca temperatura este in intervalul valid
        if t >= -150 and t <= 0:                                    #8
           sum += t                                                 #9  
           if t > alert_threshold:                                  #10
            #incrementam numarul de valori critice (temperaturi care depasesc pragul de alerta)
            critical_count += 1                                     #11
        else:                                                       #12
            return "Sensor failure!"                                #13
        

    average = round(                                                #15
       sum / len(temperatures), 2)                                  #14
    return average, critical_count                                  #16

# if __name__ == "__main__":
#     # Test cases
#     print(analyze_status([-60, -55, -70, -80, -90, -100], -50))  # Valid case
#     print(analyze_status([-60, -55, -70, -80, -90], -50))       # Invalid case: not enough temperatures
#     print(analyze_status([-60, -55, -70, -80, -90, -100], -40)) # Invalid case: alert threshold too high
#     print(analyze_status([-60, -55, -70, 10, -90, -100], -50))  # Invalid case: sensor failure