def overlap(red,yellow):
    #Return overlap between two rectangles, or None.
    ((red_lo_x, red_lo_y), (red_hi_x, red_hi_y)) = red
    ((yellow_lo_x, yellow_lo_y), \
    (yellow_hi_x, yellow_hi_y)) = yellow

    if (red_lo_x >= yellow_hi_x) \
        or (red_hi_x <= yellow_lo_x) \
        or (red_lo_y >= yellow_hi_x) \
        or (red_hi_y <= yellow_lo_y):
        return None

    lo_x = max(red_lo_x, yellow_lo_x)
    lo_y = max(red_lo_y, yellow_lo_y)
    hi_x = min(red_hi_x, yellow_hi_x)
    hi_y = min(red_hi_y, yellow_hi_y)
    return ((lo_x, lo_y), (hi_x, hi_y))
