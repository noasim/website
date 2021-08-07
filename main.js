"use strict"

let last_col_width = null
let last_num_cols = null

function order_disps()
{
    const disp_divs = disps.children
    const col_width = disp_divs[0].offsetWidth

    let num_cols = 4
    if ( window.matchMedia("(max-width: 485px)").matches)
        num_cols = 2
    else if ( window.matchMedia("(max-width: 655px)").matches)
        num_cols = 3

    if (last_col_width == col_width && last_num_cols == num_cols)
        return
    last_col_width = col_width
    last_num_cols = num_cols

    const cols_offset = Array(num_cols).fill(0)
    let index = 0;
    for(let disp of disp_divs)
    {
        const col_ind = index++ % num_cols
        disp.style.top = cols_offset[col_ind] + "px"
        cols_offset[col_ind] += disp.offsetHeight
        disp.style.right = col_width * col_ind + "px"
    }
    const gal_width = col_width * num_cols
    disps.style.width = gal_width + "px"

    if (window.gal_view !== undefined)
        gal_view.style.width = gal_width + "px"
}

function start_order_disps()
{
    order_disps()
    window.addEventListener("resize", ()=>{
        order_disps()
        show_menu()
    })
    window.addEventListener("click", (e)=>{
        if (menu_visible && e.target !== ham_but) // dismiss it
            side_menu_toggle()
    })
}


let menu_visible = false;
function side_menu_toggle() {
    menu_visible = !menu_visible
    show_menu()
}

function show_menu() {
    if (window.gal_text_menu === undefined) {
        ham_but.style.display = "none"
        return
    }
    const small_screen = window.matchMedia("(max-width: 900px)").matches
    gal_text_menu.style.display = (!small_screen || menu_visible) ? "initial" : "none"
}

function ham_click()
{
    side_menu_toggle()
}

