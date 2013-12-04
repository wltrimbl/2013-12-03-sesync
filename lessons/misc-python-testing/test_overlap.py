from rectangles import overlap
def test_overlap_with_itself():
    obj=overlap(((0,0),(1,1)),((0,0),(1,1)))
    expect=((0,0),(1,1))
    assert obj==expect
