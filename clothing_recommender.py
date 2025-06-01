import random

class Wardrobe:
    def __init__(self):
        self.wardrobe = {
            'base_layers': ['t-shirt', 'tank top', 'thermal shirt'],
            'mid_layers': ['hoodie', 'sweater', 'flannel shirt'],
            'outerwear': {
                'cold': ['winter coat', 'parka'],
                'rain': ['raincoat', 'poncho'],
                'wind': ['windbreaker'],
                'mild': ['denim jacket', 'light jacket']
            },
            'bottoms': {
                'cold': ['thermal pants', 'jeans'],
                'mild': ['chinos', 'trousers'],
                'hot': ['shorts', 'linen pants']
            },
            'footwear': {
                'rain': ['rain boots'],
                'snow': ['insulated boots'],
                'hot': ['sandals', 'sneakers'],
                'mild': ['casual shoes', 'sneakers']
            },
            'accessories': {
                'cold': ['beanie', 'gloves', 'scarf'],
                'sunny': ['sunglasses', 'cap'],
                'rain': ['umbrella']
            }
        }

class Recommender:
    def __init__(self, wardrobe: Wardrobe, preferences: dict = None):
        self.wardrobe = wardrobe.wardrobe
        self.preferences = preferences if preferences else {
            "style_preferences": [],
            "avoid_items": [],
            "must_have": []
        }

    def categorize_temperature(self, temp_fahrenheit):
        if temp_fahrenheit <= 32:
            return 'freezing'
        elif temp_fahrenheit <= 50:
            return 'cold'
        elif temp_fahrenheit <= 65:
            return 'cool'
        elif temp_fahrenheit <= 79:
            return 'mild'
        else:
            return 'hot'

    def _filter_items(self, items):
        return [item for item in items if item not in self.preferences['avoid_items']]

    def _pick_item(self, items, fallback=None):
        filtered = self._filter_items(items)
        if not filtered:
            return fallback
        # Prefer must-have if available
        for item in self.preferences['must_have']:
            if item in filtered:
                return item
        return random.choice(filtered)

    def recommend(self, weather: str, temperature_f: float):
        weather = weather.lower()
        temp_category = self.categorize_temperature(temperature_f)
        outfit_parts = []

        # Base layer
        base = self._pick_item(self.wardrobe['base_layers'])
        if base:
            outfit_parts.append(f"Base layer: {base}")

        # Mid-layer for cool/cold/freezing
        if temp_category in ['cool', 'cold', 'freezing']:
            mid = self._pick_item(self.wardrobe['mid_layers'])
            if mid:
                outfit_parts.append(f"Mid layer: {mid}")

        # Outerwear
        outerwear = None
        accessories = []

        if weather in ['rain', 'drizzle', 'thunderstorm']:
            outerwear = self._pick_item(self.wardrobe['outerwear']['rain'])
            umbrella = self._pick_item(self.wardrobe['accessories']['rain'])
            if umbrella:
                accessories.append(umbrella)
        elif weather == 'snow':
            outerwear = self._pick_item(self.wardrobe['outerwear']['cold'])
        elif temp_category in ['cold', 'freezing']:
            outerwear = self._pick_item(self.wardrobe['outerwear']['cold'])
            accessories += self._filter_items(self.wardrobe['accessories']['cold'])
        elif temp_category == 'cool':
            outerwear = self._pick_item(self.wardrobe['outerwear']['mild'])

        if outerwear:
            outfit_parts.append(f"Outerwear: {outerwear}")

        # Bottoms
        bottom = None
        if temp_category in ['freezing', 'cold']:
            bottom = self._pick_item(self.wardrobe['bottoms']['cold'])
        elif temp_category == 'cool':
            bottom = self._pick_item(self.wardrobe['bottoms']['mild'])
        else:
            bottom = self._pick_item(self.wardrobe['bottoms']['hot'])

        if bottom:
            outfit_parts.append(f"Bottom: {bottom}")

        # Footwear
        footwear = None
        if weather in ['rain', 'drizzle']:
            footwear = self._pick_item(self.wardrobe['footwear']['rain'])
        elif weather == 'snow':
            footwear = self._pick_item(self.wardrobe['footwear']['snow'])
        else:
            category = 'mild' if temp_category in ['cool', 'mild'] else 'hot'
            footwear = self._pick_item(self.wardrobe['footwear'][category])

        if footwear:
            outfit_parts.append(f"Footwear: {footwear}")

        # Sunny weather accessories
        if weather == 'clear' and temp_category in ['mild', 'hot']:
            sunny_acc = self._filter_items(self.wardrobe['accessories']['sunny'])
            accessories += sunny_acc

        if accessories:
            outfit_parts.append(f"Accessories: {', '.join(accessories)}")

        return "\n".join(outfit_parts)


def clothing_recommendations(weather, temp):
    user_preferences = {
        "style_preferences": ["casual"],
        "avoid_items": ["poncho", "thermal pants", "parka"],
        "must_have": ["sneakers", "hoodie"]
    }

    my_wardrobe = Wardrobe()
    recommender = Recommender(my_wardrobe, user_preferences)
    outfit_str = recommender.recommend(weather, temp)

    return outfit_str
