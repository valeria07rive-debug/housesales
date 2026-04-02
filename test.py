from db import add_property, get_properties

# agregar una propiedad
add_property("Casa en Naco", "Naco", "house", 100000, "available", "bonita")

# mostrar todas las propiedades
print(get_properties())

