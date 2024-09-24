import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(course):
    """Создает продукт в страйпе"""
    return stripe.Product.create(
        name=course.get("name")
    )


def create_stripe_price(amount, product):
    """Создает цену в страйпе"""
    return stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": product.get("name")},
    )


def create_stripe_session(price):
    """Создает сессию на оплату в страйпе"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
