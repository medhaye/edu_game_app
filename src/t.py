HEIGHT = 600  # Example HEIGHT value, replace with the actual one

ensemble = [
    (100, HEIGHT - 100),
    (300, HEIGHT - 150),
    (500, HEIGHT - 200),
    (700, HEIGHT - 250),
    (900, HEIGHT - 100),
    (1100, HEIGHT - 150),
]

# Adding 30 more elements
for i in range(7, 37):  # Start from 7 as 6 elements already exist
    x = ensemble[-1][0] + 200  # Increment x by 200
    y = HEIGHT - (100 + (i % 5) * 50)  # Cycle y values similar to the given pattern
    ensemble.append((x, y))

print(ensemble)
