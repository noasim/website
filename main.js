"use strict"

const NUM_COL = 4

function order_disps()
{
    const cols_offset = Array(NUM_COL).fill(0)
    let index = 0;
    const disp_divs = disps.children
    const col_width = disp_divs[0].offsetWidth
    for(let disp of disp_divs)
    {
        const col_ind = index++ % NUM_COL
        disp.style.top = cols_offset[col_ind] + "px"
        cols_offset[col_ind] += disp.offsetHeight
        disp.style.right = col_width * col_ind + "px"
    }
    const gal_width = col_width * NUM_COL
    disps.style.width = gal_width + "px"

    if (window.gal_view !== undefined)
        gal_view.style.width = gal_width + "px"
}
