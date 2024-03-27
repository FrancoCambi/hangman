def fill_pos(letters_pos):
    for i in range(12):
        letters_pos.append((letters_pos[i][0] + 55, 371))
        letters_pos.append((60, 430))
    for i in range(12):
        letters_pos.append((letters_pos[i][0] + 55, 430))
    
    return letters_pos