from collections import OrderedDict
import datetime
import peewee as pw

db = pw.SqliteDatabase('people.db')
class Person(pw.Model):
    name = pw.CharField()
    birthday = pw.DateField()
    is_relative = pw.BooleanField()

    class Meta:
        database = db

class Pet(pw.Model):
    owner = pw.ForeignKeyField(Person, related_name='pets')
    name = pw.CharField()
    animal_type = pw.CharField()
    
    class Meta:
        database = db

def create_and_connect():
    db.connect()
    db.create_tables([Person,Pet],safe=True)

def menu_loop():
    """Show menu"""
    choice= None 
    while choice !='q':
        print("Press 'q' to quit")
        for key,value in menu.items():
            print("{}){}".format(key,value.__doc__))
        choice = input("Action: ").lower().strip()

        if choice in menu:
            menu[choice]()


def add_person():
    """Agregar una nueva persona."""
    name = input("Nombre de la persona: ")
    birthday = input("Fecha de nacimiento (YYYY-MM-DD): ")
    is_relative_input = input("¿Es un familiar? (s/n): ").lower()
    is_relative = True if is_relative_input == 's' else False

    if name and birthday:
        try:
            birthday = datetime.datetime.strptime(birthday, "%Y-%m-%d").date()
            if input('Guardar persona en la base de datos? [Yn] ').lower() != 'n':
                Person.create(name=name, birthday=birthday, is_relative=is_relative)
                print("Guardado exitosamente!")
        except ValueError:
            print("Fecha inválida. Por favor, introduce la fecha en formato YYYY-MM-DD.")

def view_people(delete=False):
    """Ver todas las personas."""
    entries = Person.select().order_by(Person.birthday.desc())
    for entry in entries:
        print('Nombre: {}'.format(entry.name))
        print('Fecha de Nacimiento: {}'.format(entry.birthday.strftime('%A %B %d, %Y')))
        print('Es Familiar: {}'.format('Sí' if entry.is_relative else 'No'))
        print('\n' + '=' * 40)

        if delete:
            print('n) siguiente persona')
            print('d) borrar persona')
            print('q) volver al menú principal')

            next_action = input('Acción: [Nq] ').lower().strip()
            if next_action == 'q':
                break
            elif next_action == 'd':
                delete_person(entry)
        else:
            input('Presione Enter para continuar...')

def delete_person(entry):
    """Eliminar una persona existente."""
    response = input("¿Estás seguro de que quieres borrar a {}? [yN] ".format(entry.name)).lower()
    if response == 'y':
        entry.delete_instance()
        print("Persona borrada exitosamente.")

menu = OrderedDict([
    ('a', add_person),
    ('v', view_people),
    ('d', delete_person) 
])
if __name__ == "__main__":
    create_and_connect()
    menu_loop()