def is_first_finger_up(kpts):
    """
    kpts: list of (hand_idx, (x, y)) for all detected hands.
    Must contain at least 21 points for one hand.
    Returns True if:
        - Index finger is up
        - Middle, Ring, Pinky are down
    Thumb is ignored.
    """

    # --- Extract only Hand 0 landmarks ---
    hand0 = [pt for h, pt in kpts if h == 0]

    # Must have 21 points
    if len(hand0) < 21:
        return False

    # Get just the y-coordinates
    y = [pt[1] for pt in hand0]

    # Landmark indices
    INDEX_TIP, INDEX_PIP = 8, 6
    MIDDLE_TIP, MIDDLE_PIP = 12, 10
    RING_TIP, RING_PIP = 16, 14
    PINKY_TIP, PINKY_PIP = 20, 18

    # Logic: finger up means tip is ABOVE pip (smaller y value)
    index_up  = y[INDEX_TIP]  < y[INDEX_PIP]
    middle_dn = y[MIDDLE_TIP] > y[MIDDLE_PIP]
    ring_dn   = y[RING_TIP]   > y[RING_PIP]
    pinky_dn  = y[PINKY_TIP]  > y[PINKY_PIP]

    return index_up and middle_dn and ring_dn and pinky_dn
