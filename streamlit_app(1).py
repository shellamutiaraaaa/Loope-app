import streamlit as st

# ============================
# 1. CLASS DEFINITIONS
# ============================

class User:
    def __init__(self, name):
        self.name = name


class Category:
    def __init__(self, cid, name):
        self.categoryId = cid
        self.name = name


class Product:
    def __init__(self, pid, name, category, price, colors, sizes, images):
        self.productId = pid
        self.name = name
        self.category = category
        self.price = price
        self.colors = colors
        self.sizes = sizes
        self.images = images

    def isAvailable(self, size, color):
        return size in self.sizes and color in self.colors


class Filter:
    def __init__(self, size=None, color=None, minPrice=0, maxPrice=999999):
        self.size = size
        self.color = color
        self.minPrice = minPrice
        self.maxPrice = maxPrice

    def apply(self, products):
        result = []
        for p in products:
            if self.size and self.size not in p.sizes:
                continue
            if self.color and self.color not in p.colors:
                continue
            if not (self.minPrice <= p.price <= self.maxPrice):
                continue
            result.append(p)
        return result


class CartItem:
    def __init__(self, product, size, color, qty):
        self.product = product
        self.size = size
        self.color = color
        self.qty = qty

    @property
    def totalPrice(self):
        return self.qty * self.product.price


class Cart:
    def __init__(self):
        self.items = []

    def addItem(self, product, size, color, qty):
        self.items.append(CartItem(product, size, color, qty))

    def getTotalPrice(self):
        return sum(i.totalPrice for i in self.items)


class Checkout:
    def __init__(self, user, cart):
        self.user = user
        self.cart = cart

    def generateSummary(self):
        return self.cart.getTotalPrice()