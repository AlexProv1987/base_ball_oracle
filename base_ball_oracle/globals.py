class GlobalLevels():
    T_BALL = 't_ball'
    YOUTH = 'youth'
    ADULT = 'adult'
    level_chart = {
        't-ball':range(0,7),
        'youth':range(7,13),
        'adult':range(13,100)
        }
    
    def get_level_chart(self):
        levels = self.level_chart
        assert self.level_chart is not None,(
            "'%s'Should include level_chart or override 'get_level_chart()' method."
            % self.__class__.__name__
        )
        return levels
    
    def get_player_level(self,age):
        chart = self.get_level_chart()
        p_level = None
        for level in chart:
            if age in chart[level]:
                p_level = level
                return p_level
        return p_level
    
class ConvertValue():
    @staticmethod
    def convert(value,conversion_rate) -> int:
        converted = int(value)*int(conversion_rate)
        print(converted)
        return converted
