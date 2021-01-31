scores = input().split()
scores_iter = iter(scores)
right = 0
wrong = 0
while wrong < 3:
    try:
        score = next(scores_iter)
    except StopIteration:
        print('You won')
        print(right)
        break
    if score == 'C':
        right += 1
    elif score == 'I':
        wrong += 1
if wrong > 2:
    print('Game over')
    print(right)
