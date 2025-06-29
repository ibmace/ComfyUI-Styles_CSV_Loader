
import os
import re
import folder_paths


class StylesCSVLoader:
    """Loads styles.csv file with styles for prompts."""

    @staticmethod
    def load_styles_csv(styles_path: str):
        styles = {"Error loading styles.csv, check the console": ["", ""]}
        if not os.path.exists(styles_path):
            print(f"""Error: No styles.csv found in: {folder_paths.base_path}""")
            return styles
        try:
            with open(styles_path, "r", encoding="utf-8") as f:
                styles = [[x.replace('"', '').replace('\n', '') for x in re.split(
                    ',(?=(?:[^"]*"[^"]*")*[^"]*$)', line)] for line in f.readlines()[1:]]
                styles = {x[0]: [x[1], x[2]] for x in styles}
        except Exception as e:
            print(f"Error loading styles.csv: {e}")
        return styles

    @classmethod
    def INPUT_TYPES(cls):
        cls.styles_csv = cls.load_styles_csv(os.path.join(folder_paths.base_path, "styles.csv"))
        return {
            "required": {
                "styles": (
                    list(cls.styles_csv.keys())
                    if isinstance(cls.styles_csv, dict)
                    else cls.styles_csv,
                )
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("positive prompt", "negative prompt")
    FUNCTION = "execute"
    CATEGORY = "loaders"

    def execute(self, styles):
        # Ensure styles is a single string, not a list
        if isinstance(styles, list):
            styles = styles[0]

        data = self.__class__.styles_csv
        if isinstance(data, dict):
            return (data[styles][0], data[styles][1])
        elif isinstance(data, list):
            for entry in data:
                if entry[0] == styles:
                    return (entry[1], entry[2])
        raise ValueError("Invalid style selected or format mismatch")
