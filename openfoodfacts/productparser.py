class ProductParser:
    """
    This class contains methods that analyse the products
    that the API has returned
    """

    @staticmethod
    def separate_brands(brands):
        """
        If more than 1 brand, separate each brand and returns the first one
        """
        if "," in brands:
            brands_list = brands.split(",")
            return brands_list[0].strip()
        return brands

    @staticmethod
    def check_if_empty_values(product):
        """
        Check if any informations of a product is missing
        """
        for key, value in product.items():
            try:
                value = value.strip()
            except AttributeError:
                value = str(value)
                value = value.strip()
            if value == "":
                return True
        return False
