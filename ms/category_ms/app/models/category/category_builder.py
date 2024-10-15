from .category_model import Category

class CategoryBuilder:
    def __init__(self, time_category, tyre_type, gender):
        self.time_category = time_category
        self.tyre_type = tyre_type
        self.gender = gender

    def build(self):
        return self.time_category

