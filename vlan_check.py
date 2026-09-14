# vlan_check.py
vlan = int(input("Ingrese el número de VLAN: "))

if 1 <= vlan <= 1005:
    print(f"La VLAN {vlan} corresponde a un rango normal.")
elif 1006 <= vlan <= 4094:
    print(f"La VLAN {vlan} corresponde a un rango extendido.")
else:
    print(f"El número {vlan} no corresponde a una VLAN válida.")
