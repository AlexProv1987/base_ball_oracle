class GloveSize():
    level_chart = {
        't-ball':range(0,7),
        'youth':range(7,13),
        'adult':range(13,100)
    }
    glove_chart = {
        't-ball':{'1st base':'8.5 - 10',
                  'infield':'8.5 - 10',
                  'outfield':'8.5 - 10'},
        'youth':{
            '1st base':'11.5 - 12',
            'infield':'10.25 - 11.5',
            'outfield':'11.5 - 12.25'},
        'adult':{
            '1st base':'12 - 13',
            'infield':'11.25 - 12',
            'outfield':'12 - 12.75'}
    }

    player_level = None

    def set_player_level(self,age):
        for level in self.level_chart.keys():
            if age in self.level_chart[level]:
                self.player_level = level
        return 
    
    def get_glove_size(self, position):
        size = self.glove_chart[self.player_level][position]
        return size
    
class BatSize():
    bat_chart = {
        '26':{'weight':range(0,61),'height':range(36,41)},
        '27':{'weight':range(0,71),'height':range(36,46)},
        '28':{'weight':range(0,101),'height':range(41,49)},
        '29':{'weight':range(0,161),'height':range(41,53)},
        '30':{'weight':range(61,161),'height':range(49,61)},
        '31':{'weight':range(71,171),'height':range(49,65)},
        '32':{'weight':range(81,181),'height':range(57,69)},
        '33':{'weight':range(121,250),'height':range(61,84)},
        '34':{'weight':range(161,250),'height':range(69,84)},
    }
    def get_bat_size(self,p_height,p_weight):
        bat_size = None
        for size in self.bat_chart.keys():
            if p_weight in self.bat_chart[size]['weight']:
                if p_height in self.bat_chart[size]['height']:
                    bat_size = size
                    return bat_size
        return bat_size