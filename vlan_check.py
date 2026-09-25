print("Nombre Completo: Luis Palacios")
print("RUT: 17.194.070-2")

vlan = int(input("Ingrese el número de VLAN: "))

if 1 <= vlan <= 1005:
    print(f"La VLAN {vlan} corresponde a un rango normal.")
elif 1006 <= vlan <= 4094:
    print(f"La VLAN {vlan} corresponde a un rango extendido.")
else:
    print(f"La VLAN {vlan} no corresponde a una VLAN válida.")


