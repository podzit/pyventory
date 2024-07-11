class Product():
    """Create Product object
    """

    def __init__(self,
                 p_id:int,
                 brand:str,
                 ref:str,
                 nb:int,
                 price:float,
                 date:str,
                 argus:float,
                 last_argus:str,
                 p_type:str,
                 serial:str,
                 comment:str,
                 shop:int,
                 fact:str='',
                 photo:str=''):
        """Create Product object

        Args:
            p_id (int): Product ID
            brand (str): Product brand
            ref (str): Product reference
            nb (int): Product quantity
            price (float): Product price
            date (str): Product purchase date
            argus (float): Product argus
            last_argus (str): Product argus last checked date
            p_type (str): Product type
            serial (str): Product serial number
            comment (str): Comment about product
            shop (int): Still available to sell ?
            fact (str, optional): Bill filename. Defaults to ''.
            photo (str, optional): Picture filename. Defaults to ''.
        """
        self.p_id = p_id
        self.brand = brand
        self.ref = ref
        self.nb = nb
        self.price = price
        self.date = date
        self.argus = argus
        self.last_argus = last_argus
        self.fact = fact
        self.photo = photo
        self.p_type = p_type
        self.serial = serial
        self.comment = comment
        self.shop = shop