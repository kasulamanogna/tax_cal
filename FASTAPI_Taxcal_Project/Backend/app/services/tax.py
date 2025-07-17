def calculate_tax(amount: float, regime: str = "old") -> float:
    tax = 0
    if regime == "old":
        if amount <= 250000:
            tax = 0
        elif amount <= 500000:
            tax = (amount - 250000) * 0.05
        elif amount <= 1000000:
            tax = 12500 + (amount - 500000) * 0.20
        else:
            tax = 112500 + (amount - 1000000) * 0.30
    elif regime == "new":
        slabs = [250000, 250000, 250000, 250000, 250000, float('inf')]
        rates = [0, 0.05, 0.10, 0.15, 0.20, 0.30]
        slab_start = 0
        for slab, rate in zip(slabs, rates):
            if amount > slab_start + slab:
                tax += slab * rate
                slab_start += slab
            else:
                tax += (amount - slab_start) * rate
                break
    return tax