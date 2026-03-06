"""Color palettes for the visual repr of the Maze."""

THEMES: dict[str, dict[str, str]] = {

    "default": {
        "wall":    "\033[48;2;216;143;148m  \033[0m",  # dusty rose
        "path":    "\033[48;2;30;30;30m  \033[0m",     # charcoal
        "ft":      "\033[48;2;35;60;105m  \033[0m",    # navy blue
        "ft_wall": "\033[48;2;35;60;105m  \033[0m",    # navy blue
        "entry":   "\033[48;2;102;187;106m  \033[0m",  # medium green
        "exit":     "\033[48;2;239;83;80m  \033[0m",   # coral red
        "solved":  "\033[48;2;253;253;100m  \033[0m",  # canary yellow
    },

    "ocean": {
        "wall":    "\033[48;2;0;105;148m  \033[0m",    # ocean blue
        "path":    "\033[48;2;10;20;40m  \033[0m",     # abyss blue
        "ft":      "\033[48;2;0;60;100m  \033[0m",     # deep blue
        "ft_wall": "\033[48;2;0;60;100m  \033[0m",     # aquamarine
        "entry":   "\033[48;2;0;200;150m  \033[0m",    # aquamarine
        "exit":     "\033[48;2;255;100;0m  \033[0m",   # burnt orange
        "solved":  "\033[48;2;180;230;255m  \033[0m",  # ice blue
    },

    "forest": {
        "wall":    "\033[48;2;34;85;34m  \033[0m",     # forest green
        "path":    "\033[48;2;15;30;15m  \033[0m",     # dark forest
        "ft":      "\033[48;2;20;50;20m  \033[0m",     # shadow green
        "ft_wall": "\033[48;2;20;50;20m  \033[0m",     # shadow green
        "entry":   "\033[48;2;144;238;144m  \033[0m",  # light green
        "exit":     "\033[48;2;180;50;50m  \033[0m",   # dark red
        "solved":  "\033[48;2;255;215;0m  \033[0m",    # gold
    },

    "desert": {
        "wall":    "\033[48;2;194;154;108m  \033[0m",  # sand dune
        "path":    "\033[48;2;92;64;51m  \033[0m",     # dry earth
        "ft":      "\033[48;2;160;120;80m  \033[0m",   # dusty trail
        "ft_wall": "\033[48;2;160;120;80m  \033[0m",   # dusty trail
        "entry":   "\033[48;2;120;200;120m  \033[0m",  # oasis green
        "exit":     "\033[48;2;220;70;40m  \033[0m",   # sunset red
        "solved":  "\033[48;2;255;220;120m  \033[0m",  # golden sun
    },

    "arctic": {
        "wall":    "\033[48;2;180;210;230m  \033[0m",  # pack ice
        "path":    "\033[48;2;15;25;40m  \033[0m",     # polar night
        "ft":      "\033[48;2;40;80;120m  \033[0m",    # deep glacier
        "ft_wall": "\033[48;2;40;80;120m  \033[0m",    # deep glacier
        "entry":   "\033[48;2;80;230;200m  \033[0m",   # aurora teal
        "exit":     "\033[48;2;180;100;255m  \033[0m", # aurora violet
        "solved":  "\033[48;2;220;245;255m  \033[0m",  # fresh snow
    },

    "volcanic": {
        "wall":    "\033[48;2;45;45;45m  \033[0m",     # cooled lava rock
        "path":    "\033[48;2;20;20;20m  \033[0m",     # obsidian
        "ft":      "\033[48;2;90;0;0m  \033[0m",       # dark magma
        "ft_wall": "\033[48;2;90;0;0m  \033[0m",       # dark magma
        "entry":   "\033[48;2;255;215;0m  \033[0m",    # molten orange
        "exit":     "\033[48;2;255;40;0m  \033[0m",    # lava red
        "solved":  "\033[48;2;255;140;0m  \033[0m",    # glowing core
    },

    "cyberpunk": {
        "wall":    "\033[48;2;255;20;147m  \033[0m",   # neon pink
        "path":    "\033[48;2;10;10;30m  \033[0m",     # dark void
        "ft":      "\033[48;2;0;255;255m  \033[0m",    # neon cyan
        "ft_wall": "\033[48;2;0;255;255m  \033[0m",    # neon cyan
        "entry":   "\033[48;2;57;255;20m  \033[0m",    # electric green
        "exit":     "\033[48;2;255;69;0m  \033[0m",    # neon orange
        "solved":  "\033[48;2;255;255;0m  \033[0m",    # bright highlight
    },

    "space": {
        "wall":    "\033[48;2;20;10;60m  \033[0m",     # deep space purple
        "path":    "\033[48;2;5;5;20m  \033[0m",       # void black
        "ft":      "\033[48;2;15;5;45m  \033[0m",      # dark nebula
        "ft_wall": "\033[48;2;15;5;45m  \033[0m",      # dark nebula
        "entry":   "\033[48;2;100;220;255m  \033[0m",  # pulsar blue
        "exit":     "\033[48;2;255;100;200m  \033[0m", # nebula pink
        "solved":  "\033[48;2;255;240;180m  \033[0m",  # starlight
    },

    "freedom": {
        "wall":    "\033[48;2;20;20;20m  \033[0m",     # black
        "path":    "\033[48;2;245;245;245m  \033[0m",  # white
        "ft":      "\033[48;2;0;122;61m  \033[0m",     # palestine green
        "ft_wall": "\033[48;2;0;122;61m  \033[0m",     # palestine green
        "entry":   "\033[48;2;0;122;61m  \033[0m",     # palestine green
        "exit":     "\033[48;2;0;122;61m  \033[0m",    # palestine green
        "solved":  "\033[48;2;206;17;38m  \033[0m",    # palestine red
    },

    "mauritius": {
        "wall":    "\033[48;2;230;166;55m  \033[0m",   # amber gold
        "path":    "\033[48;2;32;102;12m  \033[0m",    # jungle green
        "ft":      "\033[48;2;107;72;192m  \033[0m",   # lavander purple
        "ft_wall": "\033[48;2;107;72;192m  \033[0m",   # lavander purple
        "entry":   "\033[48;2;5;111;223m  \033[0m",    # ocean blue
        "exit":     "\033[48;2;216;183;116m  \033[0m", # sandy beige
        "solved":  "\033[48;2;35;87;201m  \033[0m",    # sapphire blue
    },

    "baugigi": {
        "wall":    "\033[48;2;104;52;208m  \033[0m",   # electric purple
        "path":    "\033[48;2;208;52;104m  \033[0m",   # hot pink
        "ft":      "\033[48;2;104;208;52m  \033[0m",   # lime green
        "ft_wall": "\033[48;2;104;208;52m  \033[0m",   # lime green
        "entry":   "\033[48;2;208;104;52m  \033[0m",   # burnt orange
        "exit":     "\033[48;2;52;104;208m  \033[0m",  # royal blue
        "solved":  "\033[48;2;52;208;104m  \033[0m",   # mint green
    },

    "colorblind_friendly": {
        "wall":    "\033[48;2;0;114;178m  \033[0m",    # blue (safe anchor)
        "path":    "\033[48;2;20;20;20m  \033[0m",     # near-black
        "ft":      "\033[48;2;0;58;115m  \033[0m",     # dark blue
        "ft_wall": "\033[48;2;0;58;115m  \033[0m",     # dark blue
        "entry":   "\033[48;2;230;159;0m  \033[0m",    # amber/orange
        "exit":     "\033[48;2;86;180;233m  \033[0m",  # sky blue
        "solved":  "\033[48;2;240;228;66m  \033[0m",   # yellow
    },

    "colorblind_unfriendly": {
        "wall":    "\033[48;2;180;60;0m  \033[0m",     # red-brown
        "path":    "\033[48;2;60;130;0m  \033[0m",     # olive green
        "ft":      "\033[48;2;140;80;0m  \033[0m",     # muddy orange-brown
        "ft_wall": "\033[48;2;140;80;0m  \033[0m",     # muddy orange-brown
        "entry":   "\033[48;2;0;200;50m  \033[0m",     # pure green
        "exit":     "\033[48;2;220;20;20m  \033[0m",   # pure red
        "solved":  "\033[48;2;100;150;0m  \033[0m",    # yellow-green
    }
}
