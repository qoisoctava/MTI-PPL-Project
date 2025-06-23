import pytest
from zoo import Zoo

class TestAddAnimal:
    
    # @DataPoints equivalent - Fixture untuk data test
    @pytest.fixture
    def zoo(self):
        #Buat kebun binatang baru untuk setiap test.
        return Zoo("Test Zoo")
    
    @pytest.fixture
    def sample_animals(self):
        #Data hewan contoh untuk testing.
        return [
            {'name': 'Simba', 'type': 'Singa'},
            {'name': 'Dumbo', 'type': 'Gajah'},
            {'name': 'Koko', 'type': 'Monyet'},
            {'name': 'Nemo', 'type': 'Ikan'},
        ]
    
    # @Test equivalent - Test individual
    def test_add_single_animal(self, zoo):
        """Test menambah satu hewan."""
        animal = zoo.add_animal("Simba", "Singa")
        
        # Assertions untuk memverifikasi hasil
        assert animal['name'] == "Simba"
        assert animal['type'] == "Singa"
        assert zoo.count_animals() == 1
        assert zoo.is_animal_exists("Simba") == True
    
    # @Parameters equivalent - Test dengan banyak data
    @pytest.mark.parametrize("animal_name,animal_type,expected_count", [
        ("Simba", "Singa", 1),
        ("Dumbo", "Gajah", 1),
        ("Koko", "Monyet", 1),
        ("Nemo", "Ikan", 1),
        ("Raja", "Harimau", 1),
    ])
    def test_add_different_animals(self, zoo, animal_name, animal_type, expected_count):
        """Test menambah berbagai jenis hewan."""
        animal = zoo.add_animal(animal_name, animal_type)
        
        # Verifikasi animal object
        assert animal['name'] == animal_name
        assert animal['type'] == animal_type
        
        # Verifikasi state zoo
        assert zoo.count_animals() == expected_count
        assert zoo.is_animal_exists(animal_name) == True
    
    # @Parameters untuk test error handling
    @pytest.mark.parametrize("animal_name,animal_type,expected_error", [
        ("", "Singa", "Nama dan jenis hewan harus diisi"),
        ("Simba", "", "Nama dan jenis hewan harus diisi"),
        (None, "Singa", "Nama dan jenis hewan harus diisi"),
        ("Simba", None, "Nama dan jenis hewan harus diisi"),
    ])
    def test_add_animal_validation(self, zoo, animal_name, animal_type, expected_error):
        """Test validasi input saat menambah hewan."""
        with pytest.raises(ValueError, match=expected_error):
            zoo.add_animal(animal_name, animal_type)
        
        # Pastikan tidak ada hewan yang ditambahkan saat error
        assert zoo.count_animals() == 0
    
    # Test menggunakan sample_animals fixture
    def test_add_animals(self, zoo, sample_animals):
        """Test menambah beberapa hewan menggunakan fixture data."""
        # Tambah semua hewan dari fixture
        for animal_data in sample_animals:
            result = zoo.add_animal(animal_data['name'], animal_data['type'])
            assert result['name'] == animal_data['name']
            assert result['type'] == animal_data['type']
        
        # Verifikasi total hewan
        assert zoo.count_animals() == len(sample_animals)
        
        # Verifikasi semua hewan ada
        for animal_data in sample_animals:
            assert zoo.is_animal_exists(animal_data['name']) == True
    
    # Test kombinasi fixture + parametrize
    @pytest.mark.parametrize("extra_animal", [
        ("Leo", "Singa"),
        ("Jumbo", "Gajah"),
        ("Coco", "Monyet"),
    ])
    def test_add_animal_after_fixture_data(self, zoo, sample_animals, extra_animal):
        """Test menambah hewan tambahan setelah menggunakan fixture data."""
        # Setup: tambah hewan dari fixture
        for animal_data in sample_animals:
            zoo.add_animal(animal_data['name'], animal_data['type'])
        
        initial_count = zoo.count_animals()
        
        # Test: tambah hewan tambahan
        name, type_animal = extra_animal
        result = zoo.add_animal(name, type_animal)
        
        # Verify
        assert result['name'] == name
        assert result['type'] == type_animal
        assert zoo.count_animals() == initial_count + 1
        assert zoo.is_animal_exists(name) == True

# Test class tambahan untuk demonstrasi variasi
# class TestAddAnimalEdgeCases:
    
    @pytest.fixture
    def zoo(self):
        """Zoo fixture untuk edge cases."""
        return Zoo("Edge Case Zoo")
    
    def test_add_animal_with_special_characters(self, zoo):
        """Test menambah hewan dengan karakter khusus."""
        animal = zoo.add_animal("King Kong Jr.", "Gorila")
        assert animal['name'] == "King Kong Jr."
        assert animal['type'] == "Gorila"
    
    @pytest.mark.parametrize("name,animal_type", [
        ("A", "B"),  # Nama sangat pendek
        ("Supercalifragilisticexpialidocious", "Dinosaurus"),  # Nama sangat panjang
        ("123", "Robot"),  # Nama dengan angka
    ])
    def test_add_animal_boundary_cases(self, zoo, name, animal_type):
        """Test edge cases untuk nama dan tipe hewan."""
        animal = zoo.add_animal(name, animal_type)
        assert animal['name'] == name
        assert animal['type'] == animal_type
        assert zoo.count_animals() == 1