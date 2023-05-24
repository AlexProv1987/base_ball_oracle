class ValidateParamsMixIn():
    accepted_params = {}
    def validate_keys(self, request, required_amt):
        param_cnt = 0
        params = self.get_accepted_params()
        for param in request.query_params.keys():
            if param in params.keys():
                if len(request.query_params[param]) != 0:
                    param_cnt+=1
            else:
                return False
        if required_amt == 'all':
            if self.all_present(param_cnt):
                return True
        else:
            return True
        return False

    def all_present(self, cnt):
        if cnt == len(self.accepted_params):
            return True
        return False
    
    def get_accepted_params(self):
        params = self.accepted_params
        assert self.accepted_params is not None,(
            "'%s'Should include accepted_params or override 'get_accepted_params()' method."
            % self.__class__.__name__
        )
        return params