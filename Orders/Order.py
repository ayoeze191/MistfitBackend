class OrderClass():
    @staticmethod
    def total_number_of_product(self):
        order_item = self.orderitem_set.all()
        return sum([i.quantity for i in order_item])


    @staticmethod
    def get_total_amount_of_a_particular_goods_bought(self):
        total = self.product.stock_price * self.quantity
        return total

    @staticmethod
    def total_amount_of_all_goods_bought(self):
       return sum([i.get_total_amount_of_a_particular_goods_bought for i in self.orderitem_set.all()])

    
    