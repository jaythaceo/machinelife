"""Binary Search 
def binarySearch(alist, item):
	first = 0
	last = len(alist) -1
	found = False

	while first <= last and not found:
		midpoint = (first + last)//2
		if alist[midpoint] == item:
			found = True
		else:
			if item < alist[midpoint]:
				last = midpoint - 1
			else:
				first = midpoint + 1
	return found

testList = [0,1,2,3,45,3,5,234]
print(binarySearch(testList, 3))
print(binarySearch(testList, 25))
"""
shoot = 'S'
charge = 'C'
results = []
response = "Case #{x}: {swaps}"


def damage(attack):
    power = 1
    damage = 0
    for instruction in attack:
        if instruction == charge:
            power *= 2
        else:
            damage += power
    return damage


def defense(attack, shield_power):
    attack = [x for x in attack]
    base_damage = attack.count(s)
    max_damage = damage(attack)
    damage_diff = max_damage - shield_power

    if base_damage > shield_power:
        return 'IMPOSSIBLE'

    swaps = 0
    while damage_diff > 0:
        i = attack.index(charge)
        j = attack.index(shoot, i)
        i = j - 1
        # damage of a shot is 2^number_of_prior_charges
        damage_gain = 2 ** attack[:i].count(charge)
        attack[i], attack[j] = shoot, charge
        damage_diff -= damage_gain
        swaps += 1

    return swaps


for case in range(int(input(''))):
    shield, attack = input('').split()

    results.append(response.format(x=case + 1, swaps=defense(attack, int(shield))))

for result in results:
