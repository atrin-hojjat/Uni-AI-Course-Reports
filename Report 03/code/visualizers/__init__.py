import matplotlib

def SetupLibraries():
    matplotlib.rcParams.update({
        "pgf.texsystem": "xelatex",
        'text.usetex': True,
        'pgf.rcfonts': False,
        "font.family": "mononoki Nerd Font Mono",
        "font.serif": [],
        #  "font.cursive": ["mononoki Nerd Font", "mononoki Nerd Font Mono"],
    })
