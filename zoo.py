class Zoo:
    def __init__(self, name="Gembira Loka Zoo"):
        self.name = name
        self.animals = []
    
    def add_animal(self, animal_name, animal_type):
        #Tambah hewan ke kebun binatang.
        if not animal_name or not animal_type:
            raise ValueError("Nama dan jenis hewan harus diisi")
        
        animal = {
            'name': animal_name,
            'type': animal_type
        }
        self.animals.append(animal)
        return animal
    
    def count_animals(self):
        #Hitung total hewan - helper function untuk testing.
        return len(self.animals)
    
    def is_animal_exists(self, animal_name):
        #Cek apakah hewan ada - helper function untuk testing.
        for animal in self.animals:
            if animal['name'] == animal_name:
                return True
        return False