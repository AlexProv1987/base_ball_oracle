class GloveSize():
    level_chart = {
        "t-ball": range(0, 7),
        "youth": range(7, 13),
        "adult": range(13, 100),
    }
    glove_chart = {
        "t-ball": {
            "1st base": "8.5 - 10",
            "infield": "8.5 - 10",
            "outfield": "8.5 - 10",
            "catcher": "29.5-30",
        },
        "youth": {
            "1st base": "11.5 - 12",
            "infield": "10.25 - 11.5",
            "outfield": "11.5 - 12.25",
            "catcher": "30-32.5",
        },
        "adult": {
            "1st base": "12 - 13",
            "infield": "11.25 - 12",
            "outfield": "12 - 12.75",
            "catcher": "32.5-34",
        },
    }

    player_level = None

    def set_player_level(self, age):
        for level in self.level_chart.keys():
            if age in self.level_chart[level]:
                self.player_level = level
        return

    def get_glove_size(self, position):
        try:
            size = self.glove_chart[self.player_level][position]
        except:
            size = 'none found'
        return size


class BatSize():
    bat_chart = {
        "26": {"weight": range(0, 61), "height": range(36, 41)},
        "27": {"weight": range(0, 71), "height": range(36, 46)},
        "28": {"weight": range(0, 101), "height": range(41, 49)},
        "29": {"weight": range(0, 161), "height": range(41, 53)},
        "30": {"weight": range(61, 161), "height": range(49, 61)},
        "31": {"weight": range(71, 171), "height": range(49, 65)},
        "32": {"weight": range(81, 181), "height": range(57, 69)},
        "33": {"weight": range(121, 250), "height": range(61, 84)},
        "34": {"weight": range(161, 250), "height": range(69, 84)},
    }
    '''Requested a different table that does not overlap'''
    bat_drop_chart = {
        '-12 to -10':range(0,10),
        '-10':range(10,13),
        '-8':range(12,14),
        '-5':range(14,15),
        '-3':range(15,100),
    }

    def get_bat_size(self, p_height, p_weight):
        bat_size = None
        for size in self.bat_chart.keys():
            if p_weight in self.bat_chart[size]["weight"]:
                if p_height in self.bat_chart[size]["height"]:
                    bat_size = size
                    return bat_size
        return bat_size
    
    def get_bat_drop(self,p_age):
        bat_drop = ''
        for drop in self.bat_drop_chart:
            if p_age in self.bat_drop_chart[drop]:
                bat_drop = drop
                return bat_drop
        return bat_drop
