def stats_cart(cart):
    total_amount, total_quantity = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        "total_amount": total_amount,
        "total_quantity": total_quantity
    }

def stats_receipts(receipts):
    total_amount, total_quantity = 0,0

    if receipts:
        for r in receipts.values():
            total_quantity += r['quantity']
            total_amount += r['quantity'] * r['price']

    return {
        "total_amount": total_amount,
        "total_quantity": total_quantity
    }