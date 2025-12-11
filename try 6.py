# katalog_loope.py - Aplikasi Katalog & Keranjang Loopé (Final Fix Version)

import streamlit as st
import pandas as pd   # PENTING! FIX untuk error keranjang


# ============================================================
#                KELAS PRODUK, CART & REPOSITORY
# ============================================================

class Product:
    """Class Produk dengan validasi + image"""
    def __init__(self, name: str, price: float, image_url: str = "https://via.placeholder.com/150x150?text=LOOPÉ"):
        self._name = None
        self._price = None
        self.name = name
        self.price = price
        self.image_url = image_url

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Nama produk harus berupa string tidak kosong.")
        self._name = value.strip()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not (isinstance(value, (int, float)) and value >= 0):
            raise ValueError("Harga harus angka >= 0.")
        self._price = float(value)

    def subtotal(self, qty: int):
        return self.price * qty

    def display_price(self):
        return f"Rp {self.price:,.0f}"


class Cart:
    """Keranjang belanja dengan list item"""
    def __init__(self):
        self.items = []   # item = {"product": Product, "qty": int}

    def add_item(self, product: Product, qty: int):
        for it in self.items:
            if it["product"].name == product.name:
                it["qty"] += qty
                return
        self.items.append({"product": product, "qty": qty})

    def update_item(self, product_name: str, qty: int):
        for it in self.items:
            if it["product"].name == product_name:
                if qty <= 0:
                    self.items.remove(it)
                else:
                    it["qty"] = qty
                return

    def remove_item(self, product_name: str):
        self.items = [it for it in self.items if it["product"].name != product_name]

    def clear(self):
        self.items = []

    def total(self):
        return sum(it["product"].subtotal(it["qty"]) for it in self.items)

    def receipt_text(self):
        lines = []
        for it in self.items:
            p = it["product"]
            q = it["qty"]
            lines.append(f"{p.name} x{q} = Rp {p.subtotal(q):,.0f}")
        lines.append("-" * 30)
        lines.append(f"TOTAL = Rp {self.total():,.0f}")
        return "\n".join(lines)


class ProductRepository:
    """CRUD Produk"""
    def __init__(self, initial=None):
        self._products = initial[:] if initial else []

    def create_product(self, name, price, image_url=None):
        if self.get_by_name(name):
            raise ValueError("Produk dengan nama sama sudah ada.")
        p = Product(name, price, image_url)
        self._products.append(p)
        return p

    def get_all(self):
        return list(self._products)

    def get_by_name(self, name):
        for p in self._products:
            if p.name == name:
                return p
        return None

    def update_product(self, old_name, new_name=None, new_price=None):
        p = self.get_by_name(old_name)
        if not p:
            raise ValueError("Produk tidak ditemukan.")

        if new_name and new_name != old_name and self.get_by_name(new_name):
            raise ValueError("Nama baru sudah dipakai produk lain.")

        if new_name:
            p.name = new_name
        if new_price is not None:
            p.price = new_price
        return p

    def delete_product(self, name):
        p = self.get_by_name(name)
        if not p:
            raise ValueError("Produk tidak ditemukan.")
        self._products.remove(p)


# ============================================================
#                  DATA AWAL KATALOG DEFAULT
# ============================================================

default_catalog = [
    Product("Pink T-shirt", 17_000, "https://i.imgur.com/W2zU98S.png"),
    Product("Rok Mini Plaid", 12_000, "https://i.imgur.com/g0t6XkM.png"),
    Product("Black Tank Top", 18_000, "https://i.imgur.com/vHqP4Yn.png"),
    Product("Jogger Pants", 35_000, "https://i.imgur.com/7b58UoJ.png"),
]