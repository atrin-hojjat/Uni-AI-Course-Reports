(TeX-add-style-hook
 "AUTthesis"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("AUTthesis" "oneside" "msc" "12pt")))
   (add-to-list 'LaTeX-verbatim-environments-local "lstlisting")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "lstinline")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "lstinline")
   (TeX-run-style-hooks
    "latex2e"
    "commands"
    "fa_title"
    "taid"
    "TOC-TOF-LOT"
    "list-of-symbols"
    "chapter1"
    "appendix1"
    "AUTthesis12"
    "pgf"
    "pythonhighlight"
    "listings"
    "color")
   (TeX-add-symbols
    '("norm" 1)
    '("insertfig" 3))
   (LaTeX-add-labels
    "#3")
   (LaTeX-add-bibliographies
    "references")
   (LaTeX-add-color-definecolors
    "dkgreen"
    "gray"
    "mauve"))
 :latex)

