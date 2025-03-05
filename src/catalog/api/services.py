from .repository import CategoryRepository, ProductRepository


def product_list_service(category_slug):
    category = None
    category_slug = category_slug.lower() if category_slug else None

    categories = {c.slug: c for c in CategoryRepository.all()}
    products = ProductRepository.filter(available=True, select_related=["category"])

    if category_slug:
        category = categories.get(category_slug, None)
        products = [p for p in products if p.category_id == category.id]

    return category, list(categories.values()), products


def get_product_service(product_id):
    return ProductRepository.get(id=product_id, available=True)
