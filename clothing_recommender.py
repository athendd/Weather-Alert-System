import random

class Wardrobe:
    def __init__(self):
        self.wardrobe = {
            'tops': [
                {'item': 'rugby green t-shirt', 'occasions': ['casual'], 'season': ['spring', 'summer'], 'style': 'casual'},
                {'item': 'red t-shirt', 'occasions': ['casual'], 'season': ['spring', 'summer'], 'style': 'casual'},
                {'item': 'navy blue t-shirt', 'occasions': ['casual'], 'season': ['summer', 'spring', 'winter', 'fall'], 'style': 'casual'},
                {'item': 'light blue t-shirt', 'occasions': ['casual'], 'season': ['spring', 'summer'], 'style': 'casual'},
                {'item': 'navy blue rugby t-shirt', 'occasions': ['casual', 'sport'], 'season': ['spring', 'fall'], 'style': 'casual'},
                {'item': 'white sweater', 'occasions': ['casual', 'work'], 'season': ['fall', 'winter'], 'style': 'smart'},
                {'item': 'navy blue button up', 'occasions': ['formal', 'work'], 'season': ['summer', 'spring', 'winter', 'fall'], 'style': 'smart'},
                {'item': 'white button up', 'occasions': ['formal', 'work'], 'season': ['summer', 'spring', 'winter', 'fall'], 'style': 'smart'}
            ],
            'bottoms': [
                {'item': 'black striped shorts', 'occasions': ['casual'], 'season': ['summer'], 'style': 'casual'},
                {'item': 'grey shorts', 'occasions': ['casual'], 'season': ['summer'], 'style': 'casual'},
                {'item': 'maroon red shorts', 'occasions': ['casual'], 'season': ['summer'], 'style': 'casual'},
                {'item': 'green pants', 'occasions': ['work', 'casual'], 'season': ['fall', 'spring'], 'style': 'smart'},
                {'item': 'black pants', 'occasions': ['formal', 'work'], 'season': ['fall', 'winter'], 'style': 'smart'},
                {'item': 'light brown pants', 'occasions': ['casual'], 'season': ['fall', 'spring'], 'style': 'casual'},
                {'item': 'blue jeans', 'occasions': ['casual'], 'season': ['summer', 'spring', 'winter', 'fall'], 'style': 'casual'}
            ],
            'outerwear': [
                {'item': 'windbreaker jacket', 'weather': ['wind', 'mild'], 'occasions': ['casual', 'outdoor'], 'season': ['spring', 'fall'], 'style': 'casual'},
                {'item': 'raincoat', 'weather': ['rain'], 'occasions': ['outdoor'], 'season': ['spring', 'fall'], 'style': 'casual'},
                {'item': 'black winter coat', 'weather': ['cold'], 'occasions': ['formal', 'casual'], 'season': ['winter'], 'style': 'smart'},
                {'item': 'navy blue jacket', 'weather': ['mild'], 'occasions': ['casual'], 'season': ['fall', 'spring'], 'style': 'casual'},
                {'item': 'black blazer', 'weather': ['mild'], 'occasions': ['formal'], 'season': ['spring', 'fall'], 'style': 'smart'}
            ],
            'footwear': [
                {'item': 'flat footed shoes', 'occasions': ['casual', 'work'], 'season': ['summer', 'spring', 'winter', 'fall'], 'style': 'smart'},
                {'item': 'white sneakers', 'occasions': ['casual'], 'season': ['summer', 'spring', 'winter', 'fall'], 'style': 'casual'},
                {'item': 'brown boots', 'occasions': ['cold', 'casual'], 'season': ['fall', 'winter'], 'style': 'casual'},
                {'item': 'flip flops', 'occasions': ['casual'], 'season': ['summer'], 'style': 'casual'}
            ],
            'accessories': [
                {'item': 'black umbrella', 'weather': ['rain'], 'season': ['summer', 'spring', 'winter', 'fall'], 'style': 'any'},
                {'item': 'scarf', 'weather': ['cold'], 'season': ['fall', 'winter'], 'style': 'smart'},
                {'item': 'gloves', 'weather': ['cold'], 'season': ['winter'], 'style': 'any'},
                {'item': 'sunglasses', 'weather': ['sunny'], 'season': ['spring', 'summer'], 'style': 'casual'},
                {'item': 'baseball cap', 'weather': ['sunny'], 'season': ['summer'], 'style': 'casual'}
            ]
        }

class Recommender:
    def __init__(self, wardrobe: Wardrobe, preferences: dict = None):
        self.wardrobe = wardrobe.wardrobe
        self.preferences = preferences if preferences else {
            "style_preferences": [],
            "avoid_items": [],
            "must_have": [],
            "occasion": "casual",
            "season": "summer"
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

    def _filter_items(self, items, weather=None):
        return [
            item for item in items
            if item['item'] not in self.preferences['avoid_items']
            and self.preferences['occasion'] in item.get('occasions', [])
            and self.preferences['season'] in item.get('season', ['all'])
            and (not weather or weather in item.get('weather', []) or 'all' in item.get('weather', []))
        ]

    def _pick_item(self, items, category_name):
        filtered = self._filter_items(items)
        must_haves = [item for item in filtered if item['item'] in self.preferences['must_have']]
        if must_haves:
            return must_haves[0]['item']
        elif filtered:
            return random.choice(filtered)['item']
        else:
            fallback = next((item['item'] for item in items if item['item'] in self.preferences['must_have']), None)
            return f"(No seasonal match for must-have '{fallback}')" if fallback else f"(No suitable {category_name})"

    def match_styles(self, outfit):
        styles = [piece.get('style', 'casual') for piece in outfit if isinstance(piece, dict)]
        if 'smart' in styles and 'casual' in styles:
            return "⚠️ Style clash: Mixing casual and smart items."
        return ""

    def recommend(self, weather: str, temperature_f: float):
        weather = weather.lower()
        temp_category = self.categorize_temperature(temperature_f)
        outfit = []

        top = self._pick_item(self.wardrobe['tops'], "top")
        bottom = self._pick_item(self.wardrobe['bottoms'], "bottom")
        outer = self._pick_item(self._filter_items(self.wardrobe['outerwear'], weather), "outerwear")
        shoes = self._pick_item(self.wardrobe['footwear'], "footwear")

        accessories = [
            acc['item'] for acc in self.wardrobe['accessories']
            if acc['item'] not in self.preferences['avoid_items']
            and (weather in acc.get('weather', []) or 'all' in acc.get('weather', []))
            and self.preferences['season'] in acc.get('season', ['all'])
        ]

        outfit_details = [
            f"Top: {top}",
            f"Bottom: {bottom}",
            f"Outerwear: {outer}",
            f"Footwear: {shoes}"
        ]
        if accessories:
            outfit_details.append("Accessories: " + ", ".join(accessories))

        style_warning = self.match_styles([top, bottom, outer, shoes])

        return "\n".join(outfit_details + ([style_warning] if style_warning else []))
    

def main_recommendation(weather, temp):
    user_preferences = {
    "style_preferences": ["casual"],
    "avoid_items": ["flip flops", "black blazer"],
    "must_have": ["windbreaker jacket", "rugby green t-shirt", "flat footed shoes", "black striped shorts"],
    "occasion": "casual",
    "season": "summer"
    }

    my_wardrobe = Wardrobe()
    recommender = Recommender(my_wardrobe, user_preferences)
    recommendation = recommender.recommend(weather, temp)
    
    return recommendation

